# Score calculation in Evaluation.py

A score used for ranking sequences in the output is returned.

## Ranking score 

Parameters included:
* Uridine depletion
* GC content
* CAI
* MFE global
* MFE 5'

### u_depletion
U depletion is checked by counting each U at third position in codon and normalizing to 
codon number. Maximum and minimum values are 1 and 0 (all / no codons have U at third position).
When uridine depletion is not required by the user, this is not included in the final scoring 
function (by setting the weight to 0).

This part of the score was included because codons with U at the third position have been shown to be translated
less efficiently.

### gc_score
GC content is calculated for the whole sequence and we check if it is within the set boundaries.
The score is calculated as a linear function of GC content, taking bigger values at the right border
of the desired region. This is needed so that higher values of GC are rated higher:
```
score(GC) = (GC - GC_min)/(GC_max - GC_min)
```
The score is bounded in the region [0; 1].

As GC content has an influence on properties and expression rates of mRNA, we optimize the sequence to fit the GC content
in a specified window.

### CAI (Codon Adaptation Index)
CAI is calculated using BioPython Bio.SeqUtils.CodonUsage module. The score is calculated as just a CAI
value as it is bounded in region [0; 1].

### mfe_total
MFE total is calculated with the help of stem-loop prediction algorithm. Lower total MFE values 
are preferable so the score is calculated in the following way:
```
score(MFE) = exp[-MFE/5000] - 1
```
It tends to 0 when MFE -> 0, and doesn't exceed 1 for MFE values around < -3500

### mfe5_score
MFE of the 5' end is calculated using RNAfold. 
MFE has a theoretical maximum of 0, but in practice it's not even close.
The score is calculated as a decreasing exponential function of the 5' MFE: s = exp(MFE/100).
In this case s -> 0 when MFE -> minus infinity and s -> 1 when MFE -> 0. So score is bounded 
now in the region [0; 1] with 0 being worst case and 1 being best case.

The aim is to have the MFE of the 5' end of mRNA as close to 0 as possible. This means that there are few bonds among 
nucleotides of the 5' end, therefore the structure is open and more accessible to ribosomes. This is believed to improve
expression rate. 


### Score
The final value of the score is calculated as 
```
S = (w1 * u_depl_score + w2 * gc_score + w3 * CAI_score + w4 * mfe_total + w5 * mfe5_score) / (w1 + w2 + w3 + w4 + w5)
```
Where wi – are individual weights we assign to each score. The final score also ranges in [0; 1].
