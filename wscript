#!/usr/bin/python3
# this is a smith configuration file for Harmattan font project

# override the default folders
DOCDIR = ['documentation', 'web']  # add 'web' to default
STANDARDS = 'tests/reference'
generated = 'generated/'

# set package name
APPNAME = 'Harmattan'

# set the font family name
FAMILY = APPNAME

DESC_SHORT = 'An Arabic script font designed for use by languages in West Africa'

# Get version info from Regular UFO; must be first function call:
getufoinfo('source/' + FAMILY + '-Regular' + '.ufo')
# BUILDLABEL = 'beta'

ftmlTest('tools/lib/ftml-smith.xsl')

# APs to omit:
omitaps = '--omitaps "_above,_below,_center,_ring,_through,_H,_L,_O,_U,_R,above,below,center,ring,through,H,L,O,U,R"'

opts = preprocess_args({'opt': '--quick'}, {'opt': '--norename'})

noOTkern = ' -D noOTkern=yes' if '--quick' in opts else ''

cmds = [cmd('../tools/octalap -m ${SRC} -o ${TGT} ${DEP}', 'source/${DS:FILENAME_BASE}-octabox.json')]
if '--norename' not in opts:
    cmds.append(cmd('psfchangettfglyphnames ${SRC} ${DEP} ${TGT}', ['source/${DS:FILENAME_BASE}.ufo']))
# Note: ttfautohint-generated hints don't maintain stroke thickness at joins, so we're not hinting these fonts
# cmds.append(cmd('${TTFAUTOHINT} -n -c  -D arab -W ${DEP} ${TGT}'))

# iterate over designspace
designspace('source/Harmattan-RB.designspace',
    instanceparams='-l ' + generated + '${DS:FILENAME_BASE}_createintance.log',
    target = process('${DS:FILENAME_BASE}.ttf', *cmds),
    ap = generated + '${DS:FILENAME_BASE}.xml',
    version=VERSION,  # Needed to ensure dev information on version string

    graphite=gdl(generated + '${DS:FILENAME_BASE}.gdl',
        master = 'source/graphite/master.gdl',
        depends = ['source/graphite/cp1252.gdl', 'source/graphite/HarFeatures.gdh', 'source/graphite/HarGlyphs.gdh', 'source/graphite/stddef.gdh'],
        make_params = omitaps + ' --cursive "exit=entry,rtl" --cursive "_digit=digit"',
        params = '-d -q -e ${DS:FILENAME_BASE}_gdlerr.txt',
        ),
    opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
        mapfile = generated + '${DS:FILENAME_BASE}.map',
        master = 'source/opentype/master.feax',
        make_params = omitaps + noOTkern,
        params = '-e -F kernposchain_0',
        ),
    typetuner = typetuner('source/typetuner/feat_all.xml'),
    classes = 'source/classes.xml',
    script='arab',
    pdf=fret(generated + '${DS:FILENAME_BASE}-fret.pdf', params='-b -r -o i -m 48'),
    woff=woff('web/${DS:FILENAME_BASE}.woff', params='-v ' + VERSION + ' -m ../source/${DS:FAMILYNAME}-WOFF-metadata.xml'),
    )

# def configure(ctx):
#    ctx.find_program('ttfautohint')
