## Overview

A lightweight Python application that streams audio from your system's default audio device to connected clients over WebSocket. Supports real-time audio transmission across devices on the same local network with minimal latency.

## Requirements

- Python 3.12 or higher

## System Requirements

- Python 3.12 or higher
- A physical audio output device (internal speakers, headphones, or a wired audio device)
    - **Note:** `pyaudiowpatch` doesn't work with Bluetooth audio devices, so you'll need to use internal speakers or wired headphones to capture audio.



## Installation

Install the required dependencies using pip:

```bash
pip install websockets pyaudiowpatch
```

## Dependencies

```python
import asyncio
import websockets
import pyaudiowpatch as pyaudio
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
```

**Note:** `asyncio`, `socket`, `threading`, and `http.server` are part of the Python standard library and do not require separate installation.

## Configuration

To listen to audio from another device, you will need to enter the PC's IP address and port number in your client configuration.

