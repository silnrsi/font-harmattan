#!/usr/bin/python3
'generate linking classes for abs projects from glyph_data.csv'
__url__ = 'http://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2018,2020 SIL International  (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'Bob Hallissy'

import re
from silfont.core import execute
from palaso.unicode.ucd import get_ucd

argspec = [
    ('output',{'help': 'Output classes in XML format', 'nargs': '?'}, {'type': 'outfile', 'def': '_gen_classes.xml'}),
    ('-i','--input',{'help': 'Glyph info csv file'}, {'type': 'incsv', 'def': 'glyph_data.csv'}),
    ('-l','--log',{'help': 'Set log file name'}, {'type': 'outfile', 'def': '_classes.log'}),
]


def doit(args):
    logger = args.logger

    # Interate over glyph_data file looking for:
    #   Encoded glyphs whose USV shows they are Right- or Dual-joining
    #     Warn if their name has an extension
    #     Keep a list of right-joining and a list of dual-joining
    #   Unencoded chars with an extension .init, .medi, or .fina
    #     Keep a set of these for presence testing

    rjoining = set()    # names of all right-joining encoded glyphs
    djoining = set()    # names of all dual-joining encoded glyphs
    unencoded = set()   # names of all unencoded glyphs having .init, .medi, or .fina extensions
    glyphOrder = {}     # dictionary to record sort order of glyphs

    namesWithFormRE = re.compile(r'\.(init|medi|fina)')

    # Get headings from csvfile:
    incsv = args.input
    fl = incsv.firstline
    if fl is None: logger.log("Empty imput file", "S")
    # required columns:
    try:
        nameCol = fl.index('glyph_name');
        usvCol = fl.index('USV')
        orderCol = fl.index('DesignerOrder')
    except ValueError as e:
        logger.log('Missing csv input field: ' + e.message, 'S')
    except Exception as e:
        logger.log('Error reading csv input field: ' + e.message, 'S')
    next(incsv.reader, None)  # Skip first line with headers in


    # Process all records in glyph_data
    for line in incsv:
        gname = line[nameCol].strip()

        # things to ignore:
        if len(gname) == 0:
            logger.log('empty glyph name in glyph_data; ignored', 'W')
            continue
        if gname.startswith('#'):
            continue

        # Process USV
        # could be empty string, a single USV or space-separated list of USVs
        try:
            uidList = [int(x, 16) for x in line[usvCol].split()]
        except Exception as e:
            logger.log("invalid USV '{0}' ({1}); ignored.".format(line[usvCol], e.message), 'W')
            uidList = []

        if len(uidList) == 1:
            # Handle simple encoded glyphs
            uid = uidList[0]
            if get_ucd(uid, 'jt') in ('D','R'):
                if gname.find('.', 1) > 0:
                    logger.log("encoded glyph {0} has extensions -- be sure to check construction of joined forms".format(gname), 'W')
                if get_ucd(uid, 'jt') == 'R':
                    rjoining.add(gname)
                else:
                    djoining.add(gname)
                # remember glyph ordering for encoded glyphs
                glyphOrder[gname] = float(line[orderCol])
        elif len(uidList) == 0:
            # Handle unencoded glyphs
            if namesWithFormRE.search(gname):
                # This is an initial, medial, or final form -- remember it
                unencoded.add(gname)
                glyphOrder[gname] = float(line[orderCol])


    # First, find missing or mis-ordered glyphs
    # For this we have to order the glyphs as they will be in the font
    missing = []
    outOfOrder = []
    for joinType in ('Dual', 'Right'):
        glist = sorted(djoining if joinType == 'Dual' else rjoining, key=lambda x: glyphOrder[x])
        for form in (('init', 'medi', 'fina') if joinType == 'Dual' else ('fina',)):
            # compute list of contextual glyphs in same order
            glist2 = ['{0}.{1}'.format(x, form) for x in glist]
            # Check for missing or out-of-order glyphs
            lastGlyphOrder = None
            for gname in glist2:
                if gname not in glyphOrder:
                    missing.append(gname)
                else:
                    myOrder = glyphOrder[gname]
                    if lastGlyphOrder is not None and myOrder <= lastGlyphOrder:
                        outOfOrder.append(gname)
                    lastGlyphOrder = myOrder

    # Now output everything, even if missing or out of order
    # For this we sort glyphs alphabetically, and make sure lines aren't enormously long
    for joinType in ('Dual', 'Right'):
        glist = sorted(djoining if joinType == 'Dual' else rjoining)
        lines = []
        while len(glist):
            line = []
            linelgt = 0
            while len(glist) and linelgt < 120:
                gname = glist.pop(0)
                line.append(gname)
                linelgt += len(gname) +  6 # Allow for space in between, and .xxxx extension
            if len(line):
                lines.append(line)

        for form in (('isol', 'init', 'medi', 'fina') if joinType == 'Dual' else ('isol', 'fina')):
            clname = "{0}Link{1}".format(joinType, form.title())
            # Start xml element for class name
            args.output.write(u"    <class name='{0}'>\n".format(clname))
            for line in lines:
                if form != 'isol':
                    line = ['{0}.{1}'.format(x,form) for x in line]
                args.output.write(u'        {0}\n'.format(' '.join(line)))
            args.output.write(u'    </class>\n\n')

    # Emit warnings and errors
    if len(missing):
        logger.log("Missing contextual glyphs: " + ' '.join(missing), 'E')
    if len(outOfOrder):
        logger.log("The following glyphs are out of order: " + ' '.join(outOfOrder), 'E')

    args.output.close


def cmd() : execute(None,doit,argspec)
if __name__ == "__main__": cmd()