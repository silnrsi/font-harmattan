#!/bin/sh

# Assumes we're in a folder one level below root, e.g., font-harmattan/dev

# Parse ftml and create raw data list
echo reading ../tests/kerndata.ftml...
../tools/bin/grstrings.py -i ../tests/kerndata.ftml -t -f ../results/Harmattan-Regular.ttf -r rawPairData-ftml.txt

# Trace graphite to get kerning data

# Phase 0:
# ../tools/bin/glyphstring.py -f ../results/Harmattan-Regular.ttf  -r 20 -j 1 -e 0    rawPairData-ftml.txt results/kernStrings-e0.txt

# Phase 1:
# ../tools/bin/glyphstring.py -f ../results/Harmattan-Regular.ttf  -r 20 -j 1 -e 1    rawPairData-ftml.txt results/kernStrings-e1.txt

# Phase 2:
# echo generating -e2 output...
# ../tools/bin/glyphstring.py -f ../results/Harmattan-Regular.ttf  -r 20 -j 1 -e 2    rawPairData-ftml.txt results/kernStrings-e2.txt

# Phase 3: generate fea
echo generating fea output...
../tools/bin/glyphstring.py -f ../results/Harmattan-Regular.ttf  -r 20 -j 1      -R rawPairData-ftml.txt caKern.fea

# Copy result to source folder so project will compile with shortened version:
echo updating mark references and copying results to source tree...
sed -e s/kasratan-ar/@_diaB/g -e s/fathatan-ar/@_diaA/g caKern.fea > ../source/opentype/caKern.fea


# check the results (only works if RHS is one glyph)
# echo Number of potential problems:
# ../tools/bin/splitResults.py kernStrings-e2.txt kernStrings-flattened-check.txt | wc -l