#!/bin/sh

# This script rebuilds the algorithmically-generated ftml files. See README.md

# Copyright (c) 2020-2022 SIL International  (http://www.sil.org)
# Released under the MIT License (http://opensource.org/licenses/

# Assumes we"re in the root folder, i.e., font-harmattan

set -e

if [ ! -e OFL.txt ] 
then
	echo "Please cd to root of font project to use this script"
	exit 2
fi

echo "Rebuilding ftml files..."
tools/absgenftml.py -q -t "AllChars (auto)"         source/Harmattan-Regular.ufo  tests/AllChars-auto.ftml        -l logs/AllChars.log         -s "url(../references/Harmattan-Regular-v1.ttf)|Reg ref" --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "AL Sorted (auto)"        source/Harmattan-Regular.ufo  tests/ALsorted-auto.ftml        -l logs/ALsorted.log         -s "url(../references/Harmattan-Regular-v1.ttf)|Reg ref" --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "DiacTest1 (auto)"        source/Harmattan-Regular.ufo  tests/DiacTest1-auto.ftml       -l logs/DiacTest1.log                                                                 --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" & 
tools/absgenftml.py -q -t "DiacTest1 Short (auto)"  source/Harmattan-Regular.ufo  tests/DiacTest1-short-auto.ftml -l logs/DiacTest1-short.log  -s "url(../references/Harmattan-Regular-v1.ttf)|Reg ref" --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "Subtending Marks (auto)" source/Harmattan-Regular.ufo  tests/SubtendingMarks-auto.ftml -l logs/Subtending.log                                                                --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "DaggerAlef (auto)"       source/Harmattan-Regular.ufo  tests/DaggerAlef-auto.ftml      -l logs/DaggerAlef.log       -s "url(../references/Harmattan-Regular-v1.ttf)|Reg ref" --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "Kerning (auto)"          source/Harmattan-Regular.ufo  tests/Kern-auto.ftml            -l logs/Kerning.log                                                                   --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "Yehbarree (auto)"        source/Harmattan-Regular.ufo  tests/Yehbarree-auto.ftml       -l logs/Yehbarree.log                                                                 --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "Feature-Language Interactions (auto)" \
                                                	source/Harmattan-Regular.ufo tests/FeatLang-auto.ftml         -l tests/logs/FeatLang.log                                                            --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" &
wait
echo done.
