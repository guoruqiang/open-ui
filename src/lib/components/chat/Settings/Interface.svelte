<script lang="ts">
	import { getBackendConfig } from '$lib/apis';
	import { setDefaultPromptSuggestions } from '$lib/apis/configs';
	import { config, models, settings, user } from '$lib/stores';
	import { createEventDispatcher, onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import { updateUserInfo } from '$lib/apis/users';
	import { getUserPosition } from '$lib/utils';
	import { uploadBackgroundImage } from '$lib/apis/files';

	const dispatch = createEventDispatcher();

	const i18n = getContext('i18n');

	export let saveSettings: Function;

	let backgroundImageUrl = '';
	let random_image_url = '';
	let inputFiles = null;
	let filesInputElement;

	// Addons
	let titleAutoGenerate = true;
	let autoTags = true;

	let responseAutoCopy = false;
	let widescreenMode = false;
	let splitLargeChunks = false;
	let scrollOnBranchChange = true;
	let userLocation = false;
	let enableFileUpdateBase64 = false;

	// Interface
	let defaultModelId = '';
	let showUsername = false;
	let richTextInput = true;
	let largeTextAsFile = false;
	let notificationSound = true;

	let landingPageMode = '';
	let chatBubble = true;
	let chatDirection: 'LTR' | 'RTL' = 'LTR';

	let imageCompression = false;
	let imageCompressionSize = {
		width: '',
		height: ''
	};

	// Admin - Show Update Available Toast
	let showUpdateToast = true;
	let showChangelog = true;

	let showEmojiInCall = false;
	let voiceInterruption = false;
	let hapticFeedback = false;

<<<<<<< HEAD
	let streamResponse = true;
=======
	let webSearch = null;
>>>>>>> upstream/main

	const toggleSplitLargeChunks = async () => {
		splitLargeChunks = !splitLargeChunks;
		saveSettings({ splitLargeChunks: splitLargeChunks });
	};

	const toggleStreamResponse = async () => {
		streamResponse = !streamResponse;
		saveSettings({ streamResponse: streamResponse });
	};

	const togglesScrollOnBranchChange = async () => {
		scrollOnBranchChange = !scrollOnBranchChange;
		saveSettings({ scrollOnBranchChange: scrollOnBranchChange });
	};

	const toggleWidescreenMode = async () => {
		widescreenMode = !widescreenMode;
		saveSettings({ widescreenMode: widescreenMode });
	};

	const toggleChatBubble = async () => {
		chatBubble = !chatBubble;
		saveSettings({ chatBubble: chatBubble });
	};

	const toggleLandingPageMode = async () => {
		landingPageMode = landingPageMode === '' ? 'chat' : '';
		saveSettings({ landingPageMode: landingPageMode });
	};

	const toggleShowUpdateToast = async () => {
		showUpdateToast = !showUpdateToast;
		saveSettings({ showUpdateToast: showUpdateToast });
	};

	const toggleNotificationSound = async () => {
		notificationSound = !notificationSound;
		saveSettings({ notificationSound: notificationSound });
	};

	const toggleShowChangelog = async () => {
		showChangelog = !showChangelog;
		saveSettings({ showChangelog: showChangelog });
	};

	const toggleShowUsername = async () => {
		showUsername = !showUsername;
		saveSettings({ showUsername: showUsername });
	};

	const toggleEmojiInCall = async () => {
		showEmojiInCall = !showEmojiInCall;
		saveSettings({ showEmojiInCall: showEmojiInCall });
	};

	const toggleVoiceInterruption = async () => {
		voiceInterruption = !voiceInterruption;
		saveSettings({ voiceInterruption: voiceInterruption });
	};

	const toggleImageCompression = async () => {
		imageCompression = !imageCompression;
		saveSettings({ imageCompression });
	};

	const toggleHapticFeedback = async () => {
		hapticFeedback = !hapticFeedback;
		saveSettings({ hapticFeedback: hapticFeedback });
	};

	const toggleUserLocation = async () => {
		userLocation = !userLocation;

		if (userLocation) {
			const position = await getUserPosition().catch((error) => {
				toast.error(error.message);
				return null;
			});

			if (position) {
				await updateUserInfo(localStorage.token, { location: position });
				toast.success($i18n.t('User location successfully retrieved.'));
			} else {
				userLocation = false;
			}
		}

		saveSettings({ userLocation });
	};

	const toggleTitleAutoGenerate = async () => {
		titleAutoGenerate = !titleAutoGenerate;
		saveSettings({
			title: {
				...$settings.title,
				auto: titleAutoGenerate
			}
		});
	};

<<<<<<< HEAD
	const toggleEnableFileUpdateBase64 = async () => {
		enableFileUpdateBase64 = !enableFileUpdateBase64;
		saveSettings({ enableFileUpdateBase64: enableFileUpdateBase64 });
=======
	const toggleAutoTags = async () => {
		autoTags = !autoTags;
		saveSettings({ autoTags });
	};

	const toggleRichTextInput = async () => {
		richTextInput = !richTextInput;
		saveSettings({ richTextInput });
	};

	const toggleLargeTextAsFile = async () => {
		largeTextAsFile = !largeTextAsFile;
		saveSettings({ largeTextAsFile });
>>>>>>> upstream/main
	};

	const toggleResponseAutoCopy = async () => {
		const permission = await navigator.clipboard
			.readText()
			.then(() => {
				return 'granted';
			})
			.catch(() => {
				return '';
			});

		console.log(permission);

		if (permission === 'granted') {
			responseAutoCopy = !responseAutoCopy;
			saveSettings({ responseAutoCopy: responseAutoCopy });
		} else {
			toast.error(
				$i18n.t(
					'Clipboard write permission denied. Please check your browser settings to grant the necessary access.'
				)
			);
		}
	};

	const toggleChangeChatDirection = async () => {
		chatDirection = chatDirection === 'LTR' ? 'RTL' : 'LTR';
		saveSettings({ chatDirection });
	};

	const updateInterfaceHandler = async () => {
		saveSettings({
			models: [defaultModelId],
			imageCompressionSize: imageCompressionSize
		});
	};

	const toggleWebSearch = async () => {
		webSearch = webSearch === null ? 'always' : null;
		saveSettings({ webSearch: webSearch });
	};

	onMount(async () => {
		titleAutoGenerate = $settings?.title?.auto ?? true;
		autoTags = $settings.autoTags ?? true;

		responseAutoCopy = $settings.responseAutoCopy ?? false;

		showUsername = $settings.showUsername ?? false;
		showUpdateToast = $settings.showUpdateToast ?? true;
		showChangelog = $settings.showChangelog ?? true;

		showEmojiInCall = $settings.showEmojiInCall ?? false;
		voiceInterruption = $settings.voiceInterruption ?? false;

		richTextInput = $settings.richTextInput ?? true;
		largeTextAsFile = $settings.largeTextAsFile ?? false;

		landingPageMode = $settings.landingPageMode ?? '';
		chatBubble = $settings.chatBubble ?? true;
		widescreenMode = $settings.widescreenMode ?? false;
		splitLargeChunks = $settings.splitLargeChunks ?? false;
		scrollOnBranchChange = $settings.scrollOnBranchChange ?? true;
		chatDirection = $settings.chatDirection ?? 'LTR';
		userLocation = $settings.userLocation ?? false;
		enableFileUpdateBase64 = $settings.enableFileUpdateBase64 ?? false;

		notificationSound = $settings.notificationSound ?? true;

		hapticFeedback = $settings.hapticFeedback ?? false;
		streamResponse = $settings?.streamResponse ?? true;

		imageCompression = $settings.imageCompression ?? false;
		imageCompressionSize = $settings.imageCompressionSize ?? { width: '', height: '' };

		defaultModelId = $settings?.models?.at(0) ?? '';
		if ($config?.default_models) {
			defaultModelId = $config.default_models.split(',')[0];
		}

		backgroundImageUrl = $settings.backgroundImageUrl ?? null;
<<<<<<< HEAD
		random_image_url = $config?.random_image_url ?? '';
=======
		webSearch = $settings.webSearch ?? null;
>>>>>>> upstream/main
	});
</script>

<form
	class="flex flex-col h-full justify-between space-y-3 text-sm"
	on:submit|preventDefault={() => {
		updateInterfaceHandler();
		dispatch('save');
	}}
>
	<input
		bind:this={filesInputElement}
		bind:files={inputFiles}
		type="file"
		hidden
		accept="image/*"
		on:change={async () => {
			if (!inputFiles || inputFiles.length === 0) {
				toast.error($i18n.t(`File not found.`));
				return;
			}

			const file = inputFiles[0];
			const validImageTypes = ['image/gif', 'image/webp', 'image/jpeg', 'image/png'];

			if (!validImageTypes.includes(file.type)) {
				toast.error(`文件只支持以下格式：${validImageTypes.join(', ')}`);
				inputFiles = null;
				return;
			}

			const reader = new FileReader();
			reader.onload = async (event) => {
				try {
					const res = await uploadBackgroundImage(localStorage.token, file);
					// Update the background_image_url
					backgroundImageUrl =
						res?.meta?.oss_url ||
						(res?.filename
							? `/api/v1/files/background/images/${res.filename}`
							: event.target.result);
					saveSettings({ backgroundImageUrl });
				} catch (error) {
					console.error('Error uploading image:', error);
					backgroundImageUrl = event.target.result;
					saveSettings({ backgroundImageUrl });
				}
			};

			reader.readAsDataURL(file);
		}}
	/>

	<div class=" space-y-3 overflow-y-scroll max-h-[28rem] lg:max-h-full">
		<div>
			<div class=" mb-1.5 text-sm font-medium">{$i18n.t('UI')}</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Landing Page Mode')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleLandingPageMode();
						}}
						type="button"
					>
						{#if landingPageMode === ''}
							<span class="ml-2 self-center">{$i18n.t('Default')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Chat')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Chat Bubble UI')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleChatBubble();
						}}
						type="button"
					>
						{#if chatBubble === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			{#if !$settings.chatBubble}
				<div>
					<div class=" py-0.5 flex w-full justify-between">
						<div class=" self-center text-xs">
							{$i18n.t('Display the username instead of You in the Chat')}
						</div>

						<button
							class="p-1 px-3 text-xs flex rounded-sm transition"
							on:click={() => {
								toggleShowUsername();
							}}
							type="button"
						>
							{#if showUsername === true}
								<span class="ml-2 self-center">{$i18n.t('On')}</span>
							{:else}
								<span class="ml-2 self-center">{$i18n.t('Off')}</span>
							{/if}
						</button>
					</div>
				</div>
			{/if}

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Widescreen Mode')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleWidescreenMode();
						}}
						type="button"
					>
						{#if widescreenMode === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Chat direction')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={toggleChangeChatDirection}
						type="button"
					>
						{#if chatDirection === 'LTR'}
							<span class="ml-2 self-center">{$i18n.t('LTR')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('RTL')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
<<<<<<< HEAD
						{$i18n.t('Stream Chat Response')}
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded transition"
						on:click={() => {
							toggleStreamResponse();
						}}
						type="button"
					>
						{#if streamResponse === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
						{$i18n.t('Fluidly stream large external response chunks')}
=======
						{$i18n.t('Notification Sound')}
>>>>>>> upstream/main
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleNotificationSound();
						}}
						type="button"
					>
						{#if notificationSound === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			{#if $user.role === 'admin'}
				<div>
					<div class=" py-0.5 flex w-full justify-between">
						<div class=" self-center text-xs">
							{$i18n.t('Toast notifications for new updates')}
						</div>

						<button
							class="p-1 px-3 text-xs flex rounded-sm transition"
							on:click={() => {
								toggleShowUpdateToast();
							}}
							type="button"
						>
							{#if showUpdateToast === true}
								<span class="ml-2 self-center">{$i18n.t('On')}</span>
							{:else}
								<span class="ml-2 self-center">{$i18n.t('Off')}</span>
							{/if}
						</button>
					</div>
				</div>

				<div>
					<div class=" py-0.5 flex w-full justify-between">
						<div class=" self-center text-xs">
							{$i18n.t(`Show "What's New" modal on login`)}
						</div>

						<button
							class="p-1 px-3 text-xs flex rounded-sm transition"
							on:click={() => {
								toggleShowChangelog();
							}}
							type="button"
						>
							{#if showChangelog === true}
								<span class="ml-2 self-center">{$i18n.t('On')}</span>
							{:else}
								<span class="ml-2 self-center">{$i18n.t('Off')}</span>
							{/if}
						</button>
					</div>
				</div>
			{/if}

			<div class=" my-1.5 text-sm font-medium">{$i18n.t('Chat')}</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Title Auto-Generation')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleTitleAutoGenerate();
						}}
						type="button"
					>
						{#if titleAutoGenerate === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Chat Tags Auto-Generation')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleAutoTags();
						}}
						type="button"
					>
						{#if autoTags === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
<<<<<<< HEAD
						{$i18n.t('Random Chat Background Image')}
=======
						{$i18n.t('Auto-Copy Response to Clipboard')}
>>>>>>> upstream/main
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
<<<<<<< HEAD
							if (backgroundImageUrl !== null) {
								backgroundImageUrl = null;
							} else {
								backgroundImageUrl = random_image_url;
								toast.success(
									$i18n.t(
										'Random background image has been enabled, you will get a new background image every time you refresh the page~'
									)
								);
							}
							saveSettings({ backgroundImageUrl });
						}}
						type="button"
					>
						{#if backgroundImageUrl !== null}
=======
							toggleResponseAutoCopy();
						}}
						type="button"
					>
						{#if responseAutoCopy === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
						{$i18n.t('Rich Text Input for Chat')}
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleRichTextInput();
						}}
						type="button"
					>
						{#if richTextInput === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
						{$i18n.t('Paste Large Text as File')}
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleLargeTextAsFile();
						}}
						type="button"
					>
						{#if largeTextAsFile === true}
>>>>>>> upstream/main
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
						{$i18n.t('Chat Background Image')}
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							if (backgroundImageUrl !== null) {
								backgroundImageUrl = null;
								saveSettings({ backgroundImageUrl });
							} else {
								filesInputElement.click();
							}
						}}
						type="button"
					>
						{#if backgroundImageUrl !== null}
							<span class="ml-2 self-center">{$i18n.t('Reset')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Upload')}</span>
						{/if}
					</button>
				</div>
			</div>

<<<<<<< HEAD
			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
						{$i18n.t('Scroll to bottom when switching between branches')}
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded transition"
						on:click={() => {
							togglesScrollOnBranchChange();
						}}
						type="button"
					>
						{#if scrollOnBranchChange === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div class=" my-1.5 text-sm font-medium">{$i18n.t('Chat')}</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Enable File-Update Base64')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded transition"
						on:click={() => {
							toggleEnableFileUpdateBase64();
						}}
						type="button"
					>
						{#if enableFileUpdateBase64 === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Title Auto-Generation')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded transition"
						on:click={() => {
							toggleTitleAutoGenerate();
						}}
						type="button"
					>
						{#if titleAutoGenerate === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
						{$i18n.t('Response AutoCopy to Clipboard')}
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded transition"
						on:click={() => {
							toggleResponseAutoCopy();
						}}
						type="button"
					>
						{#if responseAutoCopy === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

=======
>>>>>>> upstream/main
			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Allow User Location')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleUserLocation();
						}}
						type="button"
					>
						{#if userLocation === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Haptic Feedback')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleHapticFeedback();
						}}
						type="button"
					>
						{#if hapticFeedback === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<!-- <div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
						{$i18n.t('Fluidly stream large external response chunks')}
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleSplitLargeChunks();
						}}
						type="button"
					>
						{#if splitLargeChunks === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div> -->

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">
						{$i18n.t('Scroll to bottom when switching between branches')}
					</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							togglesScrollOnBranchChange();
						}}
						type="button"
					>
						{#if scrollOnBranchChange === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Web Search in Chat')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleWebSearch();
						}}
						type="button"
					>
						{#if webSearch === 'always'}
							<span class="ml-2 self-center">{$i18n.t('Always')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Default')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div class=" my-1.5 text-sm font-medium">{$i18n.t('Voice')}</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Allow Voice Interruption in Call')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleVoiceInterruption();
						}}
						type="button"
					>
						{#if voiceInterruption === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Display Emoji in Call')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleEmojiInCall();
						}}
						type="button"
					>
						{#if showEmojiInCall === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			<div class=" my-1.5 text-sm font-medium">{$i18n.t('File')}</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Image Compression')}</div>

					<button
						class="p-1 px-3 text-xs flex rounded-sm transition"
						on:click={() => {
							toggleImageCompression();
						}}
						type="button"
					>
						{#if imageCompression === true}
							<span class="ml-2 self-center">{$i18n.t('On')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Off')}</span>
						{/if}
					</button>
				</div>
			</div>

			{#if imageCompression}
				<div>
					<div class=" py-0.5 flex w-full justify-between text-xs">
						<div class=" self-center text-xs">{$i18n.t('Image Max Compression Size')}</div>

						<div>
							<input
								bind:value={imageCompressionSize.width}
								type="number"
								class="w-20 bg-transparent outline-hidden text-center"
								min="0"
								placeholder="Width"
							/>x
							<input
								bind:value={imageCompressionSize.height}
								type="number"
								class="w-20 bg-transparent outline-hidden text-center"
								min="0"
								placeholder="Height"
							/>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>

	<div class="flex justify-end text-sm font-medium">
		<button
			class="px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"
			type="submit"
		>
			{$i18n.t('Save')}
		</button>
	</div>
</form>
