#!/bin/bash

fn=""
for f in $(ls | grep "_dem.tif");do
	#echo "./"$f
	#gdal_merge.py -o m.tif  m.tif "./"$f
	fn+="${f} "
done

echo $fn

gdal_merge.py -o mg.tif $fn

gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857"  mg.tif mg_3857.tif

#rio rgbify -b -1000 -i 0.1 mg_3857.tif mg_3857_rgb.tif

#gdal2tiles.py -z 12-15 mg_3857.tif ./tiles
