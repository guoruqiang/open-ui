<script>
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import { WEBUI_API_BASE_URL } from '$lib/constants';

	import { onMount, getContext } from 'svelte';
<<<<<<< HEAD
	import { page } from '$app/stores';
	import { settings, user, config, models, tools, functions } from '$lib/stores';
	import { splitStream } from '$lib/utils';

	import { getModelInfos, updateModelById } from '$lib/apis/models';

	import AdvancedParams from '$lib/components/chat/Settings/Advanced/AdvancedParams.svelte';
	import { getModels } from '$lib/apis';
	import Checkbox from '$lib/components/common/Checkbox.svelte';
	import Tags from '$lib/components/common/Tags.svelte';
	import Knowledge from '$lib/components/workspace/Models/Knowledge.svelte';
	import ToolsSelector from '$lib/components/workspace/Models/ToolsSelector.svelte';
	import FiltersSelector from '$lib/components/workspace/Models/FiltersSelector.svelte';
	import ActionsSelector from '$lib/components/workspace/Models/ActionsSelector.svelte';
	import { uploadModelImage, base64ToFile } from '$lib/apis/files';
	import Capabilities from '$lib/components/workspace/Models/Capabilities.svelte';

=======
>>>>>>> upstream/main
	const i18n = getContext('i18n');

	import { page } from '$app/stores';
	import { config, models, settings } from '$lib/stores';

	import { getModelById, updateModelById } from '$lib/apis/models';

	import { getModels } from '$lib/apis';
	import ModelEditor from '$lib/components/workspace/Models/ModelEditor.svelte';

	let model = null;

	onMount(async () => {
		const _id = $page.url.searchParams.get('id');
		if (_id) {
			model = await getModelById(localStorage.token, _id).catch((e) => {
				return null;
			});

<<<<<<< HEAD
				info = {
					...info,
					...JSON.parse(
						JSON.stringify(
							model?.info
								? model?.info
								: {
										id: model.id,
										name: model.name
									}
						)
					)
				};

				if (model.preset && model.owned_by === 'ollama' && !info.base_model_id.includes(':')) {
					info.base_model_id = `${info.base_model_id}:latest`;
				}

				params = { ...params, ...model?.info?.params };
				params.stop = params?.stop
					? (typeof params.stop === 'string' ? params.stop.split(',') : (params?.stop ?? [])).join(
							','
						)
					: null;

				if (model?.info?.meta?.knowledge) {
					knowledge = [...model?.info?.meta?.knowledge];
				}

				if (model?.info?.meta?.toolIds) {
					toolIds = [...model?.info?.meta?.toolIds];
				}

				if (model?.info?.meta?.filterIds) {
					filterIds = [...model?.info?.meta?.filterIds];
				}

				if (model?.info?.meta?.actionIds) {
					actionIds = [...model?.info?.meta?.actionIds];
				}

				if (model?.owned_by === 'openai') {
					capabilities.usage = false;
					capabilities.base64 = false;
					capabilities.createPPT = false;
					capabilities.createImage = false;
					capabilities.createVideo = false;
					capabilities.createSearch = false;
				}

				if (model?.info?.meta?.capabilities) {
					capabilities = { ...capabilities, ...model?.info?.meta?.capabilities };
				}

				console.log(model);
			} else {
=======
			if (!model) {
>>>>>>> upstream/main
				goto('/workspace/models');
			}
		} else {
			goto('/workspace/models');
		}
	});

	const onSubmit = async (modelInfo) => {
		const res = await updateModelById(localStorage.token, modelInfo.id, modelInfo);

		if (res) {
			await models.set(
				await getModels(
					localStorage.token,
					$config?.features?.enable_direct_connections && ($settings?.directConnections ?? null)
				)
			);
			toast.success($i18n.t('Model updated successfully'));
			await goto('/workspace/models');
		}
	};
</script>

<<<<<<< HEAD
<div class="w-full max-h-full">
	<input
		bind:this={filesInputElement}
		bind:files={inputFiles}
		type="file"
		hidden
		accept="image/*"
		on:change={async () => {
			let reader = new FileReader();
			reader.onload = async (event) => {
				let originalImageUrl = `${event.target.result}`;

				const img = new Image();
				img.src = originalImageUrl;

				img.onload = async () => {
					const canvas = document.createElement('canvas');
					const ctx = canvas.getContext('2d');

					// Calculate the aspect ratio of the image
					const aspectRatio = img.width / img.height;

					// Calculate the new width and height to fit within 100x100
					let newWidth, newHeight;
					if (aspectRatio > 1) {
						newWidth = 250 * aspectRatio;
						newHeight = 250;
					} else {
						newWidth = 250;
						newHeight = 250 / aspectRatio;
					}

					// Set the canvas size
					canvas.width = 250;
					canvas.height = 250;

					// Calculate the position to center the image
					const offsetX = (250 - newWidth) / 2;
					const offsetY = (250 - newHeight) / 2;

					// Draw the image on the canvas
					ctx.drawImage(img, offsetX, offsetY, newWidth, newHeight);

					// Get the base64 representation of the compressed image
					const compressedSrc = canvas.toDataURL();

					const file = base64ToFile(compressedSrc, `${uuidv4()}.jpg`);

					// try to upload the image
					const res = await uploadModelImage(localStorage.token, file);

					// Update the profile_image_url
					info.meta.profile_image_url =
						res?.meta?.oss_url ||
						(res?.filename ? `/api/v1/files/model/images/${res.filename}` : compressedSrc);

					inputFiles = null;
				};
			};

			if (
				inputFiles &&
				inputFiles.length > 0 &&
				['image/gif', 'image/webp', 'image/jpeg', 'image/png', 'image/svg+xml'].includes(
					inputFiles[0]['type']
				)
			) {
				reader.readAsDataURL(inputFiles[0]);
			} else {
				console.log(`Unsupported File Type '${inputFiles[0]['type']}'.`);
				inputFiles = null;
			}
		}}
	/>

	<button
		class="flex space-x-1"
		on:click={() => {
			goto('/workspace/models');
		}}
	>
		<div class=" self-center">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				class="w-4 h-4"
			>
				<path
					fill-rule="evenodd"
					d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z"
					clip-rule="evenodd"
				/>
			</svg>
		</div>
		<div class=" self-center font-medium text-sm">{$i18n.t('Back')}</div>
	</button>

	{#if model}
		<form
			class="flex flex-col max-w-2xl mx-auto mt-4 mb-10"
			on:submit|preventDefault={() => {
				updateHandler();
			}}
		>
			<div class="flex justify-center my-4">
				<div class="self-center">
					<button
						class=" {info.meta.profile_image_url
							? ''
							: 'p-4'} rounded-full border border-dashed border-gray-200 flex items-center"
						type="button"
						on:click={() => {
							filesInputElement.click();
						}}
					>
						{#if info.meta.profile_image_url}
							<img
								src={info.meta.profile_image_url}
								alt="modelfile profile"
								class=" rounded-full size-16 object-cover"
							/>
						{:else}
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 24 24"
								fill="currentColor"
								class="size-8"
							>
								<path
									fill-rule="evenodd"
									d="M12 3.75a.75.75 0 01.75.75v6.75h6.75a.75.75 0 010 1.5h-6.75v6.75a.75.75 0 01-1.5 0v-6.75H4.5a.75.75 0 010-1.5h6.75V4.5a.75.75 0 01.75-.75z"
									clip-rule="evenodd"
								/>
							</svg>
						{/if}
					</button>
				</div>
			</div>

			<div class="mt-2 my-1 flex space-x-2">
				<div class="flex-1">
					<div class=" text-sm font-semibold mb-1">{$i18n.t('Name')}*</div>

					<div>
						<input
							class="px-3 py-1.5 text-sm w-full bg-transparent border dark:border-gray-600 outline-none rounded-lg"
							placeholder={$i18n.t('Name your model')}
							bind:value={name}
							required
						/>
					</div>
				</div>

				<div class="flex-1">
					<div class=" text-sm font-semibold mb-1">{$i18n.t('Model ID')}*</div>

					<div>
						<input
							class="px-3 py-1.5 text-sm w-full bg-transparent disabled:text-gray-500 border dark:border-gray-600 outline-none rounded-lg"
							placeholder={$i18n.t('Add a model id')}
							value={id}
							disabled
							required
						/>
					</div>
				</div>
			</div>

			{#if model.preset}
				<div class="my-1">
					<div class=" text-sm font-semibold mb-1">{$i18n.t('Base Model (From)')}</div>

					<div>
						<select
							class="px-3 py-1.5 text-sm w-full bg-transparent border dark:border-gray-600 outline-none rounded-lg"
							placeholder="Select a base model (e.g. llama3, gpt-4o)"
							bind:value={info.base_model_id}
							required
						>
							<option value={null} class=" text-gray-900">{$i18n.t('Select a base model')}</option>
							{#each $models.filter((m) => m.id !== model.id && !m?.preset) as model}
								<option value={model.id} class=" text-gray-900">{model.name}</option>
							{/each}
						</select>
					</div>
				</div>
			{/if}

			<div class="my-1">
				<div class="flex w-full justify-between items-center">
					<div class=" self-center text-sm font-semibold">{$i18n.t('Description')}</div>

					<button
						class="p-1 text-xs flex rounded transition"
						type="button"
						on:click={() => {
							if (info.meta.description === null) {
								info.meta.description = '';
							} else {
								info.meta.description = null;
							}
						}}
					>
						{#if info.meta.description === null}
							<span class="ml-2 self-center">{$i18n.t('Default')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Custom')}</span>
						{/if}
					</button>
				</div>

				{#if info.meta.description !== null}
					<textarea
						class="mt-1 px-3 py-1.5 text-sm w-full bg-transparent border dark:border-gray-600 outline-none rounded-lg"
						placeholder={$i18n.t('Add a short description about what this model does')}
						bind:value={info.meta.description}
						row="3"
					/>
				{/if}
			</div>

			<hr class=" dark:border-gray-850 my-1" />

			<div class="my-2">
				<div class="flex w-full justify-between">
					<div class=" self-center text-sm font-semibold">{$i18n.t('Model Params')}</div>
				</div>

				<!-- <div class=" text-sm font-semibold mb-2"></div> -->

				<div class="mt-2">
					<div class="my-1">
						<div class=" text-xs font-semibold mb-2">{$i18n.t('System Prompt')}</div>
						<div>
							<textarea
								class="px-3 py-1.5 text-sm w-full bg-transparent border dark:border-gray-600 outline-none rounded-lg -mb-1"
								placeholder={`Write your model system prompt content here\ne.g.) You are Mario from Super Mario Bros, acting as an assistant.`}
								rows="4"
								bind:value={info.params.system}
							/>
						</div>
					</div>

					<div class="flex w-full justify-between">
						<div class=" self-center text-xs font-semibold">
							{$i18n.t('Advanced Params')}
						</div>

						<button
							class="p-1 px-3 text-xs flex rounded transition"
							type="button"
							on:click={() => {
								showAdvanced = !showAdvanced;
							}}
						>
							{#if showAdvanced}
								<span class="ml-2 self-center">{$i18n.t('Hide')}</span>
							{:else}
								<span class="ml-2 self-center">{$i18n.t('Show')}</span>
							{/if}
						</button>
					</div>

					{#if showAdvanced}
						<div class="my-2">
							<AdvancedParams
								admin={true}
								bind:params
								on:change={(e) => {
									info.params = { ...info.params, ...params };
								}}
							/>
						</div>
					{/if}
				</div>
			</div>

			<hr class=" dark:border-gray-850 my-1" />

			<div class="my-2">
				<div class="flex w-full justify-between items-center">
					<div class="flex w-full justify-between items-center">
						<div class=" self-center text-sm font-semibold">{$i18n.t('Prompt suggestions')}</div>

						<button
							class="p-1 text-xs flex rounded transition"
							type="button"
							on:click={() => {
								if ((info?.meta?.suggestion_prompts ?? null) === null) {
									info.meta.suggestion_prompts = [{ content: '' }];
								} else {
									info.meta.suggestion_prompts = null;
								}
							}}
						>
							{#if (info?.meta?.suggestion_prompts ?? null) === null}
								<span class="ml-2 self-center">{$i18n.t('Default')}</span>
							{:else}
								<span class="ml-2 self-center">{$i18n.t('Custom')}</span>
							{/if}
						</button>
					</div>

					{#if (info?.meta?.suggestion_prompts ?? null) !== null}
						<button
							class="p-1 px-2 text-xs flex rounded transition"
							type="button"
							on:click={() => {
								if (
									info.meta.suggestion_prompts.length === 0 ||
									info.meta.suggestion_prompts.at(-1).content !== ''
								) {
									info.meta.suggestion_prompts = [...info.meta.suggestion_prompts, { content: '' }];
								}
							}}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
								class="w-4 h-4"
							>
								<path
									d="M10.75 4.75a.75.75 0 00-1.5 0v4.5h-4.5a.75.75 0 000 1.5h4.5v4.5a.75.75 0 001.5 0v-4.5h4.5a.75.75 0 000-1.5h-4.5v-4.5z"
								/>
							</svg>
						</button>
					{/if}
				</div>

				{#if info?.meta?.suggestion_prompts}
					<div class="flex flex-col space-y-1 mt-2">
						{#if info.meta.suggestion_prompts.length > 0}
							{#each info.meta.suggestion_prompts as prompt, promptIdx}
								<div class=" flex border dark:border-gray-600 rounded-lg">
									<input
										class="px-3 py-1.5 text-sm w-full bg-transparent outline-none border-r dark:border-gray-600"
										placeholder={$i18n.t('Write a prompt suggestion (e.g. Who are you?)')}
										bind:value={prompt.content}
									/>

									<button
										class="px-2"
										type="button"
										on:click={() => {
											info.meta.suggestion_prompts.splice(promptIdx, 1);
											info.meta.suggestion_prompts = info.meta.suggestion_prompts;
										}}
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											viewBox="0 0 20 20"
											fill="currentColor"
											class="w-4 h-4"
										>
											<path
												d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
											/>
										</svg>
									</button>
								</div>
							{/each}
						{:else}
							<div class="text-xs text-center">No suggestion prompts</div>
						{/if}
					</div>
				{/if}
			</div>

			<div class="my-2">
				<Knowledge bind:knowledge />
			</div>

			<div class="my-2">
				<ToolsSelector bind:selectedToolIds={toolIds} tools={$tools} />
			</div>

			<div class="my-2">
				<FiltersSelector
					bind:selectedFilterIds={filterIds}
					filters={$functions.filter((func) => func.type === 'filter')}
				/>
			</div>

			<div class="my-2">
				<ActionsSelector
					bind:selectedActionIds={actionIds}
					actions={$functions.filter((func) => func.type === 'action')}
				/>
			</div>

			<div class="my-2">
				<Capabilities bind:capabilities />
			</div>

			<div class="my-1">
				<div class="flex w-full justify-between items-center">
					<div class=" self-center text-sm font-semibold">{$i18n.t('Tags')}</div>
				</div>

				<div class="mt-2">
					<Tags
						tags={info?.meta?.tags ?? []}
						deleteTag={(tagName) => {
							info.meta.tags = info.meta.tags.filter((tag) => tag.name !== tagName);
						}}
						addTag={(tagName) => {
							console.log(tagName);
							if (!(info?.meta?.tags ?? null)) {
								info.meta.tags = [{ name: tagName }];
							} else {
								info.meta.tags = [...info.meta.tags, { name: tagName }];
							}
						}}
					/>
				</div>
			</div>

			<div class="my-2 text-gray-300 dark:text-gray-700">
				<div class="flex w-full justify-between mb-2">
					<div class=" self-center text-sm font-semibold">{$i18n.t('JSON Preview')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded transition"
						type="button"
						on:click={() => {
							showPreview = !showPreview;
						}}
					>
						{#if showPreview}
							<span class="ml-2 self-center">{$i18n.t('Hide')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Show')}</span>
						{/if}
					</button>
				</div>

				{#if showPreview}
					<div>
						<textarea
							class="px-3 py-1.5 text-sm w-full bg-transparent border dark:border-gray-600 outline-none rounded-lg"
							rows="10"
							value={JSON.stringify(info, null, 2)}
							disabled
							readonly
						/>
					</div>
				{/if}
			</div>

			<div class="my-2 flex justify-end mb-20">
				<button
					class=" text-sm px-3 py-2 transition rounded-xl {loading
						? ' cursor-not-allowed bg-gray-100 dark:bg-gray-800'
						: ' bg-gray-50 hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-800'} flex"
					type="submit"
					disabled={loading}
				>
					<div class=" self-center font-medium">{$i18n.t('Save & Update')}</div>

					{#if loading}
						<div class="ml-1.5 self-center">
							<svg
								class=" w-4 h-4"
								viewBox="0 0 24 24"
								fill="currentColor"
								xmlns="http://www.w3.org/2000/svg"
								><style>
									.spinner_ajPY {
										transform-origin: center;
										animation: spinner_AtaB 0.75s infinite linear;
									}
									@keyframes spinner_AtaB {
										100% {
											transform: rotate(360deg);
										}
									}
								</style><path
									d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,19a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z"
									opacity=".25"
								/><path
									d="M10.14,1.16a11,11,0,0,0-9,8.92A1.59,1.59,0,0,0,2.46,12,1.52,1.52,0,0,0,4.11,10.7a8,8,0,0,1,6.66-6.61A1.42,1.42,0,0,0,12,2.69h0A1.57,1.57,0,0,0,10.14,1.16Z"
									class="spinner_ajPY"
								/></svg
							>
						</div>
					{/if}
				</button>
			</div>
		</form>
	{/if}
</div>
=======
{#if model}
	<ModelEditor edit={true} {model} {onSubmit} />
{/if}
>>>>>>> upstream/main
