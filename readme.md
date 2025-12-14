## Overview

A lightweight Python application that streams audio from your system's default audio device to connected clients over WebSocket. Supports real-time audio transmission across devices on the same local network with minimal latency.

## Requirements

- Python 3.12 or higher

**Note:** The `pyaudiowpatch` library currently supports Python up to version 3.12(as of December 2025) Use Python 3.12 for optimal compatibility. and choose internal audio like the speakers in a laptop to play the audio then only the ppyaudiowatch can capture the audio, it will not work if you have connected to a bluetooth speaker. you can also plug a headphone and it will work, as long as physical speaker devices are connected then it will work. in HP laptop realtek audio supported speakers work(which are essentially the internal speaker and attatched headphones)

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

