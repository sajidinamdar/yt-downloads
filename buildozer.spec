[app]
title = Universal Video Downloader
package.name = universaldownloader
package.domain = org.sajid
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,yt-dlp
orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 34
android.minapi = 24
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
