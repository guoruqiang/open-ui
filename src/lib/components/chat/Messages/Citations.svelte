<script lang="ts">
	import { getContext } from 'svelte';
	import CitationsModal from './CitationsModal.svelte';
	import Collapsible from '$lib/components/common/Collapsible.svelte';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import ChevronUp from '$lib/components/icons/ChevronUp.svelte';
<<<<<<< HEAD

	const i18n = getContext('i18n');
=======
>>>>>>> upstream/main

	const i18n = getContext('i18n');

<<<<<<< HEAD
	let _citations = [];
=======
	export let id = '';
	export let sources = [];

	let citations = [];
>>>>>>> upstream/main
	let showPercentage = false;
	let showRelevance = true;

	let showCitationModal = false;
	let selectedCitation: any = null;
	let isCollapsibleOpen = false;

<<<<<<< HEAD
	function calculateShowRelevance(citations: any[]) {
		const distances = citations.flatMap((citation) => citation.distances ?? []);
=======
	function calculateShowRelevance(sources: any[]) {
		const distances = sources.flatMap((citation) => citation.distances ?? []);
>>>>>>> upstream/main
		const inRange = distances.filter((d) => d !== undefined && d >= -1 && d <= 1).length;
		const outOfRange = distances.filter((d) => d !== undefined && (d < -1 || d > 1)).length;

		if (distances.length === 0) {
			return false;
		}

		if (
			(inRange === distances.length - 1 && outOfRange === 1) ||
			(outOfRange === distances.length - 1 && inRange === 1)
		) {
			return false;
		}

		return true;
	}

<<<<<<< HEAD
	function shouldShowPercentage(citations: any[]) {
		const distances = citations.flatMap((citation) => citation.distances ?? []);
=======
	function shouldShowPercentage(sources: any[]) {
		const distances = sources.flatMap((citation) => citation.distances ?? []);
>>>>>>> upstream/main
		return distances.every((d) => d !== undefined && d >= -1 && d <= 1);
	}

	$: {
<<<<<<< HEAD
		_citations = citations.reduce((acc, citation) => {
			citation.document.forEach((document, index) => {
				const metadata = citation.metadata?.[index];
				const distance = citation.distances?.[index];
				const id = metadata?.source ?? 'N/A';
				let source = citation?.source;

				if (metadata?.name) {
					source = { ...source, name: metadata.name };
				}

				if (id.startsWith('http://') || id.startsWith('https://')) {
					source = { name: id, ...source, url: id };
=======
		citations = sources.reduce((acc, source) => {
			if (Object.keys(source).length === 0) {
				return acc;
			}

			source.document.forEach((document, index) => {
				const metadata = source.metadata?.[index];
				const distance = source.distances?.[index];

				// Within the same citation there could be multiple documents
				const id = metadata?.source ?? 'N/A';
				let _source = source?.source;

				if (metadata?.name) {
					_source = { ..._source, name: metadata.name };
				}

				if (id.startsWith('http://') || id.startsWith('https://')) {
					_source = { ..._source, name: id, url: id };
>>>>>>> upstream/main
				}

				const existingSource = acc.find((item) => item.id === id);

				if (existingSource) {
					existingSource.document.push(document);
					existingSource.metadata.push(metadata);
					if (distance !== undefined) existingSource.distances.push(distance);
				} else {
					acc.push({
						id: id,
<<<<<<< HEAD
						source: source,
=======
						source: _source,
>>>>>>> upstream/main
						document: [document],
						metadata: metadata ? [metadata] : [],
						distances: distance !== undefined ? [distance] : undefined
					});
				}
			});
			return acc;
		}, []);

<<<<<<< HEAD
		showRelevance = calculateShowRelevance(_citations);
		showPercentage = shouldShowPercentage(_citations);
=======
		showRelevance = calculateShowRelevance(citations);
		showPercentage = shouldShowPercentage(citations);
>>>>>>> upstream/main
	}
</script>

<CitationsModal
	bind:show={showCitationModal}
	citation={selectedCitation}
	{showPercentage}
	{showRelevance}
/>

<<<<<<< HEAD
{#if _citations.length > 0}
	<div class="mt-1 mb-2 w-full flex gap-1 items-center flex-wrap">
		{#if _citations.length <= 3}
			{#each _citations as citation, idx}
				<div class="flex gap-1 text-xs font-semibold">
					<button
						class="no-toggle flex dark:text-gray-300 py-1 px-1 bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-xl max-w-96"
=======
{#if citations.length > 0}
	<div class=" py-0.5 -mx-0.5 w-full flex gap-1 items-center flex-wrap">
		{#if citations.length <= 3}
			<div class="flex text-xs font-medium flex-wrap">
				{#each citations as citation, idx}
					<button
						id={`source-${id}-${idx}`}
						class="no-toggle outline-hidden flex dark:text-gray-300 p-1 bg-white dark:bg-gray-900 rounded-xl max-w-96"
>>>>>>> upstream/main
						on:click={() => {
							showCitationModal = true;
							selectedCitation = citation;
						}}
					>
<<<<<<< HEAD
						{#if _citations.every((c) => c.distances !== undefined)}
							<div class="bg-white dark:bg-gray-700 rounded-full size-4">
								{idx + 1}
							</div>
						{/if}
						<div class="flex-1 mx-2 line-clamp-1">
							{citation.source.name}
						</div>
					</button>
				</div>
			{/each}
		{:else}
			<Collapsible bind:open={isCollapsibleOpen} className="w-full">
				<div
					class="flex items-center gap-1 text-gray-500 hover:text-gray-600 dark:hover:text-gray-400 transition cursor-pointer"
				>
					<div class="flex-grow flex items-center gap-1 overflow-hidden">
						<span class="whitespace-nowrap hidden sm:inline">{$i18n.t('References from')}</span>
						<div class="flex items-center">
							{#if _citations.length > 1 && _citations
									.slice(0, 2)
									.reduce((acc, citation) => acc + citation.source.name.length, 0) <= 50}
								{#each _citations.slice(0, 2) as citation, idx}
									<div class="flex items-center">
										<button
											class="no-toggle flex dark:text-gray-300 py-1 px-1 bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-xl max-w-96 text-xs font-semibold"
											on:click={() => {
												showCitationModal = true;
												selectedCitation = citation;
											}}
										>
											{#if _citations.every((c) => c.distances !== undefined)}
												<div class="bg-white dark:bg-gray-700 rounded-full size-4">
													{idx + 1}
												</div>
											{/if}
											<div class="flex-1 mx-2 line-clamp-1">
												{citation.source.name}
											</div>
										</button>
										{#if idx === 0}<span class="mr-1">,</span>
										{/if}
									</div>
								{/each}
							{:else}
								{#each _citations.slice(0, 1) as citation, idx}
									<div class="flex items-center">
										<button
											class="no-toggle flex dark:text-gray-300 py-1 px-1 bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-xl max-w-96 text-xs font-semibold"
											on:click={() => {
												showCitationModal = true;
												selectedCitation = citation;
											}}
										>
											{#if _citations.every((c) => c.distances !== undefined)}
												<div class="bg-white dark:bg-gray-700 rounded-full size-4">
													{idx + 1}
												</div>
											{/if}
											<div class="flex-1 mx-2 line-clamp-1">
												{citation.source.name}
											</div>
										</button>
									</div>
								{/each}
							{/if}
						</div>
						<div class="flex items-center gap-1 whitespace-nowrap">
							<span class="hidden sm:inline">{$i18n.t('and')}</span>
							<span class="text-gray-600 dark:text-gray-400">
								{_citations.length -
									(_citations.length > 1 &&
									_citations
										.slice(0, 2)
										.reduce((acc, citation) => acc + citation.source.name.length, 0) <= 50
										? 2
										: 1)}
							</span>
							<span>{$i18n.t('more')}</span>
						</div>
					</div>
					<div class="flex-shrink-0">
=======
						{#if citations.every((c) => c.distances !== undefined)}
							<div class="bg-gray-50 dark:bg-gray-800 rounded-full size-4">
								{idx + 1}
							</div>
						{/if}
						<div
							class="flex-1 mx-1 truncate text-black/60 hover:text-black dark:text-white/60 dark:hover:text-white transition"
						>
							{citation.source.name}
						</div>
					</button>
				{/each}
			</div>
		{:else}
			<Collapsible
				id="collapsible-sources"
				bind:open={isCollapsibleOpen}
				className="w-full max-w-full "
				buttonClassName="w-fit max-w-full"
			>
				<div
					class="flex w-full overflow-auto items-center gap-2 text-gray-500 hover:text-gray-600 dark:hover:text-gray-400 transition cursor-pointer"
				>
					<div
						class="flex-1 flex items-center gap-1 overflow-auto scrollbar-none w-full max-w-full"
					>
						<span class="whitespace-nowrap hidden sm:inline shrink-0"
							>{$i18n.t('References from')}</span
						>
						<div class="flex items-center overflow-auto scrollbar-none w-full max-w-full flex-1">
							<div class="flex text-xs font-medium items-center">
								{#each citations.slice(0, 2) as citation, idx}
									<button
										class="no-toggle outline-hidden flex dark:text-gray-300 p-1 bg-gray-50 hover:bg-gray-100 dark:bg-gray-900 dark:hover:bg-gray-850 transition rounded-xl max-w-96"
										on:click={() => {
											showCitationModal = true;
											selectedCitation = citation;
										}}
										on:pointerup={(e) => {
											e.stopPropagation();
										}}
									>
										{#if citations.every((c) => c.distances !== undefined)}
											<div class="bg-gray-50 dark:bg-gray-800 rounded-full size-4">
												{idx + 1}
											</div>
										{/if}
										<div class="flex-1 mx-1 truncate">
											{citation.source.name}
										</div>
									</button>
								{/each}
							</div>
						</div>
						<div class="flex items-center gap-1 whitespace-nowrap shrink-0">
							<span class="hidden sm:inline">{$i18n.t('and')}</span>
							{citations.length - 2}
							<span>{$i18n.t('more')}</span>
						</div>
					</div>
					<div class="shrink-0">
>>>>>>> upstream/main
						{#if isCollapsibleOpen}
							<ChevronUp strokeWidth="3.5" className="size-3.5" />
						{:else}
							<ChevronDown strokeWidth="3.5" className="size-3.5" />
						{/if}
					</div>
				</div>
<<<<<<< HEAD
				<div slot="content" class="mt-2">
					<div class="flex flex-wrap gap-2">
						{#each _citations as citation, idx}
							<div class="flex gap-1 text-xs font-semibold">
								<button
									class="no-toggle flex dark:text-gray-300 py-1 px-1 bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-xl max-w-96"
									on:click={() => {
										showCitationModal = true;
										selectedCitation = citation;
									}}
								>
									{#if _citations.every((c) => c.distances !== undefined)}
										<div class="bg-white dark:bg-gray-700 rounded-full size-4">
											{idx + 1}
										</div>
									{/if}
									<div class="flex-1 mx-2 line-clamp-1">
										{citation.source.name}
									</div>
								</button>
							</div>
=======
				<div slot="content">
					<div class="flex text-xs font-medium flex-wrap">
						{#each citations as citation, idx}
							<button
								id={`source-${id}-${idx}`}
								class="no-toggle outline-hidden flex dark:text-gray-300 p-1 bg-gray-50 hover:bg-gray-100 dark:bg-gray-900 dark:hover:bg-gray-850 transition rounded-xl max-w-96"
								on:click={() => {
									showCitationModal = true;
									selectedCitation = citation;
								}}
							>
								{#if citations.every((c) => c.distances !== undefined)}
									<div class="bg-gray-50 dark:bg-gray-800 rounded-full size-4">
										{idx + 1}
									</div>
								{/if}
								<div class="flex-1 mx-1 truncate">
									{citation.source.name}
								</div>
							</button>
>>>>>>> upstream/main
						{/each}
					</div>
				</div>
			</Collapsible>
		{/if}
	</div>
{/if}
