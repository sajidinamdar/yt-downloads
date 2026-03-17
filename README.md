# Universal Video Downloader (Python + Kivy + yt-dlp)

This app lets user paste a link and download video from supported platforms (YouTube, Instagram, Facebook, and many others supported by `yt-dlp`).

## Important
- Download only content you own or have permission to download.
- Some websites restrict downloads by policy.

## 1) Local Run (Windows)

```powershell
cd c:\Users\Sajid\Desktop\yt-download
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Default download folder: `C:\Users\<your-user>\Downloads`

## 2) Android APK (Kivy + Buildozer)

`Buildozer` works best on Linux/WSL. If you are on Windows, use WSL Ubuntu.

### In WSL (Ubuntu)
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git zip unzip openjdk-17-jdk \
  autoconf libtool pkg-config zlib1g-dev libncurses5-dev libtinfo6 cmake \
  libffi-dev libssl-dev
pip install --user buildozer cython
```

Copy this project into WSL path, then:

```bash
cd ~/yt-download
buildozer android debug
```

APK output path:
- `bin/universaldownloader-0.1-debug.apk`

## 3) About HD (1080p+) and FFmpeg

- `yt-dlp` can fetch best streams.
- For some platforms, high quality video/audio are separate streams and need `ffmpeg` to merge.
- On desktop, install FFmpeg for best compatibility.
- On Android packaging, FFmpeg setup is more advanced. Current app still downloads best available single/compatible stream if merge is unavailable.

## 4) BeeWare Note

You asked for Kivy and BeeWare. For Android APK today, Kivy + Buildozer is the most practical Python path.
BeeWare can be explored later for cross-platform app structure, but Android video-download workflow is usually smoother with Kivy.
# yt-downloads
