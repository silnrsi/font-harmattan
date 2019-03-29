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

# set the font family name
FAMILY = APPNAME

# licensing will eventually be obtained from UFO
COPYRIGHT = """
Copyright (c) 2007-2008, The C&MA Guinea Fulbe Team;

Copyright renewed 2011-2012, George W. Nuss (http://www.fulbefouta.com),
with the Reserved Font Name \"Fouta\".

Copyright (c) 2004-2019, SIL International (http://www.sil.org),
with Reserved Font Names \'Andika\' and \'SIL\'.

Copyright (c) 2014-2019, SIL International (http://www.sil.org/).
with Reserved Font Names \"Harmattan\" and \"SIL\".
"""
LICENSE = 'OFL.txt'

DESC_NAME = "Harmattan"
DESC_SHORT = "An Arabic script font designed for use by languages in West Africa"
# LONG_DESC now to be obtained from FONTLOG

DEBPKG = 'fonts-sil-harmattan'

# Get version info from Regular UFO; must be first function call:
getufoinfo('source/' + FAMILY + '-Regular' + '.ufo')

ftmlTest('tests/ftml-padauk.xsl', fonts = ['../references/Harmattan-Regular-1_001.ttf'], addfontindex = 1, fontmode = 'collect')

# APs to omit:
OMITAPS = '--omitaps "_above,_below,_center,_ring,_through,above,below,center,ring,through,U,L,O"'

# iterate over designspace
designspace('source/Harmattan-RB.designspace',
    params = '-l ${DS:FILENAME_BASE}_createintance.log',
    target = process('${DS:FILENAME_BASE}.ttf',
        cmd('${PSFCHANGETTFGLYPHNAMES} ${SRC} ${DEP} ${TGT}', ['source/${DS:FILENAME_BASE}.ufo']),
        cmd('${TYPETUNER} -o {$TGT} add ${SRC} ${DEP}', [ create( generated + '${DS:FILENAME_BASE}_feat.xml', 
        	cmd('${PSFTUNERALIASES} -m '+ generated + '${DS:FILENAME_BASE}.map -f ${DS:FILENAME_BASE}.ttf ${SRC} ${TGT}', ['source/typetuner/feat_all.xml'], late=1))], late=1),
        # cmd('${TTFAUTOHINT} -n -c  -D arab -W ${DEP} ${TGT}')
    ),
    ap = generated + '${DS:FILENAME_BASE}.xml',
    version=VERSION,

    graphite=gdl(generated + '${DS:FILENAME_BASE}.gdl',
        depends=['source/graphite/cp1252.gdl', 'source/graphite/HarFeatures.gdh', 'source/graphite/HarGlyphs.gdh', 'source/graphite/stddef.gdh'],
        master = 'source/graphite/master.gdl',
        make_params = OMITAPS + ' --cursive "exit=entry,rtl" --cursive "_digit=digit"',
        params = '-q -e ${DS:FILENAME_BASE}_gdlerr.txt',
        ),
    opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
        master = 'source/opentype/master.feax',
        make_params = OMITAPS,
        params = '-m ' + generated + '${DS:FILENAME_BASE}.map',
        ),
    classes = 'source/classes.xml',
    license=ofl('Harmattan', 'SIL'),
    script='arab',
    pdf=fret(params='-r'),
    woff=woff('web/${DS:FILENAME_BASE}.woff', params='-v ' + VERSION + ' -m ../source/${DS:FAMILYNAME}-WOFF-metadata.xml'),
    )

def configure(ctx):
    ctx.find_program('psfchangettfglyphnames')
    ctx.find_program('typetuner')
    ctx.find_program('psftuneraliases')
#    ctx.find_program('ttfautohint')

