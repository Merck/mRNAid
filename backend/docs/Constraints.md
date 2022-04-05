# Constraints

Constraints described here are so-called hard constraints. The violation of any of these constraints would result in unsuccessful optimization attempt.

## AvoidPattern

This constraint makes sure that the specified pattern is excluded from the final sequence. It is a build-in constraint from the DNAChisel package.

## EnforceGCContent

This is a hard constraint ensuring that the GC content across the sequence remains within defined boundaries specified by user. It is a build-in constraint from the DNAChisel package.


## Uridine depletion

This constraint ensures that there is no uridine on a third position of all the codons in a optimized sequence. It is a custom constraint created for mRNAid tool.

## EnforceTranslation

This constraint is used to make sure that the optimized sequence is translated to the same polypeptide as the original one, i.e. only synonymous  codons are used.

## AvoidRareCodons

Codons with usage frequency lower than defined by threshold are not used in the optimized sequence.