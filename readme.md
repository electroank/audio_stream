## Overview

A lightweight Python application that streams audio from your system's default audio device to connected clients over WebSocket. Supports real-time audio transmission across devices on the same local network with minimal latency.

## Requirements

- Python 3.12 or higher

**Note:** The `pyaudiowpatch` library currently supports Python up to version 3.12. Use Python 3.12 for optimal compatibility.

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

