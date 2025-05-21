#!/bin/bash

# Zielgrößen
COVER_WIDTH=1280
COVER_HEIGHT=720
THUMB_SIZE=140

# Verzeichnis vorbereiten (optional, kann auch im selben bleiben)
mkdir -p ./generated

for img in *.png; do
  # Dateiname ohne Endung
  base=$(basename "$img")
  name="${base%.*}"

  echo "🔧 Verarbeite: $img"

  # 1. Cover-Bild erzeugen
  magick "$img" -resize ${COVER_WIDTH}x${COVER_HEIGHT}^ \
         -gravity center -extent ${COVER_WIDTH}x${COVER_HEIGHT} \
         -quality 90 "generated/${name}_cover.webp"

  # 2. Thumbnail erzeugen
  magick "$img" -resize 100x100\> \
         -gravity center -background none -extent ${THUMB_SIZE}x${THUMB_SIZE} \
         -interpolate Catrom -filter Lanczos -density 144 \
         -quality 85 "generated/${name}_thumb.webp"
done

echo "✅ Alle Bilder wurden erfolgreich verarbeitet und in ./generated/ gespeichert."
