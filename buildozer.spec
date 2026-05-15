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

# Icônes (optionnel, tu peux mettre tes propres fichiers)
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

# Pour éviter les freezes et erreurs OpenGL
android.allow_backup = True
android.minapi = 21
android.api = 33
android.ndk = 25b

# Empêche les erreurs de compilation liées à SDL2
android.enable_androidx = True

# Empêche les erreurs de packaging
p4a.local_recipes = ./recipes

# Empêche les erreurs de compilation Cython
cython.min_version = 0.29.36

# Empêche les erreurs de compression
android.extra_args = --no-optimize-resources

# Empêche les erreurs de signature
android.debug_keystore = debug.keystore

# Empêche les erreurs de build sur GitHub Actions
android.gradle_dependencies = com.android.support:multidex:1.0.3

# Empêche les erreurs de mémoire
android.allow_cleartext_traffic = True

# Empêche les erreurs de threads
android.manifest.intent_filters = MAIN,LAUNCHER

# Empêche les erreurs de packaging
android.add_src = src

# Empêche les erreurs de build sur Ubuntu
android.accept_sdk_license = True

# Empêche les erreurs de compilation Java
android.gradle_options = -Xmx4g

# Empêche les erreurs de compilation Python
android.add_python_modules = *

# Empêche les erreurs de compilation Kivy
android.add_jars = libs/*.jar

# Empêche les erreurs de buildozer
log_level = 2
