## Requirements

Python 3.12 or higher

## Installation

Install the required dependencies:

```bash
pip install websockets pyaudiowpatch
```

## Required Libraries

```python
import asyncio
import websockets
import pyaudiowpatch as pyaudio
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
```

**Note:** `asyncio`, `socket`, `threading`, and `http.server` are included with Python by default.