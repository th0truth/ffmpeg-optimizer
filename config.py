from typing import Literal


LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


FFMPEG_PRESETS = (
    "ultrafast", "superfast", "veryfast",
    "faster", "fast", "medium", "slow",
    "slower", "veryslow"
)

FFMPEG_PRESET = Literal[
    "ultrafast", "superfast", "veryfast",
    "faster", "fast", "medium", "slow",
    "slower", "veryslow"
]

