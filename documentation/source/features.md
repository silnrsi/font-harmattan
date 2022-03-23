---
title: Harmattan - Font Features
fontversion: 2.000
---

Harmattan is a TrueType font with smart font capabilities added using OpenType and Graphite font technologies. The Harmattan font includes a number of optional features that provide alternative rendering that might be preferable for use in some contexts. The sections below enumerates the details of these features. Whether these features are available to users will depend on both the application and the rendering technology ([Graphite](http://graphite.sil.org/) or OpenType) being used. Most features are available in both Graphite and OpenType, though there may be minor differences in their implementation. Some applications let the user control certain features such as Character Variants to turn on the rendering of variant characters. However, at this point, most applications do not make use of those features so another solution is needed to show the variant characters. [TypeTuner](http://scripts.sil.org/ttw/fonts2go.cgi) creates tuned fonts that use the variant glyph in place of the standard glyph. TypeTuner also provides the ability to turn on support for the Kurdish, Rohingya, Sindhi, Urdu, and Wolof languages variants.

See [Using Font Features](https://software.sil.org/fonts/features/). Although that page is not targeted at Arabic script support, it does provide a comprehensive list of applications that make full use of the OpenType and Graphite font technologies.

See also [Arabic Fonts — Application Support](http://software.sil.org/arabicfonts/support/application-support/). It provides a fairly comprehensive list of applications that make full use of the OpenType and [Graphite](http://graphite.sil.org) font technologies.

This page uses web fonts (WOFF) to demonstrate font features and should display correctly in all modern browsers. For a more concise example of how to use Harmattan as a web font see *harmattan-webfont-example.html* in the font package web folder. 

*If this document is not displaying correctly a PDF version is also provided in the documentation/pdf folder of the release package.*

## End of Ayah (U+06DD) and subtending marks (U+0600..U+0605)

These Arabic characters are intended to enclose or hold one or more digits. 

Specific technical details of how to use them are discussed in the [Arabic fonts FAQ -- Subtending marks](http://software.sil.org/arabicfonts/support/faq#Ayah).

Additionally, Harmattan includes two simplified alternates for U+06DD ARABIC END OF AYAH under the Stylistic Alternates (salt) feature, but at this time we know of no OpenType-based applications that can access these. The two alternates are also available through the Character Variants feature discussed below.



## Customizing with TypeTuner

For applications that do not make use of Graphite features or the OpenType Character Variants, you can now download fonts customized with the variant glyphs you choose. Read this document, visit [TypeTuner Web](http://scripts.sil.org/ttw/fonts2go.cgi), then choose the variants and download your font.



### Test rendering engine choice 

Here is a simple test to see if Graphite is working in your browser. If it is, the following will say "RenderingGraphite". If your browser does not support Graphite it should say "RenderingOpentype". Firefox is currently the only browser that supports Graphite. See the [instructions on how to enable Graphite in Firefox](http://scripts.sil.org/cms/scripts/page.php?site_id=projects&amp;item_id=graphite_firefox#switchon).

| | 
------------- | --------------- 
Check | <span class='HarmattanL-R normal'>RenderingUnknown</span>

### Language 

<span class='affects'>Affects: U+062F, U+0630, U+0688..U+068F, U+0690, U+06EE, U+0759, U+075A, U+08AE, U+0645, U+0765, U+0766, U+08A7, U+0647, U+0626, U+060C, U+061B, U+06F4, U+06F5, U+06F6, U+06F7, U+0650, U+064F, U+064C, U+0657</span>

Unfortunately, the UI needed to access the language-specific behavior is not yet present in many applications. LibreOffice and Microsoft Word 2016 support language-specific behavior for Kurdish, Sindhi and Urdu (but not Kyrgyz, Rohingya or Wolof). Some Harfbuzz-based apps, e.g., XeTeX, can access language-specific behavior.

#### Kurdish (Northern), Rohingya, Sindhi, Urdu

Language | Meem | Heh | Comma | 4 | 6 | 7 | 0650 | 064C | Feature Setting
-- | ---: | ----: | -: | -: | -: | -: | --: | --: | ---
default | <span dir="rtl" class='Harmattan-R small'>&#x0645;&#x0020;&#x0645;&#x0645;&#x0645;</span> | <span dir="rtl" class='Harmattan-R small' >&#x0647;&#x0020;&#x0647;&#x0647;&#x0647;</span> | <span dir="rtl" class='Harmattan-R small'>&#x060C; &#x061B;</span> | <span dir="rtl" class='Harmattan-R small'>&#x06F4;</span> |<span dir="rtl" class='Harmattan-R small'>&#x06F6;</span> | <span dir="rtl" class='Harmattan-R small'>&#x06F7;</span> | <span dir="rtl" class='Harmattan-R small'>&#x0628;&#x0651;&#x0650;</span> | <span dir="rtl" class='Harmattan-R small'>&#x0628;&#x064C;</span> |
Kurdish</br>(Northern) | <span dir="rtl" class='Harmattan-R small' lang='ku'>&#x0645;&#x0020;&#x0645;&#x0645;&#x0645;</span> | <span dir="rtl" class='Harmattan-R small' lang='ku' style="color:red">&#x0647;&#x0020;&#x0647;&#x0647;&#x0647;</span> | <span dir="rtl" class='Harmattan-R small' lang='ku'>&#x060C; &#x061B;</span> | <span dir="rtl" class='Harmattan-R small' lang='ku'>&#x06F4;</span> | <span dir="rtl" class='Harmattan-R small' lang='ku'>&#x06F6;</span> | <span dir="rtl" class='Harmattan-R small' lang='ku'>&#x06F7;</span> | <span dir="rtl" class='Harmattan-R small' lang='ku'>&#x0628;&#x0651;&#x0650;</span> | <span dir="rtl" class='Harmattan-R small' lang='ku'>&#x0628;&#x064C;</span> |  `lang='ku'`
Rohingya | <span dir="rtl" class='Harmattan-R small' lang='rhg'>&#x0645;&#x0020;&#x0645;&#x0645;&#x0645;</span> | <span dir="rtl" class='Harmattan-R small' lang='rhg'>&#x0647;&#x0020;&#x0647;&#x0647;&#x0647;</span> | <span dir="rtl" class='Harmattan-R small' lang='rhg'>&#x060C; &#x061B;</span> | <span dir="rtl" class='Harmattan-R small' lang='rhg' style="color:red">&#x06F4;</span> | <span dir="rtl" class='Harmattan-R small' lang='rhg' style="color:red">&#x06F6;</span> | <span dir="rtl" class='Harmattan-R small' lang='rhg' style="color:red">&#x06F7;</span> | <span dir="rtl" class='Harmattan-R small' lang='rhg' style="color:red">&#x0628;&#x0651;&#x0650;</span> | <span dir="rtl" class='Harmattan-R small' lang='rhg' style="color:red">&#x0628;&#x064C;</span>| `lang='rhg'`
Sindhi | <span dir="rtl" class='Harmattan-R small' lang='sd' style="color:red">&#x0645;&#x0020;&#x0645;&#x0645;&#x0645;</span> | <span dir="rtl" class='Harmattan-R small' lang='sd'>&#x0647;&#x0020;&#x0647;&#x0647;&#x0647;</span> | <span dir="rtl" class='Harmattan-R small' lang='sd' style="color:red">&#x060C; &#x061B;</span> | <span dir="rtl" class='Harmattan-R small' lang='sd'>&#x06F4;</span> | <span dir="rtl" class='Harmattan-R small' lang='sd' style="color:red">&#x06F6;</span> | <span dir="rtl" class='Harmattan-R small' lang='sd' style="color:red">&#x06F7;</span> | <span dir="rtl" class='Harmattan-R small' lang='sd' style="color:red">&#x0628;&#x0651;&#x0650;</span> | <span dir="rtl" class='Harmattan-R small' lang='sd'>&#x0628;&#x064C;</span> | `lang='sd'`
Urdu | <span dir="rtl" class='Harmattan-R small' lang='ur'>&#x0645;&#x0020;&#x0645;&#x0645;&#x0645;</span> | <span dir="rtl" class='Harmattan-R small' lang='ur'>&#x0647;&#x0020;&#x0647;&#x0647;&#x0647;</span> | <span dir="rtl" class='Harmattan-R small' lang='ur'>&#x060C; &#x061B;</span> | <span dir="rtl" class='Harmattan-R small' lang='ur' style="color:red">&#x06F4;</span> | <span dir="rtl" class='Harmattan-R small' lang='ur' style="color:red">&#x06F6;</span> | <span dir="rtl" class='Harmattan-R small' lang='ur' style="color:red">&#x06F7;</span> | <span dir="rtl" class='Harmattan-R small' lang='ur' style="color:red">&#x0628;&#x0651;&#x0650;</span> | <span dir="rtl" class='Harmattan-R small' lang='ur'>&#x0628;&#x064C;</span> | `lang='ur'`

#### Wolof


Language | Dal  | 0650 | 064F | 0657 | Feature Setting
-- | -- |  --- | -- | -- | ---
default | <span dir="rtl" class='Harmattan-R small'> &#x062F;</span> | <span dir="rtl" class='Harmattan-R small'>&#x0628;&#x0651;&#x0650;</span> | <span dir="rtl" class='Harmattan-R small'>&#x0628;&#x064F;</span> | <span dir="rtl" class='Harmattan-R small'>&#x0628;&#x0657;</span>|
Wolof | <span dir="rtl" class='Harmattan-R small' lang='wo' style="color:red"> &#x062F;</span> | <span dir="rtl" class='Harmattan-R small' lang='wo' style="color:red">&#x0628;&#x0651;&#x0650;</span> | <span dir="rtl" class='Harmattan-R small' lang='wo' style="color:red">&#x0628;&#x064F;</span> | <span dir="rtl" class='Harmattan-R small' lang='wo' style="color:red">&#x0628;&#x0657;</span>| `lang='wo'`


### Character variants

There are some character shape differences in different languages which use the Arabic script. These can be accessed by using Graphite features, OpenType Character Variants, or through the language support mentioned above.  

#### Alef diacritic placement 

<span class='affects'>Affects: U+0623, U+0625, U+0627, U+064E, U+0650, U+0654, U+0655</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'> أإاَاِأإلألإ </span>| `cv02=0`
Hamza touching | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv02" 1'> أإاَاِأإلألإ </span>| `cv02=1`
Touching | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv02" 2'> أإاَاِأإلألإ </span>| `cv02=2`

#### Jeem/Hah 

<span class='affects'>Affects: U+062C, U+062D, U+062E, U+0682, U+0683, U+0684, U+0685, U+0686, U+06BF, U+0757, U+0758, U+08A2, U+08C1, U+08C5, U+08C6</span>

Feature | Sample | Feature setting
------------- | ------------: | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'>ج ججج ح ححح خ خخخ ڂ ڂڂڂ ڃ ڃڃڃ ڄ ڄڄڄ څ څڅڅ چ چچچ ڿ ڿڿڿ ݗ ݗݗݗ ݘ ݘݘݘ ࢢ ࢢࢢࢢ ࣁ ࣁࣁࣁ ࣅ ࣅࣅࣅ ࣆ ࣆࣆࣆ  </span>| `cv08=0`
Handwritten | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv08" 1'>ج ججج ح ححح خ خخخ ڂ ڂڂڂ ڃ ڃڃڃ ڄ ڄڄڄ څ څڅڅ چ چچچ ڿ ڿڿڿ ݗ ݗݗݗ ݘ ݘݘݘ ࢢ ࢢࢢࢢ ࣁ ࣁࣁࣁ ࣅ ࣅࣅࣅ ࣆ ࣆࣆࣆ  </span>| `cv08=1`

#### Dal 

<span class='affects'>Affects: U+062F, U+0630, U+0688, U+0689, U+068A, U+068B, U+068C, U+068D, U+068E, U+068F, U+0690, U+06EE, U+0759, U+075A, U+08AE</span>

Feature | Sample | Feature setting
------------- | ------------: | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'> د ذ ڈ ډ ڊ ڋ ڌ ڍ ڎ ڏ ڐ ۮ ݙ ݚ ࢮ </span>| `cv12=0`
Alternate | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv12" 1'> د ذ ڈ ډ ڊ ڋ ڌ ڍ ڎ ڏ ڐ ۮ ݙ ݚ ࢮ </span>| `cv12=1`


#### Sad/Dad 

<span class='affects'>Affects: U+0635, U+0636, U+069D, U+069E, U+06FB, U+08AF</span>

Feature | Sample | Feature setting
------------- | -----: |  ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'>ص صصص ض ضضض ڝ ڝڝڝ ڞ ڞڞڞ ࢯࢯࢯ ࢯ ۻ ۻۻۻ</span>| `cv20=0`
Half | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv20" 1'>ص صصص ض ضضض ڝ ڝڝڝ ڞ ڞڞڞ ࢯࢯࢯ ࢯ ۻ ۻۻۻ</span>| `cv20=1`


#### Meem 

<span class='affects'>Affects: U+0645, U+0765, U+0766, U+08A7</span>

Feature | Sample | Feature setting
------------- | -----: | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'> م ممم ݥ ݥݥݥ ݦ ݦݦݦ ࢧ ࢧࢧࢧ </span> | `cv44=0`
Sindhi-style | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv44" 1'> م ممم ݥ ݥݥݥ ݦ ݦݦݦ ࢧ ࢧࢧࢧ </span>| `cv44=1`


#### Heh 

<span class='affects'>Affects: U+0647</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'> ه ههه </span>| `cv48=0`
Kurdish-style | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv48" 3'> ه ههه </span>| `cv48=3`
Sindhi-style | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv48" 1'> ه ههه </span>| `cv48=1`
Urdu-style | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv48" 2'> ه ههه </span>| `cv48=2`


#### Arabic U 

<span class='affects'>Affects: U+0677, U+06C7</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'> ٷ ۇ</span> | `cv50=0`
Filled | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv50" 1'>ٷ ۇ </span>| `cv50=1`


#### Maddah 

<span class='affects'>Affects: U+0622, U+0627, U+0653, U+0653</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Small | <span dir="rtl" class='Harmattan-R normal'> آ آ ◌ٓ </span> | `cv60=0`
Large | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv60" 1'>آ آ ◌ٓ </span>| `cv60=1`


#### Shadda+kasra placement 

<span class='affects'>Affects: U+064D, U+0650 with U+0651</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Default | <span dir="rtl" class='Harmattan-R normal'> بِّ ◌ِّ بٍّ ◌ٍّ </span> | `cv62=0`
Lowered | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv62" 1'> بِّ ◌ِّ بٍّ ◌ٍّ </span>| `cv62=1`
Raised | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv62" 2'> بِّ ◌ِّ بٍّ ◌ٍّ </span> | `cv62=2`

#### Damma 


<span class='affects'>Affects: U+064F</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'> بُ ◌ُ</span> | `cv70=0`
Filled | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv70" 1'>بُ ◌ُ</span>| `cv70=1`
Short| <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv70" 2'>بُ ◌ُ</span>| `cv70=2`

#### Dammatan 

<span class='affects'>Affects: U+064C</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'>بٌ ◌ٌ</span> | `cv72=0`
Six-nine | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv72" 1'>بٌ ◌ٌ</span>| `cv72=1`

#### Inverted Damma 

<span class='affects'>Affects: U+0657</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'>بٗ ◌ٗ</span> | `cv74=0`
Filled | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv74" 2'>بٗ ◌ٗ</span>| `cv74=2`


#### Superscript Alef 

<span class='affects'>Affects: U+0670 on all yeh, sad and seen-like characters 
U+0649 U+064A U+06D0 U+06D1 U+0777 U+06CC U+0635 U+0636 U+069D U+069E U+06FB U+08AF U+0633 U+0634 U+069A U+069B U+069C U+06FA U+075C U+076D U+0770 U+077D U+077E</span>

Feature | Sample | Feature setting
------------- | ---------------: | ------------- 
Small | <span dir="rtl" class='Harmattan-R normal'>ئٰ ئٰئٰئٰ ىٰ ىٰىٰىٰ يٰ يٰيٰيٰ ٸٰ ٸٰٸٰٸٰ ېٰ ېٰېٰېٰ ۑٰ ۑٰۑٰۑٰ ݷٰ ݷٰݷٰݷٰ ࢨٰ ࢨٰࢨٰࢨٰ ࢩٰ ࢩٰࢩٰࢩٰ ؽٰ ؽٰؽٰؽٰ ؾٰ ؾٰؾٰؾٰ ؿٰ ؿٰؿٰؿٰ یٰ یٰیٰیٰ ێٰ ێٰێٰێٰ ݵٰ ݵٰݵٰݵٰ ݶٰ ݶٰݶٰݶٰ صٰ صٰصٰصٰ ضٰ ضٰضٰضٰ ڝٰ ڝٰڝٰڝٰ ڞٰ ڞٰڞٰڞٰ ۻٰ ۻٰۻٰۻٰ ࢯٰ ࢯٰࢯٰࢯٰ سٰ سٰسٰسٰ شٰ شٰشٰشٰ ښٰ ښٰښٰښٰ ڛٰ ڛٰڛٰڛٰ ڜٰ ڜٰڜٰڜٰ ۺٰ ۺٰۺٰۺٰ ݜٰ ݜٰݜٰݜٰ ݭٰ ݭٰݭٰݭٰ ݰٰ ݰٰݰٰݰٰ ݽٰ ݽٰݽٰݽٰ ݾٰ ݾٰݾٰݾٰ </span> | `cv76=0`
Large | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv76" 1'>ئٰ ئٰئٰئٰ ىٰ ىٰىٰىٰ يٰ يٰيٰيٰ ٸٰ ٸٰٸٰٸٰ ېٰ ېٰېٰېٰ ۑٰ ۑٰۑٰۑٰ ݷٰ ݷٰݷٰݷٰ ࢨٰ ࢨٰࢨٰࢨٰ ࢩٰ ࢩٰࢩٰࢩٰ ؽٰ ؽٰؽٰؽٰ ؾٰ ؾٰؾٰؾٰ ؿٰ ؿٰؿٰؿٰ یٰ یٰیٰیٰ ێٰ ێٰێٰێٰ ݵٰ ݵٰݵٰݵٰ ݶٰ ݶٰݶٰݶٰ صٰ صٰصٰصٰ ضٰ ضٰضٰضٰ ڝٰ ڝٰڝٰڝٰ ڞٰ ڞٰڞٰڞٰ ۻٰ ۻٰۻٰۻٰ ࢯٰ ࢯٰࢯٰࢯٰ سٰ سٰسٰسٰ شٰ شٰشٰشٰ ښٰ ښٰښٰښٰ ڛٰ ڛٰڛٰڛٰ ڜٰ ڜٰڜٰڜٰ ۺٰ ۺٰۺٰۺٰ ݜٰ ݜٰݜٰݜٰ ݭٰ ݭٰݭٰݭٰ ݰٰ ݰٰݰٰݰٰ ݽٰ ݽٰݽٰݽٰ ݾٰ ݾٰݾٰݾٰ </span>| `cv76=1`

#### Sukun 

<span class='affects'>Affects: U+0652</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Closed | <span dir="rtl" class='Harmattan-R normal'>بْ ◌ْ</span> | `cv78=0`
Open down | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv78" 1'>بْ ◌ْ</span>| `cv78=1`
Open left | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv78" 2'>بْ ◌ْ</span>| `cv78=2`

#### End of ayah 


<span class='affects'>Affects: U+06DD</span>

Firefox allows you to use U+06DD followed by the digits and proper rendering occurs. Some applications require the following:

* precede the entire sequence (subtending mark plus following digits) with
        202D LEFT-TO-RIGHT OVERRIDE
* follow the entire sequence with U+202C POP DIRECTIONAL FORMATTING.

Surrounding the sequence with U+202D and U+202C seems to give the most reliable results in different browsers. However, we have not found a solution that works in Internet Explorer/Edge.

In the example below, the following codepoints are used: U+202D U+06DD U+0031 U+0032 U+0033 U+202C U+202D U+06DD U+0611 U+0622 U+0663 U+202C.

Feature | Sample | Feature setting
------------- | --------------- | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'>&#x202D;&#x6DD;&#x31;&#x32;&#x33;&#x202C; &#x202D;&#x6DD;&#x0661;&#x0662;&#x0663;&#x202C;</span> | `cv80=0`
Simplified A | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv80" 1'>&#x202D;&#x6DD;&#x31;&#x32;&#x33;&#x202C; &#x202D;&#x6DD;&#x0661;&#x0662;&#x0663;&#x202C;</span>| `cv80=1`
Simplified B | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv80" 2'>&#x202D;&#x6DD;&#x31;&#x32;&#x33;&#x202C; &#x202D;&#x6DD;&#x0661;&#x0662;&#x0663;&#x202C;</span>| `cv80=2`

#### Eastern digits 


<span class='affects'>Affects: U+06F4, U+06F6, U+06F7</span>

Feature | Sample | Feature setting
------------- | ------ | ------------- 
Standard | <span dir="rtl" class='Harmattan-R normal'>&#x06F4;&#x06F6;&#x06F7;</span> | `cv82=0`
Sindhi-style | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv82" 1'>&#x06F4;&#x06F6;&#x06F7;</span>| `cv82=1`
Urdu-style | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv82" 2'>&#x06F4;&#x06F6;&#x06F7;</span>| `cv82=2`
Rohingya-style | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv82" 4'>&#x06F4;&#x06F6;&#x06F7;</span>| `cv82=4`


#### Comma 

<span class='affects'>Affects: U+060C, U+061B</span>

Feature | Sample |  Feature setting
------------- | ------ | ------------- 
Upward | <span dir="rtl" class='Harmattan-R normal'>، ؛</span> | `cv84=0`
Downward | <span dir="rtl" class='Harmattan-R normal' style='font-feature-settings: "cv84" 1'>، ؛</span>| `cv84=1`

#### Line spacing 

Allows for adjustment of the default line spacing in the font (values shown are ordered in increasing line spacing). This feature is only available with TypeTuner.

Feature | 
------------- | ---------------  
Normal |
Loose |
1.0 Compatible Normal |
1.0 Compatible Loose |



<!-- PRODUCT SITE ONLY
[font id='Harmattan' face='Harmattan-Regular' bold='Harmattan-Bold' size='150%' rtl=1]
[font id='HarmattanL' face='Harmattan-Regular' bold='Harmattan-Bold' size='100%' ltr=1]

-->


