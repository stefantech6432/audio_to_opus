#!/usr/bin/env python3
"""
Audio to Opus Converter
Converts audio files from various formats to Opus format.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional
import subprocess
import shutil


class AudioToOpusConverter:
    """Handles conversion of audio files to Opus format."""

    SUPPORTED_FORMATS = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.aiff', '.ape', '.opus'}

    def __init__(self, bitrate: int = 128, vbr: bool = True, output_dir: Optional[str] = None):
        """
        Initialize the converter.

        Args:
            bitrate: Target bitrate in kbps (default: 128)
            vbr: Use variable bitrate (default: True)
            output_dir: Output directory (default: same as input file)
        """
        self.bitrate = bitrate
        self.vbr = vbr
        self.output_dir = output_dir

        # Check if ffmpeg is available
        if not shutil.which('ffmpeg'):
            raise RuntimeError("ffmpeg is not installed or not in PATH. Please install ffmpeg.")

    def convert_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """
        Convert a single audio file to Opus format.

        Args:
            input_path: Path to input audio file
            output_path: Path to output file (optional)

        Returns:
            True if conversion was successful, False otherwise
        """
        input_file = Path(input_path)

        # Validate input file
        if not input_file.exists():
            print(f"Error: Input file '{input_path}' does not exist.", file=sys.stderr)
            return False

        if not input_file.is_file():
            print(f"Error: '{input_path}' is not a file.", file=sys.stderr)
            return False

        if input_file.suffix.lower() not in self.SUPPORTED_FORMATS:
            print(f"Warning: '{input_file.suffix}' may not be supported. Attempting conversion anyway...")

        # Determine output path
        if output_path:
            output_file = Path(output_path)
        else:
            if self.output_dir:
                output_file = Path(self.output_dir) / f"{input_file.stem}.opus"
            else:
                output_file = input_file.with_suffix('.opus')

        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Build ffmpeg command
        cmd = ['ffmpeg', '-i', str(input_file)]

        # Add codec and bitrate settings
        cmd.extend(['-c:a', 'libopus'])

        if self.vbr:
            # VBR mode with quality-based encoding
            cmd.extend(['-vbr', 'on', '-b:a', f'{self.bitrate}k'])
        else:
            # CBR mode
            cmd.extend(['-vbr', 'off', '-b:a', f'{self.bitrate}k'])

        # Add output file (overwrite if exists)
        cmd.extend(['-y', str(output_file)])

        print(f"Converting: {input_file.name} -> {output_file.name}")
        print(f"Settings: Bitrate={self.bitrate}kbps, VBR={'ON' if self.vbr else 'OFF'}")

        try:
            # Run ffmpeg
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                print(f"✓ Successfully converted: {output_file}")
                return True
            else:
                print(f"✗ Conversion failed for: {input_file.name}", file=sys.stderr)
                print(f"Error: {result.stderr}", file=sys.stderr)
                return False

        except Exception as e:
            print(f"✗ Error converting {input_file.name}: {e}", file=sys.stderr)
            return False

    def convert_files(self, input_paths: List[str]) -> tuple[int, int]:
        """
        Convert multiple audio files to Opus format.

        Args:
            input_paths: List of input file paths

        Returns:
            Tuple of (successful_count, failed_count)
        """
        successful = 0
        failed = 0

        for input_path in input_paths:
            if self.convert_file(input_path):
                successful += 1
            else:
                failed += 1
            print()  # Empty line between conversions

        return successful, failed


def main():
    """Main entry point for the converter."""
    parser = argparse.ArgumentParser(
        description='Convert audio files to Opus format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.mp3
  %(prog)s input.wav -b 192
  %(prog)s *.flac -o ./opus_files/
  %(prog)s song.mp3 -b 96 --cbr
  %(prog)s audio1.wav audio2.mp3 audio3.flac -o output/

Supported input formats:
  MP3, WAV, FLAC, M4A, AAC, OGG, WMA, AIFF, APE, OPUS
        """
    )

    parser.add_argument(
        'input_files',
        nargs='+',
        help='Input audio file(s) to convert'
    )

    parser.add_argument(
        '-o', '--output-dir',
        dest='output_dir',
        help='Output directory (default: same as input file)'
    )

    parser.add_argument(
        '-b', '--bitrate',
        type=int,
        default=128,
        help='Target bitrate in kbps (default: 128)'
    )

    parser.add_argument(
        '--cbr',
        action='store_true',
        help='Use constant bitrate instead of variable bitrate (VBR is default)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Create converter instance
    try:
        converter = AudioToOpusConverter(
            bitrate=args.bitrate,
            vbr=not args.cbr,
            output_dir=args.output_dir
        )
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Convert files
    print(f"Audio to Opus Converter")
    print(f"{'=' * 50}\n")

    successful, failed = converter.convert_files(args.input_files)

    # Print summary
    print(f"{'=' * 50}")
    print(f"Conversion complete:")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
