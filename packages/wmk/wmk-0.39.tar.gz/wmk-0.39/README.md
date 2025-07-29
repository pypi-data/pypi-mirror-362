# World Model Kit

[![PyPI](https://img.shields.io/pypi/v/wmk.svg)](https://pypi.org/project/wmk/)
[![Tests](https://github.com/journee-live/wmk/actions/workflows/test.yml/badge.svg)](https://github.com/journee-live/wmk/actions/workflows/test.yml)

**World Model Kit (WMK)** is a comprehensive toolkit designed to streamline the development, deployment, and operation of interactive world models.

### Key Features

* **High-Performance Rendering**
   Native system integration for efficient real-time visualization of world model outputs, optimized for various display environments.

* **Interactive User Interface**
   Comprehensive input processing system with support for keyboard and mouse interactions, event handling, and real-time response capabilities.

* **Extensible Architecture**
   Built on top of Pyglet, enabling easy creation of custom window classes, event handlers, and graphics components.

* **Advanced Communication Layer**
   Robust inter-process communication system featuring seamless integration with web clients and flexible message passing capabilities.

* **Media Processing**
   Built-in support for audio and video capture from PipeWire sources with real-time processing capabilities.

* **Dependency Management**
   Tools for packaging Python dependencies and project files into distributable archives with platform-specific package handling.

## Installation

```bash
pip install wmk
```

## Usage

### Interactive Display with Player

Example of using the Player and Messenger modules for interactive applications:

```python
from wmk.player import Player
from wmk.messenger import Messenger

is_user_connected = False

def handle_user_connection(message):
    nonlocal is_user_connected
    is_user_connected = True if message["type"] == "connected" else False

messenger = Messenger("/tmp/server.sock", "/tmp/client.sock")
messenger.push_handlers(connected=handle_user_connection, disconnected=handle_user_connection)

def frame_generator(window, dt):
    # Generate and return your frame here
    return frame if is_user_connected else empty_frame

player = Player(frame_generator)
player.run()

messenger.start()
```

### Media Capture with MediaConsumer

To use MediaConsumer, make sure that your system supports GStreamer, for Ubuntu install the following packages:

```
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev python3-gi libgirepository-2.0-dev libcairo2-dev
```

Install WMK with optional dependencis `media`:
```
pip install wmk[media]
```

Example of capturing audio and video from PipeWire sources:

```python
from wmk.media_consumer import MediaConsumer

def handle_media(frame):
    if frame.type == 'video':
        # Process video frame
        print(f"Received video frame: {frame.data.shape}")
    else:
        # Process audio data
        print(f"Received audio samples: {len(frame.data)}")

consumer = MediaConsumer(audio_node_id=51, video_node_id=52)
consumer.push_handlers(data=handle_media)
consumer.start()
```

### File Downloads

Using the Loader for managing file downloads:

```python
from wmk.loader import Loader

loader = Loader()

# Single file download
loader.download_file("https://example.com/file.dat", "local_file.dat")

# Multiple files in parallel
urls = {
    "https://example.com/file1.dat": "local_file1.dat",
    "https://example.com/file2.dat": "local_file2.dat"
}
results = loader.download_files(urls)
```

## Command Line Interface

WMK provides a CLI for common operations:

```bash
# Package a project
wmk package --target ./myproject --name build.zip --platform manylinux2014_x86_64

# Download a file
wmk download --url https://example.com/file.dat --filepath local_file.dat
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd wmk
python -m venv venv
source venv/bin/activate
```
And install the dependencies:
```bash
python -m pip install -e '.[test,dev]'
```
To run the tests:
```bash
python -m pytest
```
