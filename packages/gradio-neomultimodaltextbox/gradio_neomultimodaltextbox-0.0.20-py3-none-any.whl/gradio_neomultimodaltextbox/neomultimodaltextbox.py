"""gr.MultimodalTextbox() component."""

from __future__ import annotations
import numpy as np
from collections.abc import Callable, Sequence
from pathlib import Path
import asyncio
import logging
from fastapi.responses import JSONResponse
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Iterable,
    Literal,
    ParamSpec,
    TypeVar,
    TypedDict,
    cast,
    Optional,
)
from aiortc import (
    RTCIceCandidate,
    RTCPeerConnection,
    RTCSessionDescription,
    RTCIceServer,
    RTCConfiguration,
)
from aiortc.contrib.media import MediaRelay  # type: ignore
from gradio import wasm_utils
import gradio_client.utils as client_utils
from pydantic.v1 import Field
from typing_extensions import NotRequired
from gradio.components.base import Component, FormComponent, server
from gradio.data_classes import FileData, GradioModel
from gradio.events import Events
from gradio.exceptions import Error

from .stream_utils import (
    AdditionalOutputs,
    DataChannel,
    AudioCallback,
    VideoCallback,
)
from .rtmt import RTMiddleTier

if TYPE_CHECKING:
    from gradio.blocks import Block
    from gradio.components import Timer

if wasm_utils.IS_WASM:
    raise ValueError("Not supported in gradio-lite!")

logger = logging.getLogger(__name__)


class MultimodalData(GradioModel):
    text: str
    files: list[FileData] = Field(default_factory=list)
    audio: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class MultimodalPostprocess(TypedDict):
    text: str
    files: NotRequired[list[FileData]]


class MultimodalValue(TypedDict):
    text: NotRequired[str]
    files: NotRequired[list[str]]


# For the return type
R = TypeVar("R")
# For the parameter specification
P = ParamSpec("P")


class NeoMultimodalTextbox(
    FormComponent,
):
    """
    Creates a textarea for users to enter string input or display string output and also allows for the uploading of multimedia files.

    Demos: chatbot_multimodal
    Guides: creating-a-chatbot
    """

    data_model = MultimodalData
    pcs: dict[str, RTCPeerConnection] = {}
    relay = MediaRelay()
    connections: dict[str, VideoCallback | AudioCallback] = {}
    data_channels: dict[str, DataChannel] = {}
    additional_outputs: dict[str, list[AdditionalOutputs]] = {}

    EVENTS = [
        Events.change,
        Events.input,
        Events.select,
        Events.submit,
        Events.focus,
        Events.blur,
        Events.stop,
        Events.upload,
        Events.start_recording,
        Events.stop_recording,
        "tick",  # Est utilisé dans gerer le .stream (cf. Web_rtc)
        "state_change",  # Est utilisé dans le .on_additional_outputs (cf. Web_rtc)
    ]

    def __init__(
        self,
        value: str | dict[str, str | list] | Callable | None = None,
        *,
        file_types: list[str] | None = None,
        file_count: Literal["single", "multiple", "directory"] = "single",
        lines: int = 1,
        max_lines: int = 20,
        placeholder: str | None = None,
        label: str | None = None,
        info: str | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = True,
        visible: bool = True,
        elem_id: str | None = None,
        autofocus: bool = False,
        autoscroll: bool = True,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
        text_align: Literal["left", "right"] | None = None,
        rtl: bool = False,
        upload_btn: str | bool | None = True,
        submit_btn: str | bool | None = True,
        stop_btn: str | bool | None = False,
        loading_message: str = "... Loading files ...",
        audio_btn: str | bool | None = False,
        stop_audio_btn: str | bool | None = False,
        mirror_webcam: bool = True,
        rtc_configuration: dict[str, Any] | None = None,
        track_constraints: dict[str, Any] | None = None,
        time_limit: float | None = None,
        mode: Literal["send-receive"] = "send-receive",
        modality: Literal["video", "audio"] = "audio",
        rtp_params: dict[str, Any] | None = None,
        icon: str | None = None,
        icon_button_color: str | None = None,
        pulse_color: str | None = None,
        rtmt: RTMiddleTier | None = None,
    ):
        """
        Parameters:
            value: Default value to show in NeoMultimodalTextbox. A string value, or a dictionary of the form {"text": "sample text", "files": [{path: "files/file.jpg", orig_name: "file.jpg", url: "http://image_url.jpg", size: 100}]}. If callable, the function will be called whenever the app loads to set the initial value of the component.
            file_types: List of file extensions or types of files to be uploaded (e.g. ['image', '.json', '.mp4']). "file" allows any file to be uploaded, "image" allows only image files to be uploaded, "audio" allows only audio files to be uploaded, "video" allows only video files to be uploaded, "text" allows only text files to be uploaded.
            file_count: if single, allows user to upload one file. If "multiple", user uploads multiple files. If "directory", user uploads all files in selected directory. Return type will be list for each file in case of "multiple" or "directory".
            lines: minimum number of line rows to provide in textarea.
            max_lines: maximum number of line rows to provide in textarea.
            placeholder: placeholder hint to provide behind textarea.
            label: the label for this component, displayed above the component if `show_label` is `True` and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component corresponds to.
            info: additional component description, appears below the label in smaller font. Supports markdown / HTML syntax.
            every: Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            inputs: Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.
            show_label: if True, will display label.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            autofocus: If True, will focus on the textbox when the page loads. Use this carefully, as it can cause usability issues for sighted and non-sighted users.
            autoscroll: If True, will automatically scroll to the bottom of the textbox when the value changes, unless the user scrolls up. If False, will not scroll to the bottom of the textbox when the value changes.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
            text_align: How to align the text in the textbox, can be: "left", "right", or None (default). If None, the alignment is left if `rtl` is False, or right if `rtl` is True. Can only be changed if `type` is "text".
            rtl: If True and `type` is "text", sets the direction of the text to right-to-left (cursor appears on the left of the text). Default is False, which renders cursor on the right.
            upload_btn: If False, will not show a upload button. If a string, will use that string as the upload button text.
            submit_btn: If False, will not show a submit button. If a string, will use that string as the submit button text.
            stop_btn: If True, will show a stop button (useful for streaming demos). If a string, will use that string as the stop button text.
            loading_message: The string used during the files loading (when using the upload button).
            audio_btn: If False, will not show a submit button. If a string, will use that string as the submit button text.
            stop_audio_btn: If False, will not show a submit button. If a string, will use that string as the submit button text.
            mirror_webcam: if True webcam will be mirrored. Default is True.
            rtc_configuration: WebRTC configuration options. See https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection/RTCPeerConnection . If running the demo on a remote server, you will need to specify a rtc_configuration. See https://freddyaboulton.github.io/gradio-webrtc/deployment/
            track_constraints: Media track constraints for WebRTC. For example, to set video height, width use {"width": {"exact": 800}, "height": {"exact": 600}, "aspectRatio": {"exact": 1.33333}}
            time_limit: Maximum duration in seconds for recording.
            mode: WebRTC mode - "send-receive", "receive", or "send".
            modality: Type of media - "video" or "audio".
            rtp_params: See https://developer.mozilla.org/en-US/docs/Web/API/RTCRtpSender/setParameters. If you are changing the video resolution, you can set this to {"degradationPreference": "maintain-framerate"} to keep the frame rate consistent.
            icon: Icon to display on the button instead of the wave animation. The icon should be a path/url to a .svg/.png/.jpeg file.
            icon_button_color: Color of the icon button. Default is var(--color-accent) of the demo theme.
            pulse_color: Color of the pulse animation. Default is var(--color-accent) of the demo theme.
            rtmt: The RealTimeMiddleTier component to use the audio (cf Marc-Antoine OUDOTTE)
        """
        self.file_types = file_types
        self.file_count = file_count
        if value is None:
            value = {"text": "", "files": [], "audio": ""}
        if file_types is not None and not isinstance(file_types, list):
            raise ValueError(
                f"Parameter file_types must be a list. Received {file_types.__class__.__name__}"
            )
        self.lines = lines
        self.max_lines = max(lines, max_lines)
        self.placeholder = placeholder
        self.upload_btn = upload_btn
        self.submit_btn = submit_btn
        self.stop_btn = stop_btn
        self.autofocus = autofocus
        self.autoscroll = autoscroll
        self.interactive = interactive
        self.loading_message = loading_message
        super().__init__(
            label=label,
            info=info,
            every=every,
            inputs=inputs,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            value=value,
        )

        self.rtl = rtl
        self.text_align = text_align

        self.audio_btn = audio_btn
        self.stop_audio_btn = stop_audio_btn
        self.time_limit = time_limit
        self.mirror_webcam = mirror_webcam
        self.rtc_configuration = rtc_configuration
        self.mode = mode
        self.modality = modality
        self.rtp_params = rtp_params or {}
        if track_constraints is None and modality == "audio":
            track_constraints = {
                "echoCancellation": True,
                "noiseSuppression": {"exact": True},
                "autoGainControl": {"exact": True},
                "sampleRate": {"ideal": 24000},
                "sampleSize": {"ideal": 16},
                "channelCount": {"exact": 1},
            }
        if track_constraints is None and modality == "video":
            track_constraints = {
                "facingMode": "user",
                "width": {"ideal": 500},
                "height": {"ideal": 500},
                "frameRate": {"ideal": 30},
            }
        self.track_constraints = track_constraints
        if rtmt and not isinstance(rtmt, RTMiddleTier):
            raise ValueError(
                "In the stream event, the fn value should be defined and a RTMiddleTier instance"
            )
        self.rtmt = rtmt
        self.icon_button_color = icon_button_color
        self.pulse_color = pulse_color
        # need to do this here otherwise the proxy_url is not set
        self.icon = (
            icon if not icon else cast(dict, self.serve_static_file(icon)).get("url")
        )

    def set_additional_outputs(
        self, webrtc_id: str
    ) -> Callable[[AdditionalOutputs], None]:
        def set_outputs(outputs: AdditionalOutputs):
            if webrtc_id not in self.additional_outputs:
                self.additional_outputs[webrtc_id] = []
            self.additional_outputs[webrtc_id].append(outputs)

        return set_outputs

    def set_input(self, webrtc_id: str, *args):
        if webrtc_id in self.connections:
            self.connections[webrtc_id].set_args(list(args))

    def on_additional_outputs(
        self,
        fn: Callable[Concatenate[P], R],
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | set[Block] | None = None,
        js: str | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        queue: bool = True,
        show_api: bool = True,
    ):
        inputs = inputs or []
        if inputs and not isinstance(inputs, Iterable):
            inputs = [inputs]
            inputs = list(inputs)

        def handler(webrtc_id: str, *args):
            webrtc_id = webrtc_id["audio"]  # On passe du dict d'outputs à l'audio
            if (
                webrtc_id in self.additional_outputs
                and len(self.additional_outputs[webrtc_id]) > 0
            ):
                next_outputs = self.additional_outputs[webrtc_id].pop(0)
                return fn(*args, *next_outputs.args)  # type: ignore
            return (
                tuple([None for _ in range(len(outputs))])
                if isinstance(outputs, Iterable)
                else None
            )

        return self.state_change(  # type: ignore
            fn=handler,
            inputs=[self] + cast(list, inputs),
            outputs=outputs,
            js=js,
            concurrency_limit=None,
            concurrency_id=concurrency_id,
            show_progress=show_progress,
            queue=queue,
            trigger_mode="multiple",
            show_api=show_api,
        )

    def stream(
        self,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | set[Block] | None = None,
        js: str | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        time_limit: float | None = None,
        show_api: bool = False,
    ):
        from gradio.blocks import Block

        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []
        if isinstance(inputs, Block):
            inputs = [inputs]
        if isinstance(outputs, Block):
            outputs = [outputs]

        self.time_limit = time_limit

        if self.mode == "send-receive" or self.mode == "send":
            if cast(list[Block], inputs)[0] != self:
                raise ValueError(
                    "In the stream event, the first input component must be the Multimodal Component."
                )

            if (
                len(cast(list[Block], outputs)) != 1
                and cast(list[Block], outputs)[0] != self
            ):
                raise ValueError(
                    "In the stream event, the only output component must be the WebRTC component."
                )
            return self.tick(  # type: ignore
                self.set_input,
                inputs=inputs,
                outputs=None,
                concurrency_id=concurrency_id,
                concurrency_limit=concurrency_limit,
                stream_every=0.5,
                time_limit=None,
                js=js,
                show_api=show_api,
            )

    @staticmethod
    async def wait_for_time_limit(pc: RTCPeerConnection, time_limit: float):
        await asyncio.sleep(time_limit)
        await pc.close()

    def preprocess(self, payload: MultimodalData | None) -> MultimodalValue | None:
        """
        Parameters:
            payload: the text and list of file(s) entered in the multimodal textbox.
        Returns:
            Passes text value and list of file(s) as a {dict} into the function.
        """
        if payload is None:
            return None
        if self.file_types is not None:
            for f in payload.files:
                if not client_utils.is_valid_file(f.path, self.file_types):
                    raise Error(
                        f"Invalid file type: {f.mime_type}. Please upload a file that is one of these formats: {self.file_types}"
                    )
        return {
            "text": payload.text,
            "files": [f.path for f in payload.files],
            "audio": payload.audio,
        }

    def postprocess(
        self, value: MultimodalValue | str | None | np.ndarray | bytes
    ) -> MultimodalData | bytes:
        """
        Parameters:
            value: Expects a {dict} with "text" and "files", both optional. The files array is a list of file paths or URLs.
        Returns:
            The value to display in the multimodal textbox. Files information as a list of FileData objects.
        """
        if value is None:
            return MultimodalData(text="", files=[], audio="")
        if not isinstance(value, (dict, str)):
            raise ValueError(
                f"NeoMultimodalTextbox expects a string or a dictionary with optional keys 'text' and 'files'. Received {value.__class__.__name__}"
            )
        if isinstance(value, str):
            return MultimodalData(text=value, files=[], audio="")
        text = value.get("text", "")
        if "files" in value and isinstance(value["files"], list):
            files = [
                (
                    cast(FileData, file)
                    if isinstance(file, FileData | dict)
                    else FileData(
                        path=file,
                        orig_name=Path(file).name,
                        mime_type=client_utils.get_mimetype(file),
                    )
                )
                for file in value["files"]
            ]
        else:
            files = []
        if not isinstance(text, str):
            raise TypeError(
                f"Expected 'text' to be a string, but got {type(text).__name__}"
            )
        if not isinstance(files, list):
            raise TypeError(
                f"Expected 'files' to be a list, but got {type(files).__name__}"
            )
        return MultimodalData(text=text, files=files, audio="")

    def example_value(self) -> Any:
        return {"text": "sample text", "files": [], "audio": ""}

    def example_payload(self):
        return self.postprocess({"text": "sample text", "files": [], "audio": ""})

    def clean_up(self, webrtc_id: str):
        self.pcs.pop(webrtc_id, None)
        connection = self.connections.pop(webrtc_id, None)
        self.additional_outputs.pop(webrtc_id, None)
        self.data_channels.pop(webrtc_id, None)
        return connection

    @server
    async def offer(self, body):
        return await self.handle_offer(
            body, self.set_additional_outputs(body["webrtc_id"])
        )

    async def handle_offer(self, body, set_outputs):
        logger.info("Starting to handle offer")
        logger.info("Offer body %s", body)


        if body.get("type") == "ice-candidate" and "candidate" in body:
            webrtc_id = body.get("webrtc_id")
            if webrtc_id not in self.pcs:
                logger.warning(
                    f"Received ICE candidate for unknown connection: {webrtc_id}"
                )
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "failed",
                        "meta": {"error": "unknown_connection"},
                    },
                )

            pc = self.pcs[webrtc_id]
            if pc.connectionState != "closed":
                try:
                    # Parse the candidate string from the browser
                    candidate_str = body["candidate"].get("candidate", "")

                    # Example format: "candidate:2393089663 1 udp 2122260223 192.168.86.60 63692 typ host generation 0 ufrag LkZb network-id 1 network-cost 10"
                    # We need to parse this string to extract the required fields

                    # Parse the candidate string
                    parts = candidate_str.split()
                    if len(parts) >= 10 and parts[0].startswith("candidate:"):
                        foundation = parts[0].split(":", 1)[1]
                        component = int(parts[1])
                        protocol = parts[2]
                        priority = int(parts[3])
                        ip = parts[4]
                        port = int(parts[5])
                        # Find the candidate type
                        typ_index = parts.index("typ")
                        candidate_type = parts[typ_index + 1]

                        # Create the RTCIceCandidate object
                        ice_candidate = RTCIceCandidate(
                            component=component,
                            foundation=foundation,
                            ip=ip,
                            port=port,
                            priority=priority,
                            protocol=protocol,
                            type=candidate_type,
                            sdpMid=body["candidate"].get("sdpMid"),
                            sdpMLineIndex=body["candidate"].get("sdpMLineIndex"),
                        )

                        # Add the candidate to the peer connection
                        await pc.addIceCandidate(ice_candidate)
                        logger.debug(f"Added ICE candidate for {webrtc_id}")
                        return JSONResponse(
                            status_code=200, content={"status": "success"}
                        )
                    else:
                        logger.error(f"Invalid candidate format: {candidate_str}")
                        return JSONResponse(
                            status_code=200,
                            content={
                                "status": "failed",
                                "meta": {"error": "invalid_candidate_format"},
                            },
                        )
                except Exception as e:
                    logger.error(f"Error adding ICE candidate: {e}", exc_info=True)
                    return JSONResponse(
                        status_code=200,
                        content={"status": "failed", "meta": {"error": str(e)}},
                    )

            return JSONResponse(
                status_code=200,
                content={"status": "failed", "meta": {"error": "connection_closed"}},
            )

        if body["webrtc_id"] in self.connections:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "failed",
                    "meta": {
                        "error": "connection_already_exists",
                    },
                },
            )

        offer = RTCSessionDescription(sdp=body["sdp"], type=body["type"])
        if self.rtc_configuration is not None:
            ice_servers = [
                RTCIceServer(
                    urls=server['urls'],
                    username=server.get('username'),
                    credential=server.get('credential')
                ) for server in self.rtc_configuration['iceServers']
            ]
            rtc_config = RTCConfiguration(iceServers=ice_servers)
            pc = RTCPeerConnection(rtc_config)
        else:
            pc = RTCPeerConnection()
        self.pcs[body["webrtc_id"]] = pc

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            logger.info("ICE connection state change %s", pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                await pc.close()
                self.connections.pop(body["webrtc_id"], None)
                self.pcs.pop(body["webrtc_id"], None)
                logger.info("ICE connection state closed")
                logger.info(f"pcs {self.pcs}")

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            logger.info("pc.connectionState %s", pc.connectionState)
            if pc.connectionState in ["failed", "closed"]:
                await pc.close()
                connection = self.clean_up(body["webrtc_id"])
                if connection:
                    connection.stop()
                self.pcs.pop(body["webrtc_id"], None)
            if pc.connectionState == "connected":
                if self.time_limit is not None:
                    asyncio.create_task(self.wait_for_time_limit(pc, self.time_limit))

        @pc.on("track")
        def on_track(track):
            relay = MediaRelay()
            if self.modality == "video":
                raise NotImplementedError("This feature is not yet implemented")
                cb = VideoCallback(
                    relay.subscribe(track),
                    event_handler=cast(Callable, self.event_handler),
                    set_additional_outputs=set_outputs,
                    mode=cast(Literal["send", "send-receive"], self.mode),
                )
            elif self.modality == "audio":
                cb = AudioCallback(
                    relay.subscribe(track),
                    rtmt=self.rtmt,
                    set_additional_outputs=set_outputs,
                )
            self.connections[body["webrtc_id"]] = cb
            if body["webrtc_id"] in self.data_channels:
                self.connections[body["webrtc_id"]].set_channel(
                    self.data_channels[body["webrtc_id"]]
                )
            if self.mode == "send-receive":
                logger.info("Adding track to peer connection %s", cb)
                pc.addTrack(cb)
            elif self.mode == "send":
                cast(AudioCallback | VideoCallback, cb).start()

        @pc.on("datachannel")
        def _(channel):
            logger.info(f"Data channel established: {channel.label}")
            self.data_channels[body["webrtc_id"]] = channel

            async def set_channel(webrtc_id: str):
                while not self.connections.get(webrtc_id):
                    await asyncio.sleep(0.05)
                logger.info("setting channel for webrtc id %s", webrtc_id)
                self.connections[webrtc_id].set_channel(channel)

            asyncio.create_task(set_channel(body["webrtc_id"]))

            @channel.on("message")
            def on_message(message):
                logger.info(f"Received message: {message}")
                if channel.readyState == "open":
                    channel.send(f"Server received: {message}")

        # handle offer
        await pc.setRemoteDescription(offer)

        # send answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)  # type: ignore
        logger.info("done handling offer about to return")
        await asyncio.sleep(0.1)

        return {
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type,
        }
