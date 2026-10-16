#!/usr/bin/env python3
"""
Audio to LRC Converter using Google GenAI / Gemma API.
Converts MP3 audio files into LRC lyrics format with timestamps.
"""

import argparse
import os
import sys
from typing import Optional
from google import genai
from google.genai import types


LRC_PROMPT = """You are an accurate audio transcription assistant specialized in synchronized LRC lyric generation.
Please transcribe the audio from the provided file into LRC format.

Strict requirements:
1. Output format must strictly follow LRC format: [mm:ss.xx] Lyric text line by line.
2. Ensure timestamp Accuracy matches the speech/singing timing in the audio.
3. Output ONLY the LRC lyrics content. Do NOT include markdown formatting like ```lrc or any introductory/explanatory text.
"""


class AudioToLRCConverter:
    """Converter class for transforming audio files (MP3) to LRC format using Google GenAI API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        """
        Initialize the converter with API key and model.

        Args:
            api_key: Optional Google GenAI API key. If not provided,
                     will use GEMINI_API_KEY or GEMMA_API_KEY environment variable.
            model: Gemini / Gemma model name to use.
        """
        resolved_api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GEMMA_API_KEY")
        if not resolved_api_key:
            # Note: client initialization will raise error or work if default credentials exist
            self.client = genai.Client()
        else:
            self.client = genai.Client(api_key=resolved_api_key)

        self.model = model

    def convert_file(self, mp3_filepath: str, output_lrc_filepath: Optional[str] = None) -> str:
        """
        Convert an MP3 file to LRC format and optionally save to an LRC file.

        Args:
            mp3_filepath: Path to the input MP3 audio file.
            output_lrc_filepath: Path to save the resulting LRC file. If None, derives from input filepath.

        Returns:
            The LRC formatted string.
        """
        if not os.path.exists(mp3_filepath):
            raise FileNotFoundError(f"Input audio file not found: {mp3_filepath}")

        with open(mp3_filepath, "rb") as f:
            audio_bytes = f.read()

        mime_type = "audio/mp3"
        if mp3_filepath.lower().endswith(".mp3"):
            mime_type = "audio/mp3"
        elif mp3_filepath.lower().endswith(".wav"):
            mime_type = "audio/wav"
        elif mp3_filepath.lower().endswith(".ogg"):
            mime_type = "audio/ogg"
        elif mp3_filepath.lower().endswith(".m4a"):
            mime_type = "audio/m4a"

        audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type=mime_type
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=[audio_part, LRC_PROMPT]
        )

        lrc_text = response.text or ""
        cleaned_lrc = self._clean_lrc_output(lrc_text)

        if output_lrc_filepath is None:
            base, _ = os.path.splitext(mp3_filepath)
            output_lrc_filepath = f"{base}.lrc"

        with open(output_lrc_filepath, "w", encoding="utf-8") as f:
            f.write(cleaned_lrc)

        return cleaned_lrc

    @staticmethod
    def _clean_lrc_output(text: str) -> str:
        """Clean markdown code fences or extraneous tags from model output."""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()
        return cleaned


def main():
    parser = argparse.ArgumentParser(
        description="Convert MP3 audio file into LRC lyrics file using Google Gemma/Gemini API."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to input MP3 audio file"
    )
    parser.add_argument(
        "-o", "--output", help="Path to output LRC file (optional, defaults to <input_name>.lrc)"
    )
    parser.add_argument(
        "-m", "--model", default="gemini-2.5-flash", help="Model name (default: gemini-2.5-flash)"
    )
    parser.add_argument(
        "-k", "--api-key", help="Google GenAI API Key (optional, defaults to GEMINI_API_KEY or GEMMA_API_KEY env var)"
    )

    args = parser.parse_args()

    try:
        converter = AudioToLRCConverter(api_key=args.api_key, model=args.model)
        lrc_content = converter.convert_file(args.input, args.output)
        out_path = args.output or f"{os.path.splitext(args.input)[0]}.lrc"
        print(f"Successfully converted '{args.input}' -> '{out_path}'")
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
