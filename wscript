#!/usr/bin/python
# this is a smith configuration file

# set the default output folders
out = "results"
DOCDIR = "documentation"
OUTDIR = "installers"
ZIPDIR = "releases"
TESTDIR = "tests"
TESTRESULTSDIR = "tests"
STANDARDS = "reference"

# set the font name, version, licensing and description
APPNAME = "Harmattan"
VERSION = "1.001"
BUILDVERSION = "1.001"
BUILDLABEL = "alpha1"

COPYRIGHT = """
Copyright (c) 2007-2008, The C&MA Guinea Fulbe Team;

Copyright renewed 2011-2012, George W. Nuss (http://www.fulbefouta.com),
with the Reserved Font Name \"Fouta\".

Copyright (c) 2004-2015, SIL International (http://scripts.sil.org),
with Reserved Font Names \'Andika\' and \'SIL\'.

Copyright (c) 2014-2016, SIL International (http://www.sil.org/).
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


for style in ('-Regular', '-Bold'):
   font(target=process(APPNAME + style + '.ttf'),
            source='source/' + APPNAME + style + '.ufo',
            version=VERSION,
            graphite=gdl('source/graphite/Harmattan.gdl',
                         depends=('source/graphite/cp1252.gdl', 'source/graphite/HarFeatures.gdh', 'source/graphite/HarGlyphs.gdh', 'source/graphite/stddef.gdh')),
            # opentype = fea('source/opentype/' + APPNAME + '.fea'),
            license=ofl('Harmattan', 'SIL'),
            script='arab',
            pdf=fret(params='-r'),
            woff=woff('web/Harmattan-Regular.woff', params='-v ' + VERSION + ' -m ../source/Harmattan-WOFF-metadata.xml'),
            typetuner='source/typetuner/feat_all.xml',
         )

def configure(ctx):
    ctx.find_program('ttfautohint')
