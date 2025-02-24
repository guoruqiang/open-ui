<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import {
		WEBUI_NAME,
		showSidebar,
		functions,
		user,
		mobile,
		models,
		prompts,
		knowledge,
		tools
	} from '$lib/stores';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	import MenuLines from '$lib/components/icons/MenuLines.svelte';

	const i18n = getContext('i18n');

	let loaded = false;

	onMount(async () => {
		if ($user?.role !== 'admin') {
			if ($page.url.pathname.includes('/models') && !$user?.permissions?.workspace?.models) {
				goto('/');
			} else if (
				$page.url.pathname.includes('/knowledge') &&
				!$user?.permissions?.workspace?.knowledge
			) {
				goto('/');
			} else if (
				$page.url.pathname.includes('/prompts') &&
				!$user?.permissions?.workspace?.prompts
			) {
				goto('/');
			} else if ($page.url.pathname.includes('/tools') && !$user?.permissions?.workspace?.tools) {
				goto('/');
			}
		}

		loaded = true;
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Workspace')} | {$WEBUI_NAME}
	</title>
</svelte:head>

{#if loaded}
	<div
<<<<<<< HEAD
		class="font-primary flex flex-col w-full min-h-screen max-h-screen {$showSidebar
=======
		class=" relative flex flex-col w-full h-screen max-h-[100dvh] transition-width duration-200 ease-in-out {$showSidebar
>>>>>>> upstream/main
			? 'md:max-w-[calc(100%-260px)]'
			: ''} max-w-full"
	>
		<nav class="   px-2.5 pt-1 backdrop-blur-xl drag-region">
			<div class=" flex items-center gap-1">
				<div class="{$showSidebar ? 'md:hidden' : ''} self-center flex flex-none items-center">
					<button
						id="sidebar-toggle-button"
						class="cursor-pointer p-1.5 flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition"
						on:click={() => {
							showSidebar.set(!$showSidebar);
						}}
						aria-label="Toggle Sidebar"
					>
						<div class=" m-auto self-center">
							<MenuLines />
						</div>
					</button>
				</div>

				<div class="">
					<div
						class="flex gap-1 scrollbar-none overflow-x-auto w-fit text-center text-sm font-medium rounded-full bg-transparent py-1 touch-auto pointer-events-auto"
					>
						{#if $user?.role === 'admin' || $user?.permissions?.workspace?.models}
							<a
								class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes(
									'/workspace/models'
								)
									? ''
									: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
								href="/workspace/models">{$i18n.t('Models')}</a
							>
						{/if}

						{#if $user?.role === 'admin' || $user?.permissions?.workspace?.knowledge}
							<a
								class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes(
									'/workspace/knowledge'
								)
									? ''
									: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
								href="/workspace/knowledge"
							>
								{$i18n.t('Knowledge')}
							</a>
						{/if}

						{#if $user?.role === 'admin' || $user?.permissions?.workspace?.prompts}
							<a
								class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes(
									'/workspace/prompts'
								)
									? ''
									: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
								href="/workspace/prompts">{$i18n.t('Prompts')}</a
							>
						{/if}

						{#if $user?.role === 'admin' || $user?.permissions?.workspace?.tools}
							<a
								class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes('/workspace/tools')
									? ''
									: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
								href="/workspace/tools"
							>
								{$i18n.t('Tools')}
							</a>
						{/if}
					</div>
				</div>

				<!-- <div class="flex items-center text-xl font-semibold">{$i18n.t('Workspace')}</div> -->
			</div>
		</nav>

<<<<<<< HEAD
		<div class="px-4 my-1">
			<div
				class="flex scrollbar-none overflow-x-auto w-fit text-center text-sm font-medium rounded-xl bg-transparent/10 p-1"
			>
				<a
					class="min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes('/workspace/models')
						? 'bg-gray-50 dark:bg-gray-850'
						: ''} transition"
					href="/workspace/models">{$i18n.t('Models')}</a
				>

				<a
					class="min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes('/workspace/prompts')
						? 'bg-gray-50 dark:bg-gray-850'
						: ''} transition"
					href="/workspace/prompts">{$i18n.t('Prompts')}</a
				>

				<a
					class="min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes(
						'/workspace/documents'
					)
						? 'bg-gray-50 dark:bg-gray-850'
						: ''} transition"
					href="/workspace/documents"
				>
					{$i18n.t('Documents')}
				</a>

				<a
					class="min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes('/workspace/tools')
						? 'bg-gray-50 dark:bg-gray-850'
						: ''} transition"
					href="/workspace/tools"
				>
					{$i18n.t('Tools')}
				</a>

				<a
					class="min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes(
						'/workspace/functions'
					)
						? 'bg-gray-50 dark:bg-gray-850'
						: ''} transition"
					href="/workspace/functions"
				>
					{$i18n.t('Functions')}
				</a>
			</div>
		</div>

		<hr class=" my-2 dark:border-gray-850" />

		<div class=" py-1 px-5 flex-1 max-h-full overflow-y-auto">
=======
		<div class="  pb-1 px-[18px] flex-1 max-h-full overflow-y-auto" id="workspace-container">
>>>>>>> upstream/main
			<slot />
		</div>
	</div>
{/if}
