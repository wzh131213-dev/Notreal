import os
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from video_generator.executor import CodeVideoExecutor

app = FastAPI(
    title="AI Code-Based Video Generation Web API",
    description="Generates cinematic videos via AI-generated python code.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = CodeVideoExecutor(output_dir="static/videos")

class GenerateRequest(BaseModel):
    prompt: str = Field(..., example="Cyberpunk city with glowing neon rain")
    aspect_ratio: str = Field(default="16:9", example="16:9")
    duration: float = Field(default=4.0, ge=1.0, le=15.0)
    fps: int = Field(default=30, ge=10, le=60)
    resolution: str = Field(default="720p", example="720p")
    custom_code: Optional[str] = None

# Mount static files directory
os.makedirs("static/videos", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>AI Video Generator Backend is running!</h1>"

@app.post("/api/generate")
async def generate_video(req: GenerateRequest):
    """
    Generate video from prompt or code using AI code renderer.
    """
    if not req.prompt and not req.custom_code:
        raise HTTPException(status_code=400, detail="Prompt or custom_code is required.")

    result = executor.generate_and_execute(
        prompt=req.prompt,
        aspect_ratio=req.aspect_ratio,
        duration=req.duration,
        fps=req.fps,
        resolution=req.resolution,
        custom_code=req.custom_code
    )
    return result

@app.get("/api/history")
async def get_history():
    """
    Retrieve history list of generated AI videos.
    """
    return executor.get_history()

@app.get("/api/videos/{video_id}")
async def get_video_info(video_id: str):
    """
    Retrieve specific video record info.
    """
    history = executor.get_history()
    for item in history:
        if item["id"] == video_id:
            return item
    raise HTTPException(status_code=404, detail="Video not found.")

@app.get("/api/code/{video_id}")
async def get_video_code(video_id: str):
    """
    Get the AI-generated python code that created the video.
    """
    history = executor.get_history()
    for item in history:
        if item["id"] == video_id:
            return {"id": video_id, "prompt": item["prompt"], "code": item["code"]}
    raise HTTPException(status_code=404, detail="Video code not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
