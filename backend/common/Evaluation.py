import math
from typing import List, Dict
from typing import Tuple

import RNA
from Bio.Seq import Seq
from Bio.SeqUtils.CodonUsage import CodonAdaptationIndex, SynonymousCodons
from billiard import Pool
from dnachisel import Location
from dnachisel import MatchTargetCodonUsage
from objectives.Codon_pair_usage import MatchTargetCodonPairUsage
from objectives.Dinucleotide_usage import MatchTargetPairUsage
from objectives.MFE import MFE
from python_codon_tables import get_codons_table
from utils.Datatypes import OptimizationParameters
from utils.Datatypes import SequenceProperties, EvaluationResults
from utils.Logger import MyLogger

# setting up a logger
logger = MyLogger(__name__)


class Evaluation(object):
    """ This class allows evaluate the final results by calculating sequence parameters and ranking the final results"""

    def __init__(self, optimized_seqs: List[str], parameters: OptimizationParameters):
        self.input_seq = parameters.input_mRNA.upper()
        self.optimized_seqs = optimized_seqs
        self.max_GC_content = parameters.max_GC_content
        self.min_GC_content = parameters.min_GC_content
        self.GC_window_size = parameters.GC_window_size
        self.usage_threshold = parameters.usage_threshold
        self.uridine_depletion = parameters.uridine_depletion
        self.organism = parameters.organism
        self.location = parameters.location
        self.entropy_window = parameters.entropy_window
        self.five_end = parameters.five_end.replace('T', 'U')
        self.three_end = parameters.three_end.replace('T', 'U')
        self.evaluation_dict = {}
        self.dinucleotides = parameters.dinucleotides
        self.codon_pair = parameters.codon_pair

    def score(self, sequence: str, gc_ratio: float, mfe5: float, mfe_total: float) -> float:
        """
        Use sequence properties to calculate a score for ranking.
        :param sequence: RNA sequence
        :param gc_ratio: GC ratio in the sequence
        :param mfe5: MFE of the 5' end (calculated by RNAfold)
        :param mfe_total: MFE of the full sequence
        :return: ranking score
        """

        # MFE at 5' end
        mfe_5_score = math.exp(mfe5 / 100)

        # total MFE score
        mfe_score = math.exp(mfe_total / 1000)

        # Score reflecting how far we are from the target codon usage
        codon_score = 1 - (self.get_codon_comparison_organism(sequence) / (len(sequence) / 3))
        # minimum: 0
        # maximum: 1 (when normalized by length in codons) (maximum absolute value)

        # count each U at third position in codon, normalize to codon number
        u_depletion = sum(1 for i in range(0, len(sequence) - 2, 3) if sequence[i + 2] in ["U", "T"]) / (
                len(sequence) / 3)
        # minimum: 0 (no codons have U at third pos)
        # maximum: 1 (all codons have U)

        # GC content score
        gc_score = (gc_ratio - self.min_GC_content) / (self.max_GC_content - self.min_GC_content)

        # Dinucleotide frequency score
        # If a custom table is used in Objectives.py, it needs to be used here, too.
        dinucleotides = MatchTargetPairUsage()
        pair_frequencies = dinucleotides.calculate_freqs(sequence)
        di_score = self.differences_from_table(dinucleotides.pair_usage_table, pair_frequencies)
        dinucleotide_score = 1 - di_score  # This way the score should be between 0 and 1, where 1 is the best
        # normalized by number of all dinucleotides

        # Codon pair frequency score
        codon_pairs = MatchTargetCodonPairUsage()
        codon_pair_freqs = codon_pairs.calculate_freqs(sequence)
        pair_score = self.differences_from_table(codon_pairs.pair_usage_table, codon_pair_freqs)
        codon_pair_score = 1 - pair_score

        # CAI score (coincides with CAI value)
        cai_score = self.CAI(sequence)

        # Score for ranking the output
        # Uridine depletion, GC content, CAI, MFE global, MFE 5' end scores are considered
        w1 = 1  # weight for mfe5 score
        w2 = 8  # weight for gc_sore
        w3 = 10 if self.uridine_depletion else 0  # weight for Uridine depletion score
        w4 = 0 if not (
                    self.codon_pair and self.dinucleotides) else 0  # not used now, can be included by weight modification
        w5 = 0 if self.dinucleotides else 0  # not used now, can be included by weight modification
        w6 = 0 if self.codon_pair else 0  # not used now, can be included by weight modification
        w7 = 7  # weight for CAI score
        w8 = 3  # weight for total MFE score
        score = (w1 * mfe_5_score + w2 * gc_score + w3 * u_depletion + w4 * codon_score +
                 w5 * dinucleotide_score + w6 * codon_pair_score + w7 * cai_score +
                 w8 * mfe_score) / (w1 + w2 + w3 + w4 + w5 + w6 + w7 + w8)
        return score

    def differences_from_table(self, table: Dict[str, float], frequencies: Dict[str, float]) -> float:
        score = 0
        for pair, freq in frequencies.items():
            score_for_pair = abs(freq - frequencies[pair])
            score += score_for_pair
        return score / len(table)

    def get_codon_dict(self, sequence: str) -> Dict[str, dict]:
        """Create a comparison between codon frequencies in the sequence and in the chosen organism."""
        sequence = sequence.replace('U', 'T')
        comparison = MatchTargetCodonUsage(species=self.organism, location=Location(0, len(sequence), 1))
        codons = self.get_codons(sequence)

        codons_positions, aa_comparisons = comparison.compare_frequencies(codons)
        for codon in codons:
            aa = Seq(codon).translate()
            aa_comparisons[aa][codon]["count"] = aa_comparisons[aa][codon].get("count", 0) + 1
        """
        Returns dictionary in format:
         {
           "K": {
             "total": 6,
             "AAA": {
                 "sequence": 1.0,
                 "table": 0.7,
                 "count": 6
             },
             ...
           },
           "D": ...
         }
        """
        return aa_comparisons

    def get_codon_comparison_organism(self, sequence: str) -> float:
        """
        For each codon, calculate absolute difference between frequency in the sequence and in the organism, weighted by
        total number of given codon in the sequence. Return sum of these weighted differences.
        """
        aa_comparisons = self.get_codon_dict(sequence)
        codon_score = 0
        for aa, data in aa_comparisons.items():
            total = data.pop("total")
            for codon, codon_freq in data.items():
                frequency_diff = codon_freq["sequence"] - codon_freq["table"]
                count = aa_comparisons[aa][codon].get("count", 0)
                codon_score += count * abs(frequency_diff)
        return codon_score

    def get_codons(self, sequence: str) -> List[str]:
        """Return a list of codons in the sequence."""
        return [
            sequence[3 * i: 3 * (i + 1)]
            for i in range(int(len(sequence) / 3))
        ]

    def _get_max_frequency(self, codon, usage_table):
        """
        Get frequency of the most frequent synonymous codon to codon for that amino-acid - the scaling factor in the
        RCSU value (CAI is the geometric mean of RCSU values of codons)
        """
        synonymous_codons = [codons for (aa, codons) in SynonymousCodons.items() if codon in codons][0]
        max_freq = max([usage_table[codon] for codon in synonymous_codons])
        return max_freq

    def codon_table_to_biopython_index(self, codon_table: dict) -> dict:
        """Transforms table from python-codon-table library to biopython index format"""
        amino_acids = ['*', 'A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I',
                       'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

        dicts = [codon_table[aa] for aa in amino_acids]
        simple_usage_table = {key: val for dic in dicts for (key, val) in dic.items()}
        return {key: val / self._get_max_frequency(key, simple_usage_table) for key, val in simple_usage_table.items()}

    def CAI(self, sequence: str) -> float:
        """Calculates Codon Adaptation Index for a given sequence"""
        sequence = sequence.replace('U', 'T')
        cai_estimator = CodonAdaptationIndex()
        codon_table = get_codons_table(self.organism)
        index = self.codon_table_to_biopython_index(codon_table)
        cai_estimator.set_cai_index(index)
        return cai_estimator.cai_for_gene(sequence)

    def get_seq_properties(self, tag_seq: Tuple) -> SequenceProperties:
        """
        Calculate properties for the input sequence, return them as a dictionary.
        :param tag_seq: tuple of tag (tag of the sequence), seq (RNA sequence)
        :return: Dictionary of parameters
        """
        # The entire sequence consisting of fixed and variable parts
        full_seq = self.five_end + tag_seq[1] + self.three_end
        rna_sequence = full_seq.replace('T', 'U')
        dna_sequence = full_seq.replace('U', 'T')
        base_ratio = dict()
        seq_len = len(full_seq)
        # Count each nucleotide type
        a_s = sum(full_seq[x] in ['A', 'a'] for x in range(seq_len))
        ts = sum(full_seq[x] in ['U', 'u', 'T', 't'] for x in range(seq_len))
        gs = sum(full_seq[x] in ['G', 'g'] for x in range(seq_len))
        cs = sum(full_seq[x] in ['C', 'c'] for x in range(seq_len))
        # Calculate their ratio
        base_ratio['A'] = a_s / seq_len
        base_ratio['TU'] = ts / seq_len
        base_ratio['G'] = gs / seq_len
        base_ratio['C'] = cs / seq_len
        gc_ratio = base_ratio['G'] + base_ratio['C']
        at_ratio = 1 - gc_ratio

        mfe_estimator = MFE()

        rna_structure, mfe = RNA.fold(full_seq)
        # 5' MFE is calculated up to this index
        index_for_mfe_evaluation = len(self.five_end) + self.entropy_window
        _, mfe5 = RNA.fold(full_seq[:index_for_mfe_evaluation])
        _, mfe_total = RNA.fold(full_seq[index_for_mfe_evaluation:])
        score = self.score(tag_seq[1], gc_ratio, mfe5, mfe_total)

        # calculating CAI
        cai = self.CAI(tag_seq[1])

        logger.info("----------" + str(tag_seq[0]))
        for base, ratio in base_ratio.items():
            logger.info(base + "\t" + str(ratio))
        logger.info(f">>AT Ratio: {at_ratio}")
        logger.info(f">>GC Ratio: {gc_ratio}")
        logger.info(f">>MFE at 5': {mfe5}")
        logger.info(f">>Total MFE: {mfe}")
        logger.info(f">>CAI: {cai}")
        logger.info(f"Score: {score}")

        properties = SequenceProperties(seqID=tag_seq[0],
                                        RNASeq=rna_sequence,
                                        DNASeq=dna_sequence,
                                        RNA_structure=rna_structure,
                                        A_ratio=base_ratio['A'],
                                        TU_ratio=base_ratio['TU'],
                                        G_ratio=base_ratio['G'],
                                        C_ratio=base_ratio['C'],
                                        AT_ratio=at_ratio,
                                        GC_ratio=gc_ratio,
                                        MFE=mfe,
                                        MFE_5=mfe5,
                                        score=score,
                                        CAI=cai)

        return properties

    def get_evaluation(self) -> Dict:
        """
        For the set of sequences, create a dictionary containing basic properties for each of them.
        :return: Dictionary of sequence properties
        """
        tag_seqs = [('opt_' + str(i), seq) for i, seq in enumerate(self.optimized_seqs)]

        pool = Pool()
        optimized_results = pool.map(self.get_seq_properties, tag_seqs)

        optimized_results_sorted = sorted(optimized_results, key=lambda k: k.score, reverse=True)

        evaluation_results = EvaluationResults(input=self.get_seq_properties(('input', self.input_seq)),
                                               optimized=optimized_results_sorted)

        return evaluation_results.dict()
