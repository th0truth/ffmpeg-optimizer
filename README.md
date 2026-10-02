# FFmpeg Optimizer

A lightweight video optimizer written in Python that uses FFmpeg to compress video files while keeping good visual quality.

## Features

- Compress any FFmpeg-readable video to a MP4
- Quality-driven encoding via CRF (not fixed bitrate)
- Selectable encoding speed presets (`ultrafast` … `veryslow`)
- Sane streaming defaults:
  - H.264 (`libx264`), `yuv420p`, High profile, level 4.0
  - AAC audio, 96 kbps, stereo
  - `+faststart` for progressive playback
- Reports size before/after and the percentage saved
- Written in pure Python (standard library only)

## Requirements

- Python 3.10+ (uses `list[str]` / `Literal` type syntax)
- FFmpeg available in `PATH`

## Install FFmpeg:

```bash
# Debian / Ubuntu
sudo apt install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

```bash
git clone https://github.com/th0truth/ffmpeg-optimizer.git

cd ffmpeg-optimizer
```

## Usage

```bash
python main.py -f <input> -o <output> [--crf N] [-p PRESET]
```

Example:

```bash
python main.py -f input.mkv -o out/input.mp4 --crf 20 -p slow
```

### Options

| Option             | Default | Description                                     |
| ------------------ | ------- | ----------------------------------------------- |
| `-f`, `--filename` | —       | Path to the source file (required)              |
| `-o`, `--output`   | —       | Path for the optimized file (required)          |
| `--crf`            | `23`    | Quality, lower is better (18–28)                |
| `-p`, `--preset`   | `slow`  | Compression speed setting                       |


### Choosing a CRF

| CRF     | Result                                        |
| ------- | --------------------------------------------- |
| `18`    | Near-visually-lossless, largest file          |
| `20–23` | Good quality, recommended range               |
| `26–28` | Noticeably softer, smallest file              |

Slower presets produce smaller files at the same CRF, at the cost of encode time.

### Exit Codes

| Code | Meaning                  |
| ---- | ------------------------ |
| `0`  | Optimized successfully   |
| `1`  | Encoding failed          |


Released under the [MIT License](LICENSE).
