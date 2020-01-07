#!/usr/bin/python3

from struct import pack
from collections import namedtuple
import re, struct, os
import numpy as np
from sklearn.cluster.hierarchical import ward_tree
import logging as log

def skipws(s, i):
    while i < len(s):
        if s[i] not in " \t\n":
            break
        i += 1
    return i

def remove_duplicates(b):
    i = 1
    while i < len(b):
        if b[i-1] == b[i]:
            b.pop(i)
        else:
            i += 1
    return b

class Collection(object):
    ''' Collections for one glyph '''
    def __init__(self):
        self.gidmap = {}

    def addString(self, s, rounding=0):
        k = s.match[0].keystr(rounding=1)
        self.gidmap.setdefault(k, []).append(s)

    def _get_children(self, n, X, children, n_leaves):
        # calculate node centres
        res = []
        if n < n_leaves:
            return [X[n]]
        for j in range(2):
            m = children[n-n_leaves][j]
            if m >= n_leaves:
                res.extend(self._get_children(m, X, children, n_leaves))
            else:
                res.append(X[m])
        return res

    def round(self, rounding, k):
        ''' Apply clustering '''
        X = np.array([(int(x[0]), int(x[1])) for x in ((y[y.find(":")+1:]+",0").split(",") for y in self.gidmap.keys())])
        (children, _, n_leaves, parents, distances) = ward_tree(X, return_distance = True)
        done = set()
        res = []
        for i in range(len(distances)):
            if distances[i] > rounding:
                for j in range(2):
                    c = children[i][j]
                    if c not in done:
                        res.append(c)
                done.add(i+n_leaves)
        nodes = [self._get_children(x, X, children, n_leaves) for x in res]
        centres = [((min(x, key=lambda y:y[0])[0] + max(x, key=lambda y:y[0])[0]) // 2, 
                    (min(x, key=lambda y:y[1])[1] + max(x, key=lambda y:y[1])[1]) // 2) for x in nodes]
        for i, n in enumerate(nodes):
            if any(x[0] == 0 and x[1] == 0 for x in n):
                centres[i] = (0, 0)
        newmap = {}
        for i in range(len(nodes)):
            key = "{}:{},{}".format(k, centres[i][0], centres[i][1])
            newmap[key] = []
            for v in nodes[i]:
                dat = self.gidmap["{}:{},{}".format(k, v[0], v[1])]
                newmap[key].extend(dat)
                for s in dat:
                    s.match[0].positions[0] = Position(*centres[i])
        self.gidmap = newmap

    def process(self, k, rounding):
        ''' Remove small positioned strings, duplicates; cluster and reduce '''
        if rounding > 0:
            self.stripSmalls(rounding)
        self.stripDuplicates()
        if len(self.gidmap) > 1:
            self.round(rounding, k)
        return (len(self.gidmap), self.reduce())

    def stripDuplicates(self):
        for k, v in self.gidmap.items():
            self.gidmap[k] = remove_duplicates(sorted(v, key=lambda x:x.key()))

    def stripSmalls(self, rounding):
        ''' Remove any string that has positions < rounding close to 0 '''
        newmap = {}
        for k, v in self.gidmap.items():
            for s in v:
                if s.testPos(rounding):
                    newmap.setdefault(k, []).append(s)
        self.gidmap = newmap

    def reduce(self):
        ''' Reduce rules to their minimum context and remove rules covered by others '''
        res = {}
        for k, v in sorted(self.gidmap.items(), key=lambda x:len(x[1])):
            if k.endswith(":0,0"):
                continue
            res[k] = []
            for r in v:
                if any(t.isSubsetOf(r) for t in res[k]):
                    continue
                res[k].append(r)
#                lengths = [len(r.pre)+len(r.post)+3] * (len(r.post) + 1)
#                for s in range(len(r.post)+1):
#                    for p in range((1 if len(r.pre) else 0),len(r.pre)+1):
#                        if self.isUnique(k, r, p, s):
#                            lengths[s] = p
#                            break
#                best = min(enumerate(lengths), key=lambda x: (x[1], -x[0]))
#                res[k].append(String(pre=r.pre[-best[1]:], post=r.post[:best[0]], match=r.match))
        return res

    def isUnique(self, key, rule, prelen, postlen):
        ''' Returns whether a rule context is unique in this collection '''
        for k, v in self.gidmap.items():
            if k == key:
                continue
            for r in v:
                if len(r.pre) < prelen or len(r.post) < postlen:
                    continue
                if r.pre[-prelen:] == rule.pre[-prelen:] and r.post[:postlen] == rule.post[:postlen]:
                    return False
        return True

class String(object):
    def __init__(self, pre=None, post=None, match=None, text=None):
        self.pre = pre or []
        self.post = post or []
        self.match = match or []
        self.text = text
        self.gnps = []

    def copy(self):
        res = String()
        res.pre = self.pre[:]
        res.post = self.post[:]
        res.match = self.match[:]
        res.text = self.text
        res.gnps = self.gnps[:]
        return res

    @classmethod
    def fromBytes(cls, dat, variables=[]):
        # todo: support self.text
        res = cls()
        n = unpack(">H", dat[:2])[0]
        flags = n >> 12
        n = n & 0xFFF
        i = 2
        curr = self.pre
        while i < len(dat):
            if flags & 2:
                r = Node.fromBytes(dat[i:i+6*n+6], variables)
                i += 6*n + 6
            else:
                r = Node.fromBytes(dat[i:i+3+2*n], variables)
                i += 2*n + 3
            if r is not None:
                curr = self.addNode(r, curr)
        return res

    @classmethod
    def fromStr(cls, dat, variables=[], cmap={}):
        self = cls()
        end = skipws(dat, 0)
        if dat[end] == '"':
            e = dat[end+1:].find('"')
            self.text = dat[end+1:e]
            end = skipws(dat, e+1)
        curr = self.pre
        while end < len(dat):
            end = skipws(dat, end)
            n, i = Node.fromStr(dat[end:], variables, cmap)
            end = skipws(dat, end+i)
            if n is not None:
                curr = self.addNode(n, curr)
        return self

    def addNode(self, r, curr):
        if id(curr) == id(self.pre) and r.hasPositions():
            curr = self.match
        elif id(curr) == id(self.match) and not r.hasPositions():
            curr = self.post
        elif id(curr) == id(self.post) and r.hasPositions():
            self.match.extend(self.post)
            self.post = []
            curr = self.match
        curr.append(r)
        return curr

    def addString(self, r):
        if len(self) != len(r):
            return False
        mp = -1
        for i in range(len(self)):
            if r[i].pack() == self[i].pack():
                pass
            elif mp == -1:
                mp = i
            else:
                return False
        if mp == -1:
            return True
        rmp, smp = r[mp], self[mp]
        if rmp.hasPositions():
            if not smp.hasPositions():
                smp.positions = [Position(0,0)] * (len(smp.keys) - 1)
        for i, g in enumerate(rmp.keys):
            if g not in smp.keys:
                smp.keys.append(g)
                if smp.hasPositions():
                    smp.positions.append(rmp.positions[i] if rmp.hasPositions() else Position(0, 0))
        return True

    def splitgnp(self, gnps, newindex):
        newnode = self.match[0].splitwith(gnps)
        res = None
        if newnode is not None:
            newmatch = [newnode] + self.match[1:]
            res = String([x.copy() for x in self.pre], [x.copy() for x in self.post], newmatch, self.text[:])
            res.gnps = [newindex]
        return res

    def movegnp(self, f, t):
        for i, v in enumerate(self.gnps[:]):
            if v == f:
                self.gnps[i] = t

    def key(self):
        return ([x.key() for x in self.match], [x.key() for x in reversed(self.pre)], [x.key() for x in self.post])

    def __hash__(self):
        return hash(struct.pack("{}H".format(len(self)), *self.gids()))

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.key() == other.key()

    def __str__(self):
        return self.asStr()

    def __repr__(self):
        return self.asStr()

    def asBytes(self):
        return b"".join(x.asBytes for x in self.pre + self.match + self.post)

    def asStr(self, cmap=[]):
        if self.text is not None:
            res = '"'+self.text+'" '
        else:
            res = ""
        return res + " ".join(x.asStr(cmap) for x in self.pre + self.match + self.post)

    def isSubsetOf(self, other):
        if len(self.match) != len(other.match):
            return False
        if len(self.pre) > len(other.pre):
            return False
        if len(self.post) > len(other.post):
            return False
        if any(self.match[i].gid != other.match[i].gid for i in range(len(self.match))):
            return False
        if any(self.pre[-i-1].gid != other.pre[-i-1].gid for i in range(len(self.pre))):
            return False
        if any(self.post[i].gid != other.post[i].gid for i in range(len(self.post))):
            return False
        return True

    def splitall(self):
        me = self.copy()
        while len(me.match):
            res = String()
            res.pre = me.pre[:]
            res.match = [me.match[0]]
            res.post = [x.copy(nopositions=True) for x in me.match[1:]] + self.post
            res.text = me.text
            res.gnps = me.gnps[:]
            yield res
            me.pre.append(me.match.pop(0).copy(nopositions=True))
            while len(me.match) and not me.match[0].hasPositions():
                me.pre.append(me.match.pop(0))

    def gids(self):
        return [x.gid for x in self.pre + self.match + self.post]

    def __len__(self):
        return len(self.pre) + len(self.match) + len(self.post)

    def __getitem__(self, y):
        if isinstance(y, slice):
            start, stop, stride = y.indices(len(self))
        else:
            start = y
            stride = 1
            stop = start + 1
        last = 0
        res = []
        for a in (self.pre, self.match, self.post):
            l = len(a)
            if start >= last:
                while start < stop and start < l + last:
                    res.append(a[start - last])
                    start += stride
            last += l
        if start != stop:
            raise IndexError
        if isinstance(y, slice):
            if start != stop:
                raise IndexError
            else:
                return res
        elif len(res) != 1:
            raise IndexError
        else:
            return res[0]

    def weightedIndex(self, i):
        if i < len(self.match):
            return len(self.pre) + i
        i -= len(self.match)
        x = (i + 1) // 2
        if x < len(self.pre):
            return len(self.pre) - x - 1
        x = i - len(self.pre)
        if x < len(self.post):
            return len(self) - i - 1
        raise IndexError

    def filterempties(self):
        self.match = [x for x in self.match if len(x.keys)]
        return len(self.match) != 0

    def testPos(self, rounding):
        ''' Returns whether all nodes in the string have position > rounding '''
        return all(x.testPos(rounding) for x in self.match)


class Node(object):
    def __init__(self, keys=None, positions=None, index=None):
        self.keys = keys or []
        self.positions = positions or []
        self.var = None
        self.gid = keys[0] if keys else None
        self.index = index

    def copy(self, nopositions=False):
        res = Node(keys=self.keys[:], positions=(self.positions[:] if not nopositions else None))
        res.var = self.var
        return res

    @classmethod
    def fromBytes(cls, dat, variables=[]):
        # support self.index
        self = cls()
        if len(dat) < 5:
            return None
        n = unpack(">H", dat[:2])[0]
        flags = n >> 12
        n = n & 0xFFF
        if flags & 1:
            self.var = unpack(">H", dat[2:4])
            start = 4
        else:
            self.keys = unpack(">" + ("H" * n), dat[2:2+2*n])
            start = 2 + 2*n
        if flags & 2:
            poses = unpack(">" + ("H" * (2*n)), dat[start:])
            self.positions = [Position(*x) for x in zip(poses[:n], poses[n:])]
        self.gid = self.keys[0]
        return self

    @classmethod
    def fromStr(cls, dat, variables=[], cmap={}):
        self = cls()
        if dat[0] == "@":
            m = re.match(r"^@(\d+)\s*", dat)
            self.var = int(m.group(1))
            end = m.end(0)
        elif dat[0] == "[":
            end = dat.find("]")
            gnames = re.split(r"[,\s]\s*", dat[1:end])
            self.keys = [cmap.get(g, 0) for g in gnames]
        else:
            return None, 1
        end = skipws(dat, end+1)
        if end < len(dat) and dat[end] == "{":
            end = skipws(dat, end+1)
            while end < len(dat) and dat[end] != "}":
                (p, i) = Position.fromStr(dat[end:])
                if p is None:
                    p = Position(0, 0)
                self.positions.append(p)
                end = skipws(dat, end+i)
            end = skipws(dat, end+1)
        if end < len(dat) and dat[end] == "!":
            m = re.match(r"!(\d+)", dat[end:])
            if m:
                #self.index = int(m.group(1))
                end = skipws(dat, end+m.end())
        self.gid = self.keys[0]
        return (self, end)

    @property
    def pos(self):
        return self.positions[0] if len(self.positions) > 0 else None

    def asBytes(self):
        if len(self.positions):
            flags = 2
        if self.var is not None:
            flags = 1
            res = pack("b>H", flags, 1)
        else:
            res = pack("b>H" + ("H" * len(self.keys)), flags, len(self.keys), *self.keys)
        if len(self.positions):
            res += b"".join(pack(">HH", x.x, x.y) for x in self.positions)
        return res

    def asStr(self, cmap=[]):
        order = sorted(range(len(self.keys)), key=lambda x:self.keys[x])
        if self.var is not None:
            res = "@{}".format(self.var)
        else:
            keys = [self.keys[x] for x in order]
            res = "[" + ", ".join(cmap[x] if x < len(cmap) else "gid{}".format(x) for x in keys) + "]"
        if len(self.positions):
            order = sorted(range(min(len(self.positions), len(self.keys))), key=lambda x:self.keys[x])
            res += "{" + ", ".join(str(self.positions[i]) for i in order) + "}"
        if self.index is not None:
            res += "!{}".format(self.index)
        return res

    def key(self):
        return (self.var or self.keys, self.positions)

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.key() == other.key()

    def hasPositions(self):
        return len(self.positions) > 0

    def testPos(self, rounding):
        ''' Test that all positions are > rounding '''
        if not len(self.positions):
            return True
        return all(x.testPos(rounding) for x in self.positions)

    def keystr(self, rounding=0):
        p = self.positions[0] if len(self.positions) else None
        s = str(self.gid)
        if p is None:
            return s
        if rounding:
            ps = "{},{}".format(int(p.x / rounding + 0.5), int(p.y / rounding + 0.5))
        else:
            ps = "{},{}"
        return s + ":" + ps

    def pack(self):
        try:
            order = sorted(range(len(self.keys)), key=lambda x:self.keys[x])
            k = struct.pack("{}H".format(len(self.keys)), *[self.keys[x] for x in order])
            if len(self.positions):
                order = sorted(range(min(len(self.positions), len(self.keys))), key=lambda x:self.keys[x])
                poses = [self.positions[i] for i in order]
                p = struct.pack("{0}h{0}h".format(len(order)),
                                *(list(zip(*poses))[0] + list(zip(*poses))[1]))
            else:
                p = b""
            return k+p
        except TypeError:
            import pdb; pdb.set_trace()

    def match(self, gnp):
        try:
            i = self.keys.index(gnp[0])
        except ValueError:
            return None
        if len(self.positions) and len(gnp) >= 2:
            return i if self.positions[i] == gnp[1] else None
        return i

    def splitwith(self, gnps):
        newkeys = []
        newpositions = []
        for g in gnps:
            i = self.match(g)
            if i is not None:
                newkeys.append(g[0])
                del self.keys[i]
                if len(self.positions) and len(g) > 1:
                    newpositions.append(g[1])
                    del self.positions[i]
        if len(newkeys):
            return Node(newkeys, newpositions, self.index)
        else:
            return None


class Position(namedtuple('Position', ['x', 'y'])):
    def __str__(self):
        if self.y == 0:
            return str(self.x)
        else:
            return "({},{})".format(self.x, self.y)

    @classmethod
    def fromStr(cls, dat):
        m = re.match(r"^\(\s*(-?\d+(?:\.\d+(?:e-?\d+)?)?)\s*,\s*(-?\d+(?:\.\d+(?:e-?\d+)?)?)\s*\)", dat)
        if m:
            self = cls(int(float(m.group(1))), int(float(m.group(2))))
            end = m.end(0)
        elif dat[0] in "-1234567890.":
            m = re.match(r"^(-?\d*(?:\.\d+(?:e-?\d+)?)?)", dat)
            try:
                self = cls(int(float(m.group(1))), 0)
            except ValueError:
                self = None
                print(m.group(1))
            end = m.end(0)
        else:
            self = None
            end = 1
        return self, end

    def isZero(self, rounding=0):
        if rounding > 0:
            return int(self.x / rounding + 0.5) == 0 and int(self.y / rounding + 0.5) == 0
        else:
            return self.x == 0 and self.y == 0

    def testPos(self, rounding):
        return self.x * self.x + self.y * self.y > rounding * rounding


class RuleSet:
    newlkupcost = 8
    gnpformat = "{0}:{1[0]},{1[1]}"
    def __init__(self, strings):
        self.strings = strings
        self.sets = []      # list of GNPset

    def make_ruleSets(self):
        '''For each glyphnpos group into sets and collect a list of strings for each'''
        allgnps = {}
        count = 0
        order = sorted(range(len(self.strings)), key=lambda x:(self.strings[x].key(), self.strings[x]))
        for i, r in ((x, self.strings[x]) for x in order):
            for j, m in enumerate(r.match):
                if m.hasPositions:
                    s = m.asStr()
                    if s not in allgnps:
                        allgnps[s] = count
                        gnp = GNPSet(m.keys, m.positions)
                        self.sets.append(gnp)
                        gnp.rules.append(r)
                        r.gnps.append(count)
                        count += 1
                    else:
                        self.sets[allgnps[s]].rules.append(r)
                        r.gnps.append(allgnps[s])

    def cost_sets(self):
        ''' Find best next sets to split and merge '''
        results = []
        for i, left in enumerate(self.sets):
            for j, right in enumerate(self.sets[i+1:]):
                saving = len(left & right)
                if saving == 0:
                    continue
                if saving != len(left) and saving != len(right):
                    saving -= left.rulecost() + right.rulecost() + 10
                #left.set_cost(i+1+j, saving)
                #right.set_cost(i, saving)
                #log.debug("left: {}, right: {}, saving: {}".format(i, j+i+1, saving))
                if saving > 0:
                    results.append((-saving, i, j+i+1, 1 if saving == len(left) else (2 if saving == len(right) else 0)))
        return results

    def reduceSets(self, tracefile):
        ''' Split and merge sets to reduce overall GPOS size '''
        finished = False
        cs = self.cost_sets()
        while not finished and len(cs) > 0:
            finished = True
            for cost, i, j, action in sorted(cs):
                if action == 2:
                    self.sets[j].moveto(self.sets, j, self.sets[i], i)
                    finished = False
                elif action == 1:
                    self.sets[i].moveto(self.sets, i, self.sets[j], j)
                    finished = False
                else:
                    newset = GNPSet(list(self.sets[i] & self.sets[j]))
                    count = len(self.sets)
                    self.sets[i].remove(newset, count)
                    self.sets[j].remove(newset, count)
                    if len(newset.rules):
                        finished = False
                        self.sets.append(newset)
                if tracefile is not None:
                    self.outtext(tracefile, {}, mode="a")
            cs = self.cost_sets()
        if tracefile is not None:
            self.outtext(tracefile, {}, mode="a")

    def numlookups(self):
        return sum(1 if len(x.rules) else 0 for x in self.sets)

    def totallookuplength(self):
        return sum(len(x) if len(x.rules) else 0 for x in self.sets)

    def rebuild_strings(self):
        ''' Merge rules in a set and recreate strings from sets '''
        self.strings = []
        for i, s in enumerate(self.sets):
            ri = 0
            s.rules = [r for r in s.rules if len(r.match) and len(r.match[0].keys)]
            while ri < len(s.rules):
                s.rules = s.rules[:ri+1] + [r for r in s.rules[ri+1:] if not s.rules[ri].addString(r)]
                ri += 1
            self.strings.extend(s.rules)

    def outfea(self, outfile, cmap, rtl=False):
        self.rebuild_strings()
        rules = []
        allPositions = {}
        lkupmap = {}
        posfmt = "    pos {0} " + ("<{1[0]} 0 {1[0]} 0>;" if rtl else "{1[0]};")
        count = 0
        with open(outfile, "w") as outf:
            for i, g in enumerate(self.sets):
                if not len(g.rules):
                    continue
                poslkup = ["lookup kernpos_{} {{".format(count)]
                for k in sorted(g):
                    p = g.parseKey(k)
                    poslkup.append(posfmt.format(cmap[p[0]], p[1]))
                poslkup += ["}} kernpos_{};".format(count)]
                lkupmap[i] = count
                count += 1
                outf.write("\n".join(poslkup) + "\n\n")

            for r in sorted(self.strings, key=lambda x:-len(x)):
                rule = []
                for m in r.pre:
                    if len(m.keys) > 1:
                        rule.append("[" + " ".join(cmap[x] for x in m.keys) + "]")
                    else:
                        rule.append(cmap[m.keys[0]])
                count = 0
                for m in r.match:
                    if m.hasPositions:
                        s = m.asStr(cmap)
                        lnum = lkupmap[r.gnps[count]]
                        count += 1
                        if len(m.keys) > 1:
                            rule.append("[" + " ".join(cmap[x] for x in m.keys) + "]' lookup kernpos_{}".format(lnum))
                        else:
                            rule.append(cmap[m.keys[0]] + "' lookup kernpos_{}".format(lnum))
                    elif len(m.keys) > 1:
                        rule.append("[" + " ".join(cmap[x] for x in m.keys) + "]'")
                    else:
                        rule.append(cmap[m.keys[0]] + "'")
                for m in r.post:
                    if len(m.keys) > 1:
                        rule.append("[" + " ".join(cmap[x] for x in m.keys) + "]")
                    else:
                        rule.append(cmap[m.keys[0]])
                rules.append("pos " + " ".join(rule) + ";")
            outf.write("lookup mainkern {\n    ")
            outf.write("\n    ".join(rules))
            outf.write("\n} mainkern;\n")

    def outtext(self, outfile, cmap, mode="w"):
        self.rebuild_strings()
        with open(outfile, mode) as fh:
            for r in sorted(self.strings, key=lambda x:(-len(x), x.key())):
                fh.write(r.asStr(cmap=cmap)+"\n")
            if mode == "a":
                fh.write("\n----------\n")


class GNPSet:
    gnpformat = "{0}:{1[0]},{1[1]}"
    def __init__(self, gids, positions=None):
        if positions is None:  # treat gids as keys
            self.set = set(gids)
        else:
            self.set = set(self.gnpformat.format(gids[i], positions[i]) for i in range(len(gids)))
        self.rules = []
        self.setcosts = []
        self.movedto = None

    def __str__(self):
        return " ".join(self.set)

    def __contains__(self, v):
        return v in self.set

    def __len__(self):
        return len(self.set)

    def __iter__(self):
        return iter(self.set)

    def __and__(self, othergnpset):
        return self.set & othergnpset.set

    def __eq__(self, other):
        return self.set == other.set

    def add(self, gid, position=None):
        if position is None:
            self.set.add(gid)
        else:
            self.set.add(self.gnpformat.format(gid, position))

    def set_cost(self, i, cost=None):
        if i >= len(self.setcosts):
            self.setcosts += [0] * (i - len(self.setcosts) + 1)
        if cost is None:
            return self.setcosts[i]
        else:
            self.setcosts[i] = cost
            return cost

    def asgnps(self):
        res = [self.parseKey(k) for k in sorted(self.set)]
        return res
            
    def parseKey(self, key):
        gid, poses = key.split(":")
        pos = Position(*[int(float(x)) for x in poses.split(",")])
        return (int(gid), pos)

    def remove(self, newgnps, newindex):
        log.debug("Removing {}: {}".format(newindex, newgnps))
        self.set = self.set - newgnps.set
        results = []
        newg = newgnps.asgnps()
        removedc = 0
        for i, r in enumerate(self.rules[:]):
            news = r.splitgnp(newg, newindex)
            if news is not None:
                for nr in newgnps.rules:
                    if nr.addString(news):
                        break
                else:
                    results.append(news)
                    newgnps.rules.append(news)
                # why doesn't this work?
                if 0:
                    for nr in self.rules[:i-removedc]:
                        if nr.addString(r):
                            del self.rules[i - removedc]
                            # self.rules.remove(r)
                            removedc += 1
                            break
        return results

    def moveto(self, allsets, currindex, newgnps, newindex):
        #loopfind = set([currindex])
        #while newgnps.movedto is not None and newgnps.movedto not in loopfind:
        #    newgnps = allsets[newgnps.movedto]
        #    newindex = newgnps.movedto
        #    loopfind.add(newindex)
        log.debug("Moving {} to {}".format(currindex, newindex))
        for r in self.rules:
            for nr in newgnps.rules:
                if nr.addString(r):
                    break
            else:
                newgnps.rules.append(r)
            r.movegnp(currindex, newindex)
        newgnps.set.update(self.set)
        self.rules = []
        self.set = set()
        self.movedto = newindex

    def rulecost(self):
        return sum(3 * len(r) + 2 * len(r.match) + 10 for r in self.rules)


def addString(collections, s, rounding=0):
    for n in s.splitall():
        g = n.match[0].gid
        if g not in collections:
            collections[g] = Collection()
        collections[g].addString(n, rounding=rounding)

def printall(res, go):
    return "\n".join(r.asStr(cmap=go) for r in sorted(res, key=lambda x:x.key()))

if __name__ == '__main__':
    import argparse
    from fontTools import ttLib
    from multiprocessing import Pool
    
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',help='Input results file')
    parser.add_argument('outfile', help='Output results file')
    parser.add_argument('-f','--font',required=True,help='Base font')
    parser.add_argument('-r','--rounding',default=10,type=int,help='Rounding accuracy [10]')
    parser.add_argument('-j','--jobs',default=0,type=int,help='Number of parallel jobs [0=num cpus]')
    parser.add_argument('-s','--start',default=0,type=int,help='Starting phase')
    parser.add_argument('-e','--end',default=2,type=int,help="Final phase before output and stopping")
    parser.add_argument('-R','--rtl',action="store_true",help="Output rtl appropriate adjustments")
    parser.add_argument('--printeach',action='store_true',help='Print rules after each phase')
    parser.add_argument('--log',default="info",help="logging level (debug, *info*, warn, error, critical)")
    parser.add_argument('--logfile',help="Log to file")
    parser.add_argument('--tracefile',help="Trace results to file")
    args = parser.parse_args()

    loglevel = getattr(log, args.log.upper(), None)
    if isinstance(loglevel, int):
        parms = {'level': loglevel, 'format': ''}
        if args.logfile is not None:
            parms.update(filename=args.logfile, filemode="w")
        log.basicConfig(**parms)

    if args.tracefile and os.path.exists(args.tracefile):
        os.remove(args.tracefile)

    font = ttLib.TTFont(args.font)
    go = font.getGlyphOrder()
    cmap = {n: i for i, n in enumerate(go)}
    colls = {}
    linecount = 0
    with open(args.infile) as fh:
        for l in fh.readlines():
            addString(colls, String.fromStr(l, cmap=cmap), rounding=args.rounding)
            linecount += 1
    rulecount = sum(len(x) for v in colls.values() for x in v.gidmap.values())
    log.info("Input rules: {} flattened to {} rules".format(linecount, rulecount))

    def process(k):
        return (k, colls[k].process(k, args.rounding))

    if args.jobs != 1:
        if args.jobs == 0:
            pool = Pool()
        else:
            pool = Pool(processes=args.jobs)
        iterproc = pool.imap_unordered
    else:
        iterproc = map

    if args.start < 1:
        print("0: Reducing strings")
        # Remove small positioned strings, duplicates; cluster, split and reduce
        # process longest lists firsts to average out processing time
        keylengths = {k: sum(len(x) for x in v.gidmap.values()) for k, v in colls.items()}
        res = {}
        total = [0, 0]
        for k, r in iterproc(process, [x[0] for x in sorted(keylengths.items(), key=lambda y:-y[1])]):
            # print("{}: {} -> {}".format(go[k], len(colls[k].gidmap), r[0]))
            total[0] += len(colls[k].gidmap)
            total[1] += r[0]
            res[k] = r[1]
        log.info("Totals: {} -> {}".format(*total))
        res = [r for vg in sorted(res.keys()) for v in sorted(res[vg].keys()) for r in res[vg][v]]
        if args.printeach:
            print(printall(res, go))
    else:
        res = [r for vg in sorted(colls.keys()) \
                    for v in sorted(colls[vg].gidmap.keys()) for r in colls[vg].gidmap[v]]

    # res is a [maString]
    # colls = dict[gid of first moved glyph] = Collection
    # Find substrings and remove
    # This is already done in the reduce() above.
    if False and args.start < 2 and args.end > 0:
        marks = set(colls.keys())
        def process1(rules):
            finder = {}
            for r in rules:
                gs = r.gids()
                mask = 0
                for i, g in enumerate(gs):
                    if g in marks:
                        mask |= 1 << i
                for i in range(len(gs)):
                    for j in range(i+1, len(gs)+1):
                        testmask = (1 << (i+1)) - 1
                        testmask |= (1 << len(gs)) - (1 << j)
                        if (mask & testmask) != 0:
                            finder.setdefault(struct.pack("{}H".format(j-i), *gs[i:j]), []).append((r, i))
            return finder
        def process1a(rules, finder):
            newrules = []
            for r in rules:
                gs = r.gids()
                match = finder.get(struct.pack("{}H".format(len(gs)), *gs), None)
                if match is not None and len(match) > 1:
                    for m in match:
                        if m[0] == r:
                            continue
                        try:
                            n = m[0][m[1] + len(r.pre)]
                        except IndexError:
                            import pdb; pdb.set_trace()
                        if n.hasPositions() and r.match[0].pos not in n.positions:
                            n.positions.append(r.match[0].pos)
                else:
                    newrules.append(r)
            return newrules
        # can't multiprocess this because the overhead of locking is greater than the gain
        log.info("1: Merging substrings")
        finder = process1(res)
        if args.printeach:
            print(finder)
        res = process1a(res, finder)
        if args.printeach:
            print(printall(res, go))

    # res = [String]
    # Create classes
    if args.start < 2 and args.end > 0:
        log.info("1: Creating classes")
        lastlen = 0
        # import pdb; pdb.set_trace()
        for r in res:
            r.dropme = False
        maxlen = max(len(x) for x in res)
        while len(res) != lastlen:
            lastlen = len(res)
            newres = set()
            finder = {}
            for i in range(maxlen):
                for r in res:
                    if len(r) <= i:
                        continue
                    j = r.weightedIndex(i)
                    k = b"".join(x.pack() for x in r[:j] + r[j+1:])
                    if k in finder:
                        for s in finder[k]:
                            if not s.dropme and s.addString(r):
                                r.dropme = True
                                newres.discard(r)
                                newres.add(s)
                                break
                        else:
                            finder[k].append(r)
                    else:
                        finder[k] = [r]
            for r in res:
                if not r.dropme:
                    newres.add(r)
            res = list(newres)
            #res = sorted(newres, key=lambda x:x.asStr(go))
        if args.printeach:
            print(printall(res, go))
        log.info("Rule count: " + str(len(res)))

    outrules = RuleSet(res)
    outrules.make_ruleSets()
    log.info ("Lookups: {} sum {}, Strings: {}".format(outrules.numlookups(), outrules.totallookuplength(), len(outrules.strings)))
    if args.start < 3 and args.end > 1:
        log.info ("2: Reduce lookups")
        outrules.reduceSets(args.tracefile)
    if args.outfile.endswith(".fea"):
        outrules.outfea(args.outfile, go, rtl=args.rtl)
    else:
        outrules.outtext(args.outfile, go)
    log.info ("Lookups: {} sum {}, Strings: {}".format(outrules.numlookups(), outrules.totallookuplength(), len(outrules.strings)))
