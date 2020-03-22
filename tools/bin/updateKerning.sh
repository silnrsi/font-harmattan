#!/bin/sh

# This script rebuilds the kerning files for both Graphite and OpenType. See README.md

# Copyright (c) 2020 SIL International  (http://www.sil.org)
# Released under the MIT License (http://opensource.org/licenses/

# Assumes we're in the root folder, i.e., font-harmattan

# $R is the clustering radius for computing the OpenType kerning. Default is 20 but can be overridden, e.g.:
#      export R=50 updateKerning

set -x
set -e

if [ ! -e OFL.txt ] 
then
	echo "Please cd to root of font project to use this script"
	exit 2
fi

echo "Updating kerning\nrebuilding fonts without glyph kerning or renaming...\n"

smith distclean
smith configure
smith build --quick --norename

echo "\nrebuilding optimized octaboxes...\n"

tools/bin/octalap -q -j 0 -o source/Harmattan-Regular-octabox.json results/Harmattan-Regular.ttf  &
tools/bin/octalap -q -j 0 -o source/Harmattan-Bold-octabox.json    results/Harmattan-Bold.ttf

wait

echo "\nrebuilding fonts (with new octaboxes)...\n"

smith clean
smith build --quick --norename

echo "\nrebuilding collision-avoidance-based kerning...\n"

# Use a temp directory
outdir=results/grkern2fea_r${R:=20}
mkdir -p $outdir

grkern2fea -e graphite -i source/kerndata.ftml             -f results/Harmattan-Regular.ttf                 $outdir/rawPairData-Regular.txt ; \
grkern2fea -s strings  -i $outdir/rawPairData-Regular.txt -f results/Harmattan-Regular.ttf  -r ${R:=20} -R $outdir/caKern-Regular.fea;       \
sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g $outdir/caKern-Regular.fea  > source/opentype/caKern-Regular.fea &

grkern2fea -e graphite -i source/kerndata.ftml            -f results/Harmattan-Bold.ttf                 $outdir/rawPairData-Bold.txt ; \
grkern2fea -s strings -i $outdir/rawPairData-Bold.txt    -f results/Harmattan-Bold.ttf  -r ${R:=20} -R $outdir/caKern-Bold.fea;       \
sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g $outdir/caKern-Bold.fea  > source/opentype/caKern-Bold.fea &

wait

echo "finished successfullly, and the following files were regenerated:
	source/Harmattan-Regular-octabox.json
	source/Harmattan-Bold-octabox.json
	source/opentype/caKern-Regular.fea
	soure/opentype/caKern-Bold.fea

Notes:
  - Intermediate files are in $outdir
  - The fonts have not been rebuilt with these modified files. To complete the build, use:

	smith clean
	smith build test  

Please verify changes and commit results."