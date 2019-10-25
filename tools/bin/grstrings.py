#!/usr/bin/python3

import argparse, tempfile, os, sys
from palaso.font.graphite import gr2, grversion
from palaso.font.shape import GrFont
from fontTools import ttLib
import json

try:
    from glyphstring import Node, String, Position
except ModuleNotFoundError:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from glyphstring import Node, String, Position

def runtext(face, text):
    (fd, debug) = tempfile.mkstemp()
    os.close(fd)
    gr2.gr_start_logging(face.grface.face, debug.encode("utf-8"))
    glyphs = face.glyphs(text)
    gr2.gr_stop_logging(face.grface.face)
    with open(debug) as fh:
        jobj = json.load(fh)
    os.unlink(debug)
    return (glyphs, jobj)

def makestring(face, text):
    glyphs, jobj = runtext(face, text)
    s = String(text=text)
    curr = s.pre
    for g in jobj[-1]['output']:
        if 'collision' in g:
            f = g['collision']['flags']
            if (f & 17) == 17: # and g['collision']['offset'] != [0, 0]:
                curr = s.addNode(Node(keys=[g['gid']], positions=[Position(*g['collision']['offset'])],
                                      index=g['charinfo']['original']), curr)
                continue
        curr = s.addNode(Node(keys=[g['gid']], index=g['charinfo']['original']), curr)
    return s

if __name__ == '__main__':
    from multiprocessing import Pool, current_process

    def initprocess(fname, rtl):
        proc = current_process()
        proc.grface = GrFont(fname, rtl=(1 if rtl else 0))
    def proc_makestring(s):
        proc = current_process()
        return makestring(proc.grface, s)

    parser=argparse.ArgumentParser()
    parser.add_argument("outfile",help="Output file of results")
    parser.add_argument("-i","--input",action="append",help="Input test text file")
    parser.add_argument("-t","--text",action="store_true",help="Output text rather than binary")
    parser.add_argument("-f","--font",required=True,help="Path to font file")
    parser.add_argument("-d","--directory",action="append",default=[],help="Directories to search for input test files")
    parser.add_argument("-r","--rtl",action="store_true",help="Render strings rtl")
    args = parser.parse_args()

    pool = Pool(initializer=initprocess, initargs=[args.font, args.rtl])
    tt = ttLib.TTFont(args.font)
    cmap = tt.getGlyphOrder()
    strings = []
    for inf in args.input:
        for d in (['.'] + args.directory):
            fname = os.path.join(d, inf)
            if not os.path.exists(fname):
                continue
            with open(fname, "r") as fh:
                strings.extend([x.strip() for l in fh.readlines() for x in l.split()])
                break
    res = pool.imap_unordered(proc_makestring, strings)

    if args.text:
        with open(args.outfile, "w") as fh:
            for s in res:
                fh.write(s.asStr(cmap)+"\n")
    else:
        with open(args.outfile, "wb") as fh:
            for s in res:
                fh.write(s.asBytes())

