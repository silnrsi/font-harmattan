
### 2020-06-19 (SIL WSTech team) Harmattan version 2.000
  - Added a bold typeface
  - Added support for all characters in the Arabic and Arabic Supplement blocks
  - Added support for all characters in the Arabic Extended-A block (except for the
    Quranic annotation signs)
  - Added U+FDFC (rial), U+FDFD (bismillah)
  - Added U+02D0, U+02D8..U+02D9, U+02DB, U+02DD, U+034F, U+03C0, U+2044, U+2126, U+2202, U+2206, U+220F, U+2211, U+221A, U+221E, U+222B, U+2248, U+2260, U+2264..U+2265, U+2423 
  - Implemented language support for Kurdish, Rohingya, Sindhi, Urdu, and Wolof variants
  - Implemented Dal, Heh, Arabic U, Inverted Damma, and Eastern Digits features
  - Implemented new Allah ligature rules
  - Improved support for Shaddah+kasra placement feature
  - Removed "Show invisible characters" feature
  - Added UI name strings for Graphite and OpenType features
  - Improvements to the design of dal- keheh-, yeh-, qaf-, ain-, heh doachashmee-, swash kaf-, and yeh barree-based characters
  - Improvements to the design of U+FDF2 - modified to use shadda-dagger alef (not shadda-fatha)
  - Improvements to the design of rohingya yeh
  - Improvements to the design and size of digits (latin and arabic)
  - Improvements to positioning of combining marks and nuktas
  - Adjustments to spacing around many Arabic script characters
  - Rework kerning logic based on new spacing around characters 
  - Improved line spacing to support added characters
  - Modified underline and strikethrough position (used by some applications)
  - Modified superscript and subscript size and positioning (used by some applications)
  - Implemented support for UNICODE ARABIC MARK RENDERING (UTR #53) 

### 2016-04-07 (SIL NRSI team) Harmattan Version 1.001 (production release)
  - Changed internal font names
  - changed space of U+00A0 to match regular space

### 2015-03-25 (SIL NRSI team) Harmattan Version 1.00 (production release)
  - Further improvements to kerning.

### 2014-12-11 (SIL NRSI team) Harmattan alpha Version 0.119 (test release)
  - Improved kerning logic in OpenType (via GPOS) and Graphite

### 2014-10-27 (SIL NRSI team) Harmattan alpha Version 0.118 (test release)
- Improved display:
  - Reduced width of arrowhead combining marks to reduce collisions
  - Added kerning logic in OpenType (via GPOS) and Graphite

### 2014-10-14 (SIL NRSI team) Harmattan alpha Version 0.117 (test release)
- Alpha release of font for feedback
- Revision of design of characters based on feedback received
  - Shortened kasra and fatha (and similar characters and glyphs) to help with collisions
  - Adjusted design to final form of U+06D2 to help with collisions
  - Increased spacing after reh-like characters
  - African qaf, African noon, African feh added (in the Unicode pipeline)
  - A few minor anchor point tweaks
- Changed default behavior for cv62 to have the kasra in the "lowered" postion
  - Removed cv62 as an OpenType feature. It is now only available through Graphite or TypeTunerWeb
- Default linespacing adjusted to handle tallest base character with shadda and lowest base character so these are not clipped 
- Added Normal and Loose linespacing adjustments for TypeTunerWeb

### 2014-06-24 (SIL NRSI team) Harmattan alpha Version 0.111 (test release)
- Alpha release of font for feedback
- Revision of design of characters based on feedback received
  - Isolate reh and noon ghunna characters modified
  - Tatweel (U+0640) length was shortened
  - APs on many characters were adjusted
  - Adjusted design of U+08F7..U+08FD (arrowheads)
- added U+065E, U+08F0, U+08F1, U+08F2, U+08F3

### 2014-04-03 (SIL NRSI team) Harmattan alpha Version 0.106 (test release)
- Alpha release of font for feedback
- Revision of design of characters based on feedback received

### 2013-12-04 (SIL NRSI team) Harmattan alpha Version 0.010 (test release)
- Alpha release of font for feedback only (not an actual font release)
- Arabic script design work is based on Fouta font (see copyright and acknowledgments) with significant modification
- Latin script design is based on a Andika (see copyright). The Latin Andika glyphs have been reduced in size to match Harmattan

