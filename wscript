#!/usr/bin/python
# this is a smith configuration file

# set the default output folders
out = "results"  # default is currently buildlinux2
DOCDIR = ["documentation", "web"]  # add "web" to default
OUTDIR = "installers"  # until these are defaults in smith itself we need to keep them
ZIPDIR = "releases"
TESTDIR = "tests"
TESTRESULTSDIR = "tests"
STANDARDS = "references"  # default is "reference"
generated = "generated/"

# set package name
APPNAME = "Harmattan"
VERSION = "1.024"  # Eventually this will be obtained from UFO

# set the font family name
FAMILY = APPNAME

# licensing will eventually be obtained from UFO
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
# LONG_DESC now to be obtained from FONTLOG

DEBPKG = 'fonts-sil-harmattan'

ftmlTest('tests/ftml-padauk.xsl', fonts = ['../references/Harmattan-Regular-1_001.ttf'], addfontindex = 1, fontmode = 'collect')

# APs to omit:
OMITAPS = '--omitaps "_above,_below,_center,_ring,_through,above,below,center,ring,through,U,L"'

for style in ('-Regular', '-Bold'):
    UFO = 'source/' + FAMILY + style + '.ufo'
    font(target=process(FAMILY + style + '.ttf', 
            cmd('${PSFCHANGETTFGLYPHNAMES} ${SRC} ${DEP} ${TGT}', [UFO]),
            cmd('${TTFFEATPARMS} -c ${SRC} ${DEP} ${TGT}', ['source/opentype/OTFeatParms.xml'])
            ),
        source=UFO,
        ap = generated + FAMILY + style + '.xml',
        version=VERSION,
        graphite=gdl(generated + FAMILY + style + '.gdl',
            depends=['source/graphite/cp1252.gdl', 'source/graphite/HarFeatures.gdh', 'source/graphite/HarGlyphs.gdh', 'source/graphite/stddef.gdh'],
            master = 'source/graphite/master.gdl',
            make_params = OMITAPS + ' --cursive "exit=entry,rtl" --cursive "_digit=digit"',
            params = '-q',
            ),
        opentype = fea(FAMILY + style + '.fea', 	# Would like to prefix generated but smith won't build at present (smith issue #45)
            master = 'source/opentype/master.feax',
            make_params = OMITAPS,
            to_ufo = True,
            ),
        classes = 'source/classes.xml',
        license=ofl('Harmattan', 'SIL'),
        script='arab',
        pdf=fret(params='-r'),
        woff=woff('web/' + FAMILY + style + '.woff', params='-v ' + VERSION + ' -m ../source/' + FAMILY + '-WOFF-metadata.xml'),
#        typetuner='source/typetuner/feat_all.xml'
        )

AUTOGEN_TESTS = ['Empty', 'AllChars', 'DiacTest1', 'Mirrored', 'SubtendingMarks', 'DaggerAlef', 'Kern' ]

# Until we figure out how to save a copy of the font prior to glyph name changes, commenting this out:
# for testname in AUTOGEN_TESTS:
#    t = create(testname + '.ftml', cmd('perl ${SRC[0]} -t ' + testname + ' -g -f h -r local(Harmattan) -r url(../results/Harmattan-Regular.ttf) -r url(../results/tests/ftml/fonts/Harmattan-Regular_ot_arab.ttf) -r url(../results/Harmattan-Bold.ttf) ${SRC[1]} ${SRC[2]}', 
#         ['tools/bin/absGenFTML', '../results/' + FAMILY + '-Regular-wn.ttf', FAMILY + '-Regular.xml', 'tools/absGlyphList/absGlyphList.csv']))

def configure(ctx):
    ctx.find_program('psfchangettfglyphnames')
    ctx.find_program('ttffeatparms')
#    ctx.find_program('ttfautohint')

