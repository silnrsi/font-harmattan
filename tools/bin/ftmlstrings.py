#!/usr/bin/python3
"""Convert FTML XML data to list of attributed strings"""

import xml.etree.ElementTree as ET
import collections
import re

class ftmlstring(collections.UserString):
    """string wrapper with attributes holding FTML style information"

    Supports normal string methods and operations, and additionally the following attributes:

    Args:
        seq : any object which can be converted into a string using the built-in str() function.
            Used to set the initial contents of the instance.

    Attributes:
        lang : str
            language tag, in HTML (i.e. BCP47) format.
        feats : dict
            A dictionary keyed by the feature tag, returning feature value (numeric, > 0).
            Individual features can be set or cleared by setting feats attribute to any of:
                - A string consisting of comma separated tag-value pairs with tag enclosed in quotes, optionally
                  followed by a space and the decimal value. This format is identical to css font-feature-settings
                  property, for example: "'smcp', 'cv22' 2".
                - A list,tuple,etc. of strings, each of which represents one tag-value pair, formatted as above.
                - A dictionary keyed by the tag, returning value (must be numeric, >=0 )
            Setting a feature value to 0 will remove it from the dictionary
        rtl : boolean
            Whether test string is to be run with paragraph direction set right-to-left.
        data : str
            A real str object holding the string being wrapped by ftmlstring.

    Raises:
        ValueError for any invalid feature tags or values
    """

    def __init__(self, s=""):
        super().__init__(s)
        self.lang = None
        self._feats = {}
        self.rtl = False

    @property
    def feats(self):
        return self._feats

    @feats.setter
    def feats(self, val):

        def parseFeat(f:str):
            m = re.match("""(['"])([a-zA-Z0-9]{4,4})\\1(?:\s+(\d+|on|off))?$""", f)
            if not m:
                raise ValueError(f'Invalid feature syntax: {f}')
            tag, value = m.group(2,3)
            value = 1 if value in (None, 'on') else 0 if value == 'off' else int(value)
            return (tag,value)

        def setFeat(tag, value):
            if value:
                self._feats[tag] = value
            else:
                self._feats.pop(tag,None)

        if isinstance(val, str):
            for f in val.split(','):
                tag,value = parseFeat(f.strip())
                setFeat(tag,value)
        else:
            # try dictionary-like:
            try:
                for tag,value in val.items():
                    if not re.match('[a-zA-Z0-9]{4,4}$',tag):
                        raise ValueError(f'Invalid feature tag: {tag}')
                    value = int(value)
                    if value < 0:
                        raise ValueError(f'Invalid feature value: {value}')
                    setFeat(tag,value)
            except:
                # Not a dictionary, assume it is list/tuple/iterator-like
                for f in val:
                    tag, value = parseFeat(f.strip())
                    setFeat(tag,value)

def parseftml(root:ET):
    """parse an FTML document into a list ftmlstrings

    Args:
        root : ElementTree Element object representing FTML document
    Returns:
        list of ftmlstring objects, each representing one <test>, in document order

    Within <string> elements it removes <em> markup and converts backslash-u notation to Unicode characters.
    <testgroup> divisions are ignored and tests from all <testgroups> are collected together.
    """

    def replaceHex(matchobj):
        return chr(int(matchobj.group(1),16))

    strs = []
    for test in root.findall('.//test'):
        s = "".join(test.find('string').itertext())
        s = re.sub(r'\\u([a-fA-F0-9]{4,6})', replaceHex, s)
        s = ftmlstring(s)
        stylename = test.get('stylename', None)
        if stylename is not None:
            style = root.find(f'./head/styles/style[@name="{stylename}"]')
            feats = style.get('feats', None)
            if feats is not None:
                s.feats = feats
            lang = style.get('lang', None)
            if lang is not None:
                s.lang = lang
        s.rtl = test.get('rtl', "") == "True"
        strs.append(s)
    return strs

def parseFile(filename):
    """ read FTML from a file and return list of ftmlstrings

    Args:
        file : filename or file object containing XML data
    Returns:
        see parseftml()
    """

    return parseftml(ET.parse(filename))

def parseStr(xml:str):
    """ parse FTML document from a string and return list of ftmlstrings

    Args:
        xml : str
    Returns:
        see parseftml()
    """

    return parseftml(ET.fromstring(xml))


if __name__ == '__main__':
    # manually create and test ftmlstring:
    s = ftmlstring("hi there")
    s.data = "bye there"
    s.lang = "ur"
    s.feats = "'cv20' 2, 'smcp', 'kern' on"
    s.feats = {'cv12': 3, 'cv20': 0}
    print(f'string: "{s}"; lang: {s.lang}; feats: {s.feats}')

    # Parse ftml data:
    xml = """<ftml version="1.0">
  <head>
    <styles>
      <style feats="'smcp' 1" name="smcp_1"/>  
      <style lang="vi" name="viet"/>
    </styles>
  </head>
  <testgroup label="Group 1">
    <test>                    <string>abcdefghijklmnop</string> </test>
    <test stylename="smcp_1"> <string>abcdefghijklmnop</string> </test>
  </testgroup>
  <testgroup label="Group 2">
    <test stylename="viet" rtl="True"> <string>abc<em>\\u0064\\u000065fgh</em>ijklmnop</string> </test>
  </testgroup>
</ftml>
    """
    strs = parseStr(xml)
    print('\n'.join([f'string: "{s}"; rtl: {"True" if s.rtl else "False"}; lang: {s.lang}; feats: {s.feats}' for s in strs ]))
