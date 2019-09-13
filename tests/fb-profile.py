# template config file for local testing of ttfs with fontbakery.

from fontbakery.checkrunner import Section, PASS, FAIL, WARN, ERROR, INFO, SKIP
from fontbakery.callable import condition, check, disable
from fontbakery.constants import PriorityLevel
from fontbakery.message import Message
from fontbakery.fonts_profile import profile_factory
import re


# imports are used to mix in other external profiles
profile_imports =('fontbakery.profiles.opentype','fontbakery.profiles.name', 'fontbakery.profiles.head', 'fontbakery.profiles.glyf')

# example of import params for SIL common profile and ABS profile directly in pysilfont
# profile_imports = ['silfont.fbtests.common', 'silfont.fbtests.abs']

profile = profile_factory(default_section=Section("SIL font project"))


# Our own checks below
# See https://font-bakery.readthedocs.io/en/latest/developer/writing-profiles.html

# putting this at the top of the file
# can give a quick overview:
expected_check_ids = (
    'org.sil.software/checks/helloworld',
    'org.sil.software/check/has-R',
    'org.sil.software/check/aglfn_compliant'
)

# We use `check` as a decorator to wrap an ordinary python
# function into an instance of FontBakeryCheck to prepare
# and mark it as a check.
# A check id is mandatory and must be globally and timely
# unique. See "Naming Things: check-ids" below.
@check(id='org.sil.software/checks/helloworld')
# This check will run only once as it has no iterable
# arguments. Since it has no arguments at all and because
# checks should be idempotent (and this one is), there's
# not much sense in having it all. It will run once
# and always yield the same result.
def hello_world():
    """Simple "Hello (alphabets of the) World" example."""
    # The function name of a check is not very important
    # to create it, only to import it from another module
    # or to call it directly, However, a short line of
    # human readable description is mandatory, preferable
    # via the docstring of the check.

    # A status of a check can be `return`ed or `yield`ed
    # depending on the nature of the check, `return`
    # can only return just one status while `yield`
    # makes a generator out of it and it can produce
    # many statuses.
    # A status also always must be a tuple of (Status, Message)
    # For `Message` a string is OK, but for unit testing
    # it turned out that an instance of `fontbakery.message.Message`
    # can be very useful. It can additionally provide
    # a status code, better suited to figure out the exact
    # check result.
    yield PASS, 'Hello (alphabets of the) World'


@check(id='org.sil.software/check/has-R')
# This check will run once for each item in `fonts`.
# This is achieved via the iterag definition of font: fonts
def has_cap_r_in_name(font):
    """Filename contains an "R"."""
    # This test is not very useful again, but for each
    # input it can result in a PASS or a FAIL.
    if 'R' not in font:
        # This is our first check that can potentially fail.
        # To document this: return is also ok in a check.
        return FAIL, '"R" is not in font filename.'
    else:
        # since you can't return at one point in a function
        # and yield at another point, we always have to
        # use return within this check.
        return PASS, '"R" is in font filename.'


@condition
def adobe_glyphlist():
  """Get Adobe's glyph list"""
  from csv import reader
  from pkg_resources import resource_filename
  agl = {}

  # When this code is in a proper profile module, we can do the following:
  # CACHED = resource_filename('silfonts', 'data/aglfn.txt.cache')
  # Until then, we need to find the data file the hard way:
  from os.path import relpath, dirname, join
  CACHED = join(relpath(dirname(__file__)), 'fb-data/glyphlist.txt.cache')

  with open(CACHED) as f:
    for row in reader(f, delimiter=';'):
      if row[0].startswith('#'):
        continue
      (name,usvs) = row
      agl[name] = [int(usv,16) for usv in usvs.split()]

  return agl

@condition
def adobe_aglfn():
  """Get Adobe's glyph list for new fonts"""
  from csv import reader
  from pkg_resources import resource_filename
  aglfn = {}

  # When this code is in a proper profile module, we can do the following:
  # CACHED = resource_filename('silfonts', 'data/aglfn.txt.cache')
  # Until then, we need to find the data file the hard way:
  from os.path import relpath, dirname, join
  CACHED = join(relpath(dirname(__file__)), 'fb-data/aglfn.txt.cache')

  with open(CACHED) as f:
    content = reader(f, delimiter=';')
    for row in content:
      if row[0].startswith('#'):
        continue
      (usv,name,comment) = row
      aglfn[name] = int(usv,16)

  return aglfn

@check(
  id = 'org.sil.software/check/aglfn_compliant',
  conditions = ['adobe_glyphlist','adobe_aglfn']
)
def org_sil_software_check_aglfn_compliant(ttFont, adobe_glyphlist, adobe_aglfn):
  """Non-component glyph names must be agl-compliant and should be aglfn-compliant.

  Assumes glyph names are well-formed -- can be verified
  with 'com.google.fonts/check/valid_glyphnames'.
  Permits glyphnames to start with '_' (normally used
  for glyph components) as long as unencoded."""

  # FIXME: Just because a glyphname starts with "_" doesn't mean it is used only as
  # a component. It would be better to find all the component glyphs by algorithm.
  # This would require searching cmap and GSUB tables to get a list of glyphs that
  # we know are *not* components; everything else is.
  
  # Create inverse cmap, used to determine if glyphs are encoded in this font
  cmap_gname2usv = {gname: usv for usv, gname in ttFont.getBestCmap().items()}

  from fontbakery.utils import pretty_print_list
  if ttFont.sfntVersion == b'\x00\x01\x00\x00' and ttFont.get(
      "post") and ttFont["post"].formatType == 3.0:
    yield SKIP, ("TrueType fonts with a format 3.0 post table contain no"
                 " glyph names.")

  import re;
  # match names like 'u12345' or 'uni1234abcd'
  uniRE = re.compile(r'(?:u([0-9a-fA-F]{4,6})$)|(?:uni((?:[0-9a-fA-F]{4,4})+)$)')

  # Possible status bits:
  AGL_OK = 0
  NON_AGL = 0x1     # One ore more components in the glyphname are not agl
  NON_AGLFN = 0x2   # One ore more components in the glyphname are not aglfn
  MISENCODED = 0x4  # The glyph is encoded but doesn't match agl
  def agl_decode(glyphname):
    """ parses a glyph name and returns a tuple containing
    a status value and a tuple of USVs"""
    usvs = []
    status = AGL_OK
    # discard everything after first '.':
    gn = glyphname.split('.', maxsplit=1)[0]  
    # Split into components, if any, and process each:
    for c in gn.split('_'):
      m = uniRE.match(gn)
      if m:
        if m.group(1):
          usvs.append(int(m.group(1),16))
        if m.group(2):
          for i in range(0, len(m.group(2)), 4):
            usvs.append(int(m.group(2)[i:i+4],16))
      elif gn not in adobe_glyphlist:
        status |= NON_AGL
        usvs.append(None)
      else:
        usvs.extend(adobe_glyphlist[c])
        if c not in adobe_aglfn:
          status |= NON_AGLFN
    if len(usvs) == 1 and usvs[0] is not None \
            and glyphname in cmap_gname2usv \
            and usvs[0] != cmap_gname2usv[glyphname]:
      status |= MISENCODED

    return (status,usvs)

  failed = False
  component_names_unencoded = []    # These cause WARN
  component_names_encoded = []      # These cause FAIL
  non_agl_names = []                # These cause FAIL
  non_aglfn_names = []              # These cause WARN
  misencoded_glyphs = []            # name is ok but encoded differently than agl; causes FAIL
  for glyphname in ttFont.getGlyphOrder():
    if glyphname in [".null", ".notdef", "nonmarkingreturn", "tab", ".ttfautohint"]:
      # These names are explicit exceptions in the glyph naming rules
      continue
    if glyphname.startswith('_'):
      # Relaxed rules for glyph names starting with '_' normally used as glyph components
      # but they must not be encoded.
      if glyphname in cmap_gname2usv:
        component_names_encoded.append(glyphname)
        failed = True
      else:
        component_names_unencoded.append(glyphname)
      continue
    status,usvs = agl_decode(glyphname)
    if status & NON_AGL:    non_agl_names.append(glyphname)
    if status & NON_AGLFN:  non_aglfn_names.append(glyphname)
    if status & MISENCODED: misencoded_glyphs.append(glyphname)
    if status: failed = True

  if len(component_names_unencoded):
    yield WARN, \
          Message('bad_glyphname',
                  f'Glyph names should not start with underscore ("_") unless they never'
                  f' directly enter the glyph stream (for example are used only as component glyphs).' 
                  f' The following glyph names start with "_" but, because they are not encoded,'
                  f' are assumed to be used only as component glyphs: {pretty_print_list(component_names_unencoded)}.')
  if len(component_names_encoded):
    yield FAIL, \
          Message('bad_glyphname',
                  f'Glyph names should not start with underscore ("_") unless they never'
                  f' directly enter the glyph stream (for example are used only as component glyphs).' 
                  f' The following glyph names start with "_" but, because they are encoded,'
                  f' cannot be assumed to be used only as component glyphs: {", ".join(component_names_encoded)}.')
  if len(non_aglfn_names):
    yield WARN, \
          Message('bad_glyphname',
                  f'The following glyph names, though recognized by the Adobe Glyph List algorithm,' 
                  f' are not recommended for use in new fonts: {", ".join(non_aglfn_names)}.')
  if len(non_agl_names):
    yield FAIL, \
          Message('bad_glyphname',
                  f'The following glyph names will not be recognized by the Adobe Glyph List algorithm'
                  f' and should be changed: {", ".join(non_agl_names)}.')
  if len(misencoded_glyphs):
    yield FAIL, \
          Message('bad_encoding',
                  f'The following glyph names will be recognized by the Adobe Glyph List algorithm'
                  f' as a different codepoint than is indicated in the cmap: {", ".join(misencoded_glyphs)}.')
  if not failed:
    t =  ' non-component '  if len(component_names_unencoded) else ' '
    yield PASS, f'All{t}glyph names compliant with Adobe Glyph List for New Fonts'


# skip checks (they still appear)
def check_skip_filter(checkid, font=None, **iterargs):
  if checkid in (
       'com.google.fonts/check/metadata/reserved_font_name'
      , 'com.google.fonts/check/description/broken_links'
      , 'com.google.fonts/check/name/rfn'
  ):
    return False, ('We do not want or care about these checks')
  return True, None

profile.check_skip_filter = check_skip_filter

# disable checks
def check_disable_filter(checkid, font=None, **iterargs):
  if checkid in (
       'com.google.fonts/check/metadata/reserved_font_name'
      , 'com.google.fonts/check/description/broken_links'
      , 'com.google.fonts/check/name/rfn'
  ):
    return False, ('We do not want or care about these checks')
  return True, None

profile.check_skip_filter = check_skip_filter
profile.check_disable_filter = check_disable_filter
profile.auto_register(globals())


