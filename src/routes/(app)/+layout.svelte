<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { goto } from '$app/navigation';

<<<<<<< HEAD
	import { getModels as _getModels } from '$lib/apis';
	import { getAllChatTags } from '$lib/apis/chats';

=======
	import { getKnowledgeBases } from '$lib/apis/knowledge';
	import { getFunctions } from '$lib/apis/functions';
	import { getModels, getVersionUpdates } from '$lib/apis';
	import { getAllTags } from '$lib/apis/chats';
>>>>>>> upstream/main
	import { getPrompts } from '$lib/apis/prompts';
	import { getDocs } from '$lib/apis/documents';
	import { getTools } from '$lib/apis/tools';

	import { getBanners } from '$lib/apis/configs';
	import { getUserSettings } from '$lib/apis/users';

	import {
		user,
		showSettings,
		settings,
		models,
		prompts,
		documents,
		tags,
		banners,
		showChangelog,
		config,
		tools,
		functions,
		temporaryChatEnabled
	} from '$lib/stores';

	import SettingsModal from '$lib/components/chat/SettingsModal.svelte';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import ChangelogModal from '$lib/components/ChangelogModal.svelte';
	import AccountPending from '$lib/components/layout/Overlay/AccountPending.svelte';
	import { getFunctions } from '$lib/apis/functions';
	import { page } from '$app/stores';
	import dayjs from 'dayjs';

	let loaded = false;

	onMount(async () => {
		if ($user === undefined) {
			await goto('/auth');
<<<<<<< HEAD
		} else if (
			$user.role !== 'pending' ||
			($user?.expire_at !== null && $user?.expire_at < dayjs().unix() && $user.role !== 'admin')
		) {
			await Promise.all([
				(async () => {
					const userSettings = await getUserSettings(localStorage.token).catch((error) => {
						console.error(error);
						return null;
					});

					if (userSettings) {
						settings.set(userSettings.ui);
					} else {
						let localStorageSettings = {} as Parameters<(typeof settings)['set']>[0];

						try {
							localStorageSettings = JSON.parse(localStorage.getItem('settings') ?? '{}');
						} catch (e: unknown) {
							console.error('Failed to parse settings from localStorage', e);
						}

						settings.set(localStorageSettings);
					}
				})(),
				(async () => {
					try {
						models.set(await getModels());
					} catch (error) {
						console.error('Error fetching models:', error);
					}
				})(),
				(async () => {
					try {
						prompts.set(await getPrompts(localStorage.token));
					} catch (error) {
						console.error('Error fetching prompts:', error);
					}
				})(),
				(async () => {
					try {
						documents.set(await getDocs(localStorage.token));
					} catch (error) {
						console.error('Error fetching documents:', error);
					}
				})(),
				(async () => {
					try {
						tools.set(await getTools(localStorage.token));
					} catch (error) {
						console.error('Error fetching tools:', error);
					}
				})(),
				(async () => {
					try {
						functions.set(await getFunctions(localStorage.token));
					} catch (error) {
						console.error('Error fetching functions:', error);
					}
				})(),
				(async () => {
					try {
						banners.set(await getBanners(localStorage.token));
					} catch (error) {
						console.error('Error fetching banners:', error);
					}
				})(),
				(async () => {
					try {
						tags.set(await getAllChatTags(localStorage.token));
					} catch (error) {
						console.error('Error fetching tags:', error);
					}
				})()
			]);

			await tick();

			document.addEventListener('keydown', function (event) {
=======
		} else if (['user', 'admin'].includes($user.role)) {
			try {
				// Check if IndexedDB exists
				DB = await openDB('Chats', 1);

				if (DB) {
					const chats = await DB.getAllFromIndex('chats', 'timestamp');
					localDBChats = chats.map((item, idx) => chats[chats.length - 1 - idx]);

					if (localDBChats.length === 0) {
						await deleteDB('Chats');
					}
				}

				console.log(DB);
			} catch (error) {
				// IndexedDB Not Found
			}

			const userSettings = await getUserSettings(localStorage.token).catch((error) => {
				console.error(error);
				return null;
			});

			if (userSettings) {
				settings.set(userSettings.ui);
			} else {
				let localStorageSettings = {} as Parameters<(typeof settings)['set']>[0];

				try {
					localStorageSettings = JSON.parse(localStorage.getItem('settings') ?? '{}');
				} catch (e: unknown) {
					console.error('Failed to parse settings from localStorage', e);
				}

				settings.set(localStorageSettings);
			}

			models.set(
				await getModels(
					localStorage.token,
					$config?.features?.enable_direct_connections && ($settings?.directConnections ?? null)
				)
			);
			banners.set(await getBanners(localStorage.token));
			tools.set(await getTools(localStorage.token));

			document.addEventListener('keydown', async function (event) {
>>>>>>> upstream/main
				const isCtrlPressed = event.ctrlKey || event.metaKey; // metaKey is for Cmd key on Mac
				// Check if the Shift key is pressed
				const isShiftPressed = event.shiftKey;

				// Check if Ctrl + Shift + O is pressed
				if (isCtrlPressed && isShiftPressed && event.key.toLowerCase() === 'o') {
					event.preventDefault();
					console.log('newChat');
					document.getElementById('sidebar-new-chat-button')?.click();
				}

				// Check if Shift + Esc is pressed
				if (isShiftPressed && event.key === 'Escape') {
					event.preventDefault();
					console.log('focusInput');
					document.getElementById('chat-input')?.focus();
				}

				// Check if Ctrl + Shift + ; is pressed
				if (isCtrlPressed && isShiftPressed && event.key === ';') {
					event.preventDefault();
					console.log('copyLastCodeBlock');
					const button = [...document.getElementsByClassName('copy-code-button')]?.at(-1);
					button?.click();
				}

				// Check if Ctrl + Shift + C is pressed
				if (isCtrlPressed && isShiftPressed && event.key.toLowerCase() === 'c') {
					event.preventDefault();
					console.log('copyLastResponse');
					const button = [...document.getElementsByClassName('copy-response-button')]?.at(-1);
					console.log(button);
					button?.click();
				}

				// Check if Ctrl + Shift + S is pressed
				if (isCtrlPressed && isShiftPressed && event.key.toLowerCase() === 's') {
					event.preventDefault();
					console.log('toggleSidebar');
					document.getElementById('sidebar-toggle-button')?.click();
				}

				// Check if Ctrl + Shift + Backspace is pressed
				if (
					isCtrlPressed &&
					isShiftPressed &&
					(event.key === 'Backspace' || event.key === 'Delete')
				) {
					event.preventDefault();
					console.log('deleteChat');
					document.getElementById('delete-chat-button')?.click();
				}

				// Check if Ctrl + . is pressed
				if (isCtrlPressed && event.key === '.') {
					event.preventDefault();
					console.log('openSettings');
					showSettings.set(!$showSettings);
				}

				// Check if Ctrl + / is pressed
				if (isCtrlPressed && event.key === '/') {
					event.preventDefault();
					console.log('showShortcuts');
					document.getElementById('show-shortcuts-button')?.click();
				}

				// Check if Ctrl + Shift + ' is pressed
				if (isCtrlPressed && isShiftPressed && event.key.toLowerCase() === `'`) {
					event.preventDefault();
					console.log('temporaryChat');
					temporaryChatEnabled.set(!$temporaryChatEnabled);
					await goto('/');
					const newChatButton = document.getElementById('new-chat-button');
					setTimeout(() => {
						newChatButton?.click();
					}, 0);
				}
			});

			if ($user.role === 'admin' && ($settings?.showChangelog ?? true)) {
				showChangelog.set($settings?.version !== $config.version);
			}

			if ($page.url.searchParams.get('temporary-chat') === 'true') {
				temporaryChatEnabled.set(true);
			}

			await tick();
		}

		loaded = true;
	});
</script>

<SettingsModal bind:show={$showSettings} />
<ChangelogModal bind:show={$showChangelog} />

<<<<<<< HEAD
=======
{#if version && compareVersion(version.latest, version.current) && ($settings?.showUpdateToast ?? true)}
	<div class=" absolute bottom-8 right-8 z-50" in:fade={{ duration: 100 }}>
		<UpdateInfoToast
			{version}
			on:close={() => {
				localStorage.setItem('dismissedUpdateToast', Date.now().toString());
				version = null;
			}}
		/>
	</div>
{/if}

>>>>>>> upstream/main
<div class="app relative">
	<div
		class=" text-gray-700 dark:text-gray-100 bg-white dark:bg-gray-900 h-screen max-h-[100dvh] overflow-auto flex flex-row justify-end"
	>
		{#if loaded}
			{#if $user.role === 'pending' || ($user?.expire_at !== null && $user?.expire_at < dayjs().unix() && $user.role !== 'admin')}
				<AccountPending />
			{/if}

			<Sidebar />
			<slot />
		{/if}
	</div>
</div>

<style>
	.loading {
		display: inline-block;
		clip-path: inset(0 1ch 0 0);
		animation: l 1s steps(3) infinite;
		letter-spacing: -0.5px;
	}

	@keyframes l {
		to {
			clip-path: inset(0 -1ch 0 0);
		}
	}

	pre[class*='language-'] {
		position: relative;
		overflow: auto;

		/* make space  */
		margin: 5px 0;
		padding: 1.75rem 0 1.75rem 1rem;
		border-radius: 10px;
	}

	pre[class*='language-'] button {
		position: absolute;
		top: 5px;
		right: 5px;

		font-size: 0.9rem;
		padding: 0.15rem;
		background-color: #828282;

		border: ridge 1px #7b7b7c;
		border-radius: 5px;
		text-shadow: #c4c4c4 0 0 2px;
	}

	pre[class*='language-'] button:hover {
		cursor: pointer;
		background-color: #bcbabb;
	}
</style>
