"""
Video Generator Package for Non-Production Video AI Generation.
"""

from .generator import VideoGenerator, GenerationConfig, VideoJob
from .providers import BaseProvider, NonProductionProvider, LocalMockProvider, HuggingFaceInferenceProvider

__version__ = "0.1.0"
__all__ = [
    "VideoGenerator",
    "GenerationConfig",
    "VideoJob",
    "BaseProvider",
    "NonProductionProvider",
    "LocalMockProvider",
    "HuggingFaceInferenceProvider",
]
