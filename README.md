# Non-Production Video AI Generator

A Python SDK and Command Line Interface (CLI) for generating videos via non-production and open-source AI video providers. Designed for staging, testing, prototyping, and non-cost sandbox environments.

## Features

- **Non-Production Provider (`non-production`)**: Simulates AI video synthesis for staging and preview pipelines without incurring production API costs.
- **Local Mock Provider (`local-mock`)**: Ultra-fast provider for local testing and offline CI/CD pipelines.
- **HuggingFace Inference Provider (`huggingface`)**: Interfaces with non-production open models on HuggingFace Hub.
- **Python SDK**: Simple and flexible API for programmatic video generation.
- **CLI Support**: Command line tool for easy integration into shell scripts.

## Installation & Setup

```bash
# Clone the repository
git clone <repo-url>
cd <repo-dir>

# (Optional) Install in editable mode
pip install -e .
```

## Python SDK Quickstart

```python
from video_generator import VideoGenerator, GenerationConfig

# Initialize generator with non-production provider
generator = VideoGenerator(provider_name="non-production")

# Generate video from prompt
job = generator.generate_from_prompt(
    prompt="A serene sunset over a digital ocean",
    output_path="outputs/sunset.mp4",
    duration=5,
    fps=12
)

print(f"Generated Video Job ID: {job.job_id}")
print(f"Status: {job.status}")
print(f"Saved to: {job.output_path}")
```

## CLI Usage

### List Available Providers

```bash
python3 -m video_generator.cli list-providers
```

### Generate Video

```bash
python3 -m video_generator.cli generate \
  --prompt "A astronaut walking on Mars" \
  --output "mars.mp4" \
  --provider "non-production" \
  --duration 4 \
  --json
```

## Testing

Run unit tests using Python's standard `unittest` framework:

```bash
python3 -m unittest discover -s tests
```

## License

MIT
