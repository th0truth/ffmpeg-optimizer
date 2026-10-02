from typing import Literal, get_args
from pathlib import Path
import subprocess
import argparse
import logging
import sys

from config import (
    LOGGER_FORMAT,
    FFMPEG_PRESET,
    FFMPEG_PRESETS
) 


logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)
logger = logging.getLogger(__name__)


def build_cmd(
    filename: str, output: str,
    crf: int, preset: FFMPEG_PRESET = "slow"
) -> list[str]:
    return [
        "ffmpeg",
        "-nostdin",
        "-y",
        "-loglevel", "error",
        "-i", filename,
        "-c:v", "libx264",
        "-preset", preset,
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-level", "4.0",
        "-c:a", "aac",
        "-b:a", "96k",
        "-ac", "2",
        "-movflags", "+faststart",
        output
    ]


def optimizer(
    filename: str, output: str,
    crf: int = 23, preset: FFMPEG_PRESET = "slow"
) -> bool:
    """
    Compress the filename while maintaining good quality.

    Quality Parameters:
        - crf (Constant Rate Factor): 18-23 (lower is better quality)
        - preset: Compression speed setting
    """
    src = Path(filename)

    if not src.is_file():
        logger.error(
            f"Input file not found: {filename}"
        )

        return False

    Path(output).parent.mkdir(parents=True, exist_ok=True)

    try:
        command = build_cmd(filename, output, crf, preset)

        subprocess.run(
            command, check=True,
            capture_output=True,
            text=True
        )
    except FileNotFoundError:
        logger.error("ffmpeg not found in PATH.")
        
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error optimizing {filename}: {e.stderr.strip()}")

        return False
    except Exception as e:
        logger.info(f"Failed to optimize {filename}: {e}")

        return False

    before = src.stat().st_size
    after = Path(output).stat().st_size

    logger.info(
        f"Optimized: {filename} -> {output} "
        f"({before / 1024:.0f}KB -> {after / 1024:.0f}KB, "
        f"-{(1 - after / before) * 100:.0f}%)"
    )

    return True


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--filename", required=True, help="Path to the source file."
    )

    parser.add_argument(
        "-o", "--output", required=True, help="Path for the optimized file."
    )

    parser.add_argument(
        "--crf", type=int, default=23, help="Quality, lower is better (18-28)."
    )

    parser.add_argument(
        "-p", "--preset", choices=get_args(FFMPEG_PRESETS),
        default="slow", help="Compression speed setting."
    )

    args = parser.parse_args()

    if not optimizer(args.filename, args.output, args.crf, args.preset):
        sys.exit(1)


if __name__ == "__main__":
    main()
