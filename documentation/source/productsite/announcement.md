
We are very pleased to announce a new release of Harmattan, an Arabic script font designed for use by languages in West Africa. 

### Changes

This release includes the following changes for this version:

#### New

- Added:
  - 088F ARABIC LETTER NOON WITH RING ABOVE
  - FDFE ARABIC LIGATURE SUBHAANAHU WA TAAALAA
  - FDFF ARABIC LIGATURE AZZA WA JALL
  - 10EC5 ARABIC SMALL YEH BARREE WITH TWO DOTS BELOW 
  - 10EC6 ARABIC LETTER THIN NOON 
  - 10EC7 ARABIC LETTER YEH WITH FOUR DOTS BELOW 
  - 10ED0 ARABIC BIBLICAL END OF VERSE 
  - 10EFA ARABIC DOUBLE VERTICAL BAR BELOW 
  - 10EFB ARABIC SMALL LOW NOON 
- Added cv88 (Guillemet) to provide a choice for angled guillemot characters in Arabic script
- Added Malay Jawi language support 

#### Improved

- Added sample strings and feature tooltips to the character variants for applications that support them
- Made width of punctuation space (U+2008) consistent with width of period

#### Known issues

- Shaping for the newly added characters may not yet occur in applications.
- Medial and final high hamza characters may have collisions (these likely do not occur).
- Lam + high hamza alef ligature does not form as it likely does not occur.
- In InDesign: some behaviors, such as the _lam-alef_ ligature, raised _kasra_ with _shadda_, and subtending marks, will not function correctly unless **Ligatures** is turned on in the **Characters** panel.

Both desktop and web fonts are provided in a single, all-platforms package on the [Download page](https://software.sil.org/harmattan/download).
