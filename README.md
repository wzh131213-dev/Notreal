# Audio to LRC Converter (ChatGPT3 Branch)

A Python tool that connects to Google's GenAI / Gemma API to read MP3 (and other audio) files and automatically convert them into synchronized LRC lyric files.

## Features

- Supports MP3 (and WAV, OGG, M4A) input files.
- Communicates with Google's GenAI / Gemma models to transcribe audio into LRC timestamp format (`[mm:ss.xx] lyric line`).
- Command-Line Interface (CLI) and Python API usage.
- Flexible API key configuration via environment variables or command-line parameters.

## Installation

Install the required dependencies:

```bash
pip install google-genai
```

## Usage

### Command Line Interface

Set your Gemini/Gemma API key in the environment:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or run directly passing the API key via arguments:

```bash
python3 audio_to_lrc.py -i song.mp3 -o song.lrc --api-key "your-api-key-here"
```

Arguments:
- `-i`, `--input`: Path to the input MP3 file (required)
- `-o`, `--output`: Path to the output LRC file (optional, defaults to `<input_name>.lrc`)
- `-m`, `--model`: Model name to use (defaults to `gemini-2.5-flash`)
- `-k`, `--api-key`: Google GenAI API key (optional)

### Python API

```python
from audio_to_lrc import AudioToLRCConverter

converter = AudioToLRCConverter(api_key="your-api-key-here")
lrc_content = converter.convert_file("sample.mp3", "sample.lrc")
print(lrc_content)
```

## Running Tests

Run unit tests using Python's `unittest`:

```bash
python3 -m unittest discover
```
