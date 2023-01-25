#!/bin/sh

# This script rebuilds the kerning files for both Graphite and OpenType. See README.md

# Copyright (c) 2020-2022 SIL International  (http://www.sil.org)
# Released under the MIT License (http://opensource.org/licenses/

# Assumes we're in the root folder, i.e., font-harmattan

# $R is the clustering radius for computing the OpenType kerning. Default is 20 but can be overridden, e.g.:
#      export R=50 updateKerning

# --nooctalap causes script to assume optimized octaboxes needn't be recomputed

set -e	# Stop on error
# set -x	# echo before execution

if [ ! -e OFL.txt ] 
then
	echo "Please cd to root of font project to use this script"
	exit 2
fi

echo "Updating kerning\nrebuilding fonts without glyph kerning or renaming...\n"

smith distclean
smith configure
smith build --quick --norename

if [ "z$1" != "z--nooctalap" ]; then
echo "\nrebuilding optimized octaboxes...\n"

octalap -q -j 0 -o source/Harmattan-Regular-octabox.json results/Harmattan-Regular.ttf  &
octalap -q -j 0 -o source/Harmattan-Bold-octabox.json    results/Harmattan-Bold.ttf 

wait

echo "\nrebuilding fonts (with new octaboxes)...\n" 

smith clean ;
smith build --quick --norename 
fi

echo "\nrebuilding source/kerndata.ftml\n"

tools/absgenftml.py -q -t "KernData with Marks (auto)" source/Harmattan-Regular.ufo source/kerndata.ftml  -l source/logs/kerndata.log --norendercheck  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bld-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Bold_ot_arab.ttf)|Bld-OT" 

echo "\nrebuilding collision-avoidance-based kerning...\n"

# Use a temp directory
outdir=results/grkern2fea_r${R:=20}
mkdir -p $outdir

( \
  grkern2fea -e graphite -i source/kerndata.ftml -F ut53=0        -f results/Harmattan-Regular.ttf                 $outdir/rawPairData-Regular.txt        ; \
  tools/renumberKernData.py $outdir/rawPairData-Regular.txt                                                        $outdir/rawPairData-Regular-nozwj.txt  ; \
  grkern2fea -s strings  -i $outdir/rawPairData-Regular-nozwj.txt -f results/Harmattan-Regular.ttf  -r ${R:=20} -R $outdir/caKern-Regular.fea             ; \
  sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g $outdir/caKern-Regular.fea  > source/opentype/caKern-Regular.fea \
) &

( \
  grkern2fea -e graphite -i source/kerndata.ftml -F ut53=0        -f results/Harmattan-Bold.ttf                    $outdir/rawPairData-Bold.txt           ; \
  tools/renumberKernData.py $outdir/rawPairData-Bold.txt                                                           $outdir/rawPairData-Bold-nozwj.txt     ; \
  grkern2fea -s strings  -i $outdir/rawPairData-Bold-nozwj.txt    -f results/Harmattan-Bold.ttf     -r ${R:=20} -R $outdir/caKern-Bold.fea                ; \
  sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g $outdir/caKern-Bold.fea  > source/opentype/caKern-Bold.fea \
) &

wait

echo "finished successfullly, and the following files were regenerated:"
if [ "z$1" != "z--nooctalap" ]; then
echo "  - source/Harmattan-Regular-octabox.json
  - source/Harmattan-Bold-octabox.json"
fi

echo "  - source/opentype/caKern-Regular.fea
  - soure/opentype/caKern-Bold.fea

Notes:
  - Intermediate files are in $outdir
  - The fonts have not been rebuilt with these modified files. To complete the build, use:

	smith clean
	smith build test  

Please verify changes and commit results."
