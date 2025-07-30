<script lang="ts">
	import {
		beforeUpdate,
		afterUpdate,
		createEventDispatcher,
		tick
	} from "svelte";
	import { Upload } from "@gradio/upload";
	import type { SelectData, Gradio } from "@gradio/utils";
	import { type FileData, type Client } from "@gradio/client";

	import { text_area_resize, resize } from "./shared/utils";
	import InteractiveAudio from "./shared/InteractiveAudio.svelte";

	export let value: { text: string; files: FileData[]; audio: string} = {
		text: "",
		files: [],
		audio: "__webrtc_value__",
	};

	// import Video from "./shared/InteractiveVideo.svelte";

	export let value_is_output = false;
	export let lines = 1;
	export let placeholder = "Type here...";
	export let disabled = false;
	export let interactive: boolean;
	export let loading_message: string;
	export let show_label: boolean = true;
	export let container: boolean = true;
	export let max_lines: number;
	export let upload_btn: string | boolean | null = null;
	export let submit_btn: string | boolean | null = null;
	export let stop_btn: string | boolean | null = null;
	export let rtl = false;
	export let autofocus = false;
	export let text_align: "left" | "right" | undefined = undefined;
	export let autoscroll = true;
	export let root: string;
	export let file_types: string[] | null = null;
	export let max_file_size: number | null = null;
	export let upload: Client["upload"];
	export let stream_handler: Client["stream"];
	export let file_count: "single" | "multiple" | "directory" = "multiple";
	export let audio_btn: boolean = false;
	export let stop_audio_btn: boolean = false;
	export let gradio: Gradio;
	export let rtc_configuration: Object;
	export let time_limit: number | null = null;
	export let modality: "video" | "audio" = "audio";
	export let mode: "send-receive" | "receive" | "send" = "send-receive";
	export let rtp_params: RTCRtpParameters = {} as RTCRtpParameters;
	export let track_constraints: MediaTrackConstraints = {};
	export let on_change_cb: Function;
	export let server;

	let upload_component: Upload;
	let hidden_upload: HTMLInputElement;
	let el: HTMLTextAreaElement | HTMLInputElement;
	let can_scroll: boolean;
	let previous_scroll_top = 0;
	let user_has_scrolled_up = false;
	export let dragging = false;
	let uploading = false;
	let oldValue = value.text;
	let saved_message: string;
	let retrieve_saved_message: boolean = false;
	$: dispatch("drag", dragging);

	let use_audio_video_recording = false;

	$: if (audio_btn && !use_audio_video_recording) {
		use_audio_video_recording = audio_btn;
	}

	let full_container: HTMLDivElement;

	$: if (oldValue !== value.text && !uploading && !retrieve_saved_message) {
		// console.log("oldValue", oldValue)
		oldValue = value.text;
		dispatch("change", value);
		// console.log("value.text", value.text)
	}

	$: if (uploading) {
		console.log("uploading")
	}
	$: if (disabled) {
		console.log("disabled")
	}

	$: if (value === null) value = { text: "", files: [], audio: null };
	$: value, el && lines !== max_lines && resize(el, lines, max_lines, uploading);
	$: disabled = !interactive || uploading;
	$: if (uploading && !retrieve_saved_message) {
		saved_message = value.text;
		retrieve_saved_message = true;
		value.text = loading_message;
		console.log("value.text uploading", value.text);
	} else if (!uploading && retrieve_saved_message) {
		value.text = saved_message;
		retrieve_saved_message = false;
		console.log("value.text end of uploading", value.text);
	}

	let upload_btn_title:string;
	let submit_btn_title: string;
	let stop_btn_title:string;
	let audio_btn_title:string;
	let stop_audio_btn_title: string;

	if (navigator.language.startsWith('fr')) {
		upload_btn_title = "Ajouter un fichier";
		submit_btn_title = "Poser une question";
		stop_btn_title = "Arrêter";
		audio_btn_title = "Activer Neo audio";
		stop_audio_btn_title = "Arreter Neo audio"
	} else {
		upload_btn_title = "Add a file";
		submit_btn_title = "Ask a question";
		stop_btn_title = "Stop";
		audio_btn_title = "Launch Neo audio";
		stop_audio_btn_title = "Stop Neo audio"
	}

	const dispatch = createEventDispatcher<{
		change: typeof value;
		submit: undefined;
		stop: undefined;
		blur: undefined;
		select: SelectData;
		input: undefined;
		focus: undefined;
		drag: boolean;
		upload: FileData[] | FileData;
		clear: undefined;
		load: FileData[] | FileData;
		error: string;
		start_recording: undefined;
		stop_recording: undefined;
		stream: Uint8Array[];
	}>();

	beforeUpdate(() => {
		can_scroll = el && el.offsetHeight + el.scrollTop > el.scrollHeight - 100;
	});

	const scroll = (): void => {
		if (can_scroll && autoscroll && !user_has_scrolled_up) {
			el.scrollTo(0, el.scrollHeight);
		}
	};

	async function handle_change(): Promise<void> {
		dispatch("change", value);
		if (!value_is_output) {
			dispatch("input");
		}
	}

	afterUpdate(() => {
		if (autofocus && el !== null) {
			el.focus();
		}
		if (can_scroll && autoscroll) {
			scroll();
		}
		value_is_output = false;
	});

	function handle_select(event: Event): void {
		const target: HTMLTextAreaElement | HTMLInputElement = event.target as
			| HTMLTextAreaElement
			| HTMLInputElement;
		const text = target.value;
		const index: [number, number] = [
			target.selectionStart as number,
			target.selectionEnd as number
		];
		dispatch("select", { value: text.substring(...index), index: index });
	}

	async function handle_keypress(e: KeyboardEvent): Promise<void> {
		await tick();
		if (e.key === "Enter" && e.shiftKey && lines > 1) {
			e.preventDefault();
			dispatch("submit");
		} else if (
			e.key === "Enter" &&
			!e.shiftKey &&
			lines === 1 &&
			max_lines >= 1
		) {
			e.preventDefault();
			dispatch("submit");
		}
	}

	function handle_scroll(event: Event): void {
		const target = event.target as HTMLElement;
		const current_scroll_top = target.scrollTop;
		if (current_scroll_top < previous_scroll_top) {
			user_has_scrolled_up = true;
		}
		previous_scroll_top = current_scroll_top;

		const max_scroll_top = target.scrollHeight - target.clientHeight;
		const user_has_scrolled_to_bottom = current_scroll_top >= max_scroll_top;
		if (user_has_scrolled_to_bottom) {
			user_has_scrolled_up = false;
		}
	}

	async function handle_upload({
		detail
	}: CustomEvent<FileData | FileData[]>): Promise<void> {
		handle_change();
		if (Array.isArray(detail)) {
			for (let file of detail) {
				value.files.push(file);
			}
			value = value;
		} else {
			value.files.push(detail);
			value = value;
		}
		await tick();
		dispatch("change", value);
		dispatch("upload", detail);
	}

	function handle_upload_click(): void {
		if (hidden_upload) {
			hidden_upload.value = "";
			hidden_upload.click();
		}
	}

	function handle_stop(): void {
		dispatch("stop");
	}

	function handle_submit(): void {
		dispatch("submit");
	}

	function handle_paste(event: ClipboardEvent): void {
		if (!event.clipboardData) return;
		const items = event.clipboardData.items;
		for (let index in items) {
			const item = items[index];
			if (item.type.includes("text/plain")) {
				// avoids retrieving image format of pastes which contain plain/text but also have image data in their clipboardData .
				break;
			}
			if (item.kind === "file" && item.type.includes("image")) {
				const blob = item.getAsFile();
				if (blob) upload_component.load_files([blob]);
			}
		}
	}

	function handle_dragenter(event: DragEvent): void {
		event.preventDefault();
		dragging = true;
	}

	function handle_dragleave(event: DragEvent): void {
		event.preventDefault();
		const rect = full_container.getBoundingClientRect();
		const { clientX, clientY } = event;
		if (
			clientX <= rect.left ||
			clientX >= rect.right ||
			clientY <= rect.top ||
			clientY >= rect.bottom
		) {
			dragging = false;
		}
	}

	function handle_drop(event: DragEvent): void {
		event.preventDefault();
		dragging = false;
		if (event.dataTransfer && event.dataTransfer.files) {
			upload_component.load_files(Array.from(event.dataTransfer.files));
		}
	}

	function handle_audio_click_visibility(): void {
		dispatch("start_recording");
	}

	function handle_end_streaming_click_visibility(): void {
		dispatch("stop_recording");
	}

</script>

<div
	class="full-container"
	class:dragging
	bind:this={full_container}
	on:dragenter={handle_dragenter}
	on:dragleave={handle_dragleave}
	on:dragover|preventDefault
	on:drop={handle_drop}
	role="group"
	aria-label="Multimedia input field"
>
	<!-- svelte-ignore a11y-autofocus -->
	<label class:container>
		<div class="input-container">
			{#if upload_btn}
				<Upload
					bind:this={upload_component}
					on:load={handle_upload}
					{file_count}
					filetype={file_types}
					{root}
					{max_file_size}
					bind:dragging
					bind:uploading
					show_progress={false}
					disable_click={true}
					bind:hidden_upload
					on:error
					hidden={true}
					{upload}
					{stream_handler}
				></Upload>
				<button
					data-testid="upload-button"
					class="upload-button"
					title={upload_btn_title}
					{disabled}
					on:click={handle_upload_click}
					style={
						`${stop_audio_btn ? 'display: none;' : ''}`
					}>
					{#if upload_btn === true}
						<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
							<path d="M12 5L12 19" stroke-width="1.3"/>
							<path d="M5 12L19 12" stroke-width="1.3"/>
						</svg>
					{:else}
						{upload_btn}
					{/if}
				</button>
			{/if}
			<textarea
				data-testid="textbox"
				use:text_area_resize={{
					text: value.text,
					lines: lines,
					max_lines: max_lines
				}}
				class="scroll-hide"
				class:no-label={!show_label}
				dir={rtl ? "rtl" : "ltr"}
				bind:value={value.text}
				bind:this={el}
				{placeholder}
				{disabled}
				rows={lines}
				{autofocus}
				on:keypress={handle_keypress}
				on:blur
				on:select={handle_select}
				on:focus
				on:scroll={handle_scroll}
				on:paste={handle_paste}
				style={
					`${stop_audio_btn ? 'display: none; ' : ''}${text_align ? 'text-align: ' + text_align + '; ' : ''}flex-grow: 1;`
				}
			/>
			{#if use_audio_video_recording}
				{#if (mode === "send-receive" || mode == "send") && modality === "video"}
					<!-- <Video
						bind:value={value.audio}
						{label}
						{show_label}
						include_audio={false}
						{server}
						{rtc_configuration}
						{time_limit}
						{mode}
						{track_constraints}
						{rtp_params}
						{on_change_cb}
						on:clear={() => gradio.dispatch("clear")}
						on:play={() => gradio.dispatch("play")}
						on:pause={() => gradio.dispatch("pause")}
						on:upload={() => gradio.dispatch("upload")}
						on:stop={() => gradio.dispatch("stop")}
						on:end={() => gradio.dispatch("end")}
						on:start_recording={() => gradio.dispatch("start_recording")}
						on:stop_recording={() => gradio.dispatch("stop_recording")}
						on:tick={() => gradio.dispatch("tick")}
						on:error={({ detail }) => gradio.dispatch("error", detail)}
						i18n={gradio.i18n}
					>
						<UploadText i18n={gradio.i18n} type="video" />
					</Video> -->
				{:else if (mode === "send-receive" || mode === "send") && modality === "audio"}
					<InteractiveAudio
						bind:value={value.audio}
						mode={mode}
						rtc_configuration={rtc_configuration}
						i18n={gradio.i18n}
						time_limit={time_limit}
						track_constraints={track_constraints}
						rtp_params={rtp_params}
						on_change_cb={on_change_cb}
						{server}
						audio_btn={audio_btn}
						audio_btn_title={audio_btn_title}
						handle_audio_click_visibility={handle_audio_click_visibility}
						stop_audio_btn={stop_audio_btn}
						stop_audio_btn_title={stop_audio_btn_title}
						handle_end_streaming_click_visibility={handle_end_streaming_click_visibility}
						disabled={disabled}
						on:tick={() => gradio.dispatch("tick")}
						on:error={({ detail }) => gradio.dispatch("error", detail)}
					/>
				{/if}
			{/if}
			{#if submit_btn}
				<button
					class="submit-button"
					class:padded-button={submit_btn !== true}
					title={submit_btn_title}
					{disabled}
					on:click={handle_submit}
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24">
						<path d="M12 5V18M12 5L7 10M12 5L17 10" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
				</button>
			{/if}
			{#if stop_btn}
				<button
					class="stop-button"
					class:padded-button={stop_btn !== true}
					title={stop_btn_title}
					on:click={handle_stop}
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
						<rect x="8" y="8" width="8" height="8" rx="1" ry="1"/>
					</svg>
				</button>
			{/if}
		</div>
	</label>
</div>

<style>
	.full-container {
		width: 100%;
		position: relative;
	}

	.full-container.dragging::after {
		content: "";
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		pointer-events: none;
	}

	.input-container {
		display: flex;
		position: relative;
	    /* centrer verticalement les boutons de la multimodale textbox */
		align-items: center;
	}

	textarea {
		flex-grow: 1;
		outline: none !important;
		background: var(--block-background-fill);
		padding: var(--input-padding);
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
		margin-top: 0px;
		margin-bottom: 0px;
		resize: none;
		position: relative;
		z-index: 1;
	}
	textarea.no-label {
		padding-top: 5px;
		padding-bottom: 5px;
	}

	textarea:disabled {
		-webkit-opacity: 1;
		opacity: 1;
		color: var(--input-placeholder-color)
	}

	textarea::placeholder {
		color: var(--input-placeholder-color);
	}

	.upload-button,
	.submit-button,
	.stop-button {
		border: none;
		text-align: center;
		text-decoration: none;
		font-size: 14px;
		cursor: pointer;
		overflow: hidden;
		border-radius: 50%;
		min-width: 22px;
		height: 22px;
		width: 22px;
		margin: 3px;
		flex-shrink: 0;
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: var(--layer-1);
	}

	.upload-button, .submit-button {
		background-color:var(--button-secondary-background-fill);
		stroke:var(--button-secondary-text-color);
	}

	.upload-button {
		margin-right:0px;
	}

	.submit-button, .stop-button {
		margin-left:0px;
	}
	
	.stop-button svg {
		background-color:var(--button-cancel-background-fill);
		fill:var(--button-cancel-text-color);
		stroke:var(--button-cancel-text-color);
	}

	.padded-button {
		padding: 0 10px;
	}

	.upload-button,
	.submit-button {
		background: var(--button-secondary-background-fill);
	}

	.upload-button:hover,
	.submit-button:hover {
		background: var(--button-secondary-background-fill-hover);
	}

	.upload-button:disabled,
	.submit-button:disabled {
		background: var(--button-secondary-background-fill);
		cursor: initial;
	}
	.upload-button:active,
	.submit-button:active {
		box-shadow: var(--button-shadow-active);
	}
</style>
