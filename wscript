#!/usr/bin/python3
# this is a smith configuration file for Harmattan font project

# override the default folders
DOCDIR = ['documentation', 'web']  # add 'web' to default
generated = 'generated/'

# set package name
APPNAME = 'Harmattan'

# set the font family name
FAMILY = APPNAME

# Get version info from Regular UFO; must be first function call:
getufoinfo('source/masters/' + FAMILY + '-Regular' + '.ufo')

ftmlTest('tools/ftml-smith.xsl')

# APs to omit:
omitaps = '--omitaps "_above,_below,_center,_ring,_through,_H,_L,_O,_U,_R,above,below,center,ring,through,H,L,O,U,R,entry,exit"'

# smith project-specific options:
#   --autohint - autohint the font
#   --norename - omit glyph rename step
#   --quick    - omit CA-based kerning in OpenType
#   --regOnly  - build just Harmattan-Regular
#   --graphite - add graphite smarts font for kerning update purposes (otherwise font is OT-only)
opts = preprocess_args({'opt': '--autohint'}, {'opt': '--quick'}, {'opt': '--norename'},  {'opt': '--regOnly'},  {'opt': '--medOnly'}, {'opt': '--graphite'})

noOTkern = ' -D noOTkern=yes' if '--quick' in opts else ''

cmds = [cmd('ttx -m ${DEP} -o ${TGT} ${SRC}', ['source/jstf.ttx'])]
extras = {}

if '--graphite' in opts:
    # If we're going to include graphite, then we need the complete typetuner source file.
    typetunerfile = 'source/typetuner/feat_all.xml'
    extras['graphite'] = gdl(generated + '${DS:FILENAME_BASE}.gdl',
        master = 'source/graphite/master.gdl',
        depends = ['source/graphite/cp1252.gdl', 
                   'source/graphite/HarFeatures.gdh', 
                   'source/graphite/HarGlyphs.gdh', 
                   'source/graphite/stddef.gdh'],
        make_params = omitaps + ' --cursive "exit=entry,rtl" --cursive "_digit=digit"',
        params = '-d -q -e ${DS:FILENAME_BASE}_gdlerr.txt',
        )
    # Be sure to include the octaboxes
    cmds.append(cmd('${OCTALAP} -m ${SRC} -o ${TGT} ${DEP}', ["source/graphite/${DS:FILENAME_BASE}-octabox.json"])),
else:
    # Without grahite, we use a subset of the typetuner file that contains no graphite table manipulation
    typetunerfile = create(generated + 'feat_all.xml', cmd('grep -v "gr_" ${SRC} > ${TGT}', ['source/typetuner/feat_all.xml']))

if '--norename' not in opts:
    cmds.append(cmd('psfchangettfglyphnames ${SRC} ${DEP} ${TGT}', ['${source}']))

# Note: ttfautohint-generated hints don't maintain stroke thickness at joins, so we're not hinting these fonts
# but if you want to try again:
if '--autohint' in opts:
    cmds.append(cmd('${TTFAUTOHINT} -n -c  -D arab -W ${DEP} ${TGT}'))

# iterate over designspace
designspace('source/Harmattan.designspace',
    instanceparams = '-l ' + generated + '${DS:FILENAME_BASE}_createintance.log',
    instances = ['Harmattan Regular'] if '--regOnly' in opts else ['Harmattan Medium'] if '--medOnly' in opts else None,
    target = process('${DS:FILENAME_BASE}.ttf', *cmds),
    ap = generated + '${DS:FILENAME_BASE}.xml',
    version = VERSION,  # Needed to ensure dev information on version string
    opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
        mapfile = generated + '${DS:FILENAME_BASE}.map',
        master = 'source/opentype/main.feax',
        make_params = omitaps + noOTkern,
        params = '-e -F kernposchain_0',
        depends = ['source/opentype/gsub.feax', 'source/opentype/gpos.feax', 
                   'source/opentype/customCollisionSubs.feax',
                   'source/opentype/customKerning.feax',
                   'source/opentype/customShifting.feax',]
        ),
    typetuner = typetuner(typetunerfile),
    classes = 'source/classes.xml',
    script = 'arab',
    pdf = fret(generated + '${DS:FILENAME_BASE}-fret.pdf', params='-b -r -o i -m 48'),
    woff = woff('web/${DS:FILENAME_BASE}.woff', params='-v ' + VERSION + ' -m ../source/${DS:FAMILYNAME}-WOFF-metadata.xml'),
    **extras
    )

def configure(ctx):
    ctx.find_program('octalap')
    ctx.find_program('ttfautohint')
