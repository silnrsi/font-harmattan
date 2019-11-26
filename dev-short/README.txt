kerntext.ftml:
   a short (4 test) ftml file
   each test is 4 pairs followed by 4 pairs with a trailing combining mark (kasratan) below.

demo.sh:
   sequences through the following steps:      Giving the following output:
       1) run glyphstrings                        results/rawPairData-ftml.txt
       2) run glyphstring with -e 0               results/kernStrings-e0.txt
       3) run glyphstring with -e 1               results/kernStrings-e1.txt
       4) run glyphstring with -e 2               results/kernStrings-e2.txt
       5) run glyphstrings with .fea output       results/caKern.fea
       6) copy the fea file over to source/opentype so project compiles

The stdout messages from step 5:
    Input rules: 32 flattened to 32 rules
    0: Reducing strings
    Totals: 6 -> 6
    1: Merging substrings
    2: Creating classes

Analysis:

1) The rawPairData-ftml.txt looks perfect:  exactly 32 records, half of which include the combining mark (kasratan).

2) I don't understand the -e0 output:
     - two records have no RHS
     - the remaining 16 records, ... don't understand ... doesn't matter

3) The -e1 output:
     - same as -e0 except:
            - records without RHS are now absent
            - there are two kern offsets for every record, 
              even though (except for the two records including kasratan) 
              there is only one slot on both the LHS and RHS ???

4) resulting fea:

    lookup kernpos_1 {
        pos reh-ar <-194 0 -194 0>;
        pos reh-ar.fina <-164 0 -164 0>;
    } kernpos_1;
    
    lookup kernpos_2 {
        pos reh-ar <117 0 117 0>;
        pos reh-ar.fina <-164 0 -164 0>;
    } kernpos_2;
    
    lookup mainkern {
        pos [reh-ar reh-ar.fina]' lookup kernpos_1 [ainThreedots-ar.init ainTwodotshorizontalabove-ar.init ghain-ar.init];
        pos [reh-ar reh-ar.fina]' lookup kernpos_2 [ainThreedots-ar ainTwodotshorizontalabove-ar ghain-ar ghainDotbelow-ar];
        pos [reh-ar reh-ar.fina]' lookup kernpos_2 ghainDotbelow-ar.init kasratan-ar;
    } mainkern;

has some promise except that kernpos_2 can't possibly right: there are no conceivable 
shared contexts where reh-ar moves 117 *right* while reh-ar.fina moves 164 *left*.

Take, for example, take lines 3 and 4 from the raw data:
	"???" [reh-ar.fina]{116.686}!1 [ghain-ar]!2
	"??" [reh-ar]{112.749}!0 [ghain-ar]!1

and trace through the applicable (2nd) contextual kern above:
        pos [reh-ar reh-ar.fina]' lookup kernpos_2 [ainThreedots-ar ainTwodotshorizontalabove-ar ghain-ar ghainDotbelow-ar];

and you get, instead:
      [reh-ar.fina]{-164} [ghain-ar]
      [reh-ar]{117} [ghain-ar]


Once demo.sh is run you can build Harmattan from this branch and it will 
build with the generated caKern.fea so you can compare the graphite kerning 
(1st col) and opentype kerning (2nd col).

---------------------------------------------
On another topic

It looks like we can't always throw away small kerns. 

Consider the following two kern strings:
    reh-ar  -196  ghain-ar.init   
    reh-ar  -17   ghain-ar.init   kasratan-ar

Current algorithm (with -r20) throws away the 2nd of these, but in
fact it is needed and the resulting [longer] contextual rule needs 
to be before the shorter one in the fea code in order to, in effect,
mask the it.