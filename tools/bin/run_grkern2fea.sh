#!/bin/sh

# Assumes we're in a folder one level below root, e.g., font-harmattan/dev
# Puts results into ../source/opentype

# R=20

set -x
set -e

# Puts results in subfolder
outdir=grkern2fea_res7_r${R:=20}
mkdir -p $outdir

grkern2fea -e graphite -i ../tests/kerndata.ftml          -f ../results/Harmattan-Regular.ttf           $outdir/rawPairData-Regular.txt ; \
grkern2fea -s strings  -i $outdir/rawPairData-Regular.txt -f ../results/Harmattan-Regular.ttf  -r ${R:=20} -R $outdir/caKern-Regular.fea; \
sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g $outdir/caKern-Regular.fea  > ../source/opentype/caKern-Regular.fea &

grkern2fea -e graphite -i ../tests/kerndata.ftml         -f ../results/Harmattan-Bold.ttf           $outdir/rawPairData-Bold.txt ; \
grkern2fea -s strings -i $outdir/rawPairData-Bold.txt    -f ../results/Harmattan-Bold.ttf  -r ${R:=20} -R $outdir/caKern-Bold.fea; \
sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g $outdir/caKern-Bold.fea  > ../source/opentype/caKern-Bold.fea &

wait
