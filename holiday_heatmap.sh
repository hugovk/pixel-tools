#!/bin/bash

# Run in a folder full of photos.
# Extract GPS coordinates from EXIF.
# Create heatmap.

# Requires:
# * exiftool
# * heatmap.py
# * gpsheader.csv

# Extract GPS coordinates from EXIF.
time exiftool -r -c "%.6f" -d "%d/%m/%Y" -p ~/Dropbox/bin/gpsheader.csv . > /tmp/gps.csv

# Create heatmap. Uses http://www.sethoscope.net/heatmap/
WIDTH=1280
# ZOOM=14
OUT_PREFIX=holiday_heatmap

# First one saves processed data to a file, for others to load

# OSM map
time heatmap.py --verbose --width $WIDTH --decay 0.1 -B 0.8 --osm --csv /tmp/gps.csv --ignore_csv_header --save /tmp/gps.data -o "$OUT_PREFIX-osm.png"

# Black background map
time heatmap.py --verbose --width $WIDTH --decay 0.1 --background black --load /tmp/gps.data -o "$OUT_PREFIX-black.png"

# Toner map
time heatmap.py --verbose --width $WIDTH --decay 0.1 -B 0.8 --osm --osm_base http://b.tile.stamen.com/toner --load /tmp/gps.data -o "$OUT_PREFIX-toner.png"

# Watercolor map
time heatmap.py --verbose --width $WIDTH --decay 0.1 -B 0.8 --osm --osm_base http://b.tile.stamen.com/watercolor --load /tmp/gps.data -o "$OUT_PREFIX-watercolor.png"

# del %OUT_PREFIX%all.png
# normalise -i %OUT_PREFIX%$WIDTH*.png -o %OUT_PREFIX%$WIDTHnormalised -n mode
# contact_sheet -i %OUT_PREFIX%$WIDTHnormalised\* -o %OUT_PREFIX%$WIDTH-all.png %3 %4 %5 %6 %7 %8 %9


echo "Generated using <a href="http://www.sethoscope.net/heatmap/" rel="nofollow">Seth Golub's heatmap.py</a>"

echo "Map tiles by <a href="http://stamen.com/" rel="nofollow">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0" rel="nofollow">CC BY 3.0</a>. Data [and map tiles] by <a href="http://openstreetmap.org/" rel="nofollow">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0" rel="nofollow">CC BY SA</a>."

# End of file
