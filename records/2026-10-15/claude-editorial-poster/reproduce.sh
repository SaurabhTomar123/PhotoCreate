#!/usr/bin/env bash
# Reproduce the three editorial-poster prototypes (Claude lane L1, 15 October 2026).
# Every step is an existing engine command run through the normal dispatch; nothing here is new code.
#
# Usage: CLI=/path/to/photocraft-cli ./reproduce.sh
# Evidence was produced with the official photocraft-cli 0.9.0 (c699e3cda, signed Windows x64 build),
# which is 2 commits after PhotoCreate's integrated upstream ed7df56 and an ancestor of df055f3.
# The layout numbers below are hand-computed for these two images; the recipe engine (L3) computes
# them from the placed image's bounds.
set -euo pipefail
CLI="${CLI:-photocraft-cli}"
mkdir -p samples out
fetch() { # public-domain originals, Wikimedia Commons (see SOURCES.md); generic User-Agent per AGENTS.md
  [ -f "samples/$2" ] || curl -sL -A "Photocraft-dev" -o "samples/$2" "https://commons.wikimedia.org/wiki/Special:FilePath/$1?width=1600"
}
fetch NASA-Apollo8-Dec24-Earthrise.jpg earthrise.jpg
fetch Adams_The_Tetons_and_the_Snake_River.jpg tetons.jpg

# A. Gallery: framed photo on paper, serif title, rule, accent subtitle.
"$CLI" run --new '{"width":1600,"height":2000,"background":"#f1ece2","resolution":150,"name":"Editorial poster"}' \
  --cmd shape.create --params '{"kind":"rect","rect":[120,120,1360,1200],"fill":"#1d2a3a","name":"Photo frame"}' \
  --cmd file.placeEmbedded --params '{"path":"samples/earthrise.jpg","smartObject":true,"fit":true}' \
  --cmd edit.transform --params '{"scaleX":85,"scaleY":85,"dy":-280}' \
  --cmd layer.setProps --params '{"clipped":true,"name":"Photo"}' \
  --cmd type.create --params '{"x":120,"y":1560,"text":"EARTHRISE","font":"Playfair Display","size":120,"color":"#1b1b1b","name":"Title"}' \
  --cmd shape.create --params '{"kind":"line","from":[120,1610],"to":[1480,1610],"weight":3,"fill":"#1b1b1b","name":"Rule"}' \
  --cmd type.create --params '{"x":122,"y":1680,"text":"APOLLO 8  ·  24 DECEMBER 1968","font":"Inter","size":22,"color":"#b4532a","name":"Subtitle"}' \
  --cmd type.create --params '{"x":1480,"y":1890,"text":"A PHOTOCRAFT EDITORIAL","font":"Inter","size":12,"color":"#1b1b1b","align":"right","name":"Credit"}' \
  --out out/a-gallery.pcraft

# B. Bold overlay: full-bleed cover photo, gradient-map duotone, multiply shade, condensed title.
"$CLI" run --new '{"width":1600,"height":2000,"background":"#101418","resolution":150,"name":"Editorial poster B"}' \
  --cmd file.placeEmbedded --params '{"path":"samples/tetons.jpg","smartObject":true,"fit":true}' \
  --cmd edit.transform --params '{"scaleX":156.2,"scaleY":156.2}' \
  --cmd layer.setProps --params '{"name":"Photo"}' \
  --cmd layer.newAdjustmentLayer.gradientMap --params '{"stops":[[0,"#14213d"],[0.55,"#7d5a50"],[1,"#fca311"]]}' \
  --cmd layer.setProps --params '{"name":"Duotone","opacity":0.9}' \
  --cmd layer.newFillLayer.gradient --params '{"from":"#000000","to":"#ffffff","angle":90,"style":"linear"}' \
  --cmd layer.setProps --params '{"name":"Shade for text","blend":"Multiply","opacity":0.8}' \
  --cmd type.create --params '{"x":110,"y":1700,"text":"THE TETONS","font":"Bebas Neue","size":150,"color":"#ffffff","name":"Title"}' \
  --cmd type.create --params '{"x":116,"y":1800,"text":"ANSEL ADAMS  ·  1942","font":"Inter","size":22,"color":"#fca311","name":"Subtitle"}' \
  --out out/b-overlay.pcraft

# C. Swiss block: colour band, framed black-and-white photo, stacked heavy title, small columns.
"$CLI" run --new '{"width":1600,"height":2000,"background":"#ece7dc","resolution":150,"name":"Editorial poster C"}' \
  --cmd shape.create --params '{"kind":"rect","rect":[0,0,1600,760],"fill":"#d6452b","name":"Colour block"}' \
  --cmd shape.create --params '{"kind":"rect","rect":[560,520,920,1200],"fill":"#222222","name":"Photo frame"}' \
  --cmd file.placeEmbedded --params '{"path":"samples/tetons.jpg","smartObject":true,"fit":true}' \
  --cmd edit.transform --params '{"scaleX":93.7,"scaleY":93.7,"dx":220,"dy":120}' \
  --cmd layer.setProps --params '{"clipped":true,"name":"Photo"}' \
  --cmd layer.newAdjustmentLayer.blackWhite --params '{}' \
  --cmd layer.setProps --params '{"clipped":true,"name":"Black and white"}' \
  --cmd type.create --params '{"x":110,"y":330,"text":"THE","font":"Montserrat Black","size":110,"color":"#ffffff","name":"Title line 1"}' \
  --cmd type.create --params '{"x":110,"y":560,"text":"TETONS","font":"Montserrat Black","size":110,"color":"#ffffff","name":"Title line 2"}' \
  --cmd type.create --params '{"x":112,"y":900,"text":"ANSEL ADAMS","font":"Inter","size":20,"color":"#1b1b1b","name":"Subtitle"}' \
  --cmd type.create --params '{"x":112,"y":950,"text":"1942","font":"Inter","size":20,"color":"#d6452b","name":"Year"}' \
  --cmd type.create --params '{"x":112,"y":1720,"text":"No. 07","font":"Inter","size":14,"color":"#1b1b1b","name":"Issue"}' \
  --out out/c-swiss.pcraft

for n in a-gallery b-overlay c-swiss; do
  "$CLI" convert "out/$n.pcraft" "out/$n-preview.jpg" --quality 85
  "$CLI" info "out/$n.pcraft" --compact > "out/$n-layers.json"
done
