import os
import sys
import json
import uuid
import time
import traceback
import tempfile
from typing import Dict, Any, List, Optional
from video_generator.ai_coder import AICodeGenerator

HISTORY_FILE = os.path.join("output", "history.json")

class CodeVideoExecutor:
    """
    Executes AI-generated video Python scripts safely and manages video generation history.
    """

    def __init__(self, output_dir: str = "static/videos"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs("output", exist_ok=True)
        self.ai_coder = AICodeGenerator()
        self._init_history()

    def _init_history(self):
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def get_history(self) -> List[Dict[str, Any]]:
        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading history file: {e}")
        return []

    def save_history_item(self, item: Dict[str, Any]):
        history = self.get_history()
        history.insert(0, item) # Newest first
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def parse_dimensions(self, aspect_ratio: str, resolution: str) -> tuple[int, int]:
        # Base scale
        if resolution == "1080p":
            base = 1080
        elif resolution == "480p":
            base = 480
        else: # 720p default
            base = 720

        if aspect_ratio == "9:16": # Vertical Mobile
            width = int(base * 9 / 16)
            height = base
        elif aspect_ratio == "1:1": # Square
            width = base
            height = base
        else: # 16:9 Widescreen
            width = int(base * 16 / 9)
            height = base

        # Ensure dimensions are even (FFmpeg / OpenCV requirement)
        width = width if width % 2 == 0 else width + 1
        height = height if height % 2 == 0 else height + 1
        return width, height

    def generate_and_execute(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        duration: float = 4.0,
        fps: int = 30,
        resolution: str = "720p",
        custom_code: Optional[str] = None
    ) -> Dict[str, Any]:
        video_id = str(uuid.uuid4())
        width, height = self.parse_dimensions(aspect_ratio, resolution)
        video_filename = f"{video_id}.mp4"
        video_path = os.path.join(self.output_dir, video_filename)

        start_time = time.time()
        status = "processing"
        logs = []

        logs.append(f"Analyzing prompt: '{prompt}'")
        logs.append(f"Target Video Specs: {width}x{height} @ {fps}fps, Duration: {duration}s")

        # Step 1: Generate Code (or use custom supplied code)
        if custom_code and custom_code.strip():
            code = custom_code
            logs.append("Using user-provided Python script.")
        else:
            logs.append("Synthesizing Python video rendering code...")
            code = self.ai_coder.generate_code(
                prompt=prompt,
                width=width,
                height=height,
                duration=duration,
                fps=fps
            )
            logs.append("AI Code successfully synthesized!")

        # Step 2: Execute Code safely
        exec_scope = {}
        error_msg = None

        try:
            logs.append("Compiling and executing video rendering code...")
            exec(code, exec_scope)

            if "render_video" in exec_scope:
                render_fn = exec_scope["render_video"]
                render_fn(output_path=video_path, width=width, height=height, duration=duration, fps=fps)
                status = "completed"
                logs.append(f"Video rendering finished! File saved to {video_path}")
            else:
                status = "failed"
                error_msg = "Function 'render_video' not found in generated script."
                logs.append(f"Execution Error: {error_msg}")
        except Exception as e:
            status = "failed"
            error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            logs.append(f"Runtime Exception during video rendering: {error_msg}")

        elapsed_time = round(time.time() - start_time, 2)

        result_item = {
            "id": video_id,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "fps": fps,
            "resolution": resolution,
            "width": width,
            "height": height,
            "code": code,
            "video_url": f"/static/videos/{video_filename}" if status == "completed" else None,
            "status": status,
            "error": error_msg,
            "logs": logs,
            "elapsed_seconds": elapsed_time,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        if status == "completed":
            self.save_history_item(result_item)

        return result_item
