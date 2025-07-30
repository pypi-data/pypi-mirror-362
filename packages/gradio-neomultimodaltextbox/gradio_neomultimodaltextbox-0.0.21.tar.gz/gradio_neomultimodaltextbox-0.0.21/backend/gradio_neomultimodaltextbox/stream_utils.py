import logging
from typing import Any, Literal, Protocol, TypedDict, cast, Callable
import traceback
import asyncio
import time
import numpy as np
from abc import ABC, abstractmethod
from aiortc import (
    AudioStreamTrack,
    MediaStreamTrack,
    VideoStreamTrack,
)
from aiortc.contrib.media import AudioFrame, VideoFrame  # type: ignore
from aiortc.mediastreams import MediaStreamError

from .rtmt import RTMiddleTier, AdditionalOutputs

logger = logging.getLogger(__name__)


AUDIO_PTIME = 0.02


class AudioChunk(TypedDict):
    start: int
    end: int


class DataChannel(Protocol):
    def send(self, message: str) -> None: ...


class VideoCallback(VideoStreamTrack):
    """
    This works for streaming input and output
    """

    kind = "video"

    def __init__(
        self,
        track: MediaStreamTrack,
        event_handler: Callable,
        channel: DataChannel | None = None,
        set_additional_outputs: Callable | None = None,
        mode: Literal["send-receive", "send"] = "send-receive",
    ) -> None:
        super().__init__()  # don't forget this!
        self.track = track
        self.event_handler = event_handler
        self.latest_args: str | list[Any] = "not_set"
        self.channel = channel
        self.set_additional_outputs = set_additional_outputs
        self.thread_quit = asyncio.Event()
        self.mode = mode

    def set_channel(self, channel: DataChannel):
        self.channel = channel

    def set_args(self, args: list[Any]):
        self.latest_args = ["__webrtc_value__"] + list(args)

    def add_frame_to_payload(
        self, args: list[Any], frame: np.ndarray | None
    ) -> list[Any]:
        new_args = []
        for val in args:
            if isinstance(val, str) and val == "__webrtc_value__":
                new_args.append(frame)
            else:
                new_args.append(val)
        return new_args

    def array_to_frame(self, array: np.ndarray) -> VideoFrame:
        return VideoFrame.from_ndarray(array, format="bgr24")

    async def process_frames(self):
        while not self.thread_quit.is_set():
            try:
                await self.recv()
            except TimeoutError:
                continue

    def start(
        self,
    ):
        asyncio.create_task(self.process_frames())

    def stop(self):
        super().stop()
        logger.debug("video callback stop")
        self.thread_quit.set()

    async def recv(self):
        try:
            try:
                frame = cast(VideoFrame, await self.track.recv())
            except MediaStreamError:
                self.stop()
                return
            frame_array = frame.to_ndarray(format="bgr24")

            if self.latest_args == "not_set":
                return frame

            args = self.add_frame_to_payload(cast(list, self.latest_args), frame_array)

            array, outputs = self.event_handler(*args)  # TODO (split output before)
            if (
                isinstance(outputs, AdditionalOutputs)
                and self.set_additional_outputs
                and self.channel
            ):
                self.set_additional_outputs(outputs)
                self.channel.send("change")
            if array is None and self.mode == "send":
                return

            new_frame = self.array_to_frame(array)
            if frame:
                new_frame.pts = frame.pts
                new_frame.time_base = frame.time_base
            else:
                pts, time_base = await self.next_timestamp()
                new_frame.pts = pts
                new_frame.time_base = time_base

            return new_frame
        except Exception as e:
            logger.debug("exception %s", e)
            exec = traceback.format_exc()
            logger.debug("traceback %s", exec)


class StreamHandler(ABC):
    def __init__(
        self,
        expected_layout: Literal["mono", "stereo"] = "mono",
        input_sample_rate: int = 48000,
    ) -> None:
        self.expected_layout = expected_layout
        self.input_sample_rate = input_sample_rate
        self.latest_args: str | list[Any] = "not_set"
        self._resampler = None
        self._channel: DataChannel | None = None
        self._loop: asyncio.AbstractEventLoop

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return cast(asyncio.AbstractEventLoop, self._loop)

    @property
    def channel(self) -> DataChannel | None:
        return self._channel

    def set_channel(self, channel: DataChannel):
        self._channel = channel

    def set_args(self, args: list[Any]):
        logger.debug("setting args in audio callback %s", args)
        self.latest_args = ["__webrtc_value__"] + list(args)

    def shutdown(self):
        pass

    @abstractmethod
    def copy(self) -> "StreamHandler":
        pass

    def resample(self, frame: AudioFrame):
        pass

    @abstractmethod
    def receive(self, frame: tuple[int, np.ndarray]) -> None:
        pass

    @abstractmethod
    def emit(
        self,
    ) -> (
        tuple[int, np.ndarray]
        | AdditionalOutputs
        | None
        | tuple[tuple[int, np.ndarray], AdditionalOutputs]
    ):
        pass


class AudioCallback(AudioStreamTrack):
    kind = "audio"

    def __init__(
        self,
        track: MediaStreamTrack,
        rtmt: RTMiddleTier,
        channel: DataChannel | None = None,
        set_additional_outputs: Callable | None = None,
    ) -> None:
        self.track = track
        self.current_timestamp = 0
        self.latest_args: str | list[Any] = "not_set"
        self.queue = asyncio.Queue()
        self.thread_quit = asyncio.Event()
        self._start: float | None = None
        self.has_started = False
        self.last_timestamp = 0
        self.channel = channel
        self.set_additional_outputs = set_additional_outputs
        self.rtmt = rtmt
        super().__init__()

    def set_channel(self, channel: DataChannel):
        self.channel = channel

    def set_args(self, args: list[Any]):
        pass

    def start(self) -> None:
        if not self.has_started:

            self.rtmt.pts = 0
            asyncio.create_task(
                self.rtmt._forward_messages(
                    self.track,
                    self.thread_quit,
                    self.queue,
                    lambda: self.channel,
                    self.set_additional_outputs,
                )
            )

            self.has_started = True

    async def recv(self):
        try:
            if self.readyState != "live":
                raise MediaStreamError
            self.start()
            frame = await self.queue.get()
            data_time = frame.time
            if time.time() - self.last_timestamp > 10 * AUDIO_PTIME:
                # control playback rate
                self._start = time.time() - data_time
            else:
                wait = self._start + data_time - time.time()
                await asyncio.sleep(wait)
            self.last_timestamp = time.time()
            return frame
        except Exception as e:
            logger.debug("exception %s", e)
            exec = traceback.format_exc()
            logger.debug("traceback %s", exec)

    def stop(self):
        logger.debug("audio callback stop")
        self.thread_quit.set()
        super().stop()

    def shutdown(self):
        pass
