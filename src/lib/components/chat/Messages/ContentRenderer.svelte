<script>
	import { onDestroy, onMount, tick, getContext, createEventDispatcher } from 'svelte';
	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	import Markdown from './Markdown.svelte';
	import { chatId, mobile, showArtifacts, showControls, showOverview } from '$lib/stores';
	import FloatingButtons from '../ContentRenderer/FloatingButtons.svelte';
	import { createMessagesList } from '$lib/utils';

	export let id;
	export let content;
	export let history;
	export let model = null;
	export let sources = null;

	export let save = false;
	export let floatingButtons = true;
	export let bufferTime = 30;

	export let onSourceClick = () => {};
	export let onTaskClick = () => {};

	export let onAddMessages = () => {};

	let contentContainerElement;

	let floatingButtonsElement;

	const updateButtonPosition = (event) => {
		const buttonsContainerElement = document.getElementById(`floating-buttons-${id}`);
		if (
			!contentContainerElement?.contains(event.target) &&
			!buttonsContainerElement?.contains(event.target)
		) {
			closeFloatingButtons();
			return;
		}

		setTimeout(async () => {
			await tick();

			if (!contentContainerElement?.contains(event.target)) return;

			let selection = window.getSelection();

			if (selection.toString().trim().length > 0) {
				const range = selection.getRangeAt(0);
				const rect = range.getBoundingClientRect();

				const parentRect = contentContainerElement.getBoundingClientRect();

				// Adjust based on parent rect
				const top = rect.bottom - parentRect.top;
				const left = rect.left - parentRect.left;

				if (buttonsContainerElement) {
					buttonsContainerElement.style.display = 'block';

					// Calculate space available on the right
					const spaceOnRight = parentRect.width - left;
					let halfScreenWidth = $mobile ? window.innerWidth / 2 : window.innerWidth / 3;

					if (spaceOnRight < halfScreenWidth) {
						const right = parentRect.right - rect.right;
						buttonsContainerElement.style.right = `${right}px`;
						buttonsContainerElement.style.left = 'auto'; // Reset left
					} else {
						// Enough space, position using 'left'
						buttonsContainerElement.style.left = `${left}px`;
						buttonsContainerElement.style.right = 'auto'; // Reset right
					}
					buttonsContainerElement.style.top = `${top + 5}px`; // +5 to add some spacing
				}
			} else {
				closeFloatingButtons();
			}
		}, 0);
	};

	const closeFloatingButtons = () => {
		const buttonsContainerElement = document.getElementById(`floating-buttons-${id}`);
		if (buttonsContainerElement) {
			buttonsContainerElement.style.display = 'none';
		}

		if (floatingButtonsElement) {
			floatingButtonsElement.closeHandler();
		}
	};

	const keydownHandler = (e) => {
		if (e.key === 'Escape') {
			closeFloatingButtons();
		}
	};

	onMount(() => {
		if (floatingButtons) {
			contentContainerElement?.addEventListener('mouseup', updateButtonPosition);
			document.addEventListener('mouseup', updateButtonPosition);
			document.addEventListener('keydown', keydownHandler);
		}
	});

	onDestroy(() => {
		if (floatingButtons) {
			contentContainerElement?.removeEventListener('mouseup', updateButtonPosition);
			document.removeEventListener('mouseup', updateButtonPosition);
			document.removeEventListener('keydown', keydownHandler);
		}
	});
</script>

<div bind:this={contentContainerElement}>
	<Markdown
		{id}
		{content}
		{model}
		{save}
<<<<<<< HEAD
		{bufferTime}
=======
		sourceIds={(sources ?? []).reduce((acc, s) => {
			let ids = [];
			s.document.forEach((document, index) => {
				if (model?.info?.meta?.capabilities?.citations == false) {
					ids.push('N/A');
					return ids;
				}

				const metadata = s.metadata?.[index];
				const id = metadata?.source ?? 'N/A';

				if (metadata?.name) {
					ids.push(metadata.name);
					return ids;
				}

				if (id.startsWith('http://') || id.startsWith('https://')) {
					ids.push(id);
				} else {
					ids.push(s?.source?.name ?? id);
				}

				return ids;
			});

			acc = [...acc, ...ids];

			// remove duplicates
			return acc.filter((item, index) => acc.indexOf(item) === index);
		}, [])}
		{onSourceClick}
		{onTaskClick}
>>>>>>> upstream/main
		on:update={(e) => {
			dispatch('update', e.detail);
		}}
		on:code={(e) => {
			const { lang, code } = e.detail;

			if (
				(['html', 'svg'].includes(lang) || (lang === 'xml' && code.includes('svg'))) &&
				!$mobile &&
				$chatId
			) {
				showArtifacts.set(true);
				showControls.set(true);
			}
		}}
	/>
</div>

<<<<<<< HEAD
{#if floatingButtons}
	<div
		bind:this={buttonsContainerElement}
		class="absolute rounded-lg mt-1 text-xs z-[9999]"
		style="display: none"
	>
		{#if !floatingInput}
			<div
				class="flex flex-row gap-0.5 shrink-0 p-1 bg-white dark:bg-gray-850 dark:text-gray-100 text-medium rounded-lg shadow-xl"
			>
				<button
					class="px-1 hover:bg-gray-50 dark:hover:bg-gray-800 rounded flex items-center gap-1 min-w-fit"
					on:click={() => {
						selectedText = window.getSelection().toString();
						floatingInput = true;
					}}
				>
					<ChatBubble className="size-3 shrink-0" />

					<div class="shrink-0">{$i18n.t('Ask')}</div>
				</button>
				<button
					class="px-1 hover:bg-gray-50 dark:hover:bg-gray-800 rounded flex items-center gap-1 min-w-fit"
					on:click={() => {
						const selection = window.getSelection();
						dispatch('select', {
							type: 'explain',
							content: selection.toString()
						});

						// Clear selection
						selection.removeAllRanges();
						buttonsContainerElement.style.display = 'none';
					}}
				>
					<LightBlub className="size-3 shrink-0" />

					<div class="shrink-0">{$i18n.t('Explain')}</div>
				</button>
			</div>
		{:else}
			<div
				class="py-1 flex dark:text-gray-100 bg-gray-50 dark:bg-gray-800 border dark:border-gray-800 w-72 rounded-full shadow-xl"
			>
				<input
					type="text"
					class="ml-5 bg-transparent outline-none w-full flex-1 text-sm"
					placeholder={$i18n.t('Ask a question')}
					bind:value={floatingInputValue}
					on:keydown={(e) => {
						if (e.key === 'Enter') {
							selectAskHandler();
						}
					}}
				/>

				<div class="ml-1 mr-2">
					<button
						class="{floatingInputValue !== ''
							? 'bg-black text-white hover:bg-gray-900 dark:bg-white dark:text-black dark:hover:bg-gray-100 '
							: 'text-white bg-gray-200 dark:text-gray-900 dark:bg-gray-700 disabled'} transition rounded-full p-1.5 m-0.5 self-center"
						on:click={() => {
							selectAskHandler();
						}}
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 16 16"
							fill="currentColor"
							class="size-4"
						>
							<path
								fill-rule="evenodd"
								d="M8 14a.75.75 0 0 1-.75-.75V4.56L4.03 7.78a.75.75 0 0 1-1.06-1.06l4.5-4.5a.75.75 0 0 1 1.06 0l4.5 4.5a.75.75 0 0 1-1.06 1.06L8.75 4.56v8.69A.75.75 0 0 1 8 14Z"
								clip-rule="evenodd"
							/>
						</svg>
					</button>
				</div>
			</div>
		{/if}
	</div>
=======
{#if floatingButtons && model}
	<FloatingButtons
		bind:this={floatingButtonsElement}
		{id}
		model={model?.id}
		messages={createMessagesList(history, id)}
		onAdd={({ modelId, parentId, messages }) => {
			console.log(modelId, parentId, messages);
			onAddMessages({ modelId, parentId, messages });
			closeFloatingButtons();
		}}
	/>
>>>>>>> upstream/main
{/if}
