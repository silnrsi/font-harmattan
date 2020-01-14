#!/bin/sh

# Assumes we're in a folder one level below root, e.g., font-harmattan/dev
# Puts results into ../source/opentype

set +x

# Puts results in subfolder
outdir=grkern2fea_res
mkdir -p $outdir

for face in Regular Bold
do
	echo "\n*****" Parse ../tests/kerndata.ftml and generate raw kern data for $face...
	../tools/bin/grstrings.py -i ../tests/kerndata.ftml -t -f ../results/Harmattan-$face.ttf -r $outdir/rawPairData-$face.txt
	echo "\n*****" Generate fea output for $face
	../tools/bin/glyphstring.py -f ../results/Harmattan-$face.ttf  -r 20 -j 1    -R $outdir/rawPairData-$face.txt $outdir/caKern-$face.fea
	echo "\n*****" Update mark references and copy fea to source tree...
	sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g $outdir/caKern-$face.fea  > ../source/opentype/caKern-$face.fea
done
echo "\nDone.\n"
exit


# Trace graphite to get kerning data


# generate fea
echo generating Regular fea output...


echo generating Bold fea output...
../tools/bin/glyphstring.py -f ../results/Harmattan-Bold.ttf     -r 20 -j 1      -R rawPairData-Bold.txt    res/caKern-bold.fea


# Copy result to source folder so project will compile:
echo updating mark references and copying results to source tree...
sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g res/caKern.fea > ../source/opentype/caKern.fea

echo ../source/opentype/caKern.fea updated
