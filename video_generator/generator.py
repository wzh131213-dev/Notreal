"""
Core Video Generator Manager and Config Classes.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import os

from .providers import BaseProvider, NonProductionProvider, LocalMockProvider, HuggingFaceInferenceProvider


@dataclass
class GenerationConfig:
    prompt: str
    duration: int = 3
    fps: int = 10
    width: int = 320
    height: int = 240
    output_path: str = "output_video.mp4"
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VideoJob:
    job_id: str
    status: str
    output_path: str
    provider: str
    metadata: Dict[str, Any]


class VideoGenerator:
    """Main client class for generating video using non-production AI providers."""

    PROVIDERS = {
        "non-production": NonProductionProvider,
        "local-mock": LocalMockProvider,
        "huggingface": HuggingFaceInferenceProvider,
    }

    def __init__(self, provider_name: str = "non-production", provider_instance: Optional[BaseProvider] = None):
        if provider_instance:
            self.provider = provider_instance
        else:
            provider_cls = self.PROVIDERS.get(provider_name.lower())
            if not provider_cls:
                raise ValueError(f"Unknown provider '{provider_name}'. Available providers: {list(self.PROVIDERS.keys())}")
            self.provider = provider_cls()

    def generate(self, config: GenerationConfig) -> VideoJob:
        """
        Generate a video given a GenerationConfig object.
        """
        if not config.prompt or not config.prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        res = self.provider.generate(
            prompt=config.prompt,
            duration=config.duration,
            fps=config.fps,
            width=config.width,
            height=config.height,
            output_path=config.output_path,
            **config.extra_params
        )

        return VideoJob(
            job_id=res.get("job_id", "unknown"),
            status=res.get("status", "completed"),
            output_path=res.get("output_path", config.output_path),
            provider=res.get("provider", self.provider.name),
            metadata=res.get("metadata", {})
        )

    def generate_from_prompt(
        self,
        prompt: str,
        output_path: str = "output.mp4",
        duration: int = 3,
        fps: int = 10,
        width: int = 320,
        height: int = 240
    ) -> VideoJob:
        """Convenience method to generate video directly from prompt string."""
        config = GenerationConfig(
            prompt=prompt,
            output_path=output_path,
            duration=duration,
            fps=fps,
            width=width,
            height=height
        )
        return self.generate(config)
