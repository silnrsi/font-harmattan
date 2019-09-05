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

DESC_NAME = "Harmattan"
DESC_SHORT = "An Arabic script font designed for use by languages in West Africa"

DEBPKG = 'fonts-sil-harmattan'

# Get version info from Regular UFO; must be first function call:
getufoinfo('source/' + FAMILY + '-Regular' + '.ufo')
# BUILDLABEL = 'beta'

ftmlTest('tests/ftml-smith.xsl', fonts = ['../references/Harmattan-Regular-1_001.ttf'], addfontindex = 1, fontmode = 'collect')

# APs to omit:
OMITAPS = '--omitaps "_above,_below,_center,_ring,_through,_H,_L,_O,_U,_R,above,below,center,ring,through,H,L,O,U,R"'

# iterate over designspace
designspace('source/Harmattan-RB.designspace',
    instanceparams='-l ' + generated + '${DS:FILENAME_BASE}_createintance.log',
    target = process('${DS:FILENAME_BASE}.ttf',
        cmd('${PSFCHANGETTFGLYPHNAMES} ${SRC} ${DEP} ${TGT}', ['source/${DS:FILENAME_BASE}.ufo']),
#        Note: ttfautohint-generated hints don't maintain stroke thickness at joins, so we're not hinting these fonts
#        cmd('${TTFAUTOHINT} -n -c  -D arab -W ${DEP} ${TGT}')
    ),
    ap = generated + '${DS:FILENAME_BASE}.xml',
    version=VERSION,  # Needed to ensure dev information on version string

    graphite=gdl(generated + '${DS:FILENAME_BASE}.gdl',
        depends=['source/graphite/cp1252.gdl', 'source/graphite/HarFeatures.gdh', 'source/graphite/HarGlyphs.gdh', 'source/graphite/stddef.gdh'],
        master = 'source/graphite/master.gdl',
        make_params = OMITAPS + ' --cursive "exit=entry,rtl" --cursive "_digit=digit"',
        params = '-q -e ${DS:FILENAME_BASE}_gdlerr.txt',
        ),
    opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
        mapfile = generated + "${DS:FILENAME_BASE}.map",
        master = 'source/opentype/master.feax',
        make_params = OMITAPS,
        ),
    typetuner = typetuner("source/typetuner/feat_all.xml"),
    classes = 'source/classes.xml',
    script='arab',
    pdf=fret(generated + '${DS:FILENAME_BASE}-fret.pdf', params='-r -o i -m 48'),
    woff=woff('web/${DS:FILENAME_BASE}.woff', params='-v ' + VERSION + ' -m ../source/${DS:FAMILYNAME}-WOFF-metadata.xml'),
    )

def configure(ctx):
    ctx.find_program('psfchangettfglyphnames')
#    ctx.find_program('ttfautohint')

