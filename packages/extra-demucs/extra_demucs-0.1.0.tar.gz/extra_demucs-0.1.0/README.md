`extra_demucs`: Extended [Demucs](https://github.com/facebookresearch/demucs) with yt-dlp media downloading and Video
Music removal

## Features

- 🎧 **Vocal isolation** using Demucs (`--two-stems vocals`)
- 📥 **Media download** from URLs (e.g., YouTube) using `yt-dlp`
- 📁 Works with both **audio** and **video** files
- ✅ Local + remote (URL) input support

## Get started

*Make sure you have [ffmpeg](https://www.ffmpeg.org/download.html) installed.*

```bash
sudo apt install ffmpeg
```

Download package:
> Requires Python 3.9+

```bash
pip install extra-demucs
```

## Usage

```bash
from extra_demucs.separate import extra_separator

extra_separator(
    files=[
        "https://www.youtube.com/watch?v=123",
        "local_audio.mp3"
    ],
    download_format="audio",   # or "video"
    quality="medium",     # "low", "medium", "high"
    output_dir="outputs"
    model_name="htdemucs"
)

```
