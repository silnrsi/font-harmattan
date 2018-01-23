#!/usr/bin/python
# this is a smith configuration file

# set the default output folders
out = "results"
DOCDIR = ["documentation", "web"]
OUTDIR = "installers"
ZIPDIR = "releases"
TESTDIR = "tests"
TESTRESULTSDIR = "tests"
STANDARDS = "reference"

# set the font name, version, licensing and description
APPNAME = "Harmattan"
VERSION = "1.020"
# BUILDLABEL = "alpha1"

COPYRIGHT = """
Copyright (c) 2007-2008, The C&MA Guinea Fulbe Team;

Copyright renewed 2011-2012, George W. Nuss (http://www.fulbefouta.com),
with the Reserved Font Name \"Fouta\".

Copyright (c) 2004-2015, SIL International (http://scripts.sil.org),
with Reserved Font Names \'Andika\' and \'SIL\'.

Copyright (c) 2014-2017, SIL International (http://www.sil.org/).
with Reserved Font Names \"Harmattan\" and \"SIL\".
"""

LICENSE = 'OFL.txt'

DESC_NAME = "Harmattan"
DESC_SHORT = "Smart Unicode Arabic font for West African languages"
DESC_LONG = """
Harmattan, named after the trade winds that blow during the winter in West
Africa, is designed in a Warsh style to suit the needs of languages using
the Arabic script in West Africa.

The font does not cover the full Unicode Arabic repertoire. It only supports
characters known to be used by languages in West Africa.

This font makes use of state-of-the-art font technologies to support complex
typographic issues. Font smarts are implemented using OpenType and Graphite
technologies.

This font provides a simplified rendering of Arabic script, using basic
connecting glyphs but not including a wide variety of additional ligatures
or contextual alternates (only the required lam-alef ligatures). This
simplified style is often preferred for clarity, especially in non-Arabic
languages, but may be considered unattractive in more traditional and
literate communities.

Harmattan is currently available in Regular weight only. The Bold is in progress.

Font sources are published in the repository and a smith open workflow is
used for building, testing and releasing.
"""
DEBPKG = 'fonts-sil-harmattan'

ftmlTest('tests/ftml-padauk.xsl', fonts = ['../references/Harmattan-Regular-1_001.ttf'], addfontindex = 1, fontmode = 'collect')

# APs to omit:
OMITAPS = '--omitaps "_above,_below,_center,_ring,_through,above,below,center,ring,through,U,L"'

for style in ('-Regular', '-Bold'):
    UFO = 'source/' + APPNAME + style + '.ufo'
    font(target=process(APPNAME + style + '.ttf', 
            cmd('${PSFCHANGETTFGLYPHNAMES} ${SRC} ${DEP} ${TGT}', [UFO]),
            cmd('${TTFFEATPARMS} -c ${SRC} ${DEP} ${TGT}', ['source/opentype/OTFeatParms.xml'])
            ),
        source=UFO,
        ap = APPNAME + style + '.xml',
        version=VERSION,
        graphite=gdl(APPNAME + style + '.gdl',
            depends=['source/graphite/cp1252.gdl', 'source/graphite/HarFeatures.gdh', 'source/graphite/HarGlyphs.gdh', 'source/graphite/stddef.gdh'],
            master = 'source/graphite/master.gdl',
            make_params = OMITAPS + ' --cursive "exit=entry,rtl" --cursive "_digit=digit"'),
        opentype = fea(APPNAME + style + '.fea', 
            master = 'source/opentype/master.feax',
            make_params = OMITAPS),
        classes = 'source/classes.xml',
        license=ofl('Harmattan', 'SIL'),
        script='arab',
        pdf=fret(params='-r'),
        woff=woff('web/' + APPNAME + style + '.woff', params='-v ' + VERSION + ' -m ../source/' + APPNAME + '-WOFF-metadata.xml'),
#        typetuner='source/typetuner/feat_all.xml'
        )

AUTOGEN_TESTS = ['Empty', 'AllChars', 'DiacTest1', 'Mirrored', 'SubtendingMarks', 'DaggerAlef', 'Kern' ]

# Until we figure out how to save a copy of the font prior to glyph name changes, commenting this out:
# for testname in AUTOGEN_TESTS:
#    t = create(testname + '.ftml', cmd('perl ${SRC[0]} -t ' + testname + ' -g -f h -r local(Harmattan) -r url(../results/Harmattan-Regular.ttf) -r url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf) -r url(../results/Harmattan-Bold.ttf) ${SRC[1]} ${SRC[2]}', 
#         ['tools/bin/absGenFTML', '../results/' + APPNAME + '-Regular-wn.ttf', APPNAME + '-Regular.xml', 'tools/absGlyphList/absGlyphList.csv']))

def configure(ctx):
    ctx.find_program('psfchangettfglyphnames')
    ctx.find_program('ttffeatparms')
#    ctx.find_program('ttfautohint')

