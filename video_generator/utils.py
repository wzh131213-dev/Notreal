"""
Utility functions for video parameters validation and helper operations.
"""

from typing import Tuple


def validate_dimensions(width: int, height: int) -> Tuple[int, int]:
    """Validates and ensures width and height are positive multiples of 2."""
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")
    w = width if width % 2 == 0 else width + 1
    h = height if height % 2 == 0 else height + 1
    return w, h


def sanitize_prompt(prompt: str) -> str:
    """Sanitizes prompt text."""
    if not prompt:
        return ""
    return prompt.strip()
