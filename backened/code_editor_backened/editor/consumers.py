# consumers.py
import os
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import interactive_executor  # adjust your import as needed


class InteractiveExecConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.process = None  # The Docker process (interactive)
        self.output_task = None
        self.tmp_files = []

    async def disconnect(self, close_code):
        if self.process and self.process.returncode is None:
            self.process.kill()
        if self.output_task:
            self.output_task.cancel()
        for filepath in self.tmp_files:
            try:
                os.unlink(filepath)
            except Exception:
                pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except Exception:
            await self.send(json.dumps({"error": "Invalid JSON."}))
            return

        action = data.get("action")
        if action == "start":
            language = data.get("language", "").lower().strip()
            code = data.get("code", "")
            await self.start_session(language, code)
        elif action == "input":
            user_input = data.get("data", "")
            if self.process and self.process.stdin:
                self.process.stdin.write(user_input.encode('utf-8') + b'\n')
                await self.process.stdin.drain()
        else:
            await self.send(json.dumps({"error": "Unknown action."}))

    async def start_session(self, language, code):
        if language == "python":
            ext = "py"
        elif language == "c":
            ext = "c"
        elif language in ("cpp", "c++"):
            ext = "cpp"
        elif language == "javascript":
            ext = "js"
        else:
            await self.send(json.dumps({"error": "Unsupported language."}))
            return

        source_filepath = interactive_executor.create_temp_file(code, ext)
        self.tmp_files.append(source_filepath)
        mount_dir = os.path.dirname(source_filepath)
        
        try:
            self.process = await interactive_executor.start_interactive_docker(language, source_filepath, mount_dir)
        except Exception as e:
            await self.send(json.dumps({"error": str(e)}))
            return

        # Start reading output in chunks (32 bytes per read)
        self.output_task = asyncio.create_task(self.read_stream(self.process.stdout, "output"))
        asyncio.create_task(self.read_stream(self.process.stderr, "error"))
    
    async def read_stream(self, stream, stream_type):
        try:
            while True:
                # Read a full line to ensure we get complete messages (including our marker)
                line_bytes = await stream.readline()
                if not line_bytes:
                    break
                text = line_bytes.decode('utf-8', errors='replace')
                # Check if the line contains the explicit prompt marker.
                if text.startswith("PROMPT:"):
                    # Remove the marker from the output text.
                    message = text[len("PROMPT:"):]
                    payload = {"output": message, "prompt": "true"}
                else:
                    payload = {"output": text}
                await self.send(json.dumps(payload))
        except asyncio.CancelledError:
            pass
        except Exception as e:
            await self.send(json.dumps({"error": str(e)}))

