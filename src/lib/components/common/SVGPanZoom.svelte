<script lang="ts">
<<<<<<< HEAD
	import { onMount } from 'svelte';
	import panzoom from 'panzoom';
	import html2canvas from 'html2canvas';
=======
	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;

	import { toast } from 'svelte-sonner';

	import panzoom, { type PanZoom } from 'panzoom';
	import DOMPurify from 'dompurify';

	import { onMount, getContext } from 'svelte';
	const i18n = getContext('i18n');

	import { copyToClipboard } from '$lib/utils';

	import DocumentDuplicate from '../icons/DocumentDuplicate.svelte';
	import Tooltip from './Tooltip.svelte';
	import Clipboard from '../icons/Clipboard.svelte';
	import Reset from '../icons/Reset.svelte';
	import ArrowDownTray from '../icons/ArrowDownTray.svelte';

>>>>>>> upstream/main
	export let className = '';
	export let svg = '';
	export let content = '';

	let instance: PanZoom;

	let sceneParentElement: HTMLElement;
	let sceneElement: HTMLElement;

	$: if (sceneElement) {
		instance = panzoom(sceneElement, {
			bounds: true,
			boundsPadding: 0.1,
			zoomSpeed: 0.065
		});
	}
<<<<<<< HEAD

	async function downloadSVGAsPNG() {
		if (!sceneElement) return;
		try {
			const canvas = await html2canvas(sceneElement);
			const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, 'image/png'));
			if (!blob) return;

			const blobUrl = URL.createObjectURL(blob);
			console.log('blobUrl', blobUrl);
			const date = new Date();
			const timestamp =
				date.getFullYear() +
				('0' + (date.getMonth() + 1)).slice(-2) +
				('0' + date.getDate()).slice(-2) +
				'_' +
				('0' + date.getHours()).slice(-2) +
				('0' + date.getMinutes()).slice(-2);

			const imageName = `mermaid_${timestamp}.png`;

			const a = document.createElement('a');
			a.href = blobUrl;
			a.download = imageName;
			document.body.appendChild(a);
			a.click();
			a.remove();
			URL.revokeObjectURL(blobUrl);
		} catch (error) {
			console.error('图片下载失败:', error);
			alert('图片下载失败，请稍后重试');
		}
	}
</script>

<button class="download-btn" on:click={downloadSVGAsPNG}>
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-6 h-6">
		<path
			d="M10.75 2.75a.75.75 0 0 0-1.5 0v8.614L6.295 8.235a.75.75 0 1 0-1.09 1.03l4.25 4.5a.75.75 0 0 0 1.09 0l4.25-4.5a.75.75 0 0 0-1.09-1.03l-2.955 3.129V2.75Z"
		></path>
		<path
			d="M3.5 12.75a.75.75 0 0 0-1.5 0v2.5A2.75 2.75 0 0 0 4.75 18h10.5A2.75 2.75 0 0 0 18 15.25v-2.5a.75.75 0 0 0-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5Z"
		></path>
	</svg>
</button>
<div bind:this={sceneParentElement} class={className} style="position: relative;">
	<div bind:this={sceneElement} class="relative flex h-full max-h-full justify-center items-center">
=======
	const resetPanZoomViewport = () => {
		instance.moveTo(0, 0);
		instance.zoomAbs(0, 0, 1);
		console.log(instance.getTransform());
	};

	const downloadAsSVG = () => {
		const svgBlob = new Blob([svg], { type: 'image/svg+xml' });
		saveAs(svgBlob, `diagram.svg`);
	};
</script>

<div bind:this={sceneParentElement} class="relative {className}">
	<div bind:this={sceneElement} class="flex h-full max-h-full justify-center items-center">
>>>>>>> upstream/main
		{@html svg}
	</div>

	{#if content}
		<div class=" absolute top-1 right-1">
			<div class="flex gap-1">
				<Tooltip content={$i18n.t('Download as SVG')}>
					<button
						class="p-1.5 rounded-lg border border-gray-100 dark:border-none dark:bg-gray-850 hover:bg-gray-50 dark:hover:bg-gray-800 transition"
						on:click={() => {
							downloadAsSVG();
						}}
					>
						<ArrowDownTray className=" size-4" />
					</button>
				</Tooltip>

				<Tooltip content={$i18n.t('Reset view')}>
					<button
						class="p-1.5 rounded-lg border border-gray-100 dark:border-none dark:bg-gray-850 hover:bg-gray-50 dark:hover:bg-gray-800 transition"
						on:click={() => {
							resetPanZoomViewport();
						}}
					>
						<Reset className=" size-4" />
					</button>
				</Tooltip>

				<Tooltip content={$i18n.t('Copy to clipboard')}>
					<button
						class="p-1.5 rounded-lg border border-gray-100 dark:border-none dark:bg-gray-850 hover:bg-gray-50 dark:hover:bg-gray-800 transition"
						on:click={() => {
							copyToClipboard(content);
							toast.success($i18n.t('Copied to clipboard'));
						}}
					>
						<Clipboard className=" size-4" strokeWidth="1.5" />
					</button>
				</Tooltip>
			</div>
		</div>
	{/if}
</div>

<style>
	.download-btn {
		position: absolute;
		top: 10px;
		right: 10px;
		background-color: rgba(128, 128, 128, 0.5);
		border: none;
		cursor: pointer;
		padding: 8px;
		border-radius: 50%;
		transition: background-color 0.3s;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 99;
	}

	.download-btn svg {
		width: 1rem;
		height: 1rem;
		color: white;
	}

	.download-btn:hover {
		background-color: rgba(100, 100, 100, 0.7);
	}

	.relative {
		width: 100%;
		height: 100%;
	}

	svg {
		width: 100%;
		height: auto;
	}
</style>
