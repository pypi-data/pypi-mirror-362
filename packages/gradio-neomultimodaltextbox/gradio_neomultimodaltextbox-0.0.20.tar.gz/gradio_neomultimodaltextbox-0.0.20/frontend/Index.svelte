<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio, SelectData } from "@gradio/utils";
	import MultimodalTextbox from "./MultimodalTextbox.svelte";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import type { FileData } from "@gradio/client";

	export let gradio: Gradio<{
		change: typeof value;
		submit: never;
		stop: never;
		stream: never;
		blur: never;
		select: SelectData;
		input: never;
		focus: never;
		error: string;
		clear_status: LoadingStatus;
		start_recording: never;
		stop_recording: never;
		tick: never;
	}>;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: { text: string; files: FileData[]; audio: string} = {
		text: "",
		files: [],
		audio: "__webrtc_value__",
	};
	export let file_types: string[] | null = null;
	export let lines: number;
	export let placeholder = "";
	export let label = "MultimodalTextbox";
	export let info: string | undefined = undefined;
	export let show_label: boolean;
	export let max_lines: number;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let upload_btn: string | boolean | null = null;
	export let submit_btn: string | boolean | null = null;
	export let stop_btn: string | boolean | null = null;
	export let loading_message: string = "... Loading files ...";
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
	export let rtl = false;
	export let text_align: "left" | "right" | undefined = undefined;
	export let autofocus = false;
	export let autoscroll = true;
	export let interactive: boolean;
	export let root: string;
	export let file_count: "single" | "multiple" | "directory";
	export let audio_btn: boolean;
	export let stop_audio_btn: boolean;

	export let rtc_configuration: Object;
	export let time_limit: number | null = null;
	export let modality: "video" | "audio" = "audio";
	export let mode: "send-receive" | "receive" | "send" = "send-receive";
	export let rtp_params: RTCRtpParameters = {} as RTCRtpParameters;
	export let track_constraints: MediaTrackConstraints = {};
	export let server: {
		offer: (body: any) => Promise<any>;
	};

	const on_change_cb = (msg: "change" | "tick") => {
		gradio.dispatch(msg === "change" ? "state_change" : "tick");
	}

	let dragging: boolean;
</script>

<Block
	{visible}
	{elem_id}
	elem_classes={[...elem_classes, "multimodal-textbox"]}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={container}
	border_mode={dragging ? "focus" : "base"}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}

	<MultimodalTextbox
		bind:value
		bind:value_is_output
		bind:dragging
		{file_types}
		{root}
		{label}
		{info}
		{show_label}
		{lines}
		{rtl}
		{text_align}
		max_lines={!max_lines ? lines + 1 : max_lines}
		{placeholder}
		{upload_btn}
		{submit_btn}
		{stop_btn}
		{autofocus}
		{container}
		{autoscroll}
		{file_count}
		{interactive}
		{loading_message}
		{audio_btn}
		{stop_audio_btn}
		max_file_size={gradio.max_file_size}
		on_change_cb={on_change_cb}
		server={server}
		rtc_configuration={rtc_configuration}
		time_limit={time_limit}
		track_constraints={track_constraints}
		mode={mode}
		rtp_params={rtp_params}
		modality={modality}
		gradio={gradio}
		on:tick={() => gradio.dispatch("tick")}
		on:change={() => gradio.dispatch("change", value)}
		on:input={() => gradio.dispatch("input")}
		on:submit={() => gradio.dispatch("submit")}
		on:stop={() => gradio.dispatch("stop")}
		on:blur={() => gradio.dispatch("blur")}
		on:select={(e) => gradio.dispatch("select", e.detail)}
		on:focus={() => gradio.dispatch("focus")}
		on:upload={({ detail }) => gradio.dispatch("upload", detail)}
		on:error={({ detail }) => {
			gradio.dispatch("error", detail);
		}}
		on:start_recording={() => gradio.dispatch("start_recording")}
		on:stop_recording={() => gradio.dispatch("stop_recording")}

		upload={(...args) => gradio.client.upload(...args)}
		stream_handler={(...args) => gradio.client.stream(...args)}
	/>
</Block>
