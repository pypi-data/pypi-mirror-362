import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np
import pyaudio
import pyglet
from pipecat.frames.frames import (
    Frame,
    InputAudioRawFrame,
    OutputImageRawFrame,
    StartFrame,
)
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.transports.base_input import BaseInputTransport
from pipecat.transports.base_output import BaseOutputTransport
from pipecat.transports.base_transport import TransportParams

from .media_consumer import MediaConsumer


class PipecatVideoOutputProcessor(FrameProcessor):
    """A frame processor that displays video frames in a Pyglet window.

    This processor takes video frames and displays them in real-time using
    a Pyglet window. It handles frame rate timing and image conversion from
    BGR to RGB format.

    Args:
        config (dict): Configuration dictionary with the following optional keys:
            - frame_rate (int): Target frame rate in FPS (default: 30)
            - width (int): Window width in pixels (default: 1920)
            - height (int): Window height in pixels (default: 1080)
    """

    def __init__(self, config: dict):
        super().__init__()

        self.width = config.get("width", 1920)
        self.height = config.get("height", 1080)
        self.img: pyglet.image.ImageData | None = None
        self.window = config.get("window", None)
        if self.window is None:
            self.window = pyglet.window.Window(
                self.width, self.height, resizable=False, fullscreen=False
            )
        self.logger = logging.getLogger(__name__)

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        """Process incoming frames and route them to appropriate handlers.

        Args:
            frame (Frame): The frame to process
            direction (FrameDirection): The direction the frame is traveling

        Routes StartFrame, EndFrame and OutputImageRawFrame types to their
        respective handlers.
        """
        await super().process_frame(frame, direction)

        if isinstance(frame, OutputImageRawFrame):
            try:
                img = cv2.imdecode(np.frombuffer(frame.image, np.uint8), cv2.IMREAD_COLOR)
                if img is None:
                    self.logger.error("Failed to decode video frame")
                    return

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB, dst=img)
                img = cv2.flip(img, 0)  # Flip vertically for pyglet

                # Create ImageData with the correct dimensions and raw RGB data
                self.img = pyglet.image.ImageData(self.width, self.height, "RGB", img.tobytes())

                # Update the window
                self.window.switch_to()
                self.window.clear()

                # Draw the image on the window
                if self.img is not None:
                    self.img.blit(0, 0, 0, self.width, self.height)

                # Flip the window
                self.window.flip()
            except Exception as e:
                self.logger.error(f"Error processing video frame: {e}")

        await self.push_frame(frame, direction)


class PipecatAudioTransportParams(TransportParams):
    device_name: str = "pulse"


class PipecatAudioOutputTransport(BaseOutputTransport):
    _params: PipecatAudioTransportParams

    def __init__(self, params: PipecatAudioTransportParams, py_audio: pyaudio.PyAudio):
        super().__init__(params)
        self._py_audio = py_audio

        self._params = params
        self._out_stream = None
        self._sample_rate = 0
        self._device_index = None

        info = self._py_audio.get_host_api_info_by_index(0)
        num_devices = info.get("deviceCount")
        for i in range(num_devices):
            device_info = self._py_audio.get_device_info_by_host_api_device_index(0, i)

            if device_info.get("name") == self._params.device_name:
                self._device_index = i

        # We only write audio frames from a single task, so only one thread
        # should be necessary.
        self._executor = ThreadPoolExecutor(max_workers=1)
        self.logger = logging.getLogger(__name__)

    async def start(self, frame: StartFrame):
        await super().start(frame)

        if not self._device_index:
            self.logger.error("There is not a default sink")
            return

        if self._out_stream:
            return

        self._sample_rate = self._params.audio_out_sample_rate or frame.audio_out_sample_rate

        self._out_stream = self._py_audio.open(
            format=self._py_audio.get_format_from_width(2),
            channels=self._params.audio_out_channels,
            rate=self._sample_rate,
            output=True,
            output_device_index=self._device_index,
        )
        self._out_stream.start_stream()

    async def cleanup(self):
        await super().cleanup()
        if self._out_stream:
            self._out_stream.stop_stream()
            self._out_stream.close()
            self._out_stream = None

    async def write_raw_audio_frames(self, frames: bytes):
        if self._out_stream:
            await self.get_event_loop().run_in_executor(
                self._executor, self._out_stream.write, frames
            )


class PipecatAudioInputTransport(BaseInputTransport):
    def __init__(self, params: TransportParams, config: dict):
        super().__init__(params)

        self.chunk_size = config.get("chunk_size", 1024)
        self.chunk_delay = config.get("chunk_delay", 0.05)
        self._num_channels = params.audio_in_channels
        self.mic_id = config.get("mic_id", None)
        self._running = False
        self._wave_file = None
        self._last_chunk_time = 0
        self.consumer = MediaConsumer(
            audio_node_id=self.mic_id,
            audio_sample_rate=params.audio_in_sample_rate,
            audio_channels=params.audio_in_channels,
        )
        self.consumer.push_handlers(data=self._media_consumer_frame_handler)

    async def start(self, frame):
        if self.consumer.audio_pipeline:
            return
        self.consumer.start()
        await self.set_transport_ready(frame)
        await super().start(frame)

    async def stop(self, frame):
        self.consumer.stop()
        await super().stop(frame)

    def _media_consumer_frame_handler(self, frame):
        if frame.type == "audio":
            chunk = frame.data.tobytes()
            audio_raw_frame = InputAudioRawFrame(
                audio=chunk,
                sample_rate=self.consumer.audio_sample_rate,
                num_channels=self.consumer.audio_channels,
            )
            asyncio.run_coroutine_threadsafe(
                self.push_audio_frame(audio_raw_frame), self.get_event_loop()
            )
