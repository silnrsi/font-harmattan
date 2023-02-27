WHAT THIS FOLDER IS ABOUT

This folder is used to generate glyphs from components. The component definitions are stored in absGlyphList.xslx/csv/txt. Two utility scripts are run to modify the UFO files.

* psfcsv2comp -i glyphs2build.csv compdefns.txt
		-- BUG: this does not seem to be correctly handling the glyphs that use the 'center' AP.

* psfbuildcomp -i compdefns.txt --preserve "dia[AB]|alef$" --remove "_?(above|below|center|ring|through)$" ../Harmattan-Regular.ufo

  psfbuildcomp -i compdefns.txt --preserve "dia[AB]|alef$" --remove "_?(above|below|center|ring|through)$" ../Harmattan-Bold.ufo
  
	 - Use the -a option to do a dry run and see errors before the real thing.
	 
The files are:

* glyphs2build.csv - a subset of absGlyphList.csv containing only the new glyphs to be processed.
* compdefns.txt - the output of psfcsv2comp, the input to psfbuildcomp. Tweaks must be made to this file to include the following shift commands:

tchehVabove-ar.fina - _dot3d@hah-ar.fina:center[shift=0,-70]
jeemThreedotsbelow-ar.fina - _dot1_dot3d@center[shift=0,-50]
jeemThreedotsbelow-ar.init - _dot1_dot3d@below[shift=0,-70]
