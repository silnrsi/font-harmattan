# Harmattan

Harmattan is a smart open font designed by SIL International for West African Languages using the Arabic script.

### Project status [![Build Status](http://build.palaso.org/app/rest/builds/buildType:Fonts_Harmattan/statusIcon)](http://build.palaso.org/viewType.html?buildTypeId=Fonts_Harmattan&guest=1)
**NOTE: This is a development font. It is not yet ready for wider use or distribution to end-users.**   
Font sources are published in a public repository and a smith open workflow is used for building, testing and releasing.   
You can contribute and report issues but please don't use this in production yet.

## Copyright and License
For copyright and licensing - including any Reserved Font Names - see [OFL.txt](OFL.txt).

For practical information about using, modifying and redistributing this font see [OFL-FAQ.txt](OFL-FAQ.txt).

For more details about this project, including changelog and acknowledgements see [FONTLOG.txt](FONTLOG.txt).

## See also
For further information, including Unicode ranges supported, Graphite and OpenType font features
and how to use them, please see the documentation on [software.sil.org/harmattan](http://software.sil.org/harmattan/)
or in the documentation subfolder.

# Developer notes

## Building

The Harmattan project can be built from source using [smith](https://github.com/silnrsi/smith). 
Normally this is done via the sequence:
```
    smith distclean
    smith configure
    smith build test
```

Because of the relatively large GPOS table, such a build can take up to 15 minutes or longer, 
depending on hardware. If the GPOS kerning is _not_ needed (such as for regenerating certain 
source files, see below), the `--quick` parameter can be supplied: 
```
    smith distclean
    smith configure
    smith build --quick
```
The resulting files will not have functional OpenType kerning, but will be otherwise usable.

### Generated files

Four of the source files needed for the build are actually generated files but, because they 
require compute-intensive tools to create or update, are generated offline and committed 
to the repo. The files that fall into this category are:
- `source/*-octabox.json` — optimized octaboxes to enable Graphite to do more accurate kerning 
of reh-like characters to what follows.
- `source/opentype/caKern-*.fea` — contextual kerning rules that approximate the kerning effected
by the Graphite collision avoidance.

If the _design_ of any Arabic glyphs in the font changes, it is important to rebuild the 
optimized octabox.json files so that Graphite collision-avoidance-based kerning is accurate, 
and then to rebuild the OpenType kerning rules from the graphite results. A script to do this 
is in `tools/bin/updateKerning.sh`. This should be run from the root of the project. Be aware
this can take up to 30 minutes or more to complete.
