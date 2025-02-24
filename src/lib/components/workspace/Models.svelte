<script lang="ts">
	import { marked } from 'marked';

	import { toast } from 'svelte-sonner';
	import Sortable from 'sortablejs';

	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;

	import { onMount, getContext, tick } from 'svelte';
	import { goto } from '$app/navigation';
	const i18n = getContext('i18n');

	import { WEBUI_NAME, config, mobile, models as _models, settings, user } from '$lib/stores';
	import {
		createNewModel,
		deleteModelById,
		getModels as getWorkspaceModels,
		toggleModelById,
		updateModelById
	} from '$lib/apis/models';

	import { getModels } from '$lib/apis';
	import { getGroups } from '$lib/apis/groups';

	import EllipsisHorizontal from '../icons/EllipsisHorizontal.svelte';
	import ModelMenu from './Models/ModelMenu.svelte';
	import ModelDeleteConfirmDialog from '../common/ConfirmDialog.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import GarbageBin from '../icons/GarbageBin.svelte';
	import Search from '../icons/Search.svelte';
	import Plus from '../icons/Plus.svelte';
	import ChevronRight from '../icons/ChevronRight.svelte';
	import Switch from '../common/Switch.svelte';
	import Spinner from '../common/Spinner.svelte';
	import { capitalizeFirstLetter } from '$lib/utils';

	let shiftKey = false;

	let importFiles;
	let modelsImportInputElement: HTMLInputElement;
	let loaded = false;

	let models = [];

	let filteredModels = [];
	let selectedModel = null;

	let showModelDeleteConfirm = false;

	let group_ids = [];

	$: if (models) {
		filteredModels = models.filter(
			(m) => searchValue === '' || m.name.toLowerCase().includes(searchValue.toLowerCase())
		);
	}

	let searchValue = '';

	const deleteModelHandler = async (model) => {
		const res = await deleteModelById(localStorage.token, model.id).catch((e) => {
			toast.error(`${e}`);
			return null;
		});

		if (res) {
			toast.success($i18n.t(`Deleted {{name}}`, { name: model.id }));
		}

		await _models.set(
			await getModels(
				localStorage.token,
				$config?.features?.enable_direct_connections && ($settings?.directConnections ?? null)
			)
		);
		models = await getWorkspaceModels(localStorage.token);
	};

	const cloneModelHandler = async (model) => {
		sessionStorage.model = JSON.stringify({
			...model,
			id: `${model.id}-clone`,
			name: `${model.name} (Clone)`
		});
		goto('/workspace/models/create');
	};

	const shareModelHandler = async (model) => {
		toast.success($i18n.t('Redirecting you to Open WebUI Community'));

		const url = 'https://openwebui.com';

		const tab = await window.open(`${url}/models/create`, '_blank');

		// Define the event handler function
		const messageHandler = (event) => {
			if (event.origin !== url) return;
			if (event.data === 'loaded') {
				tab.postMessage(JSON.stringify(model), '*');

				// Remove the event listener after handling the message
				window.removeEventListener('message', messageHandler);
			}
		};

		window.addEventListener('message', messageHandler, false);
	};

	const hideModelHandler = async (model) => {
		let info = model.info;

		if (!info) {
			info = {
				id: model.id,
				name: model.name,
				meta: {
					suggestion_prompts: null
				},
				params: {}
			};
		}

		info.meta = {
			...info.meta,
			hidden: !(info?.meta?.hidden ?? false)
		};

		console.log(info);

		const res = await updateModelById(localStorage.token, info.id, info);

		if (res) {
			toast.success(
				$i18n.t(`Model {{name}} is now {{status}}`, {
					name: info.id,
					status: info.meta.hidden ? 'hidden' : 'visible'
				})
			);
		}

		await _models.set(
			await getModels(
				localStorage.token,
				$config?.features?.enable_direct_connections && ($settings?.directConnections ?? null)
			)
		);
		models = await getWorkspaceModels(localStorage.token);
	};

	const downloadModels = async (models) => {
		let blob = new Blob([JSON.stringify(models)], {
			type: 'application/json'
		});
		saveAs(blob, `models-export-${Date.now()}.json`);
	};

	const exportModelHandler = async (model) => {
		let blob = new Blob([JSON.stringify([model])], {
			type: 'application/json'
		});
		saveAs(blob, `${model.id}-${Date.now()}.json`);
	};

	onMount(async () => {
		models = await getWorkspaceModels(localStorage.token);
		let groups = await getGroups(localStorage.token);
		group_ids = groups.map((group) => group.id);

		loaded = true;

		const onKeyDown = (event) => {
			if (event.key === 'Shift') {
				shiftKey = true;
			}
		};

		const onKeyUp = (event) => {
			if (event.key === 'Shift') {
				shiftKey = false;
			}
		};

		const onBlur = () => {
			shiftKey = false;
		};

		window.addEventListener('keydown', onKeyDown);
		window.addEventListener('keyup', onKeyUp);
		window.addEventListener('blur-sm', onBlur);

		return () => {
			window.removeEventListener('keydown', onKeyDown);
			window.removeEventListener('keyup', onKeyUp);
			window.removeEventListener('blur-sm', onBlur);
		};
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Models')} | {$WEBUI_NAME}
	</title>
</svelte:head>

{#if loaded}
	<ModelDeleteConfirmDialog
		bind:show={showModelDeleteConfirm}
		on:confirm={() => {
			deleteModelHandler(selectedModel);
		}}
	/>

<<<<<<< HEAD
<div class="mb-3">
	<div class="flex justify-between items-center">
		<div class="flex md:self-center text-lg font-medium px-0.5">
			{$i18n.t('Models')}
			<div class="flex self-center w-[1px] h-6 mx-2.5 bg-gray-200 dark:bg-gray-700" />
			<span class="text-lg font-medium text-gray-500 dark:text-gray-300">{$models.length}</span>
		</div>
	</div>
</div>

<div class=" flex w-full space-x-2">
	<div class="flex flex-1">
		<div class=" self-center ml-1 mr-3">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				class="w-4 h-4"
			>
				<path
					fill-rule="evenodd"
					d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
					clip-rule="evenodd"
				/>
			</svg>
		</div>
		<input
			class=" w-full text-sm pr-4 py-1 rounded-r-xl outline-none bg-transparent"
			bind:value={searchValue}
			placeholder={$i18n.t('Search Models')}
		/>
	</div>

	<div>
		<a
			class=" px-2 py-2 rounded-xl border border-gray-200 dark:border-gray-600 dark:border-0 hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 transition font-medium text-sm flex items-center space-x-1"
			href="/workspace/models/create"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 16 16"
				fill="currentColor"
				class="w-4 h-4"
			>
				<path
					d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z"
				/>
			</svg>
		</a>
	</div>
</div>

<hr class=" border-gray-50 dark:border-gray-850 my-2.5" />

<a class=" flex space-x-4 cursor-pointer w-full mb-2 px-3 py-1" href="/workspace/models/create">
	<div class=" self-center w-10 flex-shrink-0">
		<div
			class="w-full h-10 flex justify-center rounded-full bg-transparent dark:bg-gray-700 border border-dashed border-gray-200"
		>
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6">
				<path
					fill-rule="evenodd"
					d="M12 3.75a.75.75 0 01.75.75v6.75h6.75a.75.75 0 010 1.5h-6.75v6.75a.75.75 0 01-1.5 0v-6.75H4.5a.75.75 0 010-1.5h6.75V4.5a.75.75 0 01.75-.75z"
					clip-rule="evenodd"
				/>
			</svg>
		</div>
	</div>

	<div class=" self-center">
		<div class=" font-semibold line-clamp-1">{$i18n.t('Create a model')}</div>
		<div class=" text-sm line-clamp-1">{$i18n.t('Customize models for a specific purpose')}</div>
	</div>
</a>

<hr class=" border-gray-50 dark:border-gray-850 my-2.5" />

<div class=" font-primary my-2 mb-5" id="model-list">
	{#each _models.filter((m) => searchValue === '' || m.name
				.toLowerCase()
				.includes(searchValue.toLowerCase())) as model}
		<div
			class=" flex space-x-4 cursor-pointer w-full px-3 py-2 dark:hover:bg-white/5 hover:bg-black/5 rounded-xl"
			id="model-item-{model.id}"
		>
			<a
				class=" flex flex-1 space-x-3.5 cursor-pointer w-full"
				href={`/?models=${encodeURIComponent(model.id)}`}
			>
				<div class=" self-start w-8 pt-0.5">
					<div
						class=" rounded-full object-cover {(model?.info?.meta?.hidden ?? false)
							? 'brightness-90 dark:brightness-50'
							: ''} "
					>
						<img
							src={model?.info?.meta?.profile_image_url ?? '/static/favicon.png'}
							alt="modelfile profile"
							class=" rounded-full w-full h-auto object-cover"
						/>
					</div>
				</div>

				<div
					class=" flex-1 self-center {(model?.info?.meta?.hidden ?? false) ? 'text-gray-500' : ''}"
				>
					<Tooltip
						content={marked.parse(
							model?.ollama?.digest
								? `${model?.ollama?.digest} *(${model?.ollama?.modified_at})*`
								: ''
						)}
						className=" w-fit"
						placement="top-start"
					>
						<div class="  font-semibold line-clamp-1">{model.name}</div>
					</Tooltip>
					<div class=" text-xs overflow-hidden text-ellipsis line-clamp-1 text-gray-500">
						{model?.info?.meta?.description
							? model?.info?.meta?.description
							: (model?.ollama?.digest ?? model.id)}
					</div>
				</div>
			</a>
			<div class="flex flex-row gap-0.5 self-center">
				{#if shiftKey}
					<Tooltip
						content={(model?.info?.meta?.hidden ?? false)
							? $i18n.t('Show Model')
							: $i18n.t('Hide Model')}
					>
						<button
							class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
							type="button"
							on:click={() => {
								hideModelHandler(model);
							}}
						>
							{#if model?.info?.meta?.hidden ?? false}
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									class="size-4"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
									/>
								</svg>
							{:else}
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									class="size-4"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
									/>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
									/>
								</svg>
							{/if}
						</button>
					</Tooltip>
=======
	<div class="flex flex-col gap-1 my-1.5">
		<div class="flex justify-between items-center">
			<div class="flex items-center md:self-center text-xl font-medium px-0.5">
				{$i18n.t('Models')}
				<div class="flex self-center w-[1px] h-6 mx-2.5 bg-gray-50 dark:bg-gray-850" />
				<span class="text-lg font-medium text-gray-500 dark:text-gray-300"
					>{filteredModels.length}</span
				>
			</div>
		</div>
>>>>>>> upstream/main

		<div class=" flex flex-1 items-center w-full space-x-2">
			<div class="flex flex-1 items-center">
				<div class=" self-center ml-1 mr-3">
					<Search className="size-3.5" />
				</div>
				<input
					class=" w-full text-sm py-1 rounded-r-xl outline-hidden bg-transparent"
					bind:value={searchValue}
					placeholder={$i18n.t('Search Models')}
				/>
			</div>

			<div>
				<a
					class=" px-2 py-2 rounded-xl hover:bg-gray-700/10 dark:hover:bg-gray-100/10 dark:text-gray-300 dark:hover:text-white transition font-medium text-sm flex items-center space-x-1"
					href="/workspace/models/create"
				>
					<Plus className="size-3.5" />
				</a>
			</div>
		</div>
	</div>

	<div class=" my-2 mb-5 gap-2 grid lg:grid-cols-2 xl:grid-cols-3" id="model-list">
		{#each filteredModels as model}
			<div
				class=" flex flex-col cursor-pointer w-full px-3 py-2 dark:hover:bg-white/5 hover:bg-black/5 rounded-xl transition"
				id="model-item-{model.id}"
			>
				<div class="flex gap-4 mt-0.5 mb-0.5">
					<div class=" w-[44px]">
						<div
							class=" rounded-full object-cover {model.is_active
								? ''
								: 'opacity-50 dark:opacity-50'} "
						>
							<img
								src={model?.meta?.profile_image_url ?? '/static/favicon.png'}
								alt="modelfile profile"
								class=" rounded-full w-full h-auto object-cover"
							/>
						</div>
					</div>

					<a
						class=" flex flex-1 cursor-pointer w-full"
						href={`/?models=${encodeURIComponent(model.id)}`}
					>
						<div class=" flex-1 self-center {model.is_active ? '' : 'text-gray-500'}">
							<Tooltip
								content={marked.parse(model?.meta?.description ?? model.id)}
								className=" w-fit"
								placement="top-start"
							>
								<div class=" font-semibold line-clamp-1">{model.name}</div>
							</Tooltip>

							<div class="flex gap-1 text-xs overflow-hidden">
								<div class="line-clamp-1">
									{#if (model?.meta?.description ?? '').trim()}
										{model?.meta?.description}
									{:else}
										{model.id}
									{/if}
								</div>
							</div>
						</div>
					</a>
				</div>

				<div class="flex justify-between items-center -mb-0.5 px-0.5">
					<div class=" text-xs mt-0.5">
						<Tooltip
							content={model?.user?.email ?? $i18n.t('Deleted User')}
							className="flex shrink-0"
							placement="top-start"
						>
							<div class="shrink-0 text-gray-500">
								{$i18n.t('By {{name}}', {
									name: capitalizeFirstLetter(
										model?.user?.name ?? model?.user?.email ?? $i18n.t('Deleted User')
									)
								})}
							</div>
						</Tooltip>
					</div>

					<div class="flex flex-row gap-0.5 items-center">
						{#if shiftKey}
							<Tooltip content={$i18n.t('Delete')}>
								<button
									class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
									type="button"
									on:click={() => {
										deleteModelHandler(model);
									}}
								>
									<GarbageBin />
								</button>
							</Tooltip>
						{:else}
							{#if $user?.role === 'admin' || model.user_id === $user?.id || model.access_control.write.group_ids.some( (wg) => group_ids.includes(wg) )}
								<a
									class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
									type="button"
									href={`/workspace/models/edit?id=${encodeURIComponent(model.id)}`}
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="w-4 h-4"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"
										/>
									</svg>
								</a>
							{/if}

							<ModelMenu
								user={$user}
								{model}
								shareHandler={() => {
									shareModelHandler(model);
								}}
								cloneHandler={() => {
									cloneModelHandler(model);
								}}
								exportHandler={() => {
									exportModelHandler(model);
								}}
								hideHandler={() => {
									hideModelHandler(model);
								}}
								deleteHandler={() => {
									selectedModel = model;
									showModelDeleteConfirm = true;
								}}
								onClose={() => {}}
							>
								<button
									class="self-center w-fit text-sm p-1.5 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
									type="button"
								>
									<EllipsisHorizontal className="size-5" />
								</button>
							</ModelMenu>

							<div class="ml-1">
								<Tooltip content={model.is_active ? $i18n.t('Enabled') : $i18n.t('Disabled')}>
									<Switch
										bind:state={model.is_active}
										on:change={async (e) => {
											toggleModelById(localStorage.token, model.id);
											_models.set(
												await getModels(
													localStorage.token,
													$config?.features?.enable_direct_connections &&
														($settings?.directConnections ?? null)
												)
											);
										}}
									/>
								</Tooltip>
							</div>
						{/if}
					</div>
				</div>
			</div>
		{/each}
	</div>

	{#if $user?.role === 'admin'}
		<div class=" flex justify-end w-full mb-3">
			<div class="flex space-x-1">
				<input
					id="models-import-input"
					bind:this={modelsImportInputElement}
					bind:files={importFiles}
					type="file"
					accept=".json"
					hidden
					on:change={() => {
						console.log(importFiles);

						let reader = new FileReader();
						reader.onload = async (event) => {
							let savedModels = JSON.parse(event.target.result);
							console.log(savedModels);

							for (const model of savedModels) {
								if (model?.info ?? false) {
									if ($_models.find((m) => m.id === model.id)) {
										await updateModelById(localStorage.token, model.id, model.info).catch(
											(error) => {
												return null;
											}
										);
									} else {
										await createNewModel(localStorage.token, model.info).catch((error) => {
											return null;
										});
									}
								}
							}

							await _models.set(
								await getModels(
									localStorage.token,
									$config?.features?.enable_direct_connections &&
										($settings?.directConnections ?? null)
								)
							);
							models = await getWorkspaceModels(localStorage.token);
						};

						reader.readAsText(importFiles[0]);
					}}
				/>

				<button
					class="flex text-xs items-center space-x-1 px-3 py-1.5 rounded-xl bg-gray-50 hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-gray-200 transition"
					on:click={() => {
						modelsImportInputElement.click();
					}}
				>
					<div class=" self-center mr-2 font-medium line-clamp-1">{$i18n.t('Import Models')}</div>

					<div class=" self-center">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 16 16"
							fill="currentColor"
							class="w-3.5 h-3.5"
						>
							<path
								fill-rule="evenodd"
								d="M4 2a1.5 1.5 0 0 0-1.5 1.5v9A1.5 1.5 0 0 0 4 14h8a1.5 1.5 0 0 0 1.5-1.5V6.621a1.5 1.5 0 0 0-.44-1.06L9.94 2.439A1.5 1.5 0 0 0 8.878 2H4Zm4 9.5a.75.75 0 0 1-.75-.75V8.06l-.72.72a.75.75 0 0 1-1.06-1.06l2-2a.75.75 0 0 1 1.06 0l2 2a.75.75 0 1 1-1.06 1.06l-.72-.72v2.69a.75.75 0 0 1-.75.75Z"
								clip-rule="evenodd"
							/>
						</svg>
					</div>
				</button>

				<button
					class="flex text-xs items-center space-x-1 px-3 py-1.5 rounded-xl bg-gray-50 hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-gray-200 transition"
					on:click={async () => {
						downloadModels($_models);
					}}
				>
					<div class=" self-center mr-2 font-medium line-clamp-1">{$i18n.t('Export Models')}</div>

					<div class=" self-center">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 16 16"
							fill="currentColor"
							class="w-3.5 h-3.5"
						>
							<path
								fill-rule="evenodd"
								d="M4 2a1.5 1.5 0 0 0-1.5 1.5v9A1.5 1.5 0 0 0 4 14h8a1.5 1.5 0 0 0 1.5-1.5V6.621a1.5 1.5 0 0 0-.44-1.06L9.94 2.439A1.5 1.5 0 0 0 8.878 2H4Zm4 3.5a.75.75 0 0 1 .75.75v2.69l.72-.72a.75.75 0 1 1 1.06 1.06l-2 2a.75.75 0 0 1-1.06 0l-2-2a.75.75 0 0 1 1.06-1.06l.72.72V6.25A.75.75 0 0 1 8 5.5Z"
								clip-rule="evenodd"
							/>
						</svg>
					</div>
				</button>
			</div>
		</div>
	{/if}

	{#if $config?.features.enable_community_sharing}
		<div class=" my-16">
			<div class=" text-xl font-medium mb-1 line-clamp-1">
				{$i18n.t('Made by Open WebUI Community')}
			</div>

			<a
				class=" flex cursor-pointer items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-850 w-full mb-2 px-3.5 py-1.5 rounded-xl transition"
				href="https://openwebui.com/#open-webui-community"
				target="_blank"
			>
				<div class=" self-center">
					<div class=" font-semibold line-clamp-1">{$i18n.t('Discover a model')}</div>
					<div class=" text-sm line-clamp-1">
						{$i18n.t('Discover, download, and explore model presets')}
					</div>
				</div>

				<div>
					<div>
						<ChevronRight />
					</div>
				</div>
			</a>
		</div>
	{/if}
{:else}
	<div class="w-full h-full flex justify-center items-center">
		<Spinner />
	</div>
{/if}
