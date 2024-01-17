from statistics import mean

from Bio.Seq import Seq
from dnachisel import DnaOptimizationProblem, EnforceTranslation, Location
from common.objectives.Dinucleotide_usage import MatchTargetPairUsage


def test_frequencies():
    """Check calculation of frequencies"""
    seq1 = "AGCAGAGAAGGCGGAAGCAGTGGCGTCCGCAGCTGGGGCTT"
    """
    AG GC CA AG GA AG GA AA AG GG GC CG GG GA AA AG GC CA AG GT TG GG GC CG GT TC CC CG GC CA AG GC CT TG GG GG GG GC CT TT
    40 dinucleotides  
    """
    counts = {"TT": 1, "TC": 1, "TA": 0, "TG": 2,
              "CT": 2, "CC": 1, "CA": 3, "CG": 3,
              "AT": 0, "AC": 0, "AA": 2, "AG": 7,
              "GT": 2, "GC": 7, "GA": 3, "GG": 6}

    total_count = 40
    objective = MatchTargetPairUsage()

    calculated_freqs = objective.calculate_freqs(seq1)
    for pair, value in calculated_freqs.items():
        assert value == counts[pair] / total_count
    score = objective.calculate_score(calculated_freqs)
    print(score)


def get_ratios_from_sequence(sequence):
    """Function to calculate dinucleotide frequencies from the input sequence"""
    objective = MatchTargetPairUsage()
    pair_usage_table = objective.pair_usage_table
    total_number_of_dinuc = len(sequence) - 1
    calculated_freqs = {}
    counts = {}
    for i in range(0, len(sequence) - 1):
        counts[sequence[i:i + 2]] = counts.get(sequence[i:i + 2], 0) + 1
    for pair, _ in pair_usage_table.items():
        calculated_freqs[pair] = counts.get(pair, 0) / total_number_of_dinuc
    return calculated_freqs


def calculate_mean_ratio(calculated_freqs):
    """Function which calculates mean value from the dictionary of frequencies"""
    objective = MatchTargetPairUsage()
    pair_usage_table = objective.pair_usage_table
    ratios = []
    for pair, fr in calculated_freqs.items():
        ratios.append(fr / pair_usage_table[pair])
    return mean([abs(1 - ratio) for ratio in ratios])

def optimization(organism: str):
    """Check that optimized dinucleotide frequencies are closer to target than original ones"""
    input_sequence = "CCGTCGCGGCAGGTTATTATACCTCATTCCTTGGAGACATACAACTATCAATGGGACTTGAGGTTAAGGTATTCCCGCATGAACGCGTGTACTGAAAATATGAAGGCGAGGGCGGAAGCTTTCATTAGCGAGCACCTACAACGTTAGAGTTGGTCGTGTCTTGCTATGCGTCCAGCACATCTGTAAGCCGGTATAAGGCCAGGGGCGGTACATATCGTACAGATCTAGTACATGTTGATAACTTTCATCTGTCGTAGGAAGGCGGAGCCGCCCCTGACGGACGTAGAAAGGGGAATGGGCACTGAGACCCAGTGAGCCCCTTTTGCGTTCTTGGCAAATACCTAGACCTTCTGGTCGTCCTATCGTAATATCTCCTGATACTCATGACAGCAGGATAGCAGCCTGCAACCTCCATGTACTTCGTTGGATTCTTTCCGAGTCTCGTGTGAGTAGATGCTTTGGGGAGTTACCTCTAACACATGGCTTGTTTATTCGTAATTCGACTCCCATGCTTGCTTTTAAACGTCTGTCAACATGAACATTCTGGTCGCACGACGATTAAGAAAGGGAACTTCGTGTTGATGTAGTAGGATATAGCAG"
    objective = MatchTargetPairUsage(species=organism)
    problem = DnaOptimizationProblem(input_sequence, objectives=[objective])
    problem.resolve_constraints()
    problem.optimize()

    optimized_sequence = problem.sequence
    # optimized_sequence = "CCAGCCCGGGTCGCCGGCTACGCAGGTTATTGTTGGACACAAGCAACAAACTAGATCGGAAGGTCTTATATCGTAATACAGACTAGGAATTTGGCGCGCTGGCGTCTGCTTCAAGTCCGCCAGGGTAATGGCCTTGAATACGGATCCCCAGACCTTCTCGCGACCATGCCAGGGAGAGAGCAGTCCATGCTAAACTCCGACCCACGGTCAACATCAATCCGTGTAAGTAGGGTTATTCATAACTATATCAGCAGCGTGGCCGATGGCGACAATTTAGGTCTTAAGTCGGGAGGCAACACCTTATACCCTACATCGTAGACCGCCGCCAACGACGTAATTTGGCTGTCAAGGAGGCGGGCGTGTGAGACCTCTTGTTCGTCTATAGAGACACGGTCATCCCATATTTTATGTAGATCGCGACGTGAAATTGAGCTAATTGGCCGTCTTGATTGAAAGGGAGAACCCTATCCTGTGGGAATTACAAATCGGTCTTGATTGTGGAAGGTTCCTAGGAATCATGCCTCAAGCGCATACAGTAGTGCCGCACATTAAACCGTAGTGTCTAGGATGCTTACGGGGCTGACTGGCCTCATGGGATCT"
    optimized_ratios = get_ratios_from_sequence(optimized_sequence)
    optimized_mean = calculate_mean_ratio(optimized_ratios)

    input_ratios = get_ratios_from_sequence(input_sequence)
    input_mean = calculate_mean_ratio(input_ratios)

    assert optimized_mean < input_mean


def test_optimized_frequencies_human():
    optimization('h_sapiens')

def test_optimized_frequencies_mouse():
    optimization('m_musculus')



def test_correct_translation():
    input_sequence = "AUGACGAAAUCAGAUAUAGCUAAGGAACUCGCAAGGAGGCACGGCAUAUCCUACAAAAAAGCCCUCCUUAUAGUCAACAUGACCUUUGAGAUACUAAAAGCAAAAAUACUGAACGGUGAAAAGGUAGAGGUAAGGGGACUGGGAACCUUUAAGUUGAAGAGAAAACCGGGAAGGUUCGUAAAGAACCCGAAAACGGGUAUAGAAAUUUACGUAAAGGAGAGGUACGUUCCCUACUACAAGAUGUCUAAACUUUUAAGGAAGAAACUAAACGGCGAUAAAGAAAGGGAGGAGUGUUUGACUUGA"
    original_translation = Seq(input_sequence).translate()
    objective = MatchTargetPairUsage(species='h_sapiens')
    constraint = EnforceTranslation(genetic_table='Standard', location=Location(0, len(input_sequence), 1))

    problem = DnaOptimizationProblem(input_sequence.replace('U', 'T'), objectives=[objective], constraints=[constraint])
    problem.resolve_constraints()
    problem.optimize()
    optimized_sequence = problem.sequence
    translation = Seq(optimized_sequence).translate()

    assert translation == original_translation

    optimized_ratios = get_ratios_from_sequence(optimized_sequence)
    optimized_mean = calculate_mean_ratio(optimized_ratios)

    input_ratios = get_ratios_from_sequence(input_sequence)
    input_mean = calculate_mean_ratio(input_ratios)

    assert optimized_mean < input_mean
