import asyncio
import datetime
import logging
import os
import time
from collections import defaultdict

import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from open_webui.apps.filter.wordsSearch import wordsSearch
from open_webui.apps.socket.utils import RedisDict
from open_webui.apps.webui.routers.chats import request_share_chat_by_id, request_get_chat_by_id
from open_webui.config import (
    AppConfig,
    ENABLE_MESSAGE_FILTER,
    CHAT_FILTER_WORDS_FILE,
    CHAT_FILTER_WORDS,
    ENABLE_REPLACE_FILTER_WORDS,
    REPLACE_FILTER_WORDS,
    ENABLE_WECHAT_NOTICE,
    ENABLE_DAILY_USAGES_NOTICE,
    SEND_FILTER_MESSAGE_TYPE,
    WECHAT_NOTICE_SUFFIX,
    WECHAT_APP_SECRET,
)
from open_webui.env import DATA_DIR, SRC_LOG_LEVELS, WEBUI_URL, WEBUI_NAME, WEBSOCKET_REDIS_URL, WEBSOCKET_MANAGER
from open_webui.utils.utils import (
    get_admin_user,
)
from pydantic import BaseModel

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["FILTER"])

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
scheduler = AsyncIOScheduler()

app.state.config = AppConfig()

app.state.config.ENABLE_MESSAGE_FILTER = ENABLE_MESSAGE_FILTER
app.state.config.CHAT_FILTER_WORDS_FILE = CHAT_FILTER_WORDS_FILE
app.state.config.CHAT_FILTER_WORDS = CHAT_FILTER_WORDS
app.state.config.ENABLE_REPLACE_FILTER_WORDS = ENABLE_REPLACE_FILTER_WORDS
app.state.config.REPLACE_FILTER_WORDS = REPLACE_FILTER_WORDS
app.state.config.ENABLE_WECHAT_NOTICE = ENABLE_WECHAT_NOTICE
app.state.config.WECHAT_APP_SECRET = WECHAT_APP_SECRET
app.state.config.ENABLE_DAILY_USAGES_NOTICE = ENABLE_DAILY_USAGES_NOTICE
app.state.config.SEND_FILTER_MESSAGE_TYPE = SEND_FILTER_MESSAGE_TYPE
app.state.config.WECHAT_NOTICE_SUFFIX = WECHAT_NOTICE_SUFFIX

file_path = os.path.join(DATA_DIR, app.state.config.CHAT_FILTER_WORDS_FILE)
user_usage = defaultdict(lambda: defaultdict(int))
redis_client = None
if WEBSOCKET_REDIS_URL and WEBSOCKET_MANAGER == "redis":
    user_usage = RedisDict(
        "open-webui:user_usage", redis_url=WEBSOCKET_REDIS_URL
    )
usage_lock = asyncio.Lock()
search = None


async def reset_usage():
    global user_usage
    if isinstance(user_usage, RedisDict):
        user_usage.clear()
    else:
        user_usage = defaultdict(lambda: defaultdict(int))


async def new_number_sign_up_notice(name, role, email):
    data = await notice_newnumber_signup_to_wechatapp(name, role, email)
    await send_message_to_wechatapp(data)


async def daily_send_usage():
    datas = await prepare_usage_to_wechatapp()
    for data in datas:
        await send_message_to_wechatapp(data)


async def prepare_usage_to_wechatapp():
    if app.state.config.SEND_FILTER_MESSAGE_TYPE.lower() == "markdown":
        contents = await init_markdown_usages()
        msg_type = "markdown"
    else:
        contents = await init_usages()
        msg_type = "text"

    datas = [
        {
            "msgtype": msg_type,
            msg_type: {
                "content": content,
                "mentioned_list": [] if msg_type == "markdown" else None,
            }
        }
        for content in contents
    ]

    return datas


async def notice_newnumber_signup_to_wechatapp(name, role, email):
    data = {
        "msgtype": "text",
        "text": {
            "content": f"✨✨✨{WEBUI_NAME}"
                       f"\n\n🤖用户：{name}"
                       f"\n\n🔍角色：{role}"
                       f"\n\n📮邮箱：{email}"
                       f"\n\n🌟用户已注册成功，请确认是否正式通过！"
                       f"\n\n{app.state.config.WECHAT_NOTICE_SUFFIX}"
        }
    }
    return data


async def prepare_data_to_wechatapp(share_id, user, replyType: str, content: str):
    if replyType.lower() == "markdown":
        data = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": f"🚨{user.name}提问敏感消息！",
                        "description": "💢💢💢为了API的正常运行，赶紧点开看看吧！",
                        "url": f"{WEBUI_URL}/s/{share_id}",
                        "picurl": f"{WEBUI_URL}/static/favicon.png"
                    }
                ]
            }
        }
    else:
        data = {
            "msgtype": "text",
            "text": {
                "content": f"🚨🚨🚨 警告"
                           f"\n\n{user.name}提问敏感消息！"
                           f"\n\n😅 {content}"
                           f"\n\n🔗 {WEBUI_URL}/s/{share_id}"
                           f"\n\n💢 为了API的正常运行，赶紧点开看看吧！"
                           f"\n\n{app.state.config.WECHAT_NOTICE_SUFFIX}"
            }
        }
    return data


async def send_message_to_wechatapp(data):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={app.state.config.WECHAT_APP_SECRET}"
    log.info(f"Send message to WeChat app: {url}")
    headers = {'Content-type': 'application/json'}
    log.info(f"Send message to WeChat app: {data}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()  # 如果状态码不是200-299，会引发异常
                response_text = await response.text()
                log.info(f"POST 请求成功: {url}, 状态码: {response.status}, 响应: {response_text}")
                return response_text
    except aiohttp.ClientError as e:
        log.error(f"POST 请求失败: {url}, 错误: {str(e)}")


async def init_file():
    if app.state.config.CHAT_FILTER_WORDS_FILE:
        if os.path.exists(DATA_DIR):
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    unique_lines = set(line.strip() for line in lines)
                    joined_text = ",".join(unique_lines)
                    app.state.config.CHAT_FILTER_WORDS = joined_text if joined_text else ""
            else:
                await write_words_to_file()


async def write_words_to_file():
    new_bad_words = set(
        word.strip() for word in app.state.config.CHAT_FILTER_WORDS.split(",")
    )
    app.state.config.CHAT_FILTER_WORDS = ",".join(sorted(new_bad_words))
    if app.state.config.CHAT_FILTER_WORDS:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(sorted(new_bad_words)) + "\n")
    else:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("")
    log.info(f"Create a new bad words file: {file_path}")


async def app_start():
    global search

    log.info("Initializing files...")
    await init_file()

    if app.state.config.ENABLE_WECHAT_NOTICE:
        log.info("WeChat notice enabled.")
        scheduler.add_job(reset_usage, 'cron', day_of_week='sun', hour=0, minute=0, id='reset_usage')
        log.info("Added reset_usage job.")
        if app.state.config.ENABLE_DAILY_USAGES_NOTICE:
            log.info("Daily usages notice enabled.")
            scheduler.add_job(daily_send_usage, 'cron', hour=23, minute=30, id='daily_send_usage')
            log.info("Added daily_send_usage job.")
        scheduler.start()
        log.info("Scheduler started.")

    search = None
    if app.state.config.ENABLE_MESSAGE_FILTER and app.state.config.CHAT_FILTER_WORDS:
        log.info("Message filter enabled with keywords.")
        search = wordsSearch()
        search.SetKeywords(app.state.config.CHAT_FILTER_WORDS.split(","))
        log.info("Keywords set for message filter.")


class FILTERConfigForm(BaseModel):
    ENABLE_MESSAGE_FILTER: bool
    CHAT_FILTER_WORDS: str
    CHAT_FILTER_WORDS_FILE: str
    ENABLE_REPLACE_FILTER_WORDS: bool
    REPLACE_FILTER_WORDS: str
    ENABLE_WECHAT_NOTICE: bool
    WECHAT_APP_SECRET: str
    ENABLE_DAILY_USAGES_NOTICE: bool
    SEND_FILTER_MESSAGE_TYPE: str
    WECHAT_NOTICE_SUFFIX: str


@app.get("/config")
async def get_filter_config(user=Depends(get_admin_user)):
    return {
        "ENABLE_MESSAGE_FILTER": app.state.config.ENABLE_MESSAGE_FILTER,
        "CHAT_FILTER_WORDS": app.state.config.CHAT_FILTER_WORDS,
        "CHAT_FILTER_WORDS_FILE": app.state.config.CHAT_FILTER_WORDS_FILE,
        "ENABLE_REPLACE_FILTER_WORDS": app.state.config.ENABLE_REPLACE_FILTER_WORDS,
        "REPLACE_FILTER_WORDS": app.state.config.REPLACE_FILTER_WORDS,
        "ENABLE_WECHAT_NOTICE": app.state.config.ENABLE_WECHAT_NOTICE,
        "WECHAT_APP_SECRET": app.state.config.WECHAT_APP_SECRET,
        "ENABLE_DAILY_USAGES_NOTICE": app.state.config.ENABLE_DAILY_USAGES_NOTICE,
        "SEND_FILTER_MESSAGE_TYPE": app.state.config.SEND_FILTER_MESSAGE_TYPE,
        "WECHAT_NOTICE_SUFFIX": app.state.config.WECHAT_NOTICE_SUFFIX,
    }


@app.post("/config/update")
async def update_filter_config(
        form_data: FILTERConfigForm, user=Depends(get_admin_user)
):
    global search
    global file_path

    app.state.config.ENABLE_MESSAGE_FILTER = form_data.ENABLE_MESSAGE_FILTER
    app.state.config.CHAT_FILTER_WORDS_FILE = form_data.CHAT_FILTER_WORDS_FILE
    app.state.config.ENABLE_REPLACE_FILTER_WORDS = form_data.ENABLE_REPLACE_FILTER_WORDS
    app.state.config.REPLACE_FILTER_WORDS = form_data.REPLACE_FILTER_WORDS
    app.state.config.ENABLE_WECHAT_NOTICE = form_data.ENABLE_WECHAT_NOTICE
    app.state.config.WECHAT_APP_SECRET = form_data.WECHAT_APP_SECRET
    app.state.config.ENABLE_DAILY_USAGES_NOTICE = form_data.ENABLE_DAILY_USAGES_NOTICE
    app.state.config.SEND_FILTER_MESSAGE_TYPE = form_data.SEND_FILTER_MESSAGE_TYPE
    app.state.config.WECHAT_NOTICE_SUFFIX = form_data.WECHAT_NOTICE_SUFFIX

    request_file_path = os.path.join(DATA_DIR, app.state.config.CHAT_FILTER_WORDS_FILE)

    if request_file_path != file_path:
        app.state.config.CHAT_FILTER_WORDS = form_data.CHAT_FILTER_WORDS
        file_path = request_file_path
        await init_file()

    else:
        if app.state.config.CHAT_FILTER_WORDS != form_data.CHAT_FILTER_WORDS:
            app.state.config.CHAT_FILTER_WORDS = form_data.CHAT_FILTER_WORDS
            await write_words_to_file()

    search = wordsSearch()
    search.SetKeywords(app.state.config.CHAT_FILTER_WORDS.split(","))

    if not app.state.config.ENABLE_DAILY_USAGES_NOTICE and scheduler.get_job('daily_send_usage'):
        scheduler.remove_job('daily_send_usage')
        if not scheduler.get_job('daily_send_usage'):
            log.info("Remove daily_send_usage job.")
    elif app.state.config.ENABLE_DAILY_USAGES_NOTICE and not scheduler.get_job('daily_send_usage'):
        scheduler.add_job(daily_send_usage, 'cron', hour=23, minute=30, id='daily_send_usage')
        if scheduler.get_job('daily_send_usage'):
            log.info("Add daily_send_usage job.")

    return {
        "ENABLE_MESSAGE_FILTER": app.state.config.ENABLE_MESSAGE_FILTER,
        "CHAT_FILTER_WORDS": app.state.config.CHAT_FILTER_WORDS,
        "CHAT_FILTER_WORDS_FILE": app.state.config.CHAT_FILTER_WORDS_FILE,
        "ENABLE_REPLACE_FILTER_WORDS": app.state.config.ENABLE_REPLACE_FILTER_WORDS,
        "REPLACE_FILTER_WORDS": app.state.config.REPLACE_FILTER_WORDS,
        "ENABLE_WECHAT_NOTICE": app.state.config.ENABLE_WECHAT_NOTICE,
        "WECHAT_APP_SECRET": app.state.config.WECHAT_APP_SECRET,
        "ENABLE_DAILY_USAGES_NOTICE": app.state.config.ENABLE_DAILY_USAGES_NOTICE,
        "SEND_FILTER_MESSAGE_TYPE": app.state.config.SEND_FILTER_MESSAGE_TYPE,
        "WECHAT_NOTICE_SUFFIX": app.state.config.WECHAT_NOTICE_SUFFIX,
    }


async def init_markdown_usages():
    usage_strings = []
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y年%m月%d日 %H时%M分")
    reply_text = f"### 📅 **{formatted_now}**\n\n### 🤖 **{WEBUI_NAME} 使用情况如下：**"
    usage_strings.append(reply_text)

    if isinstance(user_usage, RedisDict):
        all_users = user_usage.keys()
        users_data = ((user_name, user_usage.get(user_name, {})) for user_name in all_users)
    else:
        users_data = user_usage.items()

    for user_name, models in users_data:
        if not models:
            continue
        model_usage_list = [f"{model}: {count}" for model, count in sorted(models.items())]
        usage_string = f"⭐用户 {user_name} \n" + "\n".join(model_usage_list)
        usage_strings.append(usage_string)

    usage_strings.append(f"{app.state.config.WECHAT_NOTICE_SUFFIX}")
    return usage_strings


async def init_usages():
    usage_strings = []
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y年%m月%d日 %H时%M分")
    reply_text = f"📅 {formatted_now}\n\n🤖 {WEBUI_NAME}使用如下："
    usage_strings.append(reply_text)

    if isinstance(user_usage, RedisDict):
        all_users = user_usage.keys()
        users_data = ((user_name, user_usage.get(user_name, {})) for user_name in all_users)
    else:
        users_data = user_usage.items()

    for user_name, models in users_data:
        if not models:
            continue
        model_usage_list = [f"{model}: {count}" for model, count in sorted(models.items())]
        usage_string = f"⭐用户 {user_name} \n" + "\n".join(model_usage_list)
        usage_strings.append(usage_string)

    usage_strings.append(f"{app.state.config.WECHAT_NOTICE_SUFFIX}")
    return usage_strings


async def process_user_usage(model, user):
    global user_usage
    model_name = model.get("name", "")
    user_name = user.name
    try:
        # 获取用户的使用数据，如果不存在则初始化
        async with usage_lock:
            if isinstance(user_usage, RedisDict):
                user_data = user_usage.get(user_name, {})
                user_data[model_name] = user_data.get(model_name, 0) + 1
                user_usage[user_name] = user_data
            else:
                user_usage[user_name][model_name] += 1
    except Exception as e:
        log.error(f"处理用户使用数据时发生错误: {e}")


@app.post("/usages")
async def get_usages(
        user=Depends(get_admin_user)
):
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="Permission denied.")

    return {"data": await init_usages()}


async def content_filter_message(payload: dict, content: str, user):
    if content:
        chat_id = payload.get("metadata", {}).get("chat_id", None)
        if chat_id:
            log.info("chat_id: " + chat_id)
        start_time = time.time()
        filter_condition = search.FindFirst(content)
        if filter_condition:
            filter_word = filter_condition["Keyword"]
            log.info(
                "The time taken to check the filter words: %.6fs",
                time.time() - start_time,
            )

            if chat_id and app.state.config.ENABLE_WECHAT_NOTICE:
                try:
                    if chat_id != "local":
                        await request_share_chat_by_id(chat_id, user)
                        share_response = await request_get_chat_by_id(chat_id, user)
                        share_id = getattr(share_response, 'share_id', None)

                        if share_id:
                            log.info(f"Share ID: {share_id}")
                            data = await prepare_data_to_wechatapp(
                                share_id, user,
                                app.state.config.SEND_FILTER_MESSAGE_TYPE, content
                            )
                            await send_message_to_wechatapp(data)
                    else:
                        data = {
                            "msgtype": "text",
                            "text": {
                                "content": f"🚨🚨🚨 警告"
                                           f"\n\n{user.name}提问敏感消息！"
                                           f"\n\n😅 {content[:100]}"
                                           f"\n\n💢 为了API的正常运行，赶紧点开看看吧！"
                                           f"\n\n{app.state.config.WECHAT_NOTICE_SUFFIX}"
                            }
                        }
                        await send_message_to_wechatapp(data)
                except Exception as e:
                    log.error(f"发送消息到微信应用失败: {e}")

            if not app.state.config.ENABLE_REPLACE_FILTER_WORDS:
                detail_message = (
                    f"Yubb Chat: 您的消息包含敏感词语（`{filter_word}`）无法发送。请创建新话题并重试。"
                )
                raise HTTPException(
                    status_code=503, detail=detail_message
                )
            else:
                filter_text = search.Replace(content, app.state.config.REPLACE_FILTER_WORDS)
                return filter_text
    return content


async def filter_message(payload: dict, user):
    messages = payload.get("messages", None)

    if app.state.config.ENABLE_MESSAGE_FILTER and search:
        if messages:
            for message in reversed(messages):
                if message.get("role") == "user":
                    content = message.get("content")
                    if isinstance(content, str):
                        message["content"] = await content_filter_message(payload, content, user)
                    elif isinstance(content, list):
                        for item in content:
                            if item.get("type", "image_url") == "text":
                                item_content = item.get("text", "")
                                item["text"] = await content_filter_message(payload, item_content, user)
                    break
