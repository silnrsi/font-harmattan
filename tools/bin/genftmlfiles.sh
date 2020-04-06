#!/bin/sh

# This script rebuilds the algorithmically-generated ftml files. See README.md

# Copyright (c) 2020 SIL International  (http://www.sil.org)
# Released under the MIT License (http://opensource.org/licenses/

# Assumes we're in the root folder, i.e., font-harmattan

set -x
set -e

if [ ! -e OFL.txt ] 
then
	echo "Please cd to root of font project to use this script"
	exit 2
fi

tools/bin/absgenftml.py -t 'AllChars (NG)'         source/Harmattan-Regular.ufo  tests/AllChars.ftml        -l tests/logs/AllChars.log         -s 'url(reference/Harmattan-Regular.ttf)' --ap "_?dia[AB]$" --xsl ../tools/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "ku,sd,ur,wo,rhg" -s 'url(../results/Harmattan-Regular.ttf)' -s 'url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)' -s 'url(../results/Harmattan-Bold.ttf)'
tools/bin/absgenftml.py -t 'AL Sorted (NG)'        source/Harmattan-Regular.ufo  tests/ALsorted.ftml        -l tests/logs/ALsorted.log         -s 'url(reference/Harmattan-Regular.ttf)' --ap "_?dia[AB]$" --xsl ../tools/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "ku,sd,ur,wo,rhg" -s 'url(../results/Harmattan-Regular.ttf)' -s 'url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)' -s 'url(../results/Harmattan-Bold.ttf)'
tools/bin/absgenftml.py -t 'DiacTest1 (NG)'        source/Harmattan-Regular.ufo  tests/DiacTest1.ftml       -l tests/logs/DiacTest1.log                                                  --ap "_?dia[AB]$" --xsl ../tools/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "ku,sd,ur,wo,rhg" -s 'url(../results/Harmattan-Regular.ttf)' -s 'url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)' -s 'url(../results/Harmattan-Bold.ttf)' 
tools/bin/absgenftml.py -t 'DiacTest1 Short (NG)'  source/Harmattan-Regular.ufo  tests/DiacTest1-short.ftml -l tests/logs/DiacTest1-short.log  -s 'url(reference/Harmattan-Regular.ttf)' --ap "_?dia[AB]$" --xsl ../tools/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "ku,sd,ur,wo,rhg" -s 'url(../results/Harmattan-Regular.ttf)' -s 'url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)' -s 'url(../results/Harmattan-Bold.ttf)'
tools/bin/absgenftml.py -t 'Subtending Marks (NG)' source/Harmattan-Regular.ufo  tests/SubtendingMarks.ftml -l tests/logs/Subtending.log                                                 --ap "_?dia[AB]$" --xsl ../tools/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "ku,sd,ur,wo,rhg" -s 'url(../results/Harmattan-Regular.ttf)' -s 'url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)' -s 'url(../results/Harmattan-Bold.ttf)'
tools/bin/absgenftml.py -t 'DaggerAlef (NG)'       source/Harmattan-Regular.ufo  tests/DaggerAlef.ftml      -l tests/logs/DaggerAlef.log       -s 'url(reference/Harmattan-Regular.ttf)' --ap "_?dia[AB]$" --xsl ../tools/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "ku,sd,ur,wo,rhg" -s 'url(../results/Harmattan-Regular.ttf)' -s 'url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)' -s 'url(../results/Harmattan-Bold.ttf)'
tools/bin/absgenftml.py -t 'Kerning (NG)'          source/Harmattan-Regular.ufo  tests/Kern.ftml            -l tests/logs/Kerning.log                                                    --ap "_?dia[AB]$" --xsl ../tools/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "ku,sd,ur,wo,rhg" -s 'url(../results/Harmattan-Regular.ttf)' -s 'url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)' -s 'url(../results/Harmattan-Bold.ttf)'
tools/bin/absgenftml.py -t 'Yehbarree (NG)'        source/Harmattan-Regular.ufo  tests/Yehbarree.ftml       -l tests/logs/Yehbarree.log                                                  --ap "_?dia[AB]$" --xsl ../tools/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "ku,sd,ur,wo,rhg" -s 'url(../results/Harmattan-Regular.ttf)'   -s 'url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)' -s 'url(../results/Harmattan-Bold.ttf)'
