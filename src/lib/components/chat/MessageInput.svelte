<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { v4 as uuidv4 } from 'uuid';
<<<<<<< HEAD
	import { onMount, tick, getContext, createEventDispatcher } from 'svelte';
=======
	import { createPicker, getAuthToken } from '$lib/utils/google-drive-picker';

	import { onMount, tick, getContext, createEventDispatcher, onDestroy } from 'svelte';
>>>>>>> upstream/main
	const dispatch = createEventDispatcher();

	import {
		type Model,
		mobile,
		settings,
		showSidebar,
		models,
		config,
		showCallOverlay,
		tools,
		user as _user,
		showControls,
		TTSWorker
	} from '$lib/stores';

<<<<<<< HEAD
	import { processDocToVectorDB } from '$lib/apis/rag';

	import { blobToFile, findWordIndices } from '$lib/utils';
	import { transcribeAudio } from '$lib/apis/audio';
	import { uploadFile, base64ToFile } from '$lib/apis/files';

	import {
		SUPPORTED_FILE_TYPE,
		SUPPORTED_FILE_EXTENSIONS,
		WEBUI_BASE_URL,
		WEBUI_API_BASE_URL
	} from '$lib/constants';
=======
	import { blobToFile, compressImage, createMessagesList, findWordIndices } from '$lib/utils';
	import { transcribeAudio } from '$lib/apis/audio';
	import { uploadFile } from '$lib/apis/files';
	import { generateAutoCompletion } from '$lib/apis';
	import { deleteFileById } from '$lib/apis/files';

	import { WEBUI_BASE_URL, WEBUI_API_BASE_URL, PASTED_TEXT_CHARACTER_LIMIT } from '$lib/constants';
>>>>>>> upstream/main

	import InputMenu from './MessageInput/InputMenu.svelte';
	import VoiceRecording from './MessageInput/VoiceRecording.svelte';
	import FilesOverlay from './MessageInput/FilesOverlay.svelte';
	import Commands from './MessageInput/Commands.svelte';

	import RichTextInput from '../common/RichTextInput.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import FileItem from '../common/FileItem.svelte';
	import Image from '../common/Image.svelte';

	import XMark from '../icons/XMark.svelte';
	import Headphone from '../icons/Headphone.svelte';
	import GlobeAlt from '../icons/GlobeAlt.svelte';
	import PhotoSolid from '../icons/PhotoSolid.svelte';
	import Photo from '../icons/Photo.svelte';
	import CommandLine from '../icons/CommandLine.svelte';
	import { KokoroWorker } from '$lib/workers/KokoroWorker';

	const i18n = getContext('i18n');

	export let transparentBackground = false;

	export let onChange: Function = () => {};
	export let createMessagePair: Function;
	export let stopResponse: Function;

	export let autoScroll = false;

	export let atSelectedModel: Model | undefined = undefined;
	export let selectedModels: [''];

	let selectedModelIds = [];
	$: selectedModelIds = atSelectedModel !== undefined ? [atSelectedModel.id] : selectedModels;

	export let history;

	export let prompt = '';
	export let files = [];

	export let selectedToolIds = [];

	export let imageGenerationEnabled = false;
	export let webSearchEnabled = false;
	export let codeInterpreterEnabled = false;

	$: onChange({
		prompt,
		files,
		selectedToolIds,
		imageGenerationEnabled,
		webSearchEnabled
	});

	let loaded = false;
	let recording = false;

	let chatInputContainerElement;
	let chatInputElement;

	let filesInputElement;
	let commandsElement;

	let inputFiles;
	let dragged = false;

	let user = null;
	export let placeholder = '';

	let visionCapableModels = [];
	let notBase64CapableModels = [];

	$: visionCapableModels = [...(atSelectedModel ? [atSelectedModel] : selectedModels)].filter(
		(model) =>
			$models.find((m) => (atSelectedModel ? m.id === model.id : m.id === model))?.info?.meta
				?.capabilities?.vision ?? false
	);

	$: notBase64CapableModels = [...(atSelectedModel ? [atSelectedModel] : selectedModels)].filter(
		(model) =>
			!(
				$models.find((m) => (atSelectedModel ? m.id === model.id : m.id === model))?.info?.meta
					?.capabilities?.base64 ?? false
			)
	);

	const scrollToBottom = () => {
		const element = document.getElementById('messages-container');
		element.scrollTo({
			top: element.scrollHeight,
			behavior: 'smooth'
		});
	};

<<<<<<< HEAD
	const compressImage = (file) => {
		return new Promise((resolve, reject) => {
			const img = new Image();
			const originalImageUrl = URL.createObjectURL(file);
			img.src = originalImageUrl;

			img.onload = () => {
				const canvas = document.createElement('canvas');
				const ctx = canvas.getContext('2d');

				canvas.width = img.width;
				canvas.height = img.height;
				ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

				const maxFileSize = 2.5 * 1024 * 1024;
				const minFileSize = 2.0 * 1024 * 1024;
				let minRatio = 0.1;
				let maxRatio = 1.0;
				let compressionRatio = maxRatio;
				let compressedFile;
				const tolerance = 0.005;

				const tryCompress = (ratio) => {
					const base64 = canvas.toDataURL('image/jpeg', ratio);
					return base64ToFile(base64, `${crypto.randomUUID()}.jpg`);
				};

				while (maxRatio - minRatio > tolerance) {
					compressedFile = tryCompress(compressionRatio);
					const compressedFileSize = compressedFile.size;

					if (compressedFileSize <= maxFileSize && compressedFileSize >= minFileSize) {
						console.log('压缩文件已在目标区间内，停止压缩。');
						break;
					}

					if (compressedFileSize < minFileSize) {
						minRatio = compressionRatio;
					} else {
						maxRatio = compressionRatio;
					}
					compressionRatio = (minRatio + maxRatio) / 2;
				}

				console.log(`最终压缩率: ${compressionRatio}`);
				console.log(`最终文件大小: ${(compressedFile.size / 1024 / 1024).toFixed(2)} MB`);

				resolve(compressedFile);
			};
			img.onerror = (e) => reject(new Error('图片加载失败'));
		});
	};

	const uploadImageHandler = async (file) => {
		console.log(`Original file size: ${(file.size / 1024 / 1024).toFixed(2)} MB`);

		const imageItem = {
			id: null,
			url: '/loading.gif',
			status: 'uploaded',
			type: 'image',
			name: file.name,
			size: file.size,
			error: ''
		};

		files = [...files, imageItem];

		let compressedFile;
		try {
			compressedFile = await compressImage(file);
		} catch (error) {
			toast.error(error.message || error);
			compressedFile = file;
		}

		imageItem.name = compressedFile.name;
		imageItem.size = compressedFile.size;

		try {
			let uploadedFile = null;
			uploadedFile = await uploadFile(localStorage.token, compressedFile);
			if (uploadedFile) {
				const image_url = `${WEBUI_API_BASE_URL}/files/${uploadedFile.id}/preview`;
				imageItem.id = uploadFile.id;
				imageItem.status = 'processed';
				imageItem.url = image_url;
				files = files;
				files = files.filter(
					(f, index, self) =>
						index === self.findIndex((t) => t.name === f.name && t.size === f.size)
				);
			}
		} catch (error) {
			imageItem.status = '';
			toast.error(error.message || error);
		}
		files = files.filter((item) => item.status !== '');
	};

	const uploadFileHandler = async (file, base64_url, enableBase64) => {
		console.log(file);
=======
	const screenCaptureHandler = async () => {
		try {
			// Request screen media
			const mediaStream = await navigator.mediaDevices.getDisplayMedia({
				video: { cursor: 'never' },
				audio: false
			});
			// Once the user selects a screen, temporarily create a video element
			const video = document.createElement('video');
			video.srcObject = mediaStream;
			// Ensure the video loads without affecting user experience or tab switching
			await video.play();
			// Set up the canvas to match the video dimensions
			const canvas = document.createElement('canvas');
			canvas.width = video.videoWidth;
			canvas.height = video.videoHeight;
			// Grab a single frame from the video stream using the canvas
			const context = canvas.getContext('2d');
			context.drawImage(video, 0, 0, canvas.width, canvas.height);
			// Stop all video tracks (stop screen sharing) after capturing the image
			mediaStream.getTracks().forEach((track) => track.stop());
>>>>>>> upstream/main

			// bring back focus to this current tab, so that the user can see the screen capture
			window.focus();

			// Convert the canvas to a Base64 image URL
			const imageUrl = canvas.toDataURL('image/png');
			// Add the captured image to the files array to render it
			files = [...files, { type: 'image', url: imageUrl }];
			// Clean memory: Clear video srcObject
			video.srcObject = null;
		} catch (error) {
			// Handle any errors (e.g., user cancels screen sharing)
			console.error('Error capturing screen:', error);
		}
	};

	const uploadFileHandler = async (file, fullContext: boolean = false) => {
		if ($_user?.role !== 'admin' && !($_user?.permissions?.chat?.file_upload ?? true)) {
			toast.error($i18n.t('You do not have permission to upload files.'));
			return null;
		}

		const tempItemId = uuidv4();
		const fileItem = {
			type: 'file',
			file: '',
			id: null,
			url: '',
			name: file.name,
			collection_name: '',
			status: 'uploaded',
			size: file.size,
<<<<<<< HEAD
			base64: false,
			base64_url: '',
			error: ''
		};

		files = [...files, fileItem];
=======
			error: '',
			itemId: tempItemId,
			...(fullContext ? { context: 'full' } : {})
		};
>>>>>>> upstream/main

		if (fileItem.size == 0) {
			toast.error($i18n.t('You cannot upload an empty file.'));
			return null;
		}

		files = [...files, fileItem];
		// Check if the file is an audio file and transcribe/convert it to text file
		if (['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/x-m4a'].includes(file['type'])) {
			const res = await transcribeAudio(localStorage.token, file).catch((error) => {
				toast.error(`${error}`);
				return null;
			});

			if (res) {
				console.log(res);
				const blob = new Blob([res.text], { type: 'text/plain' });
				file = blobToFile(blob, `${file.name}.txt`);

				fileItem.name = file.name;
				fileItem.size = file.size;
			}
		}

		try {
			let uploadedFile = null;
			uploadedFile = await uploadFile(localStorage.token, file);

			if (uploadedFile) {
<<<<<<< HEAD
				fileItem.url = `${WEBUI_API_BASE_URL}/files/${uploadedFile.id}/content`;
				const fileType = file['type'];
				const fileExtension = file.name.split('.').pop();
				fileItem.id = uploadedFile.id;

				if (!enableBase64) {
					fileItem.file = uploadedFile;
					if (
						SUPPORTED_FILE_TYPE.includes(fileType) ||
						SUPPORTED_FILE_EXTENSIONS.includes(fileExtension)
					) {
						await processFileItem(fileItem);
					} else {
						toast.error(
							$i18n.t(
								`Unknown file type '{{file_type}}'. Proceeding with the file upload anyway.`,
								{
									file_type: fileType
								}
							)
						);
						await processFileItem(fileItem);
					}
				} else {
					fileItem.type = fileExtension;
					fileItem.base64 = true;
					fileItem.base64_url = `${WEBUI_API_BASE_URL}/files/${uploadedFile.id}/preview`;
					fileItem.status = 'processed';
					files = files;
				}
				files = files.filter(
					(f, index, self) =>
						index === self.findIndex((t) => t.name === f.name && t.size === f.size)
				);
			}
		} catch (error) {
			fileItem.status = '';
			toast.error(error.message || error);
=======
				console.log('File upload completed:', {
					id: uploadedFile.id,
					name: fileItem.name,
					collection: uploadedFile?.meta?.collection_name
				});

				if (uploadedFile.error) {
					console.warn('File upload warning:', uploadedFile.error);
					toast.warning(uploadedFile.error);
				}

				fileItem.status = 'uploaded';
				fileItem.file = uploadedFile;
				fileItem.id = uploadedFile.id;
				fileItem.collection_name =
					uploadedFile?.meta?.collection_name || uploadedFile?.collection_name;
				fileItem.url = `${WEBUI_API_BASE_URL}/files/${uploadedFile.id}`;

				files = files;
			} else {
				files = files.filter((item) => item?.itemId !== tempItemId);
			}
		} catch (e) {
			toast.error(`${e}`);
			files = files.filter((item) => item?.itemId !== tempItemId);
>>>>>>> upstream/main
		}
		files = files.filter((item) => item.status !== '');
	};

<<<<<<< HEAD
	const processFileItem = async (fileItem) => {
		try {
			const is_base64 = fileItem.base64;
			const res = await processDocToVectorDB(localStorage.token, fileItem.id, is_base64);

			if (res) {
				fileItem.status = 'processed';
				if (res.base64) {
					fileItem.base64 = true;
				} else {
					fileItem.collection_name = res.collection_name;
				}
=======
	const inputFilesHandler = async (inputFiles) => {
		console.log('Input files handler called with:', inputFiles);
		inputFiles.forEach((file) => {
			console.log('Processing file:', {
				name: file.name,
				type: file.type,
				size: file.size,
				extension: file.name.split('.').at(-1)
			});

			if (
				($config?.file?.max_size ?? null) !== null &&
				file.size > ($config?.file?.max_size ?? 0) * 1024 * 1024
			) {
				console.log('File exceeds max size limit:', {
					fileSize: file.size,
					maxSize: ($config?.file?.max_size ?? 0) * 1024 * 1024
				});
				toast.error(
					$i18n.t(`File size should not exceed {{maxSize}} MB.`, {
						maxSize: $config?.file?.max_size
					})
				);
				return;
			}

			if (
				['image/gif', 'image/webp', 'image/jpeg', 'image/png', 'image/avif'].includes(file['type'])
			) {
				if (visionCapableModels.length === 0) {
					toast.error($i18n.t('Selected model(s) do not support image inputs'));
					return;
				}
				let reader = new FileReader();
				reader.onload = async (event) => {
					let imageUrl = event.target.result;

					if ($settings?.imageCompression ?? false) {
						const width = $settings?.imageCompressionSize?.width ?? null;
						const height = $settings?.imageCompressionSize?.height ?? null;

						if (width || height) {
							imageUrl = await compressImage(imageUrl, width, height);
						}
					}

					files = [
						...files,
						{
							type: 'image',
							url: `${imageUrl}`
						}
					];
				};
				reader.readAsDataURL(file);
			} else {
				uploadFileHandler(file);
>>>>>>> upstream/main
			}
		} catch (e) {
			// Remove the failed doc from the files array
			// files = files.filter((f) => f.id !== fileItem.id);
			fileItem.status = '';
			toast.error(e);
		}
		files = files;
	};

	const processFileCountLimit = async (inputFiles) => {
		const maxFiles = $config?.file?.max_count || 1;
		const currentFilesCount = files.length;
		const inputFilesCount = inputFiles.length;
		const totalFilesCount = currentFilesCount + inputFilesCount;

		if (currentFilesCount >= maxFiles || totalFilesCount > maxFiles) {
			toast.error(
				$i18n.t('File count exceeds the limit of {{maxFiles}}. Please remove some files.', {
					maxFiles: maxFiles
				})
			);
			if (currentFilesCount >= maxFiles) {
				return [false, null];
			}
			if (totalFilesCount > maxFiles) {
				inputFiles = inputFiles.slice(0, maxFiles - currentFilesCount);
			}
		}
		return [true, inputFiles];
	};

	const readFileAsDataURL = (file) => {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.onload = (event) => resolve(event.target.result);
			reader.onerror = reject;
			reader.readAsDataURL(file);
		});
	};

<<<<<<< HEAD
	const processFileSizeLimit = async (file) => {
		const maxSizeInBytes = $config?.file?.max_size * 1024 * 1024;
		const isImage = ['image/gif', 'image/webp', 'image/jpeg', 'image/png'].includes(file.type);

		if (file.size > maxSizeInBytes) {
			toast.error(
				$i18n.t('File size should not exceed {{maxSize}} MB.', {
					maxSize: $config?.file?.max_size
				})
			);
			return;
		}

		if (file.size == 0) {
			toast.error($i18n.t('You cannot upload an empty file.'));
			return;
		}

		if (isImage && visionCapableModels.length === 0) {
			toast.error($i18n.t('Selected model(s) do not support image inputs'));
			return;
		}

		try {
			const dataURL = await readFileAsDataURL(file);
			if (isImage) {
				await uploadImageHandler(file);
			} else {
				const shouldUpdateBase64 = $settings?.enableFileUpdateBase64 ?? false;
				const modelsUpdateBase64 = shouldUpdateBase64 && notBase64CapableModels.length === 0;
				await uploadFileHandler(file, dataURL, modelsUpdateBase64);
			}
		} catch (error) {
			console.error('Error reading file:', error);
		}
	};

	onMount(() => {
		window.setTimeout(() => chatTextAreaElement?.focus(), 0);
=======
	const handleKeyDown = (event: KeyboardEvent) => {
		if (event.key === 'Escape') {
			console.log('Escape');
			dragged = false;
		}
	};
>>>>>>> upstream/main

	const onDragOver = (e) => {
		e.preventDefault();

		// Check if a file is being dragged.
		if (e.dataTransfer?.types?.includes('Files')) {
			dragged = true;
		} else {
			dragged = false;
		}
	};

	const onDragLeave = () => {
		dragged = false;
	};

<<<<<<< HEAD
			if (e.dataTransfer?.files) {
				const inputFiles = Array.from(e.dataTransfer?.files);
				if (inputFiles && inputFiles.length > 0) {
					const [canProcess, filesToProcess] = await processFileCountLimit(inputFiles);
					if (!canProcess) {
						dragged = false;
						return;
					}
					filesToProcess.forEach((file) => {
						console.log(file, file.name.split('.').at(-1));
						processFileSizeLimit(file);
					});
				} else {
					toast.error($i18n.t(`File not found.`));
				}
=======
	const onDrop = async (e) => {
		e.preventDefault();
		console.log(e);

		if (e.dataTransfer?.files) {
			const inputFiles = Array.from(e.dataTransfer?.files);
			if (inputFiles && inputFiles.length > 0) {
				console.log(inputFiles);
				inputFilesHandler(inputFiles);
>>>>>>> upstream/main
			}
		}

		dragged = false;
	};

	onMount(async () => {
		loaded = true;

		window.setTimeout(() => {
			const chatInput = document.getElementById('chat-input');
			chatInput?.focus();
		}, 0);

		window.addEventListener('keydown', handleKeyDown);

		await tick();

		const dropzoneElement = document.getElementById('chat-container');

		dropzoneElement?.addEventListener('dragover', onDragOver);
		dropzoneElement?.addEventListener('drop', onDrop);
		dropzoneElement?.addEventListener('dragleave', onDragLeave);
	});

	onDestroy(() => {
		console.log('destroy');
		window.removeEventListener('keydown', handleKeyDown);

		const dropzoneElement = document.getElementById('chat-container');

		if (dropzoneElement) {
			dropzoneElement?.removeEventListener('dragover', onDragOver);
			dropzoneElement?.removeEventListener('drop', onDrop);
			dropzoneElement?.removeEventListener('dragleave', onDragLeave);
		}
	});
</script>

<FilesOverlay show={dragged} />

{#if loaded}
	<div class="w-full font-primary">
		<div class=" mx-auto inset-x-0 bg-transparent flex justify-center">
			<div
				class="flex flex-col px-3 {($settings?.widescreenMode ?? null)
					? 'max-w-full'
					: 'max-w-6xl'} w-full"
			>
				<div class="relative">
					{#if autoScroll === false && history?.currentId}
						<div
							class=" absolute -top-12 left-0 right-0 flex justify-center z-30 pointer-events-none"
						>
<<<<<<< HEAD
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
								class="w-5 h-5"
							>
								<path
									fill-rule="evenodd"
									d="M10 3a.75.75 0 01.75.75v10.638l3.96-4.158a.75.75 0 111.08 1.04l-5.25 5.5a.75.75 0 01-1.08 0l-5.25-5.5a.75.75 0 111.08-1.04l3.96 4.158V3.75A.75.75 0 0110 3z"
									clip-rule="evenodd"
								/>
							</svg>
						</button>
					</div>
				{/if}
			</div>

			<div class="w-full relative">
				{#if atSelectedModel !== undefined}
					<div
						class="px-3 py-1 text-left w-full flex justify-between items-center absolute bottom-0 left-0 right-0 bg-gradient-to-t from-white dark:from-gray-900 z-10"
					>
						<div class="flex items-center gap-2 text-sm dark:text-gray-500">
							<img
								alt="model profile"
								class="size-4 max-w-[28px] object-cover rounded-full"
								src={$models.find((model) => model.id === atSelectedModel.id)?.info?.meta
									?.profile_image_url ??
									($i18n.language === 'dg-DG'
										? `/doge.png`
										: `${WEBUI_BASE_URL}/static/favicon.png`)}
							/>
							<div>
								<span>{$i18n.t('Talking to ')}</span><strong>{atSelectedModel.name}</strong>
							</div>
						</div>
						<div>
=======
>>>>>>> upstream/main
							<button
								class=" bg-white border border-gray-100 dark:border-none dark:bg-white/20 p-1.5 rounded-full pointer-events-auto"
								on:click={() => {
									autoScroll = true;
									scrollToBottom();
								}}
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 20 20"
									fill="currentColor"
									class="w-5 h-5"
								>
									<path
										fill-rule="evenodd"
										d="M10 3a.75.75 0 01.75.75v10.638l3.96-4.158a.75.75 0 111.08 1.04l-5.25 5.5a.75.75 0 01-1.08 0l-5.25-5.5a.75.75 0 111.08-1.04l3.96 4.158V3.75A.75.75 0 0110 3z"
										clip-rule="evenodd"
									/>
								</svg>
							</button>
						</div>
					{/if}
				</div>

<<<<<<< HEAD
				<Commands
					bind:this={commandsElement}
					bind:prompt
					bind:files
					on:select={(e) => {
						const data = e.detail;

						if (data?.type === 'model') {
							atSelectedModel = data.data;
						}

						chatTextAreaElement?.focus();
					}}
				/>
			</div>
		</div>
	</div>

	<div class="{transparentBackground ? 'bg-transparent' : 'bg-white dark:bg-gray-900'} ">
		<div class="max-w-6xl px-4 mx-auto inset-x-0">
			<div class="">
				<input
					bind:this={filesInputElement}
					bind:files={inputFiles}
					type="file"
					hidden
					multiple
					on:change={async () => {
						if (inputFiles && inputFiles.length > 0) {
							const _inputFiles = Array.from(inputFiles);
							const [canProcess, filesToProcess] = await processFileCountLimit(_inputFiles);
							if (!canProcess) {
								filesInputElement.value = '';
								return;
							}
							filesToProcess.forEach((file) => {
								console.log(file, file.name.split('.').at(-1));
								processFileSizeLimit(file);
							});
						} else {
							toast.error($i18n.t(`File not found.`));
						}

						filesInputElement.value = '';
					}}
				/>

				{#if recording}
					<VoiceRecording
						bind:recording
						on:cancel={async () => {
							recording = false;

							await tick();
							document.getElementById('chat-textarea')?.focus();
						}}
						on:confirm={async (e) => {
							const response = e.detail;
							prompt = `${prompt}${response} `;

							recording = false;

							await tick();
							document.getElementById('chat-textarea')?.focus();

							if ($settings?.speechAutoSend ?? false) {
								dispatch('submit', prompt);
							}
						}}
					/>
				{:else}
					<form
						class="w-full flex gap-1.5"
						on:submit|preventDefault={() => {
							// check if selectedModels support image input
							dispatch('submit', prompt);
						}}
					>
=======
				<div class="w-full relative">
					{#if atSelectedModel !== undefined || selectedToolIds.length > 0 || webSearchEnabled || ($settings?.webSearch ?? false) === 'always' || imageGenerationEnabled || codeInterpreterEnabled}
>>>>>>> upstream/main
						<div
							class="px-3 pb-0.5 pt-1.5 text-left w-full flex flex-col absolute bottom-0 left-0 right-0 bg-linear-to-t from-white dark:from-gray-900 z-10"
						>
<<<<<<< HEAD
							{#if files.length > 0}
								<div class="mx-1 mt-2.5 mb-1 flex flex-wrap gap-2">
									{#each files as file, fileIdx}
										{#if file.type === 'image'}
											<div class=" relative group">
												<div class="relative">
													<img
														src={file.url}
														alt="input"
														class=" h-16 w-16 rounded-xl object-cover bg-white"
													/>
													{#if atSelectedModel ? visionCapableModels.length === 0 : selectedModels.length !== visionCapableModels.length}
														<Tooltip
															className=" absolute top-1 left-1"
															content={$i18n.t('{{ models }}', {
																models: [...(atSelectedModel ? [atSelectedModel] : selectedModels)]
																	.filter((id) => !visionCapableModels.includes(id))
																	.join(', ')
															})}
														>
															<svg
																xmlns="http://www.w3.org/2000/svg"
																viewBox="0 0 24 24"
																fill="currentColor"
																class="size-4 fill-yellow-300"
															>
																<path
																	fill-rule="evenodd"
																	d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z"
																	clip-rule="evenodd"
																/>
															</svg>
														</Tooltip>
													{/if}
												</div>
												<div class=" absolute -top-1 -right-1">
													<button
														class=" bg-gray-400 text-white border border-white rounded-full group-hover:visible invisible transition"
														type="button"
														on:click={() => {
															files.splice(fileIdx, 1);
															files = files;
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
											</div>
										{:else}
											<FileItem
												name={file.name}
												type={file.type}
												size={file?.size}
												status={file.status}
												dismissible={true}
												on:dismiss={() => {
													files.splice(fileIdx, 1);
													files = files;
												}}
											/>
										{/if}
									{/each}
								</div>
							{/if}

							<div class=" flex">
								<div class=" self-center ml-0.5 flex space-x-1">
									<InputMenu
										bind:webSearchEnabled
										bind:selectedToolIds
										tools={$tools.reduce((a, e, i, arr) => {
											if (availableToolIds.includes(e.id) || ($_user?.role ?? 'user') === 'admin') {
												a[e.id] = {
													name: e.name,
													description: e.meta.description,
													icon_url: e.meta?.manifest?.icon_url || null,
													enabled: false
												};
											}
											return a;
										}, {})}
										uploadFilesHandler={() => {
											filesInputElement.click();
										}}
										onClose={async () => {
											await tick();
											chatTextAreaElement?.focus();
										}}
									>
										<button
											class="bg-gray-50 hover:bg-gray-100 text-gray-800 dark:bg-gray-850 dark:text-white dark:hover:bg-gray-800 transition rounded-full p-2 outline-none focus:outline-none"
											type="button"
											aria-label="More"
										>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												viewBox="0 0 24 24"
												fill="currentColor"
												class="size-5"
											>
												<path
													d="M9 7C9 4.23858 11.2386 2 14 2C16.7614 2 19 4.23858 19 7V15C19 18.866 15.866 22 12 22C8.13401 22 5 18.866 5 15V9C5 8.44772 5.44772 8 6 8C6.55228 8 7 8.44772 7 9V15C7 17.7614 9.23858 20 12 20C14.7614 20 17 17.7614 17 15V7C17 5.34315 15.6569 4 14 4C12.3431 4 11 5.34315 11 7V15C11 15.5523 11.4477 16 12 16C12.5523 16 13 15.5523 13 15V9C13 8.44772 13.4477 8 14 8C14.5523 8 15 8.44772 15 9V15C15 16.6569 13.6569 18 12 18C10.3431 18 9 16.6569 9 15V7Z"
=======
							{#if selectedToolIds.length > 0}
								<div class="flex items-center justify-between w-full">
									<div class="flex items-center gap-2.5 text-sm dark:text-gray-500">
										<div class="pl-1">
											<span class="relative flex size-2">
												<span
													class="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-400 opacity-75"
												/>
												<span class="relative inline-flex rounded-full size-2 bg-yellow-500" />
											</span>
										</div>
										<div class="  text-ellipsis line-clamp-1 flex">
											{#each selectedToolIds.map((id) => {
												return $tools ? $tools.find((t) => t.id === id) : { id: id, name: id };
											}) as tool, toolIdx (toolIdx)}
												<Tooltip
													content={tool?.meta?.description ?? ''}
													className=" {toolIdx !== 0 ? 'pl-0.5' : ''} shrink-0"
													placement="top"
												>
													{tool.name}
												</Tooltip>

												{#if toolIdx !== selectedToolIds.length - 1}
													<span>, </span>
												{/if}
											{/each}
										</div>
									</div>
								</div>
							{/if}

							{#if webSearchEnabled || ($config?.features?.enable_web_search && ($settings?.webSearch ?? false)) === 'always'}
								<div class="flex items-center justify-between w-full">
									<div class="flex items-center gap-2.5 text-sm dark:text-gray-500">
										<div class="pl-1">
											<span class="relative flex size-2">
												<span
													class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"
>>>>>>> upstream/main
												/>
												<span class="relative inline-flex rounded-full size-2 bg-blue-500" />
											</span>
										</div>
										<div class=" translate-y-[0.5px]">{$i18n.t('Search the internet')}</div>
									</div>
								</div>
							{/if}

<<<<<<< HEAD
								<textarea
									id="chat-textarea"
									bind:this={chatTextAreaElement}
									class="scrollbar-hidden bg-gray-50 dark:bg-gray-850 dark:text-gray-100 outline-none w-full py-3 px-1 rounded-xl resize-none h-[48px]"
									placeholder={placeholder
										? placeholder
										: $i18n.t('Send a Message and Use @ to Select a Model')}
									bind:value={prompt}
									on:keypress={(e) => {
										if (
											!$mobile ||
											!(
												'ontouchstart' in window ||
												navigator.maxTouchPoints > 0 ||
												navigator.msMaxTouchPoints > 0
											)
										) {
											// Prevent Enter key from creating a new line
											if (e.key === 'Enter' && !e.shiftKey) {
												e.preventDefault();
											}
=======
							{#if imageGenerationEnabled}
								<div class="flex items-center justify-between w-full">
									<div class="flex items-center gap-2.5 text-sm dark:text-gray-500">
										<div class="pl-1">
											<span class="relative flex size-2">
												<span
													class="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"
												/>
												<span class="relative inline-flex rounded-full size-2 bg-teal-500" />
											</span>
										</div>
										<div class=" translate-y-[0.5px]">{$i18n.t('Generate an image')}</div>
									</div>
								</div>
							{/if}
>>>>>>> upstream/main

							{#if codeInterpreterEnabled}
								<div class="flex items-center justify-between w-full">
									<div class="flex items-center gap-2.5 text-sm dark:text-gray-500">
										<div class="pl-1">
											<span class="relative flex size-2">
												<span
													class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"
												/>
												<span class="relative inline-flex rounded-full size-2 bg-green-500" />
											</span>
										</div>
										<div class=" translate-y-[0.5px]">{$i18n.t('Execute code for analysis')}</div>
									</div>
								</div>
							{/if}

							{#if atSelectedModel !== undefined}
								<div class="flex items-center justify-between w-full">
									<div class="pl-[1px] flex items-center gap-2 text-sm dark:text-gray-500">
										<img
											crossorigin="anonymous"
											alt="model profile"
											class="size-3.5 max-w-[28px] object-cover rounded-full"
											src={$models.find((model) => model.id === atSelectedModel.id)?.info?.meta
												?.profile_image_url ??
												($i18n.language === 'dg-DG'
													? `/doge.png`
													: `${WEBUI_BASE_URL}/static/favicon.png`)}
										/>
										<div class="translate-y-[0.5px]">
											Talking to <span class=" font-medium">{atSelectedModel.name}</span>
										</div>
									</div>
									<div>
										<button
											class="flex items-center dark:text-gray-500"
											on:click={() => {
												atSelectedModel = undefined;
											}}
										>
											<XMark />
										</button>
									</div>
								</div>
							{/if}
						</div>
					{/if}

					<Commands
						bind:this={commandsElement}
						bind:prompt
						bind:files
						on:upload={(e) => {
							dispatch('upload', e.detail);
						}}
						on:select={(e) => {
							const data = e.detail;

							if (data?.type === 'model') {
								atSelectedModel = data.data;
							}

							const chatInputElement = document.getElementById('chat-input');
							chatInputElement?.focus();
						}}
					/>
				</div>
			</div>
		</div>

		<div class="{transparentBackground ? 'bg-transparent' : 'bg-white dark:bg-gray-900'} ">
			<div
				class="{($settings?.widescreenMode ?? null)
					? 'max-w-full'
					: 'max-w-6xl'} px-2.5 mx-auto inset-x-0"
			>
				<div class="">
					<input
						bind:this={filesInputElement}
						bind:files={inputFiles}
						type="file"
						hidden
						multiple
						on:change={async () => {
							if (inputFiles && inputFiles.length > 0) {
								const _inputFiles = Array.from(inputFiles);
								inputFilesHandler(_inputFiles);
							} else {
								toast.error($i18n.t(`File not found.`));
							}

							filesInputElement.value = '';
						}}
					/>

					{#if recording}
						<VoiceRecording
							bind:recording
							on:cancel={async () => {
								recording = false;

								await tick();
								document.getElementById('chat-input')?.focus();
							}}
							on:confirm={async (e) => {
								const { text, filename } = e.detail;
								prompt = `${prompt}${text} `;

								recording = false;

								await tick();
								document.getElementById('chat-input')?.focus();

<<<<<<< HEAD
											const commandOptionButton = [
												...document.getElementsByClassName('selected-command-option-button')
											]?.at(-1);
											commandOptionButton.scrollIntoView({ block: 'center' });
										}

										if (commandsContainerElement && e.key === 'ArrowDown') {
											e.preventDefault();
											commandsElement.selectDown();

											const commandOptionButton = [
												...document.getElementsByClassName('selected-command-option-button')
											]?.at(-1);
											commandOptionButton.scrollIntoView({ block: 'center' });
										}

										if (commandsContainerElement && e.key === 'Enter') {
											e.preventDefault();

											const commandOptionButton = [
												...document.getElementsByClassName('selected-command-option-button')
											]?.at(-1);

											if (e.shiftKey) {
												prompt = `${prompt}\n`;
											} else if (commandOptionButton) {
												commandOptionButton?.click();
											} else {
												document.getElementById('send-message-button')?.click();
											}
										}

										if (commandsContainerElement && e.key === 'Tab') {
											e.preventDefault();

											const commandOptionButton = [
												...document.getElementsByClassName('selected-command-option-button')
											]?.at(-1);

											commandOptionButton?.click();
										} else if (e.key === 'Tab') {
											const words = findWordIndices(prompt);

											if (words.length > 0) {
												const word = words.at(0);
												const fullPrompt = prompt;

												prompt = prompt.substring(0, word?.endIndex + 1);
												await tick();

												e.target.scrollTop = e.target.scrollHeight;
												prompt = fullPrompt;
												await tick();

												e.preventDefault();
												e.target.setSelectionRange(word?.startIndex, word.endIndex + 1);
											}

											e.target.style.height = '';
											e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
										}

										if (e.key === 'Escape') {
											console.log('Escape');
											atSelectedModel = undefined;
										}
									}}
									rows="1"
									on:input={async (e) => {
										e.target.style.height = '';
										e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
										user = null;
									}}
									on:focus={async (e) => {
										e.target.style.height = '';
										e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
									}}
									on:paste={async (e) => {
										const clipboardData = e.clipboardData || window.clipboardData;

										try {
											if (clipboardData && clipboardData.items) {
												const inputFiles = Array.from(clipboardData.items)
													.map((item) => item.getAsFile())
													.filter((file) => file);

												const [canProcess, filesToProcess] =
													await processFileCountLimit(inputFiles);
												if (!canProcess) {
													return;
												}
												filesToProcess.forEach((file) => {
													console.log(file, file.name.split('.').at(-1));
													processFileSizeLimit(file);
												});
											} else {
												toast.error($i18n.t(`File not found.`));
											}
										} catch (error) {
											console.error('Error processing files:', error);
											toast.error($i18n.t(`An error occurred while processing files.`));
										}
									}}
								/>

								<div class="self-center flex space-x-1 mr-1.5">
									{#if !history?.currentId || history.messages[history.currentId]?.done == true}
										<Tooltip content={$i18n.t('Record voice')}>
											<button
												id="voice-input-button"
												class=" text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-850 transition rounded-full p-1.5 mr-0.5 self-center"
												type="button"
												on:click={async () => {
													try {
														let stream = await navigator.mediaDevices
															.getUserMedia({ audio: true })
															.catch(function (err) {
																toast.error(
																	$i18n.t(
																		`Permission denied when accessing microphone: {{error}}`,
																		{
																			error: err
																		}
																	)
																);
																return null;
															});

														if (stream) {
															recording = true;
															const tracks = stream.getTracks();
															tracks.forEach((track) => track.stop());
=======
								if ($settings?.speechAutoSend ?? false) {
									dispatch('submit', prompt);
								}
							}}
						/>
					{:else}
						<form
							class="w-full flex gap-1.5"
							on:submit|preventDefault={() => {
								// check if selectedModels support image input
								dispatch('submit', prompt);
							}}
						>
							<div
								class="flex-1 flex flex-col relative w-full rounded-3xl px-1 bg-gray-600/5 dark:bg-gray-400/5 dark:text-gray-100"
								dir={$settings?.chatDirection ?? 'LTR'}
							>
								{#if files.length > 0}
									<div class="mx-2 mt-2.5 -mb-1 flex items-center flex-wrap gap-2">
										{#each files as file, fileIdx}
											{#if file.type === 'image'}
												<div class=" relative group">
													<div class="relative flex items-center">
														<Image
															src={file.url}
															alt="input"
															imageClassName=" size-14 rounded-xl object-cover"
														/>
														{#if atSelectedModel ? visionCapableModels.length === 0 : selectedModels.length !== visionCapableModels.length}
															<Tooltip
																className=" absolute top-1 left-1"
																content={$i18n.t('{{ models }}', {
																	models: [
																		...(atSelectedModel ? [atSelectedModel] : selectedModels)
																	]
																		.filter((id) => !visionCapableModels.includes(id))
																		.join(', ')
																})}
															>
																<svg
																	xmlns="http://www.w3.org/2000/svg"
																	viewBox="0 0 24 24"
																	fill="currentColor"
																	class="size-4 fill-yellow-300"
																>
																	<path
																		fill-rule="evenodd"
																		d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z"
																		clip-rule="evenodd"
																	/>
																</svg>
															</Tooltip>
														{/if}
													</div>
													<div class=" absolute -top-1 -right-1">
														<button
															class=" bg-white text-black border border-white rounded-full group-hover:visible invisible transition"
															type="button"
															on:click={() => {
																files.splice(fileIdx, 1);
																files = files;
															}}
														>
															<svg
																xmlns="http://www.w3.org/2000/svg"
																viewBox="0 0 20 20"
																fill="currentColor"
																class="size-4"
															>
																<path
																	d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
																/>
															</svg>
														</button>
													</div>
												</div>
											{:else}
												<FileItem
													item={file}
													name={file.name}
													type={file.type}
													size={file?.size}
													loading={file.status === 'uploading'}
													dismissible={true}
													edit={true}
													on:dismiss={async () => {
														if (file.type !== 'collection' && !file?.collection) {
															if (file.id) {
																// This will handle both file deletion and Chroma cleanup
																await deleteFileById(localStorage.token, file.id);
															}
>>>>>>> upstream/main
														}

														// Remove from UI state
														files.splice(fileIdx, 1);
														files = files;
													}}
													on:click={() => {
														console.log(file);
													}}
												/>
											{/if}
										{/each}
									</div>
								{/if}

								<div class="px-2.5">
									{#if $settings?.richTextInput ?? true}
										<div
											class="scrollbar-hidden text-left bg-transparent dark:text-gray-100 outline-hidden w-full pt-3 px-1 resize-none h-fit max-h-80 overflow-auto"
										>
											<RichTextInput
												bind:this={chatInputElement}
												bind:value={prompt}
												id="chat-input"
												messageInput={true}
												shiftEnter={!$mobile ||
													!(
														'ontouchstart' in window ||
														navigator.maxTouchPoints > 0 ||
														navigator.msMaxTouchPoints > 0
													)}
												placeholder={placeholder ? placeholder : $i18n.t('Send a Message')}
												largeTextAsFile={$settings?.largeTextAsFile ?? false}
												autocomplete={$config?.features.enable_autocomplete_generation}
												generateAutoCompletion={async (text) => {
													if (selectedModelIds.length === 0 || !selectedModelIds.at(0)) {
														toast.error($i18n.t('Please select a model first.'));
													}

													const res = await generateAutoCompletion(
														localStorage.token,
														selectedModelIds.at(0),
														text,
														history?.currentId
															? createMessagesList(history, history.currentId)
															: null
													).catch((error) => {
														console.log(error);

														return null;
													});

													console.log(res);
													return res;
												}}
												on:keydown={async (e) => {
													e = e.detail.event;

													const isCtrlPressed = e.ctrlKey || e.metaKey; // metaKey is for Cmd key on Mac
													const commandsContainerElement =
														document.getElementById('commands-container');

													if (e.key === 'Escape') {
														stopResponse();
													}

													// Command/Ctrl + Shift + Enter to submit a message pair
													if (isCtrlPressed && e.key === 'Enter' && e.shiftKey) {
														e.preventDefault();
														createMessagePair(prompt);
													}

													// Check if Ctrl + R is pressed
													if (prompt === '' && isCtrlPressed && e.key.toLowerCase() === 'r') {
														e.preventDefault();
														console.log('regenerate');

														const regenerateButton = [
															...document.getElementsByClassName('regenerate-response-button')
														]?.at(-1);

														regenerateButton?.click();
													}

													if (prompt === '' && e.key == 'ArrowUp') {
														e.preventDefault();

														const userMessageElement = [
															...document.getElementsByClassName('user-message')
														]?.at(-1);

														if (userMessageElement) {
															userMessageElement.scrollIntoView({ block: 'center' });
															const editButton = [
																...document.getElementsByClassName('edit-user-message-button')
															]?.at(-1);

															editButton?.click();
														}
													}

													if (commandsContainerElement) {
														if (commandsContainerElement && e.key === 'ArrowUp') {
															e.preventDefault();
															commandsElement.selectUp();

															const commandOptionButton = [
																...document.getElementsByClassName('selected-command-option-button')
															]?.at(-1);
															commandOptionButton.scrollIntoView({ block: 'center' });
														}

														if (commandsContainerElement && e.key === 'ArrowDown') {
															e.preventDefault();
															commandsElement.selectDown();

															const commandOptionButton = [
																...document.getElementsByClassName('selected-command-option-button')
															]?.at(-1);
															commandOptionButton.scrollIntoView({ block: 'center' });
														}

														if (commandsContainerElement && e.key === 'Tab') {
															e.preventDefault();

															const commandOptionButton = [
																...document.getElementsByClassName('selected-command-option-button')
															]?.at(-1);

															commandOptionButton?.click();
														}

														if (commandsContainerElement && e.key === 'Enter') {
															e.preventDefault();

															const commandOptionButton = [
																...document.getElementsByClassName('selected-command-option-button')
															]?.at(-1);

															if (commandOptionButton) {
																commandOptionButton?.click();
															} else {
																document.getElementById('send-message-button')?.click();
															}
														}
													} else {
														if (
															!$mobile ||
															!(
																'ontouchstart' in window ||
																navigator.maxTouchPoints > 0 ||
																navigator.msMaxTouchPoints > 0
															)
														) {
															// Prevent Enter key from creating a new line
															// Uses keyCode '13' for Enter key for chinese/japanese keyboards
															if (e.keyCode === 13 && !e.shiftKey) {
																e.preventDefault();
															}

															// Submit the prompt when Enter key is pressed
															if (prompt !== '' && e.keyCode === 13 && !e.shiftKey) {
																dispatch('submit', prompt);
															}
														}
													}

													if (e.key === 'Escape') {
														console.log('Escape');
														atSelectedModel = undefined;
														selectedToolIds = [];
														webSearchEnabled = false;
														imageGenerationEnabled = false;
													}
												}}
												on:paste={async (e) => {
													e = e.detail.event;
													console.log(e);

													const clipboardData = e.clipboardData || window.clipboardData;

													if (clipboardData && clipboardData.items) {
														for (const item of clipboardData.items) {
															if (item.type.indexOf('image') !== -1) {
																const blob = item.getAsFile();
																const reader = new FileReader();

																reader.onload = function (e) {
																	files = [
																		...files,
																		{
																			type: 'image',
																			url: `${e.target.result}`
																		}
																	];
																};

																reader.readAsDataURL(blob);
															} else if (item.type === 'text/plain') {
																if ($settings?.largeTextAsFile ?? false) {
																	const text = clipboardData.getData('text/plain');

																	if (text.length > PASTED_TEXT_CHARACTER_LIMIT) {
																		e.preventDefault();
																		const blob = new Blob([text], { type: 'text/plain' });
																		const file = new File([blob], `Pasted_Text_${Date.now()}.txt`, {
																			type: 'text/plain'
																		});

																		await uploadFileHandler(file, true);
																	}
																}
															}
														}
													}
												}}
											/>
										</div>
									{:else}
										<textarea
											id="chat-input"
											bind:this={chatInputElement}
											class="scrollbar-hidden bg-transparent dark:text-gray-100 outline-hidden w-full pt-3 px-1 resize-none"
											placeholder={placeholder ? placeholder : $i18n.t('Send a Message')}
											bind:value={prompt}
											on:keypress={(e) => {
												if (
													!$mobile ||
													!(
														'ontouchstart' in window ||
														navigator.maxTouchPoints > 0 ||
														navigator.msMaxTouchPoints > 0
													)
												) {
													// Prevent Enter key from creating a new line
													if (e.key === 'Enter' && !e.shiftKey) {
														e.preventDefault();
													}

													// Submit the prompt when Enter key is pressed
													if (prompt !== '' && e.key === 'Enter' && !e.shiftKey) {
														dispatch('submit', prompt);
													}
												}
											}}
											on:keydown={async (e) => {
												const isCtrlPressed = e.ctrlKey || e.metaKey; // metaKey is for Cmd key on Mac
												const commandsContainerElement =
													document.getElementById('commands-container');

												if (e.key === 'Escape') {
													stopResponse();
												}
												// Command/Ctrl + Shift + Enter to submit a message pair
												if (isCtrlPressed && e.key === 'Enter' && e.shiftKey) {
													e.preventDefault();
													createMessagePair(prompt);
												}

												// Check if Ctrl + R is pressed
												if (prompt === '' && isCtrlPressed && e.key.toLowerCase() === 'r') {
													e.preventDefault();
													console.log('regenerate');

													const regenerateButton = [
														...document.getElementsByClassName('regenerate-response-button')
													]?.at(-1);

													regenerateButton?.click();
												}

												if (prompt === '' && e.key == 'ArrowUp') {
													e.preventDefault();

													const userMessageElement = [
														...document.getElementsByClassName('user-message')
													]?.at(-1);

													const editButton = [
														...document.getElementsByClassName('edit-user-message-button')
													]?.at(-1);

													console.log(userMessageElement);

													userMessageElement.scrollIntoView({ block: 'center' });
													editButton?.click();
												}

												if (commandsContainerElement && e.key === 'ArrowUp') {
													e.preventDefault();
													commandsElement.selectUp();

													const commandOptionButton = [
														...document.getElementsByClassName('selected-command-option-button')
													]?.at(-1);
													commandOptionButton.scrollIntoView({ block: 'center' });
												}

												if (commandsContainerElement && e.key === 'ArrowDown') {
													e.preventDefault();
													commandsElement.selectDown();

													const commandOptionButton = [
														...document.getElementsByClassName('selected-command-option-button')
													]?.at(-1);
													commandOptionButton.scrollIntoView({ block: 'center' });
												}

												if (commandsContainerElement && e.key === 'Enter') {
													e.preventDefault();

													const commandOptionButton = [
														...document.getElementsByClassName('selected-command-option-button')
													]?.at(-1);

													if (e.shiftKey) {
														prompt = `${prompt}\n`;
													} else if (commandOptionButton) {
														commandOptionButton?.click();
													} else {
														document.getElementById('send-message-button')?.click();
													}
												}

												if (commandsContainerElement && e.key === 'Tab') {
													e.preventDefault();

													const commandOptionButton = [
														...document.getElementsByClassName('selected-command-option-button')
													]?.at(-1);

													commandOptionButton?.click();
												} else if (e.key === 'Tab') {
													const words = findWordIndices(prompt);

													if (words.length > 0) {
														const word = words.at(0);
														const fullPrompt = prompt;

														prompt = prompt.substring(0, word?.endIndex + 1);
														await tick();

														e.target.scrollTop = e.target.scrollHeight;
														prompt = fullPrompt;
														await tick();

														e.preventDefault();
														e.target.setSelectionRange(word?.startIndex, word.endIndex + 1);
													}

													e.target.style.height = '';
													e.target.style.height = Math.min(e.target.scrollHeight, 320) + 'px';
												}

												if (e.key === 'Escape') {
													console.log('Escape');
													atSelectedModel = undefined;
													selectedToolIds = [];
													webSearchEnabled = false;
													imageGenerationEnabled = false;
												}
											}}
											rows="1"
											on:input={async (e) => {
												e.target.style.height = '';
												e.target.style.height = Math.min(e.target.scrollHeight, 320) + 'px';
											}}
											on:focus={async (e) => {
												e.target.style.height = '';
												e.target.style.height = Math.min(e.target.scrollHeight, 320) + 'px';
											}}
											on:paste={async (e) => {
												const clipboardData = e.clipboardData || window.clipboardData;

												if (clipboardData && clipboardData.items) {
													for (const item of clipboardData.items) {
														if (item.type.indexOf('image') !== -1) {
															const blob = item.getAsFile();
															const reader = new FileReader();

															reader.onload = function (e) {
																files = [
																	...files,
																	{
																		type: 'image',
																		url: `${e.target.result}`
																	}
																];
															};

															reader.readAsDataURL(blob);
														} else if (item.type === 'text/plain') {
															if ($settings?.largeTextAsFile ?? false) {
																const text = clipboardData.getData('text/plain');

																if (text.length > PASTED_TEXT_CHARACTER_LIMIT) {
																	e.preventDefault();
																	const blob = new Blob([text], { type: 'text/plain' });
																	const file = new File([blob], `Pasted_Text_${Date.now()}.txt`, {
																		type: 'text/plain'
																	});

																	await uploadFileHandler(file, true);
																}
															}
														}
													}
												}
											}}
										/>
									{/if}
								</div>

								<div class=" flex justify-between mt-1.5 mb-2.5 mx-0.5 max-w-full">
									<div class="ml-1 self-end gap-0.5 flex items-center flex-1 max-w-[80%]">
										<InputMenu
											bind:selectedToolIds
											{screenCaptureHandler}
											{inputFilesHandler}
											uploadFilesHandler={() => {
												filesInputElement.click();
											}}
											uploadGoogleDriveHandler={async () => {
												try {
													const fileData = await createPicker();
													if (fileData) {
														const file = new File([fileData.blob], fileData.name, {
															type: fileData.blob.type
														});
														await uploadFileHandler(file);
													} else {
														console.log('No file was selected from Google Drive');
													}
												} catch (error) {
													console.error('Google Drive Error:', error);
													toast.error(
														$i18n.t('Error accessing Google Drive: {{error}}', {
															error: error.message
														})
													);
												}
											}}
											onClose={async () => {
												await tick();

												const chatInput = document.getElementById('chat-input');
												chatInput?.focus();
											}}
										>
											<button
												class="bg-transparent hover:bg-gray-100 text-gray-800 dark:text-white dark:hover:bg-gray-800 transition rounded-full p-1.5 outline-hidden focus:outline-hidden"
												type="button"
												aria-label="More"
											>
												<svg
													xmlns="http://www.w3.org/2000/svg"
													viewBox="0 0 20 20"
													fill="currentColor"
													class="size-5"
												>
													<path
														d="M10.75 4.75a.75.75 0 0 0-1.5 0v4.5h-4.5a.75.75 0 0 0 0 1.5h4.5v4.5a.75.75 0 0 0 1.5 0v-4.5h4.5a.75.75 0 0 0 0-1.5h-4.5v-4.5Z"
													/>
												</svg>
											</button>
										</InputMenu>

										<div class="flex gap-0.5 items-center overflow-x-auto scrollbar-none flex-1">
											{#if $_user}
												{#if $config?.features?.enable_web_search && ($_user.role === 'admin' || $_user?.permissions?.features?.web_search)}
													<Tooltip content={$i18n.t('Search the internet')} placement="top">
														<button
															on:click|preventDefault={() => (webSearchEnabled = !webSearchEnabled)}
															type="button"
															class="px-1.5 @sm:px-2.5 py-1.5 flex gap-1.5 items-center text-sm rounded-full font-medium transition-colors duration-300 focus:outline-hidden max-w-full overflow-hidden {webSearchEnabled ||
															($settings?.webSearch ?? false) === 'always'
																? 'bg-blue-100 dark:bg-blue-500/20 text-blue-500 dark:text-blue-400'
																: 'bg-transparent text-gray-600 dark:text-gray-300 border-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'}"
														>
															<GlobeAlt className="size-5" strokeWidth="1.75" />
															<span
																class="hidden @sm:block whitespace-nowrap overflow-hidden text-ellipsis translate-y-[0.5px] mr-0.5"
																>{$i18n.t('Web Search')}</span
															>
														</button>
													</Tooltip>
												{/if}

												{#if $config?.features?.enable_image_generation && ($_user.role === 'admin' || $_user?.permissions?.features?.image_generation)}
													<Tooltip content={$i18n.t('Generate an image')} placement="top">
														<button
															on:click|preventDefault={() =>
																(imageGenerationEnabled = !imageGenerationEnabled)}
															type="button"
															class="px-1.5 @sm:px-2.5 py-1.5 flex gap-1.5 items-center text-sm rounded-full font-medium transition-colors duration-300 focus:outline-hidden max-w-full overflow-hidden {imageGenerationEnabled
																? 'bg-gray-100 dark:bg-gray-500/20 text-gray-600 dark:text-gray-400'
																: 'bg-transparent text-gray-600 dark:text-gray-300 border-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 '}"
														>
															<Photo className="size-5" strokeWidth="1.75" />
															<span
																class="hidden @sm:block whitespace-nowrap overflow-hidden text-ellipsis translate-y-[0.5px] mr-0.5"
																>{$i18n.t('Image')}</span
															>
														</button>
													</Tooltip>
												{/if}

												{#if $config?.features?.enable_code_interpreter && ($_user.role === 'admin' || $_user?.permissions?.features?.code_interpreter)}
													<Tooltip content={$i18n.t('Execute code for analysis')} placement="top">
														<button
															on:click|preventDefault={() =>
																(codeInterpreterEnabled = !codeInterpreterEnabled)}
															type="button"
															class="px-1.5 @sm:px-2.5 py-1.5 flex gap-1.5 items-center text-sm rounded-full font-medium transition-colors duration-300 focus:outline-hidden max-w-full overflow-hidden {codeInterpreterEnabled
																? 'bg-gray-100 dark:bg-gray-500/20 text-gray-600 dark:text-gray-400'
																: 'bg-transparent text-gray-600 dark:text-gray-300 border-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 '}"
														>
															<CommandLine className="size-5" strokeWidth="1.75" />
															<span
																class="hidden @sm:block whitespace-nowrap overflow-hidden text-ellipsis translate-y-[0.5px] mr-0.5"
																>{$i18n.t('Code Interpreter')}</span
															>
														</button>
													</Tooltip>
												{/if}
											{/if}
										</div>
									</div>

									<div class="self-end flex space-x-1 mr-1 shrink-0">
										{#if !history?.currentId || history.messages[history.currentId]?.done == true}
											<Tooltip content={$i18n.t('Record voice')}>
												<button
													id="voice-input-button"
													class=" text-gray-600 dark:text-gray-300 hover:text-gray-700 dark:hover:text-gray-200 transition rounded-full p-1.5 mr-0.5 self-center"
													type="button"
													on:click={async () => {
														try {
															let stream = await navigator.mediaDevices
																.getUserMedia({ audio: true })
																.catch(function (err) {
																	toast.error(
																		$i18n.t(
																			`Permission denied when accessing microphone: {{error}}`,
																			{
																				error: err
																			}
																		)
																	);
																	return null;
																});

															if (stream) {
																recording = true;
																const tracks = stream.getTracks();
																tracks.forEach((track) => track.stop());
															}
															stream = null;
														} catch {
															toast.error($i18n.t('Permission denied when accessing microphone'));
														}
													}}
													aria-label="Voice Input"
												>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														viewBox="0 0 20 20"
														fill="currentColor"
														class="w-5 h-5 translate-y-[0.5px]"
													>
														<path d="M7 4a3 3 0 016 0v6a3 3 0 11-6 0V4z" />
														<path
															d="M5.5 9.643a.75.75 0 00-1.5 0V10c0 3.06 2.29 5.585 5.25 5.954V17.5h-1.5a.75.75 0 000 1.5h4.5a.75.75 0 000-1.5h-1.5v-1.546A6.001 6.001 0 0016 10v-.357a.75.75 0 00-1.5 0V10a4.5 4.5 0 01-9 0v-.357z"
														/>
													</svg>
												</button>
											</Tooltip>
										{/if}

										{#if !history.currentId || history.messages[history.currentId]?.done == true}
											{#if prompt === '' && files.length === 0}
												<div class=" flex items-center">
													<Tooltip content={$i18n.t('Call')}>
														<button
															class=" {webSearchEnabled ||
															($settings?.webSearch ?? false) === 'always'
																? 'bg-blue-500 text-white hover:bg-blue-400 '
																: 'bg-black text-white hover:bg-gray-900 dark:bg-white dark:text-black dark:hover:bg-gray-100'} transition rounded-full p-1.5 self-center"
															type="button"
															on:click={async () => {
																if (selectedModels.length > 1) {
																	toast.error($i18n.t('Select only one model to call'));

																	return;
																}

																if ($config.audio.stt.engine === 'web') {
																	toast.error(
																		$i18n.t(
																			'Call feature is not supported when using Web STT engine'
																		)
																	);

																	return;
																}
																// check if user has access to getUserMedia
																try {
																	let stream = await navigator.mediaDevices.getUserMedia({
																		audio: true
																	});
																	// If the user grants the permission, proceed to show the call overlay

																	if (stream) {
																		const tracks = stream.getTracks();
																		tracks.forEach((track) => track.stop());
																	}

																	stream = null;

																	if (!$TTSWorker) {
																		await TTSWorker.set(
																			new KokoroWorker({
																				dtype: $settings.audio?.tts?.engineConfig?.dtype ?? 'fp32'
																			})
																		);

																		await $TTSWorker.init();
																	}

																	showCallOverlay.set(true);
																	showControls.set(true);
																} catch (err) {
																	// If the user denies the permission or an error occurs, show an error message
																	toast.error(
																		$i18n.t('Permission denied when accessing media devices')
																	);
																}
															}}
															aria-label="Call"
														>
															<Headphone className="size-5" />
														</button>
													</Tooltip>
												</div>
											{:else}
												<div class=" flex items-center">
													<Tooltip content={$i18n.t('Send message')}>
														<button
															id="send-message-button"
															class="{!(prompt === '' && files.length === 0)
																? webSearchEnabled || ($settings?.webSearch ?? false) === 'always'
																	? 'bg-blue-500 text-white hover:bg-blue-400 '
																	: 'bg-black text-white hover:bg-gray-900 dark:bg-white dark:text-black dark:hover:bg-gray-100 '
																: 'text-white bg-gray-200 dark:text-gray-900 dark:bg-gray-700 disabled'} transition rounded-full p-1.5 self-center"
															type="submit"
															disabled={prompt === '' && files.length === 0}
														>
															<svg
																xmlns="http://www.w3.org/2000/svg"
																viewBox="0 0 16 16"
																fill="currentColor"
																class="size-5"
															>
																<path
																	fill-rule="evenodd"
																	d="M8 14a.75.75 0 0 1-.75-.75V4.56L4.03 7.78a.75.75 0 0 1-1.06-1.06l4.5-4.5a.75.75 0 0 1 1.06 0l4.5 4.5a.75.75 0 0 1-1.06 1.06L8.75 4.56v8.69A.75.75 0 0 1 8 14Z"
																	clip-rule="evenodd"
																/>
															</svg>
														</button>
													</Tooltip>
												</div>
											{/if}
										{:else}
											<div class=" flex items-center">
												<Tooltip content={$i18n.t('Stop')}>
													<button
														class="bg-white hover:bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-800 transition rounded-full p-1.5"
														on:click={() => {
															stopResponse();
														}}
													>
														<svg
															xmlns="http://www.w3.org/2000/svg"
															viewBox="0 0 24 24"
															fill="currentColor"
															class="size-5"
														>
															<path
																fill-rule="evenodd"
																d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm6-2.438c0-.724.588-1.312 1.313-1.312h4.874c.725 0 1.313.588 1.313 1.313v4.874c0 .725-.588 1.313-1.313 1.313H9.564a1.312 1.312 0 01-1.313-1.313V9.564z"
																clip-rule="evenodd"
															/>
														</svg>
													</button>
												</Tooltip>
											</div>
										{/if}
									</div>
								</div>
<<<<<<< HEAD
								{#if !history.currentId || history.messages[history.currentId]?.done == true}
									{#if prompt === ''}
										<div class=" flex items-center">
											<Tooltip content={$i18n.t('Call')}>
												<button
													class=" bg-black text-white hover:bg-gray-900 dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full p-2 self-center"
													type="button"
													on:click={async () => {
														if (selectedModels.length > 1) {
															toast.error($i18n.t('Select only one model to call'));

															return;
														}

														if ($config.audio.stt.engine === 'web') {
															toast.error(
																$i18n.t('Call feature is not supported when using Web STT engine')
															);

															return;
														}
														// check if user has access to getUserMedia
														try {
															let stream = await navigator.mediaDevices.getUserMedia({
																audio: true
															});
															// If the user grants the permission, proceed to show the call overlay

															if (stream) {
																const tracks = stream.getTracks();
																tracks.forEach((track) => track.stop());
															}

															stream = null;

															showCallOverlay.set(true);
															showControls.set(true);
														} catch (err) {
															// If the user denies the permission or an error occurs, show an error message
															toast.error(
																$i18n.t('Permission denied when accessing media devices')
															);
														}
													}}
													aria-label="Call"
												>
													<Headphone className="size-5" />
												</button>
											</Tooltip>
										</div>
									{:else}
										<div class=" flex items-center">
											<Tooltip content={$i18n.t('Send message')}>
												<button
													id="send-message-button"
													class="{prompt !== ''
														? 'bg-black text-white hover:bg-gray-900 dark:bg-white dark:text-black dark:hover:bg-gray-100 '
														: 'text-white bg-gray-200 dark:text-gray-900 dark:bg-gray-700 disabled'} transition rounded-full p-1.5 m-0.5 self-center"
													type="submit"
													disabled={prompt === ''}
												>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														viewBox="0 0 16 16"
														fill="currentColor"
														class="size-6"
													>
														<path
															fill-rule="evenodd"
															d="M8 14a.75.75 0 0 1-.75-.75V4.56L4.03 7.78a.75.75 0 0 1-1.06-1.06l4.5-4.5a.75.75 0 0 1 1.06 0l4.5 4.5a.75.75 0 0 1-1.06 1.06L8.75 4.56v8.69A.75.75 0 0 1 8 14Z"
															clip-rule="evenodd"
														/>
													</svg>
												</button>
											</Tooltip>
										</div>
									{/if}
								{:else}
									<div class=" flex items-center">
										<button
											class="bg-white hover:bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-800 transition rounded-full p-1.5"
											on:click={() => {
												stopResponse();
											}}
										>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												viewBox="0 0 24 24"
												fill="currentColor"
												class="size-6"
											>
												<path
													fill-rule="evenodd"
													d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm6-2.438c0-.724.588-1.312 1.313-1.312h4.874c.725 0 1.313.588 1.313 1.313v4.874c0 .725-.588 1.313-1.313 1.313H9.564a1.312 1.312 0 01-1.313-1.313V9.564z"
													clip-rule="evenodd"
												/>
											</svg>
										</button>
									</div>
								{/if}
							</div>
						</div>
					</form>
				{/if}
=======
							</div>
						</form>
					{/if}
				</div>
>>>>>>> upstream/main
			</div>
		</div>
	</div>
{/if}
