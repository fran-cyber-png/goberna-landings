# uso: sec.sh nombre yFigma hFigma yPrev hPrev
F=../_figma/full1920.png; D=ds1920.png
magick $F -crop 1920x$3+0+$2 +repage -resize 960x cmp/f.png
magick $D -crop 1920x$5+0+$4 +repage -resize 960x cmp/d.png
magick cmp/f.png cmp/d.png -background white -gravity north +append cmp/$1.png
