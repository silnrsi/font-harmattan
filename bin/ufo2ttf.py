#!/usr/bin/python

# Convert a UFO into a ttf file without OpenType tables
# using minimal processing (compared to fontmake)

# Copyright (c) 2017, SIL International (http://www.sil.org)
#
# This script is released under the terms of the MIT License.
# For details, see the full text of the license in the file LICENSE.

# The easiest way to install all the needed libraries is to install fontmake.
#   [sudo] pip install fontmake
# If you want to isolate all the libraries fontmake needs,
# you can install it in a virtual environment and run this script there

from __future__ import print_function
import sys
import defcon, ufo2ft.outlineCompiler

try:
    ufo_fn = sys.argv[1]
    ttf_fn = sys.argv[2]
except:
    print("ufo2ttf <ufo> <output ttf>")
    sys.exit()

PUBLIC_PREFIX = 'public.'

ufo = defcon.Font(ufo_fn)

# print('Converting UFO to ttf and compiling fea
# font = ufo2ft.compileTTF(ufo,
    # glyphOrder = ufo.lib.get(PUBLIC_PREFIX + 'glyphOrder'),
    # useProductionNames = False)

print('Converting UFO to ttf without OT')
outlineCompiler = ufo2ft.outlineCompiler.OutlineTTFCompiler(ufo,
    glyphOrder=ufo.lib.get(PUBLIC_PREFIX + 'glyphOrder'),
    convertCubics=True)
font = outlineCompiler.compile()

print('Saving ttf file')
font.save(ttf_fn)

print('Done')
