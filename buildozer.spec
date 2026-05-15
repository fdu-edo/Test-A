[app]
title = TestA
package.name = testa
package.domain = org.francois
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.archs = arm64-v8a

icon.filename = icon.png
presplash.filename = presplash.png

android.api = 33
android.minapi = 21
android.ndk = 25b
android.enable_androidx = True
android.allow_backup = True
android.accept_sdk_license = True

log_level = 2
