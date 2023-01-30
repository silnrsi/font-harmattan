#!/bin/bash

# This script rebuilds the kerning files for both Graphite and OpenType. See README.md

# Copyright (c) 2020-2022 SIL International  (http://www.sil.org)
# Released under the MIT License (http://opensource.org/licenses/

# Assumes we're in the root folder, i.e., font-harmattan

# $R is the clustering radius for computing the OpenType kerning. Default is 20 but can be overridden, e.g.:
#      export R=50 updateKerning

# Command line options:
#    --ftml        rebuild ftml before rebuilding kerning
#    --ftmlOnly    rebuild only ftml
#    --octalap     rebuild optimized octaboxes (otherwise assumes they are acceptable)
#    --regOnly     process only the Regular font rather than Regular and Bold
#    --noKern      debugging tool to skip the actual building of fea files 

set -e	# Stop on error
# set -x	# echo before execution

if [ ! -e OFL.txt ] 
then
	echo "Please cd to root of font project to use this script"
	exit 2
fi

# Default settings:
REGONLY=""
WEIGHTS=(Regular Bold)
OCTALAP=0
FTML=0
FTMLONLY=0
KERN=1

# Look for options:
while [[ $# -gt 0 ]]
do
  case $1 in
    --regOnly)
    REGONLY="--regOnly"
    WEIGHTS=(Regular)
    ;;
  
    --octalap)
    OCTALAP=1
    ;;

    --ftml)
    FTML=1
    ;;
    
    --ftmlOnly)
    FTML=2
    ;;

    --noKern)
    KERN=0
    ;;

    *)
    echo "unrecognized parameter $1"
    echo "Command line options:"
    echo "   --ftml         rebuild ftml"
    echo "   --ftmlOnly     rebuild ftml but do nothing else"
    echo "   --octalap      rebuild optimized octaboxes"
    echo "   --regOnly      process only the Lateef Regular font rather than all six"
    echo "   --noKern       do not try to regenerate the caKerning"
    exit 
  esac
  shift
done

if [ ${FTML} -gt 0 ]
then
  echo "rebuilding kerndata.ftml..."

  tools/absgenftml.py -q -t "KernData with Marks (auto)" -f h --norendercheck  \
        --ap "_?dia[AB]$"  -l source/logs/kerndata.log \
        --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv -w 75% \
        -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" \
        -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" \
        -s "url(../results/Harmattan-Bold.ttf)|Bld-Gr" \
        -s "url(../results/tests/ftml/fonts/Harmattan-Bold_ot_arab.ttf)|Bld-OT" \
        source/Harmattan-Regular.ufo source/kerndata.ftml 
fi

if [ ${FTML} -gt 1 ]
then
  echo "finished successfullly and source/kerndata.ftml has been rebuilt."
  exit
fi

echo -e "\nUpdating kerning\n"

echo -e "\nrebuilding with graphite and fonts without glyph kerning or renaming...\n"

smith distclean
smith configure --graphite
smith build --graphite --quick --norename $REGONLY

if [ ${OCTALAP} == 1 ]; 
then
  echo -e "\nrebuilding optimized octaboxes...\n"
  
  for w in "${WEIGHTS[@]}"
  do
    octalap -q -j 0 -o source/Harmattan-$w-octabox.json results/Harmattan-$w.ttf  &
  done
  wait
  
  echo -e "\nrebuilding fonts with graphite and new octaboxes but without glyph kerning or renaming...\n" 
  
  smith clean ;
  smith build --graphite --quick --norename $REGONLY
fi

if [ ${KERN} == 1 ]
then
  echo -e "\nrebuilding collision-avoidance-based kerning...\n"

  # Use a temp directory
  outdir=results/grkern2fea_r${R:=20}
  mkdir -p $outdir

  for w in "${WEIGHTS[@]}"
  do
    ( \
      grkern2fea -e graphite -i source/kerndata.ftml -F ut53=0        -f results/Harmattan-$w.ttf                 $outdir/rawPairData-$w.txt        ; \
      tools/renumberKernData.py $outdir/rawPairData-$w.txt                                                        $outdir/rawPairData-$w-nozwj.txt  ; \
      grkern2fea -s strings  -i $outdir/rawPairData-$w-nozwj.txt -f results/Harmattan-$w.ttf  -r ${R:=20} -R $outdir/caKern-$w.fea             ; \
      sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g $outdir/caKern-$w.fea  > source/opentype/caKern-$w.fea \
    ) &
  done
  wait
fi

echo "finished successfullly, and the following files were regenerated:"
if [ ${FTML} -gt 0 ]
then
  echo " - source/kerndata.ftml"
fi

if [ ${OCTALAP} == 1 ] 
then
  for w in "${WEIGHTS[@]}" 
  do
      echo " - source/Harmattan-$w-octabox.json"
  done
fi

if [ ${KERN} == 1 ]
then
  for w in "${WEIGHTS[@]}"
  do
    echo " - source/opentype/caKern-$w.fea"
  done
fi

echo "
Notes:
  - Intermediate files are in $outdir
  - The fonts have not been rebuilt with these modified files. To complete the build, use:

	smith clean
	smith build test  

Please verify changes and commit results."
