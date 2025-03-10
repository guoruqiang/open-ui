import asyncio
import hashlib
import json
import logging
from pathlib import Path
from typing import Literal, Optional, overload

import aiohttp
import requests
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask

from open_webui.apps.filter.main import process_user_usage

from open_webui.apps.openai.utils.streaming import (
    convert_from_stream_headers,
    convert_to_stream_data,
)
from open_webui.apps.webui.models.models import Models
from open_webui.config import (
    AIOHTTP_CLIENT_TIMEOUT,
    CACHE_DIR,
    CORS_ALLOW_ORIGIN,
    ENABLE_MODEL_FILTER,
    ENABLE_OPENAI_API,
    MODEL_FILTER_LIST,
    OPENAI_API_BASE_URLS,
    OPENAI_API_KEYS,
    OPENAI_API_NOSTREAM_MODELS,
    AppConfig,
)
from open_webui.constants import ERROR_MESSAGES
from open_webui.env import SRC_LOG_LEVELS
from open_webui.utils.payload import (
    apply_model_params_to_body_openai,
    apply_model_system_prompt_to_body,
)
from open_webui.utils.utils import get_admin_user, get_verified_user

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["OPENAI"])

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.config = AppConfig()

app.state.config.ENABLE_MODEL_FILTER = ENABLE_MODEL_FILTER
app.state.config.MODEL_FILTER_LIST = MODEL_FILTER_LIST

app.state.config.ENABLE_OPENAI_API = ENABLE_OPENAI_API
app.state.config.OPENAI_API_BASE_URLS = OPENAI_API_BASE_URLS
app.state.config.OPENAI_API_KEYS = OPENAI_API_KEYS

app.state.MODELS = {}


@app.middleware("http")
async def check_url(request: Request, call_next):
    if len(app.state.MODELS) == 0:
        await get_all_models()

    response = await call_next(request)
    return response


@app.get("/config")
async def get_config(user=Depends(get_admin_user)):
    return {"ENABLE_OPENAI_API": app.state.config.ENABLE_OPENAI_API}


class OpenAIConfigForm(BaseModel):
    enable_openai_api: Optional[bool] = None


@app.post("/config/update")
async def update_config(form_data: OpenAIConfigForm, user=Depends(get_admin_user)):
    app.state.config.ENABLE_OPENAI_API = form_data.enable_openai_api
    return {"ENABLE_OPENAI_API": app.state.config.ENABLE_OPENAI_API}


class UrlsUpdateForm(BaseModel):
    urls: list[str]


class KeysUpdateForm(BaseModel):
    keys: list[str]


@app.get("/urls")
async def get_openai_urls(user=Depends(get_admin_user)):
    return {"OPENAI_API_BASE_URLS": app.state.config.OPENAI_API_BASE_URLS}


@app.post("/urls/update")
async def update_openai_urls(form_data: UrlsUpdateForm, user=Depends(get_admin_user)):
    await get_all_models()
    app.state.config.OPENAI_API_BASE_URLS = form_data.urls
    return {"OPENAI_API_BASE_URLS": app.state.config.OPENAI_API_BASE_URLS}


@app.get("/keys")
async def get_openai_keys(user=Depends(get_admin_user)):
    return {"OPENAI_API_KEYS": app.state.config.OPENAI_API_KEYS}


@app.post("/keys/update")
async def update_openai_key(form_data: KeysUpdateForm, user=Depends(get_admin_user)):
    app.state.config.OPENAI_API_KEYS = form_data.keys
    return {"OPENAI_API_KEYS": app.state.config.OPENAI_API_KEYS}


@app.post("/audio/speech")
async def speech(request: Request, user=Depends(get_verified_user)):
    idx = None
    try:
        idx = app.state.config.OPENAI_API_BASE_URLS.index("https://api.openai.com/v1")
        body = await request.body()
        name = hashlib.sha256(body).hexdigest()

        SPEECH_CACHE_DIR = Path(CACHE_DIR).joinpath("./audio/speech/")
        SPEECH_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        file_path = SPEECH_CACHE_DIR.joinpath(f"{name}.mp3")
        file_body_path = SPEECH_CACHE_DIR.joinpath(f"{name}.json")

        # Check if the file already exists in the cache
        if file_path.is_file():
            return FileResponse(file_path)

        headers = {}
        headers["Authorization"] = f"Bearer {app.state.config.OPENAI_API_KEYS[idx]}"
        headers["Content-Type"] = "application/json"
        if "openrouter.ai" in app.state.config.OPENAI_API_BASE_URLS[idx]:
            headers["HTTP-Referer"] = "https://openwebui.com/"
            headers["X-Title"] = "Open WebUI"
        r = None
        try:
            r = requests.post(
                url=f"{app.state.config.OPENAI_API_BASE_URLS[idx]}/audio/speech",
                data=body,
                headers=headers,
                stream=True,
            )

            r.raise_for_status()

            # Save the streaming content to a file
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            with open(file_body_path, "w") as f:
                json.dump(json.loads(body.decode("utf-8")), f)

            # Return the saved file
            return FileResponse(file_path)

        except Exception as e:
            log.exception(e)
            error_detail = "Open WebUI: Server Connection Error"
            if r is not None:
                try:
                    res = r.json()
                    if "error" in res:
                        error_detail = f"External: {res['error']}"
                except Exception:
                    error_detail = f"External: {e}"

            raise HTTPException(
                status_code=r.status_code if r else 500, detail=error_detail
            )

    except ValueError:
        raise HTTPException(status_code=401, detail=ERROR_MESSAGES.OPENAI_NOT_FOUND)


async def fetch_url(url, key):
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        headers = {"Authorization": f"Bearer {key}"}
        async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()
    except Exception as e:
        # Handle connection error here
        log.error(f"Connection error: {e}")
        return None


async def cleanup_response(
    response: Optional[aiohttp.ClientResponse],
    session: Optional[aiohttp.ClientSession],
):
    if response:
        response.close()
    if session:
        await session.close()


def merge_models_lists(model_lists):
    log.debug(f"merge_models_lists {model_lists}")
    merged_list = []

    for idx, models in enumerate(model_lists):
        if models is not None and "error" not in models:
            merged_list.extend(
                [
                    {
                        **model,
                        "name": model.get("name", model["id"]),
                        "owned_by": "openai",
                        "openai": model,
                        "urlIdx": idx,
                    }
                    for model in models
                    if not any(
                        name in model["id"]
                        for name in [
                            "babbage",
                            "dall-e",
                            "davinci",
                            "embedding",
                            "tts",
                            "whisper",
                            "swap",
                            "BAAI",
                            "fishaudio",
                            "reranker",
                            "gizmo-g*",
                            "g-*",
                            "black-forest-labs",
                            "SenseVoiceSmall",
                        ]
                    )
                ]
            )

    return merged_list


def is_openai_api_disabled():
    api_keys = app.state.config.OPENAI_API_KEYS
    no_keys = len(api_keys) == 1 and api_keys[0] == ""
    return no_keys or not app.state.config.ENABLE_OPENAI_API


async def get_all_models_raw() -> list:
    if is_openai_api_disabled():
        return []

    # Check if API KEYS length is same than API URLS length
    num_urls = len(app.state.config.OPENAI_API_BASE_URLS)
    num_keys = len(app.state.config.OPENAI_API_KEYS)

    if num_keys != num_urls:
        # if there are more keys than urls, remove the extra keys
        if num_keys > num_urls:
            new_keys = app.state.config.OPENAI_API_KEYS[:num_urls]
            app.state.config.OPENAI_API_KEYS = new_keys
        # if there are more urls than keys, add empty keys
        else:
            app.state.config.OPENAI_API_KEYS += [""] * (num_urls - num_keys)

    tasks = [
        fetch_url(f"{url}/models", app.state.config.OPENAI_API_KEYS[idx])
        for idx, url in enumerate(app.state.config.OPENAI_API_BASE_URLS)
    ]

    responses = await asyncio.gather(*tasks)
    log.debug(f"get_all_models:responses() {responses}")

    return responses


@overload
async def get_all_models(raw: Literal[True]) -> list: ...


@overload
async def get_all_models(raw: Literal[False] = False) -> dict[str, list]: ...


async def get_all_models(raw=False) -> dict[str, list] | list:
    log.info("get_all_models()")
    if is_openai_api_disabled():
        return [] if raw else {"data": []}

    responses = await get_all_models_raw()
    if raw:
        return responses

    def extract_data(response):
        if response and "data" in response:
            return response["data"]
        if isinstance(response, list):
            return response
        return None

    models = {"data": merge_models_lists(map(extract_data, responses))}

    log.debug(f"models: {models}")
    app.state.MODELS = {model["id"]: model for model in models["data"]}

    return models


@app.get("/models")
@app.get("/models/{url_idx}")
async def get_models(url_idx: Optional[int] = None, user=Depends(get_verified_user)):
    if url_idx is None:
        models = await get_all_models()
        if app.state.config.ENABLE_MODEL_FILTER:
            if str(user.role) not in ["admin", "vip", "svip"]:
                models["data"] = list(
                    filter(
                        lambda model: model["id"] in app.state.config.MODEL_FILTER_LIST,
                        models["data"],
                    )
                )
        return models
    else:
        url = app.state.config.OPENAI_API_BASE_URLS[url_idx]
        key = app.state.config.OPENAI_API_KEYS[url_idx]

        headers = {}
        headers["Authorization"] = f"Bearer {key}"
        headers["Content-Type"] = "application/json"

        r = None

        timeout_duration = 10

        try:
            r = requests.request(
                method="GET",
                url=f"{url}/models",
                headers=headers,
                timeout=timeout_duration,
            )
            r.raise_for_status()

            response_data = r.json()

            if "api.openai.com" in url:
                # Filter the response data
                response_data["data"] = [
                    model
                    for model in response_data["data"]
                    if not any(
                        name in model["id"]
                        for name in [
                            "babbage",
                            "dall-e",
                            "davinci",
                            "embedding",
                            "tts",
                            "whisper",
                        ]
                    )
                ]

            return response_data
        except Exception as e:
            log.exception(e)
            error_detail = "Open WebUI: Server Connection Error"
            if r is not None:
                try:
                    res = r.json()
                    if "error" in res:
                        error_detail = f"External: {res['error']}"
                except Exception:
                    error_detail = f"External: {e}"

            raise HTTPException(
                status_code=r.status_code if r else 500,
                detail=error_detail,
            )


@app.post("/chat/completions")
@app.post("/chat/completions/{url_idx}")
async def generate_chat_completion(
    form_data: dict,
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
):
    idx = 0
    payload = {**form_data}

    if "metadata" in payload:
        del payload["metadata"]

    model_id = form_data.get("model")
    model_info = Models.get_model_by_id(model_id)

    if model_info:
        if model_info.base_model_id:
            payload["model"] = model_info.base_model_id

        params = model_info.params.model_dump()
        payload = apply_model_params_to_body_openai(params, payload)
        payload = apply_model_system_prompt_to_body(params, payload, user)

    model = app.state.MODELS[payload.get("model")]
    idx = model["urlIdx"]

    if "pipeline" in model and model.get("pipeline"):
        payload["user"] = {
            "name": user.name,
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }

    # handle special cases for certain models
    stream_requested = payload.get("stream", False)
    if model_id in OPENAI_API_NOSTREAM_MODELS:
        log.info("Model does not support streaming; patching request")
        # patch max_tokens -> max_completion_tokens and stream if 🍓
        if "max_tokens" in payload:
            payload["max_completion_tokens"] = payload.pop("max_tokens")
        if "messages" in payload:
            for msg in payload["messages"]:
                if msg["role"] == "system":
                    msg["role"] = "user"
        # hard-code stream=False regardless of upstream in svelte/etc.
        payload["stream"] = False

    # Convert the modified body back to JSON
    payload = json.dumps(payload)

    log.debug(payload)

    url = app.state.config.OPENAI_API_BASE_URLS[idx]
    key = app.state.config.OPENAI_API_KEYS[idx]

    headers = {}
    headers["Authorization"] = f"Bearer {key}"
    headers["Content-Type"] = "application/json"
    if "openrouter.ai" in app.state.config.OPENAI_API_BASE_URLS[idx]:
        headers["HTTP-Referer"] = "https://openwebui.com/"
        headers["X-Title"] = "Open WebUI"

    r = None
    session = None
    error = None

    try:
        # NOTE: have seen better OAI performance with httpx/http2 than aiohttp/http1.1
        session = aiohttp.ClientSession(
            trust_env=True,
            timeout=aiohttp.ClientTimeout(total=AIOHTTP_CLIENT_TIMEOUT),
        )
        r = await session.request(
            method="POST",
            url=f"{url}/chat/completions",
            data=payload,
            headers=headers,
        )

        # check for non-200 status and log the response if it's not a 200
        if r.status != 200:
            log.error(f"Non-200 status code: {r.status}")
            log.error(f"Request: {payload}")
            log.error(f"Response: {await r.text()}")
        r.raise_for_status()

        # Check if response is SSE
        if "text/event-stream" in r.headers.get("Content-Type", ""):
            log.info("Streaming response from original event stream")
            return StreamingResponse(
                r.content,
                status_code=r.status,
                headers=dict(r.headers),
                background=BackgroundTask(
                    cleanup_response, response=r, session=session
                ),
            )
        else:
            response_data = await r.json()
            log.info("Received non-streaming response from upstream")

            if stream_requested:
                log.info("Streaming response from non-streaming response")

                # Setup async generator for Starlette
                async def content_generator():
                    try:
                        for line in convert_to_stream_data(response_data):
                            log.info(f"Yielding line: {line}")
                            yield line + b"\n\n"
                    except Exception as e:
                        log.error(f"Error in content_generator: {e}")
                        raise

                headers = convert_from_stream_headers(r.headers)

                # Ensure no conflicting Content-Length headers are present
                if "content-length" in headers:
                    log.warning("Removing Content-Length for streaming response")
                    del headers["content-length"]

                # Set Transfer-Encoding: chunked for streaming
                headers["transfer-encoding"] = "chunked"

                return StreamingResponse(
                    content_generator(),
                    status_code=r.status,
                    headers=headers,
                    background=BackgroundTask(
                        cleanup_response, response=r, session=session
                    ),
                )
            else:
                log.info("Returning non-streaming response to client")
                # close the session
                return response_data
    except Exception as e:
        log.exception(e)
        error = e
        error_detail = "Open WebUI: Server Connection Error"
        if r is not None:
            try:
                res = await r.json()
                print(res)
                if "error" in res:
                    error_detail = f"External: {res['error']['message'] if 'message' in res['error'] else res['error']}"
            except Exception:
                error_detail = f"External: {e}"
        raise HTTPException(status_code=r.status if r else 500, detail=error_detail)
    finally:
        if not stream_requested:
            if r:
                r.close()
            if session:
                await session.close()
        if not error:
            await process_user_usage(model, user)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(path: str, request: Request, user=Depends(get_verified_user)):
    idx = 0

    body = await request.body()

    url = app.state.config.OPENAI_API_BASE_URLS[idx]
    key = app.state.config.OPENAI_API_KEYS[idx]

    target_url = f"{url}/{path}"

    headers = {}
    headers["Authorization"] = f"Bearer {key}"
    headers["Content-Type"] = "application/json"

    r = None
    session = None
    streaming = False

    try:
        session = aiohttp.ClientSession(trust_env=True)
        r = await session.request(
            method=request.method,
            url=target_url,
            data=body,
            headers=headers,
        )

        r.raise_for_status()

        # Check if response is SSE
        if "text/event-stream" in r.headers.get("Content-Type", ""):
            streaming = True
            return StreamingResponse(
                r.content,
                status_code=r.status,
                headers=dict(r.headers),
                background=BackgroundTask(
                    cleanup_response, response=r, session=session
                ),
            )
        else:
            response_data = await r.json()
            return response_data
    except Exception as e:
        log.exception(e)
        error_detail = "Open WebUI: Server Connection Error"
        if r is not None:
            try:
                res = await r.json()
                if "error" in res:
                    error_detail = f"External: {res['error']['message'] if 'message' in res['error'] else res['error']}"
            except Exception:
                error_detail = f"External: {e}"
        raise HTTPException(status_code=r.status if r else 500, detail=error_detail)
    finally:
        if not streaming and session:
            if r:
                r.close()
            await session.close()
