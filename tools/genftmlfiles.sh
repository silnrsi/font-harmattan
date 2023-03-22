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

prevfont="references/v2.000/Harmattan-Regular.ttf"
prevver="2.0"

echo "Rebuilding ftml files..."
tools/absgenftml.py -q -t "AllChars (auto)"                      source/masters/Harmattan-Regular.ufo  tests/AllChars-auto.ftml        -l logs/AllChars.log        --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../$prevfont)|$prevver"  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Medium.ttf)|Med" -s "url(../results/Harmattan-SemiBold.ttf)|SeBld" -s "url(../results/Harmattan-Bold.ttf)|Bold" &
tools/absgenftml.py -q -t "AL Sorted (auto)"                     source/masters/Harmattan-Regular.ufo  tests/ALsorted-auto.ftml        -l logs/ALsorted.log        --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75%                                  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Bold.ttf)|Bold"  &
tools/absgenftml.py -q -t "DiacTest1 (auto)"                     source/masters/Harmattan-Regular.ufo  tests/DiacTest1-auto.ftml       -l logs/DiacTest1.log       --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75%                                  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Bold.ttf)|Bold"  &
tools/absgenftml.py -q -t "DiacTest1 Short (auto)"               source/masters/Harmattan-Regular.ufo  tests/DiacTest1-short-auto.ftml -l logs/DiacTest1-short.log --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../$prevfont)|$prevver"  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Medium.ttf)|Med" -s "url(../results/Harmattan-SemiBold.ttf)|SeBld" -s "url(../results/Harmattan-Bold.ttf)|Bold" &
tools/absgenftml.py -q -t "Subtending Marks (auto)"              source/masters/Harmattan-Regular.ufo  tests/SubtendingMarks-auto.ftml -l logs/Subtending.log      --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75%                                  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Bold.ttf)|Bold"  &
tools/absgenftml.py -q -t "DaggerAlef (auto)"                    source/masters/Harmattan-Regular.ufo  tests/DaggerAlef-auto.ftml      -l logs/DaggerAlef.log      --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../$prevfont)|$prevver"  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Bold.ttf)|Bold"  &
tools/absgenftml.py -q -t "Yehbarree (auto)"                     source/masters/Harmattan-Regular.ufo  tests/Yehbarree-auto.ftml       -l logs/Yehbarree.log       --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../$prevfont)|$prevver"  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Bold.ttf)|Bold"  &
tools/absgenftml.py -q -t "Feature-Language Interactions (auto)" source/masters/Harmattan-Regular.ufo  tests/FeatLang-auto.ftml        -l tests/logs/FeatLang.log  --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../$prevfont)|$prevver"  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Bold.ttf)|Bold"  &
tools/absgenftml.py -q -t "Kerning (auto)"                       source/masters/Harmattan-Regular.ufo  tests/Kern-auto.ftml            -l logs/Kerning.log         --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv --langs "sd,ur,ku,rhg,ky,wo" -w 75% -s "url(../$prevfont)|$prevver"  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Medium.ttf)|Med" -s "url(../results/Harmattan-SemiBold.ttf)|SeBld" -s "url(../results/Harmattan-Bold.ttf)|Bold" &
# tools/absgenftml.py -q -t "KernData with Marks (auto)"           source/masters/Harmattan-Regular.ufo  source/kerndata.ftml            -l source/logs/kerndata.log --prevfont "$prevfont"  --ap "_?dia[AB]$" --xsl ../tools/lib/ftml.xsl --scale 250 -i source/glyph_data.csv    --norendercheck    -f h   -w 75% -s "url(../$prevfont)|$prevver"  -s "url(../results/Harmattan-Regular.ttf)|Reg" -s "url(../results/Harmattan-Medium.ttf)|Med" -s "url(../results/Harmattan-SemiBold.ttf)|SeBld" -s "url(../results/Harmattan-Bold.ttf)|Bold" &
wait
echo done.
