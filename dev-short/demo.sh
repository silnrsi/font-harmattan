#!/bin/sh

# put results in a subfolder
mkdir -p results

# Parse ftml and create raw data list
../tools/bin/grstrings.py -i kerntext.ftml -t -f ../results/Harmattan-Regular.ttf -r results/rawPairData-ftml.txt

# Trace graphite to get kerning data

# Phase 0:
../tools/bin/glyphstring.py -f ../results/Harmattan-Regular.ttf  -r 20 -j 1 -e 0    results/rawPairData-ftml.txt results/kernStrings-e0.txt

# Phase 1:
../tools/bin/glyphstring.py -f ../results/Harmattan-Regular.ttf  -r 20 -j 1 -e 1    results/rawPairData-ftml.txt results/kernStrings-e1.txt

# Phase 2:
../tools/bin/glyphstring.py -f ../results/Harmattan-Regular.ttf  -r 20 -j 1 -e 2    results/rawPairData-ftml.txt results/kernStrings-e2.txt

# Phase 3: generate fea
../tools/bin/glyphstring.py -f ../results/Harmattan-Regular.ttf  -r 20 -j 1      -R results/rawPairData-ftml.txt results/caKern.fea

# Copy result to source folder so project will compile with shortened version:
cp results/caKern.fea ../source/opentype