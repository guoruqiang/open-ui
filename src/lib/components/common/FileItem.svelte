<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';
<<<<<<< HEAD
=======
	import { formatFileSize } from '$lib/utils';

	import FileItemModal from './FileItemModal.svelte';
	import GarbageBin from '../icons/GarbageBin.svelte';
	import Spinner from './Spinner.svelte';
	import Tooltip from './Tooltip.svelte';
>>>>>>> upstream/main

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let className = 'w-72';
	export let colorClassName = 'bg-white dark:bg-gray-800';
	export let url: string | null = null;

	export let clickHandler: Function | null = null;

<<<<<<< HEAD
	export let dismissible = false;
	export let status = 'processed';
=======
	export let item = null;
	export let edit = false;
	export let small = false;
>>>>>>> upstream/main

	export let name: string;
	export let type: string;
	export let size: number;

<<<<<<< HEAD
	function formatSize(size) {
		if (size == null) return 'Unknown size';
		if (typeof size !== 'number' || size < 0) return 'Invalid size';
		if (size === 0) return '0 B';
		const units = ['B', 'KB', 'MB', 'GB', 'TB'];
		let unitIndex = 0;

		while (size >= 1024 && unitIndex < units.length - 1) {
			size /= 1024;
			unitIndex++;
		}
		return `${size.toFixed(1)} ${units[unitIndex]}`;
	}
</script>

<div class="relative group">
	<button
		class="h-14 {className} flex items-center space-x-3 {colorClassName} rounded-xl border border-gray-100 dark:border-gray-800 text-left"
		type="button"
		on:click={async () => {
			if (clickHandler === null) {
				if (url) {
					// if (type === 'file') {
					// 	window.open(`${url}/content`, '_blank').focus();
					// } else {
					// 	window.open(`${url}`, '_blank').focus();
					// }
=======
	import { deleteFileById } from '$lib/apis/files';

	let showModal = false;
</script>

{#if item}
	<FileItemModal bind:show={showModal} bind:item {edit} />
{/if}

<button
	class="relative group p-1.5 {className} flex items-center gap-1 {colorClassName} {small
		? 'rounded-xl'
		: 'rounded-2xl'} text-left"
	type="button"
	on:click={async () => {
		if (item?.file?.data?.content) {
			showModal = !showModal;
		} else {
			if (url) {
				if (type === 'file') {
					window.open(`${url}/content`, '_blank').focus();
				} else {
>>>>>>> upstream/main
					window.open(`${url}`, '_blank').focus();
				}
			} else {
				clickHandler();
			}
<<<<<<< HEAD
		}}
	>
		<div class="p-4 py-[1.1rem] bg-red-400 text-white rounded-l-xl">
			{#if status === 'processed'}
=======
		}

		dispatch('click');
	}}
>
	{#if !small}
		<div class="p-3 bg-black/20 dark:bg-white/10 text-white rounded-xl">
			{#if !loading}
>>>>>>> upstream/main
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="currentColor"
					class=" size-5"
				>
					<path
						fill-rule="evenodd"
						d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625ZM7.5 15a.75.75 0 0 1 .75-.75h7.5a.75.75 0 0 1 0 1.5h-7.5A.75.75 0 0 1 7.5 15Zm.75 2.25a.75.75 0 0 0 0 1.5H12a.75.75 0 0 0 0-1.5H8.25Z"
						clip-rule="evenodd"
					/>
					<path
						d="M12.971 1.816A5.23 5.23 0 0 1 14.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 0 1 3.434 1.279 9.768 9.768 0 0 0-6.963-6.963Z"
					/>
				</svg>
			{:else}
<<<<<<< HEAD
				<svg
					class=" size-5 translate-y-[0.5px]"
					fill="currentColor"
					viewBox="0 0 24 24"
					xmlns="http://www.w3.org/2000/svg"
					><style>
						.spinner_qM83 {
							animation: spinner_8HQG 1.05s infinite;
						}
						.spinner_oXPr {
							animation-delay: 0.1s;
						}
						.spinner_ZTLf {
							animation-delay: 0.2s;
						}
						@keyframes spinner_8HQG {
							0%,
							57.14% {
								animation-timing-function: cubic-bezier(0.33, 0.66, 0.66, 1);
								transform: translate(0);
							}
							28.57% {
								animation-timing-function: cubic-bezier(0.33, 0, 0.66, 0.33);
								transform: translateY(-6px);
							}
							100% {
								transform: translate(0);
							}
						}
					</style><circle class="spinner_qM83" cx="4" cy="12" r="2.5" /><circle
						class="spinner_qM83 spinner_oXPr"
						cx="12"
						cy="12"
						r="2.5"
					/><circle class="spinner_qM83 spinner_ZTLf" cx="20" cy="12" r="2.5" /></svg
				>
			{/if}
		</div>

		<div class="flex flex-col justify-center -space-y-0.5 pl-1.5 pr-4 w-full">
=======
				<Spinner />
			{/if}
		</div>
	{/if}

	{#if !small}
		<div class="flex flex-col justify-center -space-y-0.5 px-2.5 w-full">
>>>>>>> upstream/main
			<div class=" dark:text-gray-100 text-sm font-medium line-clamp-1 mb-1">
				{name}
			</div>

<<<<<<< HEAD
			<div class=" flex justify-between text-gray-500 text-xs">
=======
			<div class=" flex justify-between text-gray-500 text-xs line-clamp-1">
>>>>>>> upstream/main
				{#if type === 'file'}
					{$i18n.t('File')}
				{:else if type === 'doc'}
					{$i18n.t('Document')}
				{:else if type === 'collection'}
					{$i18n.t('Collection')}
				{:else}
<<<<<<< HEAD
					<span class=" capitalize">{type.toUpperCase()}</span>
				{/if}
				{#if size}
					<span class="capitalize">{formatSize(size)}</span>
				{/if}
			</div>
		</div>
	</button>
=======
					<span class=" capitalize line-clamp-1">{type}</span>
				{/if}
				{#if size}
					<span class="capitalize">{formatFileSize(size)}</span>
				{/if}
			</div>
		</div>
	{:else}
		<Tooltip content={name} className="flex flex-col w-full" placement="top-start">
			<div class="flex flex-col justify-center -space-y-0.5 px-2.5 w-full">
				<div class=" dark:text-gray-100 text-sm flex justify-between items-center">
					{#if loading}
						<div class=" shrink-0 mr-2">
							<Spinner className="size-4" />
						</div>
					{/if}
					<div class="font-medium line-clamp-1 flex-1">{name}</div>
					<div class="text-gray-500 text-xs capitalize shrink-0">{formatFileSize(size)}</div>
				</div>
			</div>
		</Tooltip>
	{/if}
>>>>>>> upstream/main

	{#if dismissible}
		<div class=" absolute -top-1 -right-1">
			<button
				class=" bg-white text-black border border-white rounded-full group-hover:visible invisible transition"
				type="button"
				on:click={() => {
					dispatch('dismiss');
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
	{/if}
</div>
