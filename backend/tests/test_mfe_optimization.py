import RNA
import pytest
from dnachisel import DnaOptimizationProblem
from objectives.MFE_optimization import MinimizeMFE


@pytest.fixture
def parameters():
    return {
        'input_sequence': 'CCGTCGCGGCAGGTTATTATACCTCATTCCTTGGAGACATACAACTATCAATGGGACTTGAGGTTAAGGTATTCCCGCATGAACGCGTGTACTGAAAATATGAAGGCGAGGGCGGAAGCTTTCATTAGCGAGCACCTACAACGTTAGAGTTGGTCGTGTCTTGCTATGCGTCCAGCACATCTGTAAGCCGGTATAAGGCCAGGGGCGGTACATATCGTACAGATCTAGTACATGTTGATAACTTTCATCTGTCGTAGGAAGGCGGAGCCGCCCCTGACGGACGTAGAAAGGGGAATGGGCACTGAGACCCAGTGAGCCCCTTTTGCGTTCTTGGCAAATACCTAGACCTTCTGGTCGTCCTATCGTAATATCTCCTGATACTCATGACAGCAGGATAGCAGCCTGCAACCTCCATGTACTTCGTTGGATTCTTTCCGAGTCTCGTGTGAGTAGATGCTTTGGGGAGTTACCTCTAACACATGGCTTGTTTATTCGTAATTCGACTCCCATGCTTGCTTTTAAACGTCTGTCAACATGAACATTCTGGTCGCACGACGATTAAGAAAGGGAACTTCGTGTTGATGTAGTAGGATATAGCAG',
        'five_end': 'CCGTCG',
        'entropy_window': 30}


def optimization(parameters, method):
    """Check that the optimized MFE is closer to zero than input MFE"""
    input_sequence = parameters['input_sequence']
    five_end = parameters['five_end']
    entropy_window = parameters['entropy_window']
    objective = MinimizeMFE(entropy_window=entropy_window, five_end=five_end, mfe_method=method)
    problem = DnaOptimizationProblem(input_sequence, objectives=[objective])
    problem.resolve_constraints()
    problem.optimize()

    optimized_sequence = problem.sequence
    _, input_mfe = RNA.fold(five_end + input_sequence[:entropy_window])
    _, output_mfe = RNA.fold(five_end + optimized_sequence[:entropy_window])

    assert input_mfe < output_mfe


def test_stem_loop_optimization(parameters):
    optimization(parameters, 'stem-loop')


def test_rna_fold_optimization(parameters):
    optimization(parameters, 'RNAfold')
