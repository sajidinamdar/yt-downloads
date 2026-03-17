import os
from typing import Callable, Optional

import yt_dlp


def download_video(
    url: str,
    output_dir: str,
    max_height: int = 1080,
    status_callback: Optional[Callable[[str], None]] = None,
) -> str:
    def emit(message: str) -> None:
        if status_callback:
            status_callback(message)

    emit("Fetching video info...")

    outtmpl = os.path.join(output_dir, "%(title).120s.%(ext)s")

    ydl_opts = _build_ydl_opts(outtmpl, max_height, emit)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded = ydl.prepare_filename(info)
    except yt_dlp.utils.DownloadError as exc:
        # Fallback to a single combined stream when separate video/audio merge is not available.
        if _needs_single_stream_fallback(exc):
            emit("Retrying with a compatible format...")
            fallback_opts = _build_ydl_opts(outtmpl, max_height, emit, prefer_single_stream=True)
            with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded = ydl.prepare_filename(info)
        else:
            raise RuntimeError(_clean_error_message(exc)) from exc

    base, _ext = os.path.splitext(downloaded)
    mp4_candidate = base + ".mp4"
    if os.path.exists(mp4_candidate):
        return mp4_candidate
    return downloaded


def _build_ydl_opts(outtmpl, max_height, emit, prefer_single_stream=False):
    if prefer_single_stream:
        format_selector = f"best[height<={max_height}]/best"
    else:
        format_selector = f"bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}]/best"

    return {
        "outtmpl": outtmpl,
        "format": format_selector,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "logger": _YtDlpLogger(emit),
        "progress_hooks": [_make_hook(emit)],
    }


def _make_hook(emit):
    def hook(progress_data):
        status = progress_data.get("status")
        if status == "downloading":
            percent = progress_data.get("_percent_str", "").strip()
            speed = progress_data.get("_speed_str", "").strip()
            eta = progress_data.get("_eta_str", "").strip()
            emit(f"Downloading... {percent} | Speed: {speed} | ETA: {eta}")
        elif status == "finished":
            emit("Download finished, processing file...")

    return hook


def _needs_single_stream_fallback(exc) -> bool:
    message = _clean_error_message(exc).lower()
    return "ffmpeg" in message or "requested format is not available" in message


def _clean_error_message(exc) -> str:
    message = str(exc).strip()
    if message.upper().startswith("ERROR:"):
        message = message[6:].strip()
    return message or "Download failed."


class _YtDlpLogger:
    def __init__(self, emit):
        self._emit = emit

    def debug(self, message):
        if message.startswith("[debug]"):
            return
        self._emit(message)

    def warning(self, message):
        self._emit(f"Warning: {message}")

    def error(self, message):
        self._emit(f"Error: {message}")
