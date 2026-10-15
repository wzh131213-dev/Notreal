"""
Command Line Interface for Non-Production AI Video Generator.
"""

import argparse
import sys
import json
from typing import List, Optional

from .generator import VideoGenerator, GenerationConfig


def main(args: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Non-Production AI Video Generator CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'generate' command
    gen_parser = subparsers.add_parser("generate", help="Generate a video from a text prompt")
    gen_parser.add_argument("--prompt", "-p", type=str, required=True, help="Text prompt for video generation")
    gen_parser.add_argument("--output", "-o", type=str, default="output.mp4", help="Output file path (default: output.mp4)")
    gen_parser.add_argument("--provider", type=str, default="non-production", choices=["non-production", "local-mock", "huggingface"], help="Provider to use")
    gen_parser.add_argument("--duration", "-d", type=int, default=3, help="Video duration in seconds")
    gen_parser.add_argument("--fps", type=int, default=10, help="Frames per second")
    gen_parser.add_argument("--width", type=int, default=320, help="Video width in pixels")
    gen_parser.add_argument("--height", type=int, default=240, help="Video height in pixels")
    gen_parser.add_argument("--json", action="store_true", help="Output result as JSON string")

    # 'list-providers' command
    list_parser = subparsers.add_parser("list-providers", help="List available non-production AI providers")

    parsed = parser.parse_args(args)

    if not parsed.command or parsed.command == "generate":
        if not hasattr(parsed, "prompt") or not parsed.prompt:
            parser.print_help()
            return 1

        try:
            generator = VideoGenerator(provider_name=parsed.provider)
            config = GenerationConfig(
                prompt=parsed.prompt,
                output_path=parsed.output,
                duration=parsed.duration,
                fps=parsed.fps,
                width=parsed.width,
                height=parsed.height
            )
            job = generator.generate(config)

            if parsed.json:
                res_data = {
                    "job_id": job.job_id,
                    "status": job.status,
                    "output_path": job.output_path,
                    "provider": job.provider,
                    "metadata": job.metadata
                }
                print(json.dumps(res_data, indent=2))
            else:
                print(f"[SUCCESS] Video AI Generation complete!")
                print(f"  Job ID:      {job.job_id}")
                print(f"  Provider:    {job.provider}")
                print(f"  Output Path: {job.output_path}")
                print(f"  Status:      {job.status}")
            return 0
        except Exception as e:
            print(f"[ERROR] Failed to generate video: {e}", file=sys.stderr)
            return 1

    elif parsed.command == "list-providers":
        print("Available Non-Production AI Video Providers:")
        for name, cls in VideoGenerator.PROVIDERS.items():
            inst = cls()
            print(f"  - {name:<16} (Production: {inst.is_production}, Class: {cls.__name__})")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
