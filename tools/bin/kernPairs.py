#!/usr/bin/env python
'generate ftml tests from glyph_data.csv and UFO'
__url__ = 'http://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2018 SIL International  (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'Bob Hallissy'

import re
from silfont.core import execute
import silfont.ftml_builder as FB
from palaso.unicode.ucd import get_ucd

try:
    str = unicode
    chr = unichr
except NameError: # Will  occur with Python 3
    pass

argspec = [
    ('ifont',{'help': 'Input UFO'}, {'type': 'infont'}),
#    ('output',{'help': 'Output text file', 'nargs': '?'}, {'type': 'outfile', 'def': 'kernStrings.txt'}),
    ('-i','--input',{'help': 'Glyph info csv file'}, {'type': 'incsv', 'def': 'glyph_data.csv'}),
    ('-f','--fontcode',{'help': 'letter to filter for glyph_data'},{}),
    ('-l','--log',{'help': 'Set log file name'}, {'type': 'outfile', 'def': '_ftml.log'}),
    ('--langs',{'help':'List of bcp47 language tags', 'default': None}, {}),
    ('--rtl', {'help': 'enable right-to-left features', 'action': 'store_true'}, {}),
    ('--ap', {'help': 'regular expression describing APs to examine', 'default': '.'}, {}),
    ('--xsl', {'help': 'XSL stylesheet to use'}, {}),
]


joinSortKey = {
    'Ain' : 1,
    'Alef' : 2,
    'Beh' : 3,
    'Yeh' : 4, 'Farsi_Yeh' :4 , # Near Beh Due To Medial Form
    'Noon' :5, 'African_Noon' : 5,  # Near Yeh Due To Medial Form
    'Nya' : 6,  # Near Noon Due To Final Form
    'Sad' : 7,  # Near Noon Due To Final Form
    'Seen' : 8,
    'Yeh_With_Tail' : 9,
    'Rohingya_Yeh' : 10,
    'Yeh_Barree' : 11, 'Burushaski_Yeh_Barree' : 11,
    'Dal' : 12,
    'Feh' : 13, 'African_Feh' : 13,
    'Gaf' : 14, 'Kaf' : 14,
    'Swash_Kaf' :15 ,
    'Hah' : 16,
    'Heh' : 17,
    'Heh_Goal' : 18,
    'Teh_Marbuta' : 19, 'Teh_Marbuta_Goal' : 19,
    'Knotted_Heh' :20,
    'Lam' : 21,
    'Meem' : 22,
    'Qaf' : 23, 'African_Qaf' : 23,
    'Reh' :24 ,
    'Tah' : 26,
    'Waw' : 27,
    'Straight_Waw' : 28,
}

def doit(args):
    logger = args.logger

    # Read input csv
    builder = FB.FTMLBuilder(logger, incsv = args.input, fontcode = args.fontcode, font = args.ifont, ap = args.ap,
                             rtlenable = True, langs = args.langs)

    # Override default base (25CC) for displaying combining marks
    builder.diacBase = 0x0628   # beh

    # Initialize plaintext document:
    with open('kernStrings.txt','w',encoding='utf8') as fh:
        rehs = sorted(filter(lambda uid: get_ucd(uid,'jg') == 'Reh', builder.uids() ))
        uids = filter(lambda uid: get_ucd(uid, 'jt') in ('D', 'R'), builder.uids())
        uids = sorted(uids, key=lambda uid: joinSortKey.get(get_ucd(uid, 'jg'), 99) * 65536 + uid)
#        waws = sorted(filter(lambda uid: get_ucd(uid,'jg') == 'Waw', builder.uids()))
        zwj  = chr(0x200D)   # Zero width joiner
#        ma = chr(0x064B)     # Mark above (fathatan)
#        mb = chr(0x064D)     # Mark below (kasratan)

        for uid1 in rehs: # (rehs[0],)
            c1 = chr(uid1)
            for uid2 in uids:
                c2 = chr(uid2)
#                for featlist in builder.permuteFeatures(uids=(uid1,uid2)):
#                    ftml.setFeatures(featlist)
                # fh.write(f'{uid1:04X}+{uid2:04X}: ')
                if get_ucd(uid2, 'jt') == 'D':
                    fh.write(zwj + c1 + c2 + zwj + ' ')
                    fh.write(      c1 + c2 + zwj + ' ')
                fh.write(    zwj + c1 + c2       + ' ')
                fh.write(          c1 + c2       + '\n')
#                ftml.clearFeatures()



def cmd() : execute("UFO",doit,argspec)
if __name__ == "__main__": cmd()
