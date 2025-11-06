# Audio to Opus Converter

A simple and efficient Python-based audio converter that converts various audio formats to Opus format using ffmpeg.

## Features

- **Multiple Format Support**: Convert from MP3, WAV, FLAC, M4A, AAC, OGG, WMA, AIFF, APE, and more
- **Flexible Encoding**: Choose between VBR (Variable Bitrate) and CBR (Constant Bitrate) encoding
- **Configurable Bitrate**: Set custom bitrate from low to high quality
- **Batch Processing**: Convert multiple files at once
- **Simple CLI**: Easy-to-use command-line interface
- **No Python Dependencies**: Uses only Python standard library

## Requirements

- **Python 3.6+**
- **ffmpeg** (must be installed separately)

### Installing ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd audio_to_opus
```

2. Make the script executable (Linux/macOS):
```bash
chmod +x audio_to_opus.py
```

## Usage

### Basic Usage

Convert a single file:
```bash
python audio_to_opus.py input.mp3
```

### Advanced Options

```bash
python audio_to_opus.py [OPTIONS] INPUT_FILES...
```

**Options:**
- `-o, --output-dir DIR` : Specify output directory (default: same as input)
- `-b, --bitrate KBPS` : Set target bitrate in kbps (default: 128)
- `--cbr` : Use constant bitrate instead of variable bitrate
- `--version` : Show version information
- `-h, --help` : Show help message

### Examples

**Convert with custom bitrate:**
```bash
python audio_to_opus.py song.mp3 -b 192
```

**Convert multiple files:**
```bash
python audio_to_opus.py song1.mp3 song2.wav song3.flac
```

**Convert all FLAC files in current directory:**
```bash
python audio_to_opus.py *.flac
```

**Specify output directory:**
```bash
python audio_to_opus.py *.mp3 -o ./converted/
```

**Use constant bitrate (CBR):**
```bash
python audio_to_opus.py input.wav -b 96 --cbr
```

**High-quality conversion:**
```bash
python audio_to_opus.py input.flac -b 256
```

## Supported Input Formats

- MP3 (`.mp3`)
- WAV (`.wav`)
- FLAC (`.flac`)
- M4A (`.m4a`)
- AAC (`.aac`)
- OGG Vorbis (`.ogg`)
- WMA (`.wma`)
- AIFF (`.aiff`)
- APE (`.ape`)
- OPUS (`.opus`) - for re-encoding

## Bitrate Recommendations

- **64 kbps**: Low quality, good for voice/podcasts
- **96 kbps**: Acceptable quality for general listening
- **128 kbps**: Good quality (default)
- **160 kbps**: Very good quality
- **192 kbps**: High quality
- **256 kbps**: Very high quality, near-transparent

## About Opus Format

Opus is a lossy audio coding format developed by the Xiph.Org Foundation and standardized by the IETF. It offers:

- **Superior quality** at lower bitrates compared to MP3
- **Low latency** suitable for real-time applications
- **Wide range** of bitrates (6-510 kbps)
- **Good compression** efficiency
- **Open and royalty-free**

## License

This project is provided as-is for educational and practical use.

## Troubleshooting

**"ffmpeg is not installed or not in PATH"**
- Make sure ffmpeg is installed and accessible from command line
- Test by running `ffmpeg -version`

**Conversion fails for certain files**
- Verify the input file is not corrupted
- Check that the file format is supported by ffmpeg
- Try with different encoding settings

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
