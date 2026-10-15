"""
AI Video Generation Provider Implementations for Non-Production & Sandbox Environments.
"""

from abc import ABC, abstractmethod
import time
import os
import json
import uuid
from typing import Dict, Any, Optional

class BaseProvider(ABC):
    """Abstract base class for video generation providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_production(self) -> bool:
        """Indicates whether this provider is for production or non-production/testing."""
        pass

    @abstractmethod
    def generate(self, prompt: str, duration: int, fps: int, width: int, height: int, output_path: str, **kwargs) -> Dict[str, Any]:
        """
        Initiates or completes video generation.
        Returns metadata dict containing job_id, status, output_path, provider info, etc.
        """
        pass


class NonProductionProvider(BaseProvider):
    """
    Standard non-production video AI provider for staging/testing/preview.
    Generates simulated video files or animated GIF previews without incurring API costs.
    """

    @property
    def name(self) -> str:
        return "non-production-ai"

    @property
    def is_production(self) -> bool:
        return False

    def generate(self, prompt: str, duration: int = 3, fps: int = 10, width: int = 320, height: int = 240, output_path: str = "output.mp4", **kwargs) -> Dict[str, Any]:
        job_id = f"nonprod-{uuid.uuid4().hex[:8]}"
        start_time = time.time()

        # Simulate video synthesis by creating a mock file with metadata header or fallback format
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        meta = {
            "job_id": job_id,
            "provider": self.name,
            "environment": "non-production",
            "prompt": prompt,
            "duration": duration,
            "fps": fps,
            "resolution": f"{width}x{height}",
            "created_at": time.time(),
            "status": "completed"
        }

        # Write dummy binary/json content to output_path to simulate output video artifact
        with open(output_path, "wb") as f:
            f.write(b"SIMULATED_NON_PRODUCTION_VIDEO_HEADER\n")
            f.write(json.dumps(meta, indent=2).encode("utf-8"))

        return {
            "job_id": job_id,
            "status": "completed",
            "output_path": output_path,
            "provider": self.name,
            "duration_seconds": round(time.time() - start_time, 3),
            "metadata": meta
        }


class LocalMockProvider(BaseProvider):
    """Local offline provider for fast unit testing and offline development."""

    @property
    def name(self) -> str:
        return "local-mock"

    @property
    def is_production(self) -> bool:
        return False

    def generate(self, prompt: str, duration: int = 2, fps: int = 5, width: int = 160, height: int = 120, output_path: str = "mock_output.mp4", **kwargs) -> Dict[str, Any]:
        job_id = f"mock-{uuid.uuid4().hex[:8]}"
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        meta = {
            "job_id": job_id,
            "provider": self.name,
            "prompt": prompt,
            "status": "completed"
        }

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Mock Video Content for prompt: {prompt}\n")

        return {
            "job_id": job_id,
            "status": "completed",
            "output_path": output_path,
            "provider": self.name,
            "metadata": meta
        }


class HuggingFaceInferenceProvider(BaseProvider):
    """Non-production community provider targeting free/open inference endpoints on HuggingFace Hub."""

    def __init__(self, api_token: Optional[str] = None, model_id: str = "damo-vilab/text-to-video-ms-1.7b"):
        self.api_token = api_token or os.environ.get("HF_API_TOKEN")
        self.model_id = model_id

    @property
    def name(self) -> str:
        return "huggingface-inference"

    @property
    def is_production(self) -> bool:
        return False

    def generate(self, prompt: str, duration: int = 3, fps: int = 8, width: int = 256, height: int = 256, output_path: str = "hf_output.mp4", **kwargs) -> Dict[str, Any]:
        job_id = f"hf-{uuid.uuid4().hex[:8]}"
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        meta = {
            "job_id": job_id,
            "provider": self.name,
            "model_id": self.model_id,
            "prompt": prompt,
            "authenticated": self.api_token is not None,
            "status": "completed"
        }

        with open(output_path, "wb") as f:
            f.write(f"HF_INFERENCE_SIMULATED_VIDEO_{self.model_id}\n".encode("utf-8"))
            f.write(json.dumps(meta).encode("utf-8"))

        return {
            "job_id": job_id,
            "status": "completed",
            "output_path": output_path,
            "provider": self.name,
            "metadata": meta
        }
