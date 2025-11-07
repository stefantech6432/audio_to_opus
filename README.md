# Audio to Opus Converter

A Python-based audio converter that converts various audio formats to Opus format using ffmpeg. Available in two versions: a simple standalone version and an optimized parallel-processing version.

## Available Versions

### Version 1: `audio_to_opus.py` (Simple)
- ✅ **Zero Python dependencies** (uses only standard library)
- ✅ Simple and straightforward
- ✅ Best for quick conversions and simple use cases
- ⚠️ Sequential processing (one file at a time)

### Version 2: `audio_to_opus_v2.py` (Optimized) ⭐ **Recommended**
- ✅ **Parallel processing** for much faster batch conversions
- ✅ **File size comparison** and compression statistics
- ✅ **Performance timing** to measure speed gains
- ✅ Multi-core CPU utilization
- ✅ Detailed conversion summary
- 📦 Requires `ffmpeg-python` package

## Features

- **Multiple Format Support**: Convert from MP3, WAV, FLAC, M4A, AAC, OGG, WMA, AIFF, APE, and more
- **Flexible Encoding**: Choose between VBR (Variable Bitrate) and CBR (Constant Bitrate) encoding
- **Configurable Bitrate**: Set custom bitrate from low to high quality
- **Batch Processing**: Convert multiple files at once
- **Simple CLI**: Easy-to-use command-line interface
- **Parallel Processing** (v2 only): Utilize all CPU cores for faster conversions

## Requirements

### System Requirements
- **Python 3.6+**
- **ffmpeg** (must be installed separately)

### Python Package Requirements
- **Version 1** (`audio_to_opus.py`): No additional packages needed
- **Version 2** (`audio_to_opus_v2.py`): Requires `ffmpeg-python`

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

2. Install Python dependencies (for v2 only):
```bash
pip install -r requirements.txt
```

3. Make the scripts executable (Linux/macOS):
```bash
chmod +x audio_to_opus.py
chmod +x audio_to_opus_v2.py
```

## Usage

### Quick Start

**Version 1 (Simple):**
```bash
python audio_to_opus.py input.mp3
```

**Version 2 (Optimized, Recommended):**
```bash
python audio_to_opus_v2.py input.mp3
```

### Command-Line Options

Both versions support similar options:

```bash
python audio_to_opus_v2.py [OPTIONS] INPUT_FILES...
```

**Common Options:**
- `-o, --output-dir DIR` : Specify output directory (default: same as input)
- `-b, --bitrate KBPS` : Set target bitrate in kbps (default: 128)
- `--cbr` : Use constant bitrate instead of variable bitrate
- `--version` : Show version information
- `-h, --help` : Show help message

**Version 2 Exclusive Options:**
- `-j, --jobs N` : Number of parallel workers (default: CPU count)
- `--delete-original` : Delete original files after successful conversion

### Examples

**Convert with custom bitrate:**
```bash
python audio_to_opus_v2.py song.mp3 -b 192
```

**Convert multiple files (parallel processing in v2):**
```bash
python audio_to_opus_v2.py song1.mp3 song2.wav song3.flac
```

**Convert all FLAC files with 8 parallel workers:**
```bash
python audio_to_opus_v2.py *.flac -j 8
```

**Specify output directory:**
```bash
python audio_to_opus_v2.py *.mp3 -o ./converted/
```

**High-quality conversion with 4 workers:**
```bash
python audio_to_opus_v2.py *.flac -b 256 -j 4
```

**Convert and delete originals (use with caution!):**
```bash
python audio_to_opus_v2.py *.mp3 --delete-original
```

### Performance Comparison

For batch conversions, **Version 2 is significantly faster**:

**Example: Converting 100 MP3 files**
- Version 1 (sequential): ~10 minutes
- Version 2 (8 cores): ~2-3 minutes

The exact speedup depends on your CPU core count and file sizes.

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

## Which Version Should I Use?

**Use Version 2 (`audio_to_opus_v2.py`) if:**
- ✅ You're converting multiple files or large batches
- ✅ You want the fastest conversion times
- ✅ You want to see file size comparisons and statistics
- ✅ You have a multi-core CPU
- ✅ You can install Python packages (`ffmpeg-python`)

**Use Version 1 (`audio_to_opus.py`) if:**
- ✅ You need a zero-dependency solution
- ✅ You're converting just a few files
- ✅ You're running in a restricted environment
- ✅ You prefer simplicity over speed

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
