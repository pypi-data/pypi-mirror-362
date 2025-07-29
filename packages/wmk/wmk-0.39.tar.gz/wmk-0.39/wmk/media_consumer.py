import json
import logging
import subprocess
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

import numpy as np
from pyglet.event import EventDispatcher


@dataclass
class Frame:
    """Data class to store frame data with timestamp"""

    type: Literal["audio", "video"]
    data: np.ndarray
    timestamp: datetime


class MediaConsumer(EventDispatcher):
    """MediaConsumer handles audio and video capture from PipeWire sources.

    This class provides functionality to capture audio and video streams from PipeWire nodes
    using GStreamer pipelines. It processes the media data and emits events containing
    frame data as numpy arrays.

    Attributes:
        audio_node_id (int, optional): PipeWire node ID for audio capture.
        video_node_id (int, optional): PipeWire node ID for video capture.
        running (bool): Flag to indicate if the consumer is running.
        audio_sample_rate (int): Sample rate for audio capture (default: 48000).
        audio_channels (int): Number of audio channels to capture (default: 1).
        loop (GLib.MainLoop): GLib main loop for handling GStreamer events.
        audio_pipeline (Gst.Pipeline): GStreamer pipeline for audio capture.
        video_pipeline (Gst.Pipeline): GStreamer pipeline for video capture.

    Raises:
        RuntimeError: If GStreamer dependencies (gi, gstreamer) are not installed.

    Events:
        data: Emitted when new media data is available.
            Args:
                frame (Frame): Contains frame data, type ('audio' or 'video'), and timestamp.

    Example:
        >>> consumer = MediaConsumer(audio_node_id=51, video_node_id=52)
        >>> def on_data(frame):
        ...     if frame.type == 'video':
        ...         print(f"Received video frame: {frame.data.shape}")
        ...     else:
        ...         print(f"Received audio data: {len(frame.data)} samples")
        >>> consumer.push_handlers(data=on_data)
        >>> consumer.start()
    """

    event_types = ["data"]
    _gst_initialized = False
    _init_lock = threading.Lock()
    Gst = None
    GLib = None

    @classmethod
    def _initialize_gstreamer(cls):
        """Initialize GStreamer once for all instances."""
        if not cls._gst_initialized:
            with cls._init_lock:
                if not cls._gst_initialized:  # Double-check pattern
                    try:
                        import gi

                        gi.require_version("Gst", "1.0")
                        from gi.repository import GLib, Gst

                        cls.Gst = Gst
                        cls.GLib = GLib
                        Gst.init(None)
                        cls._gst_initialized = True
                    except (ImportError, ValueError) as e:
                        raise RuntimeError(
                            "GStreamer dependencies not found. Please install gstreamer and gi packages."
                        ) from e

    def __init__(
        self,
        audio_node_id: int | None = None,
        video_node_id: int | None = None,
        audio_sample_rate: int = 48000,
        audio_channels: int = 1,
    ) -> None:
        super().__init__()

        # Initialize GStreamer at class level if needed
        self._initialize_gstreamer()

        self.running = False

        self.audio_node_id = audio_node_id
        self.video_node_id = video_node_id

        # Create GLib main loop
        self.loop = self.GLib.MainLoop()
        self.loop_thread = None

        # Pipeline storage
        self.audio_pipeline = None
        self.video_pipeline = None

        self.audio_sample_rate = audio_sample_rate
        self.audio_channels = audio_channels

        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _find_defualt_audio_node(self, name: str) -> int | None:
        """
        Find PipeWire node ID by name.
        """
        try:
            # Run pw-dump command to get all nodes
            result = subprocess.run(["pw-dump"], capture_output=True, text=True, check=False)
            if result.returncode != 0:
                self.logger.error(f"pw-dump failed: {result.stderr}")
                return None

            # Parse JSON output
            nodes = json.loads(result.stdout)

            # Search for node with matching name
            for node in nodes:
                if node.get("type") == "PipeWire:Interface:Node":
                    info = node.get("info", {})
                    if info.get("props", {}).get("node.name") == name:
                        node_id = node.get("id")
                        self.logger.debug(f"Found node '{name}' with ID {node_id}")
                        return node_id

            self.logger.debug(f"No node found with name '{name}'")
            return None

        except Exception as e:
            self.logger.error(f"Error finding audio node: {e}")
            return None

    def start(self) -> None:
        if self.running:
            self.logger.warning("MediaConsumer is already running")
            return

        """Start capturing from PipeWire streams."""
        self._setup_audio_pipeline()
        self._setup_video_pipeline()

        # Start GLib main loop in a separate thread
        self.loop_thread = threading.Thread(target=self.loop.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()

    def stop(self) -> None:
        """Stop all pipeline processing."""
        if self.audio_pipeline:
            self.audio_pipeline.set_state(self.Gst.State.NULL)

        if self.video_pipeline:
            self.video_pipeline.set_state(self.Gst.State.NULL)

        if self.loop.is_running():
            self.loop.quit()

        if self.loop_thread:
            self.loop_thread.join()

        self.running = False

    def _setup_video_pipeline(self) -> None:
        """Set up the GStreamer pipeline for video capture."""
        if not self.video_node_id:
            self.logger.error("No video node ID provided for capture")
            return

        pipeline_str = f"""
            pipewiresrc path={self.video_node_id} !
            videoconvert ! video/x-raw,format=RGB !
            appsink name=video_sink emit-signals=true
        """

        self.video_pipeline = self.Gst.parse_launch(pipeline_str)
        video_sink = self.video_pipeline.get_by_name("video_sink")
        video_sink.connect("new-sample", self._on_video_sample)

        # Start playing
        ret = self.video_pipeline.set_state(self.Gst.State.PLAYING)
        if ret == self.Gst.StateChangeReturn.FAILURE:
            self.logger.error("Failed to set video pipeline to PLAYING state")
        else:
            self.logger.info("Video pipeline set to PLAYING state")

    def _setup_audio_pipeline(self) -> None:
        """Set up the GStreamer pipeline for audio capture."""

        # Find default audio node if not provided
        if not self.audio_node_id:
            self.audio_node_id = self._find_defualt_audio_node("VirtualSink")
            if not self.audio_node_id:
                self.logger.error("No audio node found for capture")
                return

        pipeline_str = f"""
            pipewiresrc path={self.audio_node_id} !
            audioconvert !
            audio/x-raw,format=S16LE,rate={self.audio_sample_rate},channels={self.audio_channels} !
            appsink name=audio_sink emit-signals=true
        """

        self.audio_pipeline = self.Gst.parse_launch(pipeline_str)
        audio_sink = self.audio_pipeline.get_by_name("audio_sink")
        audio_sink.connect("new-sample", self._on_audio_sample)

        ret = self.audio_pipeline.set_state(self.Gst.State.PLAYING)
        if ret == self.Gst.StateChangeReturn.FAILURE:
            self.logger.error("Failed to set audio pipeline to PLAYING state")
        else:
            self.logger.info("Audio pipeline set to PLAYING state")

    def _on_video_sample(self, sink):
        """Callback for handling new video frames.

        Args:
            sink: GStreamer video sink element

        Returns:
            Gst.FlowReturn: Status of the operation
        """
        sample = sink.emit("pull-sample")
        if sample:
            buffer = sample.get_buffer()
            caps = sample.get_caps()

            # Get buffer data
            success, map_info = buffer.map(self.Gst.MapFlags.READ)
            if success:
                # Get video format info from caps
                structure = caps.get_structure(0)
                width = structure.get_value("width")
                height = structure.get_value("height")

                # Convert buffer to numpy array
                video_array = np.ndarray((height, width, 3), buffer=map_info.data, dtype=np.uint8)

                # Store the frame with timestamp
                frame = Frame(type="video", data=video_array.copy(), timestamp=datetime.now())
                self.dispatch_event("data", frame)

                buffer.unmap(map_info)

        return self.Gst.FlowReturn.OK

    def _on_audio_sample(self, sink):
        """Callback for handling new audio samples.

        Args:
            sink: GStreamer audio sink element

        Returns:
            Gst.FlowReturn: Status of the operation
        """
        sample = sink.emit("pull-sample")
        if sample:
            buffer = sample.get_buffer()

            # Get buffer data
            success, map_info = buffer.map(self.Gst.MapFlags.READ)
            if success:
                # Convert buffer to numpy array
                audio_array = np.frombuffer(map_info.data, dtype=np.int16)

                # Store the audio buffer with timestamp
                frame = Frame(type="audio", data=audio_array.copy(), timestamp=datetime.now())
                self.dispatch_event("data", frame)

                buffer.unmap(map_info)

        return self.Gst.FlowReturn.OK
