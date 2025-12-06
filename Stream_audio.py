import asyncio
import websockets
import pyaudiowpatch as pyaudio
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


HTTP_PORT = 8000
WS_PORT = 8765
CHUNK = 384          
RATE = 48000        

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

LOCAL_IP = get_local_ip()

HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Low Latency Audio</title>
    <style>
        body {{ background-color: #111; color: #fff; font-family: monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
        button {{ background: #ff4757; color: white; border: none; padding: 20px 40px; font-size: 1.5rem; border-radius: 10px; cursor: pointer; }}
        #status {{ margin-top: 20px; color: #aaa; }}
    </style>
</head>
<body>
    <h1>Audio Stream</h1>
    <button id="playBtn">START STREAMING</button>
    <div id="status">Ready</div>

    <script>
        const WS_URL = "ws://{LOCAL_IP}:{WS_PORT}";
        let audioCtx;
        let ws;
        let nextTime = 0;
        

        const BUFFER_TOLERANCE = 0.04; 

        document.getElementById('playBtn').addEventListener('click', async () => {{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)({{ 
                sampleRate: {RATE},
                latencyHint: 'interactive'  // Request lowest latency from browser
            }});
            if (audioCtx.state === 'suspended') await audioCtx.resume();
            connectWebSocket();
        }});

        function connectWebSocket() {{
            ws = new WebSocket(WS_URL);
            ws.binaryType = 'arraybuffer';
            const status = document.getElementById('status');

            ws.onopen = () => status.innerText = "LIVE";
            
            ws.onmessage = (event) => {{
                const arrayBuffer = event.data;
                const int16Data = new Int16Array(arrayBuffer);
                const float32Data = new Float32Array(int16Data.length);
                
                // Convert PCM Int16 to Float32
                for (let i = 0; i < int16Data.length; i++) {{
                    float32Data[i] = int16Data[i] / 32768;
                }}

                const buffer = audioCtx.createBuffer(2, float32Data.length / 2, {RATE});
                const ch0 = buffer.getChannelData(0);
                const ch1 = buffer.getChannelData(1);
                for (let i = 0; i < buffer.length; i++) {{
                    ch0[i] = float32Data[i * 2];
                    ch1[i] = float32Data[i * 2 + 1];
                }}

                const source = audioCtx.createBufferSource();
                source.buffer = buffer;
                source.connect(audioCtx.destination);

                // --- THE ULTRA LOW LATENCY MAGIC ---
                // If the scheduled time is in the past, reset it to "now"
                if (nextTime < audioCtx.currentTime) {{
                    nextTime = audioCtx.currentTime;
                }}
                
                // If the scheduled time is too far in the future (lag accumulation),
                // snap it back to "now" + tiny buffer. This drops old audio.
                if (nextTime > audioCtx.currentTime + BUFFER_TOLERANCE) {{
                    // Skip stale audio to stay live
                    nextTime = audioCtx.currentTime + 0.015;
                }}

                source.start(nextTime);
                nextTime += buffer.duration;
            }};
        }}
    </script>
</body>
</html>
"""

class SimpleHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))
    def log_message(self, format, *args): pass

def run_http_server():
    server = HTTPServer(('0.0.0.0', HTTP_PORT), SimpleHTTPHandler)
    server.serve_forever()

async def audio_stream(websocket):
    p = pyaudio.PyAudio()
    try:
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
        

        stream = p.open(format=pyaudio.paInt16,
                        channels=2, 
                        rate=RATE,
                        input=True,
                        input_device_index=default_speakers["index"],
                        frames_per_buffer=CHUNK,
                        stream_callback=None)  
        
        print(f"Streaming Ultra Low Latency from: {default_speakers['name']}")

        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            await websocket.send(data)
            await asyncio.sleep(0)

    except Exception:
        pass
    finally:
        if 'stream' in locals(): stream.stop_stream(); stream.close()
        p.terminate()

async def main():
    threading.Thread(target=run_http_server, daemon=True).start()
    print(f"\n⚡ LOW LATENCY SERVER: http://{LOCAL_IP}:{HTTP_PORT}\n")
    async with websockets.serve(audio_stream, "0.0.0.0", WS_PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())