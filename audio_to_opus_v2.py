#!/usr/bin/env python3
"""
Audio to Opus Converter (Optimized Version)
Converts audio files from various formats to Opus format with parallel processing.

This version combines:
- Parallel processing for faster batch conversions
- File size comparison statistics
- Flexible CLI interface
- Multiple format support
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import shutil

try:
    import ffmpeg
except ImportError:
    print("Error: ffmpeg-python is not installed.", file=sys.stderr)
    print("Install it with: pip install ffmpeg-python", file=sys.stderr)
    sys.exit(1)


class ConversionStats:
    """Tracks conversion statistics."""

    def __init__(self):
        self.successful = 0
        self.failed = 0
        self.total_input_size = 0.0
        self.total_output_size = 0.0
        self.file_details = []

    def add_success(self, input_size: float, output_size: float, input_name: str, output_name: str):
        """Add successful conversion statistics."""
        self.successful += 1
        self.total_input_size += input_size
        self.total_output_size += output_size
        self.file_details.append({
            'input': input_name,
            'output': output_name,
            'input_size': input_size,
            'output_size': output_size,
            'saved': input_size - output_size
        })

    def add_failure(self):
        """Add failed conversion count."""
        self.failed += 1

    def print_summary(self, elapsed_time: float):
        """Print conversion summary."""
        print(f"\n{'=' * 70}")
        print("CONVERSION SUMMARY")
        print(f"{'=' * 70}")
        print(f"Total files processed: {self.successful + self.failed}")
        print(f"  ✓ Successful: {self.successful}")
        print(f"  ✗ Failed: {self.failed}")

        if self.successful > 0:
            print(f"\nSize Analysis:")
            print(f"  Original size: {self.total_input_size:.2f} MB")
            print(f"  Converted size: {self.total_output_size:.2f} MB")
            saved = self.total_input_size - self.total_output_size
            if self.total_input_size > 0:
                percent = (saved / self.total_input_size) * 100
                print(f"  Space saved: {saved:.2f} MB ({percent:.1f}%)")

        print(f"\nPerformance:")
        print(f"  Time elapsed: {elapsed_time:.2f} seconds")
        if self.successful > 0:
            print(f"  Average per file: {elapsed_time / self.successful:.2f} seconds")
        print(f"{'=' * 70}")


class AudioToOpusConverter:
    """Handles conversion of audio files to Opus format with parallel processing."""

    SUPPORTED_FORMATS = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.aiff', '.ape', '.opus'}

    def __init__(
        self,
        bitrate: int = 128,
        vbr: bool = True,
        output_dir: Optional[str] = None,
        delete_original: bool = False,
        workers: Optional[int] = None
    ):
        """
        Initialize the converter.

        Args:
            bitrate: Target bitrate in kbps (default: 128)
            vbr: Use variable bitrate (default: True)
            output_dir: Output directory (default: same as input file)
            delete_original: Delete original files after successful conversion
            workers: Number of parallel workers (default: CPU count)
        """
        self.bitrate = bitrate
        self.vbr = vbr
        self.output_dir = output_dir
        self.delete_original = delete_original
        self.workers = workers or os.cpu_count()

        # Check if ffmpeg is available
        if not shutil.which('ffmpeg'):
            raise RuntimeError("ffmpeg is not installed or not in PATH. Please install ffmpeg.")

    def convert_file(self, input_path: str) -> Tuple[bool, Optional[dict]]:
        """
        Convert a single audio file to Opus format.

        Args:
            input_path: Path to input audio file

        Returns:
            Tuple of (success: bool, stats: dict or None)
        """
        input_file = Path(input_path)

        # Validate input file
        if not input_file.exists():
            print(f"✗ Error: Input file '{input_path}' does not exist.", file=sys.stderr)
            return False, None

        if not input_file.is_file():
            print(f"✗ Error: '{input_path}' is not a file.", file=sys.stderr)
            return False, None

        # Determine output path
        if self.output_dir:
            output_file = Path(self.output_dir) / f"{input_file.stem}.opus"
        else:
            output_file = input_file.with_suffix('.opus')

        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Get input file size
            input_size = input_file.stat().st_size / (1024 ** 2)  # MB

            # Build ffmpeg command using ffmpeg-python
            stream = ffmpeg.input(str(input_file))

            # Set output options
            output_kwargs = {'acodec': 'libopus', 'b:a': f'{self.bitrate}k'}

            if self.vbr:
                output_kwargs['vbr'] = 'on'
            else:
                output_kwargs['vbr'] = 'off'

            stream = ffmpeg.output(stream, str(output_file), **output_kwargs)

            # Run conversion
            ffmpeg.run(stream, quiet=True, overwrite_output=True)

            # Get output file size
            output_size = output_file.stat().st_size / (1024 ** 2)  # MB

            # Print success message
            saved = input_size - output_size
            percent = (saved / input_size * 100) if input_size > 0 else 0
            print(f"✓ {input_file.name} => {output_file.name}")
            print(f"  Size: {input_size:.2f} MB => {output_size:.2f} MB (saved {saved:.2f} MB, {percent:.1f}%)")

            # Delete original if requested
            if self.delete_original:
                input_file.unlink()
                print(f"  Deleted original: {input_file.name}")

            return True, {
                'input_size': input_size,
                'output_size': output_size,
                'input_name': input_file.name,
                'output_name': output_file.name
            }

        except ffmpeg.Error as e:
            print(f"✗ Conversion failed for: {input_file.name}", file=sys.stderr)
            if e.stderr:
                error_msg = e.stderr.decode('utf-8') if isinstance(e.stderr, bytes) else str(e.stderr)
                print(f"  Error: {error_msg}", file=sys.stderr)
            return False, None
        except Exception as e:
            print(f"✗ Error converting {input_file.name}: {e}", file=sys.stderr)
            return False, None

    def convert_files_parallel(self, input_paths: List[str]) -> ConversionStats:
        """
        Convert multiple audio files to Opus format using parallel processing.

        Args:
            input_paths: List of input file paths

        Returns:
            ConversionStats object with conversion statistics
        """
        stats = ConversionStats()

        print(f"Processing {len(input_paths)} file(s) with {self.workers} worker(s)...")
        print(f"Settings: Bitrate={self.bitrate}kbps, VBR={'ON' if self.vbr else 'OFF'}")
        print(f"{'=' * 70}\n")

        # Use ProcessPoolExecutor for parallel processing
        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            # Submit all jobs
            future_to_path = {
                executor.submit(self.convert_file, path): path
                for path in input_paths
            }

            # Process completed conversions
            for future in as_completed(future_to_path):
                success, file_stats = future.result()

                if success and file_stats:
                    stats.add_success(
                        file_stats['input_size'],
                        file_stats['output_size'],
                        file_stats['input_name'],
                        file_stats['output_name']
                    )
                else:
                    stats.add_failure()

                print()  # Empty line between conversions

        return stats


def main():
    """Main entry point for the converter."""
    parser = argparse.ArgumentParser(
        description='Convert audio files to Opus format (with parallel processing)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.mp3
  %(prog)s input.wav -b 192
  %(prog)s *.flac -o ./opus_files/
  %(prog)s song.mp3 -b 96 --cbr
  %(prog)s *.mp3 -j 4 --delete-original
  %(prog)s audio1.wav audio2.mp3 -b 160 -j 8

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
        '-j', '--jobs',
        type=int,
        dest='workers',
        help=f'Number of parallel workers (default: CPU count = {os.cpu_count()})'
    )

    parser.add_argument(
        '--delete-original',
        action='store_true',
        help='Delete original files after successful conversion'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2.0.0'
    )

    args = parser.parse_args()

    # Validate bitrate
    if args.bitrate < 6 or args.bitrate > 510:
        print("Warning: Opus bitrate should be between 6 and 510 kbps", file=sys.stderr)

    # Create converter instance
    try:
        converter = AudioToOpusConverter(
            bitrate=args.bitrate,
            vbr=not args.cbr,
            output_dir=args.output_dir,
            delete_original=args.delete_original,
            workers=args.workers
        )
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Start timing
    start_time = time.perf_counter()

    # Convert files
    print(f"\nAudio to Opus Converter v2.0 (Optimized)")
    print(f"{'=' * 70}\n")

    stats = converter.convert_files_parallel(args.input_files)

    # End timing
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Print summary
    stats.print_summary(elapsed)

    return 0 if stats.failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
