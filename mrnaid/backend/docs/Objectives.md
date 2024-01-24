# Objectives

Objectives are soft constraints used during the optimization with the help of DNAChisel constraint solver. During the optimization the score for every objective is calculated and the tool tries to minimize it.

Several constraints are used as optimization objectives in the mRNAid tool. The description of them is presented below.

## MatchTargetCodonUsage

This objective is a build-in objective into the DNAChisel package. Based on the target host usage frequencies of codons it calculates the usage frequencies of codons in a given sequence and calculates a score based on that. This score is then a subject of minimization.
This codon optimization is used by default unless one of the other two is selected by the user - *MatchTargetPairUsage* or *MatchTargetCodonPairUsage*

## EnforceGCContent

This objective is also a build-in DNAChisel one. We used the option to specify the sliding window size, in which DNAChisel tries to keep the amount of GC content as close as possible to the specified one. It is based on the score which definition can be found in DNAChisel documentation.

## Minimize MFE (minimal free energy)

This is a custom objective which is implemented in this tool. `MinimizeMFE()` class is inherited from the DNAChisel `Specification()` class and extends it. 

It calculates the score, which DNAChisel optimizer tries to minimize. The score is based on MFE calculation, which is done by one of the two possible methods:

* Using `viennarna` conda package. This package allows to calculate the MFE and sequence secondary structure. The MFE calculation is based on thoroughly analyzing possible secondary structures and can take up to several seconds for a given sequence. This might be a significant performance limitation when optimization algorithm needs to scan across many possible sequences

* Using custom algorithm taken from 'Nucleic Acids Research, 2013, Vol. 41, No. 6 e73'. This algorithm is based on correlated stem-loop prediction. It is less accurate, but much better in terms of time performance (3-4-fold time boost comparing to viennarna).


## MatchTargetPairUsage

This is a custom objective which has been implemented based on pair usage table taken from CoCoPUTs database https://bigd.big.ac.cn/databasecommons/database/id/6462.

It calculates the difference between the frequencies of nucleotide pairs in host organism (homo sapiens) and a current sequence. Then the score is calculated by the following logic:

```python
    ratios = []
    for pair, frequency in calculated_freqs.items():
        ratios.append(frequency / self.pair_usage_table[pair])
    return mean([abs(1 - ratio) for ratio in ratios])
```
The total score is used by DNAChisel optimization algorithm as the subject for maximization.

## MatchTargetCodonPairUsage

This is another custom objective being implemented on the base of the usage table taken 
from CoCoPUTs database. It calculates the difference between the frequencies of codon pairs in
the host organism (homo sapiens) and compares them with frequencies in the current sequence.
Then the score is calculated by the following logic:

```python 
    ratios = []
    for pair, frequency in calculated_freqs.items():
        table_frequency = self.pair_usage_table[pair]
        ratios.append(table_frequency / frequency)
    return mean([abs(1 - ratio) for ratio in ratios])
```

The total score is used by DNAChisel optimization algorithm as the subject for maximization.
