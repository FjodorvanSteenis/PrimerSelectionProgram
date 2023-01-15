# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 18:43:01 2022

@author: Fjodor

FUNCTION IMPROVEMENT

Primer3:
    Ideal parameters:
-Product size range: 100-200 bp (90-250 bp will also suite, but longer and shorter can be problematic)
-Number to return: 500
-Primer size: 22 bp (21 bp, 20 bp, 23 bp also will work)
-Primer Tm: 57.0 – 83.0
-Max Tm difference: 2.0
-Primer GC%: 50.0 – 50.0 (50.0-60.0 is also good) (45.0-65.0 can sometimes work)
-Max Poly-X: 3 (4 or 5 can also work)
-CG Clamp: 1 (0), least important parameter and can be set to 0 to get more choices

Can’t find primer? First set clamp to 0, then max poly x to 4, then size range 90-200, then primer size to 21, then product size range to 90-250, if still not then GC % max to 60, then GC min to 47, if still not then poly-X to 5, length to max 23 

"""

import Modules as md
import pandas as pd
import time

start = time.time()

Primer3Output = "Primer3Output.txt"
ParsedPrimerList = md.Primer3Parser(Primer3Output)
# Parser Works! 

Alignment = "GH9Alignment.fas"
AlignmentDict = md.FastaAlignmentParser(Alignment)
# AlignmentParser Works!

SelectedLeftPrimers = md.SelectionFunction2(ParsedPrimerList, AlignmentDict, "Left", 1)
SelectedPrimerPairList = md.SelectionFunction2(SelectedLeftPrimers, AlignmentDict, "Right", 0)


GeneName = ParsedPrimerList[0].GeneName
md.SaveSelectedPrimers(SelectedPrimerPairList, GeneName, "PrimerResults.txt")
# SaveSelectedPrimers Works!


# End of timing
end = time.time()
Durationunrounded = end-start
Duration = round(Durationunrounded, 2)

print(f"That took {Duration} seconds!")

print(f"The number of primers that were checked is: {len(ParsedPrimerList)}")
print(f"The number of left primers that made it through is: {len(SelectedLeftPrimers)}")


LstLSeq = []
LstRSeq = []
for i in SelectedPrimerPairList :
    Lprimer = i.LeftPrimer          
    LstLSeq.append(Lprimer)
    Rprimer = i.RCoRP
    LstRSeq.append(Rprimer)        
            
df = pd.DataFrame(list(zip(LstLSeq, LstRSeq)),
               columns =['LefSequence', 'RightSequence'])            
            
df.to_excel('SequencesOutput.xlsx')
print("Sequences have been saved to Excel")