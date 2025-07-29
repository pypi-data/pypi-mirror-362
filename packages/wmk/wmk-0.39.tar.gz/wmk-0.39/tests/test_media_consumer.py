from unittest.mock import Mock, patch

import numpy as np
import pytest

from wmk.media_consumer import MediaConsumer


@pytest.fixture(autouse=True)
def reset_media_consumer():
    """Reset MediaConsumer class state before each test"""
    MediaConsumer._gst_initialized = False
    MediaConsumer.Gst = None
    MediaConsumer.GLib = None
    yield


@pytest.fixture
def mock_gi_dependencies():
    """Mock GStreamer and GLib dependencies"""
    with patch.dict(
        "sys.modules",
        {
            "gi": Mock(),
            "gi.repository": Mock(),
        },
    ) as mocked:
        # Setup gi mock
        gi_mock = mocked["gi"]
        gi_mock.require_version = Mock()

        # Setup Gst mock
        gst_mock = Mock()
        gst_mock.init.return_value = None
        gst_mock.FlowReturn.OK = 0
        gst_mock.State.PLAYING = 1
        gst_mock.State.NULL = 0
        gst_mock.StateChangeReturn.FAILURE = 0
        gst_mock.StateChangeReturn.SUCCESS = 1
        gst_mock.MapFlags.READ = 1

        # Setup GLib mock
        glib_mock = Mock()
        mock_loop = Mock()
        mock_loop.run = Mock()
        mock_loop.quit = Mock()
        mock_loop.is_running.return_value = True
        glib_mock.MainLoop.return_value = mock_loop

        # Attach mocks to gi.repository
        mocked["gi.repository"].Gst = gst_mock
        mocked["gi.repository"].GLib = glib_mock

        yield gst_mock, glib_mock


@pytest.fixture
def consumer(mock_gi_dependencies):
    return MediaConsumer(audio_node_id=51, video_node_id=52)


def test_gstreamer_initialized_once(mock_gi_dependencies):
    """Test that GStreamer is initialized only once for multiple instances"""
    gst_mock, _ = mock_gi_dependencies

    # Create first instance
    consumer1 = MediaConsumer()
    assert MediaConsumer._gst_initialized is True
    init_count = gst_mock.init.call_count

    # Create second instance
    consumer2 = MediaConsumer()
    assert gst_mock.init.call_count == init_count

    # Verify both instances share the same Gst reference
    assert consumer1.Gst is consumer2.Gst
    assert consumer1.Gst is MediaConsumer.Gst


def test_gstreamer_thread_safety(mock_gi_dependencies):
    """Test thread-safe initialization of GStreamer"""
    import threading

    consumers = []

    def create_consumer():
        consumers.append(MediaConsumer())

    # Create multiple consumers simultaneously
    threads = [threading.Thread(target=create_consumer) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify all instances share the same Gst reference
    assert all(c.Gst is MediaConsumer.Gst for c in consumers)
    assert len(consumers) == 5


def test_init(consumer):
    assert MediaConsumer._gst_initialized is True
    assert MediaConsumer.Gst is not None
    assert MediaConsumer.GLib is not None
    assert consumer.audio_node_id == 51
    assert consumer.video_node_id == 52
    assert consumer.audio_sample_rate == 48000
    assert consumer.audio_channels == 1


def test_start(consumer):
    with (
        patch.object(consumer, "_setup_audio_pipeline") as mock_audio_setup,
        patch.object(consumer, "_setup_video_pipeline") as mock_video_setup,
    ):
        consumer.start()

        mock_audio_setup.assert_called_once()
        mock_video_setup.assert_called_once()
        assert consumer.loop_thread is not None
        assert consumer.loop_thread.daemon is True


def test_stop(consumer):
    consumer.audio_pipeline = Mock()
    consumer.video_pipeline = Mock()
    consumer.loop_thread = Mock()

    consumer.stop()

    consumer.audio_pipeline.set_state.assert_called_once_with(consumer.Gst.State.NULL)
    consumer.video_pipeline.set_state.assert_called_once_with(consumer.Gst.State.NULL)
    consumer.loop.quit.assert_called_once()


def test_setup_video_pipeline(consumer):
    mock_pipeline = Mock()
    mock_sink = Mock()
    mock_pipeline.get_by_name.return_value = mock_sink
    consumer.Gst.parse_launch.return_value = mock_pipeline

    consumer._setup_video_pipeline()

    consumer.Gst.parse_launch.assert_called_once()
    mock_sink.connect.assert_called_once_with("new-sample", consumer._on_video_sample)
    mock_pipeline.set_state.assert_called_once_with(consumer.Gst.State.PLAYING)


def test_setup_audio_pipeline(consumer):
    mock_pipeline = Mock()
    mock_sink = Mock()
    mock_pipeline.get_by_name.return_value = mock_sink
    consumer.Gst.parse_launch.return_value = mock_pipeline

    consumer._setup_audio_pipeline()

    consumer.Gst.parse_launch.assert_called_once()
    mock_sink.connect.assert_called_once_with("new-sample", consumer._on_audio_sample)
    mock_pipeline.set_state.assert_called_once_with(consumer.Gst.State.PLAYING)


def test_on_video_sample(consumer):
    mock_sink = Mock()
    mock_sample = Mock()
    mock_buffer = Mock()
    mock_caps = Mock()
    mock_structure = Mock()

    # Mock video sample data
    mock_sink.emit.return_value = mock_sample
    mock_sample.get_buffer.return_value = mock_buffer
    mock_sample.get_caps.return_value = mock_caps
    mock_caps.get_structure.return_value = mock_structure
    mock_structure.get_value.side_effect = [640, 480]  # width, height

    # Mock buffer mapping
    mock_map_info = Mock()
    mock_map_info.data = np.zeros((480, 640, 3), dtype=np.uint8).tobytes()
    mock_buffer.map.return_value = (True, mock_map_info)

    # Add event handler
    received_frame = None

    def on_data(frame):
        nonlocal received_frame
        received_frame = frame

    consumer.push_handlers(data=on_data)

    result = consumer._on_video_sample(mock_sink)

    assert result == consumer.Gst.FlowReturn.OK
    assert received_frame is not None
    assert received_frame.type == "video"
    assert isinstance(received_frame.data, np.ndarray)
    assert received_frame.data.shape == (480, 640, 3)


def test_on_audio_sample(consumer):
    mock_sink = Mock()
    mock_sample = Mock()
    mock_buffer = Mock()

    # Mock audio sample data
    mock_sink.emit.return_value = mock_sample
    mock_sample.get_buffer.return_value = mock_buffer

    # Mock buffer mapping
    mock_map_info = Mock()
    mock_map_info.data = np.zeros(1024, dtype=np.int16).tobytes()
    mock_buffer.map.return_value = (True, mock_map_info)

    # Add event handler
    received_frame = None

    def on_data(frame):
        nonlocal received_frame
        received_frame = frame

    consumer.push_handlers(data=on_data)

    result = consumer._on_audio_sample(mock_sink)

    assert result == consumer.Gst.FlowReturn.OK
    assert received_frame is not None
    assert received_frame.type == "audio"
    assert isinstance(received_frame.data, np.ndarray)
    assert received_frame.data.dtype == np.int16


def test_missing_gstreamer():
    """Test error handling when GStreamer is not available"""
    with patch.dict("sys.modules", {"gi": None}):
        with pytest.raises(RuntimeError) as excinfo:
            MediaConsumer()
        assert "GStreamer dependencies not found" in str(excinfo.value)
        assert MediaConsumer._gst_initialized is False
        assert MediaConsumer.Gst is None
        assert MediaConsumer.GLib is None
