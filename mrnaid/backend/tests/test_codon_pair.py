from statistics import mean

from dnachisel import DnaOptimizationProblem
from common.objectives.Codon_pair_usage import MatchTargetCodonPairUsage


def get_ratios_from_sequence(sequence):
    """Function to calculate codon pair frequencies from the input sequence"""
    objective = MatchTargetCodonPairUsage()
    pair_usage_table = objective.pair_usage_table
    total_number_of_pairs = len(sequence) / 3 - 1
    calculated_freqs = {}
    counts = {}
    for i in range(0, len(sequence) - 3, 3):
        counts[sequence[i:i + 6]] = counts.get(sequence[i:i + 6], 0) + 1
    for pair, _ in counts.items():
        calculated_freqs[pair] = counts.get(pair, 0) / total_number_of_pairs
    return calculated_freqs


def calculate_mean_ratio(calculated_freqs):
    """Function which calculates mean value from the dictionary of frequencies"""
    objective = MatchTargetCodonPairUsage()
    pair_usage_table = objective.pair_usage_table
    ratios = []
    for pair, fr in calculated_freqs.items():
        ratios.append(pair_usage_table[pair] / fr)
    return mean([abs(1 - ratio) for ratio in ratios])


def optimization(organism):
    """Check that optimized codon pair frequencies are closer to target than original ones"""
    input_sequence = "CCGTCGCGGCAGGTTATTATACCTCATTCCTTGGAGACATACAACTATCAATGGGACTTGAGGTTAAGGTATTCCCGCATGAACGCGTGTACTGAAAATATGAAGGCGAGGGCGGAAGCTTTCATTAGCGAGCACCTACAACGTTAGAGTTGGTCGTGTCTTGCTATGCGTCCAGCACATCTGTAAGCCGGTATAAGGCCAGGGGCGGTACATATCGTACAGATCTAGTACATGTTGATAACTTTCATCTGTCGTAGGAAGGCGGAGCCGCCCCTGACGGACGTAGAAAGGGGAATGGGCACTGAGACCCAGTGAGCCCCTTTTGCGTTCTTGGCAAATACCTAGACCTTCTGGTCGTCCTATCGTAATATCTCCTGATACTCATGACAGCAGGATAGCAGCCTGCAACCTCCATGTACTTCGTTGGATTCTTTCCGAGTCTCGTGTGAGTAGATGCTTTGGGGAGTTACCTCTAACACATGGCTTGTTTATTCGTAATTCGACTCCCATGCTTGCTTTTAAACGTCTGTCAACATGAACATTCTGGTCGCACGACGATTAAGAAAGGGAACTTCGTGTTGATGTAGTAGGATATAGCAG"
    objective = MatchTargetCodonPairUsage(species=organism)
    problem = DnaOptimizationProblem(input_sequence, objectives=[objective])
    problem.resolve_constraints()
    problem.optimize()

    optimized_sequence = problem.sequence
    optimized_ratios = get_ratios_from_sequence(optimized_sequence)
    optimized_mean = calculate_mean_ratio(optimized_ratios)

    input_ratios = get_ratios_from_sequence(input_sequence)
    input_mean = calculate_mean_ratio(input_ratios)

    assert optimized_mean < input_mean


def test_optimized_frequencies_human():
    optimization('h_sapiens')

def test_optimized_frequencies_mouse():
    optimization('m_musculus')