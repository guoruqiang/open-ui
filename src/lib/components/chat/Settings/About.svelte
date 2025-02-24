<script lang="ts">
	import { getVersionUpdates } from '$lib/apis';
	import { getOllamaVersion } from '$lib/apis/ollama';
	import { WEBUI_BUILD_HASH, WEBUI_VERSION } from '$lib/constants';
	import { WEBUI_NAME, config, showChangelog } from '$lib/stores';
	import { compareVersion } from '$lib/utils';
	import { onMount, getContext } from 'svelte';

	import Tooltip from '$lib/components/common/Tooltip.svelte';

	const i18n = getContext('i18n');

	let ollamaVersion = '';

	let updateAvailable = null;
	let version = {
		current: '',
		latest: ''
	};

	const checkForVersionUpdates = async () => {
		updateAvailable = null;
		version = await getVersionUpdates(localStorage.token).catch((error) => {
			return {
				current: WEBUI_VERSION,
				latest: WEBUI_VERSION
			};
		});

		console.log(version);

		updateAvailable = compareVersion(version.latest, version.current);
		console.log(updateAvailable);
	};

	onMount(async () => {
		ollamaVersion = await getOllamaVersion(localStorage.token).catch((error) => {
			return '';
		});

		checkForVersionUpdates();
	});
</script>

<<<<<<< HEAD
<div class="text-sm text-gray-700 dark:text-gray-200 w-full flex flex-col space-y-4">
	<div class=" space-y-3">
		<hr class=" dark:border-gray-850" />
		<div class="w-full items-center text-center text-lg">
			<b> 本站使用协议 </b> <br />
		</div>

		<div
			class="text-xm text-gray-700 dark:text-gray-200 space-y-4 justify-between items-cent"
			style="width: 95%; margin-left: 2.5%;"
		>
			<li style="text-align: justify;">
				根据<a
					href="https://www.gov.cn/zhengce/zhengceku/202307/content_6891752.htm"
					style="color: #3A7B99;">《生成式人工智能服务管理暂行办法》</a
				>规定生成式人工智能生成的内容应当体现社会主义价值观，严禁生成违法违规内容信息，例如政治言论、淫秽色情、枪支暴力、“科学上网”、军队战争等内容信息，本平台内容由AI生成，用户应当辨别信息的真实性，严禁引导诱导欺骗等方式使用生成式人工智能出现种族、民族、信仰、国别、地域、性别、年龄、职业等歧视；尊重知识产权、商业道德，不得利用算法、数据、平台等优势实施不公平竞争；用户应当尊重他人合法利益，防止生成伤害他人身心健康，损害肖像权、名誉权和个人隐私，侵犯知识产权的内容。
			</li>
			<li style="text-align: justify;">
				本平台内容由AI生成，用户应当自行辨别AI大模型生成的信息的<strong>真实性</strong>！
			</li>
			<li style="text-align: justify;">
				<strong>注意：如果在使用过程中出现不明网址和联系方式，请勿相信！</strong>
			</li>
			<li style="text-align: justify;">
				如果检测到违反<a
					href="https://www.gov.cn/zhengce/zhengceku/202307/content_6891752.htm"
					style="color: #3A7B99;">《生成式人工智能服务管理暂行办法》</a
				>规定，将进行<strong>封号处理！</strong>
			</li>
		</div>
		<!-- <div class="flex space-x-1">
			<a href="https://discord.gg/5rJgQTnV4s" target="_blank">
				<img
					alt="Discord"
					src="https://img.shields.io/badge/Discord-Open_WebUI-blue?logo=discord&logoColor=white"
				/>
			</a>

			<a href="https://twitter.com/OpenWebUI" target="_blank">
				<img
					alt="X (formerly Twitter) Follow"
					src="https://img.shields.io/twitter/follow/OpenWebUI"
				/>
			</a>

			<a href="https://github.com/open-webui/open-webui" target="_blank">
				<img
					alt="Github Repo"
					src="https://img.shields.io/github/stars/open-webui/open-webui?style=social&label=Star us on Github"
				/>
			</a>
		</div> -->
		<div class="mt-2 text-xs text-gray-400 dark:text-gray-500 text-right">
			{#if !$WEBUI_NAME.includes('Open WebUI')}
				<span class=" text-gray-500 dark:text-gray-300 font-medium">{$WEBUI_NAME}</span> -
			{/if}
			{$i18n.t('Amend by')}
			<a
				class=" text-gray-500 dark:text-gray-300 font-medium"
				href="https://github.com/yubb-ai/open-ui"
				target="_blank">Yanyutin753</a
			>
		</div>

		<hr class=" dark:border-gray-850" />

		<!-- <div>
=======
<div class="flex flex-col h-full justify-between space-y-3 text-sm mb-6">
	<div class=" space-y-3 overflow-y-scroll max-h-[28rem] lg:max-h-full">
		<div>
>>>>>>> upstream/main
			<div class=" mb-2.5 text-sm font-medium flex space-x-2 items-center">
				<div>
					{$WEBUI_NAME}
					{$i18n.t('Version')}
				</div>
			</div>
			<div class="flex w-full justify-between items-center">
				<div class="flex flex-col text-xs text-gray-700 dark:text-gray-200">
					<div class="flex gap-1">
						<Tooltip content={WEBUI_BUILD_HASH}>
							v{WEBUI_VERSION}
						</Tooltip>

						<a
							href="https://github.com/open-webui/open-webui/releases/tag/v{version.latest}"
							target="_blank"
						>
							{updateAvailable === null
								? $i18n.t('Checking for updates...')
								: updateAvailable
									? `(v${version.latest} ${$i18n.t('available!')})`
									: $i18n.t('(latest)')}
						</a>
					</div>

					<button
						class=" underline flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-500"
						on:click={() => {
							showChangelog.set(true);
						}}
					>
						<div>{$i18n.t("See what's new")}</div>
					</button>
				</div>

				<button
					class=" text-xs px-3 py-1.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-lg font-medium"
					on:click={() => {
						checkForVersionUpdates();
					}}
				>
					{$i18n.t('Check for updates')}
				</button>
			</div>
		</div>

		{#if ollamaVersion}
			<hr class=" border-gray-100 dark:border-gray-850" />

			<div>
				<div class=" mb-2.5 text-sm font-medium">{$i18n.t('Ollama Version')}</div>
				<div class="flex w-full">
					<div class="flex-1 text-xs text-gray-700 dark:text-gray-200">
						{ollamaVersion ?? 'N/A'}
					</div>
				</div>
			</div>
<<<<<<< HEAD
		{/if} -->
=======
		{/if}

		<hr class=" border-gray-100 dark:border-gray-850" />

		<div class="mt-2 text-xs text-gray-400 dark:text-gray-500">
			Emoji graphics provided by
			<a href="https://github.com/jdecked/twemoji" target="_blank">Twemoji</a>, licensed under
			<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC-BY 4.0</a>.
		</div>

		<div class="flex space-x-1">
			<a href="https://discord.gg/5rJgQTnV4s" target="_blank">
				<img
					alt="Discord"
					src="https://img.shields.io/badge/Discord-Open_WebUI-blue?logo=discord&logoColor=white"
				/>
			</a>

			<a href="https://twitter.com/OpenWebUI" target="_blank">
				<img
					alt="X (formerly Twitter) Follow"
					src="https://img.shields.io/twitter/follow/OpenWebUI"
				/>
			</a>

			<a href="https://github.com/open-webui/open-webui" target="_blank">
				<img
					alt="Github Repo"
					src="https://img.shields.io/github/stars/open-webui/open-webui?style=social&label=Star us on Github"
				/>
			</a>
		</div>

		<div>
			<pre
				class="text-xs text-gray-400 dark:text-gray-500">Copyright (c) {new Date().getFullYear()} <a
					href="https://openwebui.com"
					target="_blank"
					class="underline">Open WebUI (Timothy Jaeryang Baek)</a
				>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
</pre>
		</div>

		<div class="mt-2 text-xs text-gray-400 dark:text-gray-500">
			{#if !$WEBUI_NAME.includes('Open WebUI')}
				<span class=" text-gray-500 dark:text-gray-300 font-medium">{$WEBUI_NAME}</span> -
			{/if}
			{$i18n.t('Created by')}
			<a
				class=" text-gray-500 dark:text-gray-300 font-medium"
				href="https://github.com/tjbck"
				target="_blank">Timothy J. Baek</a
			>
		</div>
>>>>>>> upstream/main
	</div>
</div>
