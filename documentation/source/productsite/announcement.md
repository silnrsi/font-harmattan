
#### Changes

The most significant change to this version is the addition of a bold typeface. There are other major changes to this version:

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
  - Improvements to the design of dal- keheh-, yeh-, qaf-, ain-, heh doachashmee-, swash kaf-, 
    and yeh barree-based characters
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

**Note:** We reserve the right to alter metrics in future releases. Future versions of the font may result in different lines, line spacing, or paragraph lengths. Do not expect that a document laid out in one version will always have the same page breaks, etc., in future fonts.

Both desktop and web fonts are provided in a single, all-platforms package on the [Download Page](https://software.sil.org/harmattan/download/).

#### Known issues

At the time of the Harmattan 2.000 release there is a known issue for printing with Harmattan in Word 2019 and Word 365. Printing to a printer or to pdf may cause a reh-like glyph to shift in its advanced width. The result is that there appears to be a small space between the preceding character and the reh-like character. Microsoft is working on releasing an update that includes a fix for this issue. Once Microsoft releases the update, the solution to this issue will be to update Microsoft Office. You can do this by opening a document in Word and go to **File &gt; Account &gt; Update Options &gt; Update Now**.



