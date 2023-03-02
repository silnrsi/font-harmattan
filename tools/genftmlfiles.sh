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

if [ ! -e results/flo_cache/Harmattan-Regular.woff ]
then
	# Cache the Regular font from FLO to use as the "previous font"
	echo "Retrieving FLO woff2 for comparison"
	mkdir -p results/flo_cache/
	wget -nv -P results/flo_cache/ "http://fonts.languagetechnology.org/fonts/sil/harmattan/web/Harmattan-Regular.woff"
	echo
fi

echo "Rebuilding ftml files..."
tools/absgenftml.py -q -t "AllChars (auto)"            source/masters/Harmattan-Regular.ufo  tests/AllChars-auto.ftml        -l logs/AllChars.log        --prevfont results/flo_cache/Harmattan-Regular.woff -s "url(../references/Harmattan-Regular-v1.ttf)|Reg ref" --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "AL Sorted (auto)"           source/masters/Harmattan-Regular.ufo  tests/ALsorted-auto.ftml        -l logs/ALsorted.log        --prevfont results/flo_cache/Harmattan-Regular.woff -s "url(../references/Harmattan-Regular-v1.ttf)|Reg ref" --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "DiacTest1 (auto)"           source/masters/Harmattan-Regular.ufo  tests/DiacTest1-auto.ftml       -l logs/DiacTest1.log       --prevfont results/flo_cache/Harmattan-Regular.woff                                                          --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" & 
tools/absgenftml.py -q -t "DiacTest1 Short (auto)"     source/masters/Harmattan-Regular.ufo  tests/DiacTest1-short-auto.ftml -l logs/DiacTest1-short.log --prevfont results/flo_cache/Harmattan-Regular.woff -s "url(../references/Harmattan-Regular-v1.ttf)|Reg ref" --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "Subtending Marks (auto)"    source/masters/Harmattan-Regular.ufo  tests/SubtendingMarks-auto.ftml -l logs/Subtending.log      --prevfont results/flo_cache/Harmattan-Regular.woff                                                          --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "DaggerAlef (auto)"          source/masters/Harmattan-Regular.ufo  tests/DaggerAlef-auto.ftml      -l logs/DaggerAlef.log      --prevfont results/flo_cache/Harmattan-Regular.woff -s "url(../references/Harmattan-Regular-v1.ttf)|Reg ref" --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "Kerning (auto)"             source/masters/Harmattan-Regular.ufo  tests/Kern-auto.ftml            -l logs/Kerning.log         --prevfont results/flo_cache/Harmattan-Regular.woff                                                          --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "Yehbarree (auto)"           source/masters/Harmattan-Regular.ufo  tests/Yehbarree-auto.ftml       -l logs/Yehbarree.log       --prevfont results/flo_cache/Harmattan-Regular.woff                                                          --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bold-Gr" &
tools/absgenftml.py -q -t "Feature-Language Interactions (auto)" \
                                                	   source/masters/Harmattan-Regular.ufo  tests/FeatLang-auto.ftml        -l tests/logs/FeatLang.log  --prevfont results/flo_cache/Harmattan-Regular.woff                                                          --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT"                                                 &
tools/absgenftml.py -q -t "KernData with Marks (auto)" source/masters/Harmattan-Regular.ufo  source/kerndata.ftml            -l source/logs/kerndata.log --norendercheck       -f h                                                                                   --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv                              -w 75% -s "url(../results/Harmattan-Regular.ttf)|Reg-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf)|Reg-OT" -s "url(../results/Harmattan-Bold.ttf)|Bld-Gr" -s "url(../results/tests/ftml/fonts/Harmattan-Bold_ot_arab.ttf)|Bld-OT" &
wait
echo done.
