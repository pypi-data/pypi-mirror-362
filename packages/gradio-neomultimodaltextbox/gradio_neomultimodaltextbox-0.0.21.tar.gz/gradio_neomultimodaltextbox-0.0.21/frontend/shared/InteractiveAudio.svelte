<script lang="ts">
	import type { I18nFormatter } from "@gradio/utils";
	import { createEventDispatcher, onMount } from "svelte";

    import { start, stop } from "./webrtc_utils";
    import { get_devices, set_available_devices, setAudioOutputToHeadset} from "./stream_utils";
    import AudioWave from "./AudioWave.svelte";


    export let mode: "send-receive" | "send";
    export let value: string | null = null;
    export let rtc_configuration: Object | null = null;
    export let i18n: I18nFormatter;
    export let time_limit: number | null = null;
    export let track_constraints: MediaTrackConstraints = {};
    export let rtp_params: RTCRtpParameters = {} as RTCRtpParameters;
    export let on_change_cb: (mg: "tick" | "change") => void;
    export let icon: string | undefined = undefined;
    export let icon_button_color: string = "var(--body-text-color)";
    export let pulse_color: string = "var(--body-text-color)";

    export let audio_btn: boolean = false;
    export let audio_btn_title: string = "";
    export let handle_audio_click_visibility: Function = function() {};

    export let stop_audio_btn_title: string = "";
    export let handle_end_streaming_click_visibility: Function = function() {};
	export let disabled = false;


    let stopword_recognized = false;

    let notification_sound;

    onMount(() => {
        if (value === "__webrtc_value__") {
            notification_sound = new Audio("https://huggingface.co/datasets/freddyaboulton/bucket/resolve/main/pop-sounds.mp3");
        }
    });

    let _on_change_cb = (msg: "change" | "tick" | "stopword") => {
        if (msg === "stopword") {
            console.log("stopword recognized");
            stopword_recognized = true;
            setTimeout(() => {
                stopword_recognized = false;
            }, 3000);
        } else {
            on_change_cb(msg);
        }
    };

    let _time_limit: number | null = null;
    
    export let server: {
        offer: (body: any) => Promise<any>;
    };

    let stream_state: "open" | "closed" | "waiting" = "closed";
    let audio_player: HTMLAudioElement;
    let audio_container: HTMLDivElement;
    let pc: RTCPeerConnection;
    let _webrtc_id = null;
    let stream: MediaStream;
    let available_audio_devices: MediaDeviceInfo[];
    let selected_device: MediaDeviceInfo | null = null;
    let mic_accessed = false;

    const audio_source_callback = () => {
        console.log("stream in callback", stream);
        if(mode==="send") return stream;
        else return audio_player.srcObject as MediaStream
    }


    const dispatch = createEventDispatcher<{
        tick: undefined;
        state_change: undefined;
        error: string
        play: undefined;
        stop: undefined;
	}>();


    async function access_mic(): Promise<void> {
        
        try {
            const constraints = selected_device ? { deviceId: { exact: selected_device.deviceId }, ...track_constraints } : track_constraints;
            const stream_ = await navigator.mediaDevices.getUserMedia({ audio: constraints });
            stream = stream_;
        } catch (err) {
            if (!navigator.mediaDevices) {
                dispatch("error", i18n("audio.no_device_support"));
                return;
            }
            if (err instanceof DOMException && err.name == "NotAllowedError") {
                dispatch("error", i18n("audio.allow_recording_access"));
                return;
            }
            throw err;
        }
        available_audio_devices = set_available_devices(await get_devices(), "audioinput");
        mic_accessed = true;
        const used_devices = stream
                    .getTracks()
                    .map((track) => track.getSettings()?.deviceId)[0];

        selected_device = used_devices
            ? available_audio_devices.find((device) => device.deviceId === used_devices) ||
                available_audio_devices[0]
            : available_audio_devices[0];
    }

    async function stop_mic(): Promise<void> {
        if (stream) {
            // Arrêter toutes les pistes audio du flux
            stream.getTracks().forEach(track => track.stop());
            stream = null; // Libérer la référence au flux
            mic_accessed = false; // Mettre à jour l'état d'accès au micro
        }
    }

    async function switch_streaming(): Promise<void> {
        if (stream_state === "open" || stream_state === "waiting") {
            stream_state = "waiting";
            stop(pc);
            _time_limit = null;
            await stop_mic();
            stream_state = "closed";
            return;
        }
        stream_state = "waiting";
        _webrtc_id = Math.random().toString(36).substring(2);
        value = _webrtc_id;
        console.log(value)
        pc = new RTCPeerConnection(rtc_configuration);
        pc.addEventListener("connectionstatechange",
            async (event) => {
                console.log("connection state change:", pc.connectionState);
                switch(pc.connectionState) {
                    case "connected":
                        console.info("connected");
                        _time_limit = time_limit;
                        stream_state = "open";
                        break;
                    case "disconnected":
                    case "failed":
                    case "closed":
                        console.info("closed");
                        stream_state = "closed";
                        _time_limit = null;
                        stop(pc);
                        break;
                    default:
                        break;
                }
            }
        )
        pc.addEventListener("iceconnectionstatechange", async (event) => {
            console.info("ICE connection state change:", pc.iceConnectionState);
            if (pc.iceConnectionState === "failed" || pc.iceConnectionState === "disconnected" || pc.iceConnectionState === "closed") {
                await stop(pc);
            }
        });

        stream = null
        
        try {
            await access_mic();
        } catch (err) {
            if (!navigator.mediaDevices) {
                dispatch("error", i18n("audio.no_device_support"));
                return;
            }
            if (err instanceof DOMException && err.name == "NotAllowedError") {
                dispatch("error", i18n("audio.allow_recording_access"));
                return;
            }
            throw err;
        }
        if (stream == null) return;
        setAudioOutputToHeadset(audio_player);
        start(stream, pc, mode === "send" ? null: audio_player, server.offer, _webrtc_id, "audio", _on_change_cb, rtp_params).then((connection) => {
            pc = connection;
        }).catch((error) => {
            console.error("interactive audio error: ", error)
        });
        }
        $: if(stopword_recognized){
            notification_sound.play();
    }

    function handle_audio_click() {
        handle_audio_click_visibility();
        switch_streaming();
    }

    function handle_end_streaming_click() {
        handle_end_streaming_click_visibility();
        if (stream_state === "open" || stream_state === "waiting") {         
            switch_streaming();
        } else {
            stream_state = "closed";
        }
    }

</script>

<div bind:this={audio_container} class="audio-container{audio_btn ? '' : ' large'}">
    <audio
    class="standard-player"
    class:hidden={value === "__webrtc_value__"}
    bind:this={audio_player}
    on:ended={() => dispatch("stop")}
    on:play={() => dispatch("play")}
    />
    {#if audio_btn}
    <button
        class="audio-button"
        class:padded-button={audio_btn !== true}
        title={audio_btn_title}
        {disabled}
        on:click={handle_audio_click}
    >
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 4a2.4 2.4 0 0 0-2.4 2.4v5.6a2.4 2.4 0 0 0 4.8 0V6.4a2.4 2.4 0 0 0-2.4-2.4Z" ></path>
            <path d="M17.6 10.4v1.6a5.6 5.6 0 0 1-11.2 0v-1.6"></path>
            <line x1="12" x2="12" y1="17.6" y2="20"></line>
        </svg>
    </button>
    {:else if stream_state === "open" || stream_state === "waiting"}
        {#if stream_state === "open"}
        <div class="audiowave">
            <AudioWave {audio_source_callback} {stream_state} {icon} {icon_button_color} {pulse_color}/>
        </div>
        {:else}
        <div class="audio-blinker">
            <span>·</span><span>·</span><span>·</span>
        </div>
        {/if}
    <button
        class="stop-audio-button"
        title={stop_audio_btn_title}
        {disabled}
        on:click={handle_end_streaming_click}
    >
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
            <rect x="8" y="8" width="8" height="8" rx="1" ry="1"/>
        </svg>
    </button>
    {/if}
</div>

<style>

    .audio-container {
        display: flex;
		height: 30px;
        min-width: 25px;
		justify-content: center;
		align-items: center;
	}

    .audio-container.large {
        width: 100%;
    }

    :global(::part(wrapper)) {
        margin-bottom: var(--size-2);
    }

    .standard-player {
        width: 100%;
        padding: var(--size-2);
    }

    .hidden {
        display: none;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(var(--primary-500-rgb), 0.7);
        }
        
        70% {
            transform: scale(1.25);
            box-shadow: 0 0 0 10px rgba(var(--primary-500-rgb), 0);
        }
        
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(var(--primary-500-rgb), 0);
        }
    }

	@media (--screen-md) {
		button {
			bottom: var(--size-4);
		}
	}

	@media (--screen-xl) {
		button {
			bottom: var(--size-8);
		}
	}

    .stop-audio-button, .audio-button {
		margin-left:0px;
	}

	.stop-audio-button,
	.audio-button {
		border: none;
		text-align: center;
		text-decoration: none;
		font-size: 14px;
		cursor: pointer;
		overflow: hidden;
		border-radius: 50%;
		min-width: 18px;
		height: 18px;
		width: 18px;
		margin: 3px;
		flex-shrink: 0;
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: var(--layer-1);
        margin-left: auto;
	}
	
	.stop-audio-button {
		background-color:var(--button-cancel-background-fill);
	}

	.stop-audio-button svg {
		stroke:var(--button-cancel-text-color);
		fill:var(--button-cancel-text-color);
	}

	.padded-button {
		padding: 0 10px;
	}

	.audio-button {
		background: var(--button-secondary-background-fill);
	}

	.audio-button:hover {
		background: var(--button-secondary-background-fill-hover);
	}

	.audio-button:disabled {
		background: var(--button-secondary-background-fill);
		cursor: initial;
	}
	.audio-button:active {
		box-shadow: var(--button-shadow-active);
	}

    .audiowave {
        flex-grow: 1;
        text-align: center;
    }

    .audio-blinker {
        flex-grow: 1;
        text-align: center;
        animation: blinker 1.5s cubic-bezier(.5, 0, 1, 1) infinite alternate;
        font-size: 3em;
        line-height: 20px;
        color: var(--body-text-color);
    }
    .audio-blinker span {
        opacity: 0;
        animation-name: blinker;
        animation-duration: 1.5s;
        animation-timing-function: cubic-bezier(.5, 0, 1, 1);
        animation-iteration-count: infinite;
    }
    .audio-blinker span:nth-child(1) {
        animation-delay: 0s;
    }
    .audio-blinker span:nth-child(2) {
        animation-delay: .5s; /* Délai pour le deuxième point */
    }
    .audio-blinker span:nth-child(3) {
        animation-delay: 1s; /* Délai pour le troisième point */
    }
    @keyframes blinker {  
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }

</style>