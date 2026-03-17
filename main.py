import os
import threading
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from downloader import download_video


class DownloaderUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=12, spacing=10, **kwargs)
        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        self.title_label = Label(
            text="Universal Video Downloader (yt-dlp)",
            size_hint_y=None,
            height=44,
            bold=True,
        )
        self.add_widget(self.title_label)

        self.url_input = TextInput(
            hint_text="Paste video URL (YouTube / Instagram / Facebook ...)",
            multiline=False,
            size_hint_y=None,
            height=44,
        )
        self.add_widget(self.url_input)

        self.download_folder_label = Label(
            text=f"Save to: {self.download_folder}",
            size_hint_y=None,
            height=44,
            halign="left",
            valign="middle",
        )
        self.download_folder_label.bind(size=self._resize_status)
        self.add_widget(self.download_folder_label)

        self.quality_input = TextInput(
            text="1080",
            hint_text="Max quality (e.g. 1080, 720)",
            multiline=False,
            size_hint_y=None,
            height=44,
            input_filter="int",
        )
        self.add_widget(self.quality_input)

        self.download_btn = Button(
            text="Download Video",
            size_hint_y=None,
            height=50,
        )
        self.download_btn.bind(on_press=self.on_download_click)
        self.add_widget(self.download_btn)

        self.status_label = Label(
            text="Status: Ready",
            halign="left",
            valign="top",
        )
        self.status_label.bind(size=self._resize_status)
        self.add_widget(self.status_label)

    def _resize_status(self, instance, value):
        instance.text_size = (value[0], None)

    def on_download_click(self, _instance):
        url = self.url_input.text.strip()
        quality = self.quality_input.text.strip()

        if not url:
            self.set_status("Status: Please paste a valid URL.")
            return

        try:
            max_height = int(quality) if quality else 1080
        except ValueError:
            self.set_status("Status: Quality must be number like 1080 or 720.")
            return

        os.makedirs(self.download_folder, exist_ok=True)

        self.download_btn.disabled = True
        self.set_status(f"Status: Download started in {self.download_folder}...")

        worker = threading.Thread(
            target=self._download_task,
            args=(url, self.download_folder, max_height),
            daemon=True,
        )
        worker.start()

    def _download_task(self, url, folder, max_height):
        try:
            result_path = download_video(
                url=url,
                output_dir=folder,
                max_height=max_height,
                status_callback=self.set_status_threadsafe,
            )
            self.set_status_threadsafe(f"Status: Done. Saved at: {result_path}")
        except Exception as exc:
            self.set_status_threadsafe(f"Status: Failed - {exc}")
        finally:
            Clock.schedule_once(lambda _dt: setattr(self.download_btn, "disabled", False), 0)

    def set_status_threadsafe(self, text):
        Clock.schedule_once(lambda _dt: self.set_status(text), 0)

    def set_status(self, text):
        now = datetime.now().strftime("%H:%M:%S")
        self.status_label.text = f"[{now}] {text}"


class DownloaderApp(App):
    def build(self):
        self.title = "Universal Video Downloader"
        return DownloaderUI()


if __name__ == "__main__":
    DownloaderApp().run()
