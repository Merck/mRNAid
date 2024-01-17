import pytest
from Bio.Data.CodonTable import TranslationError
from utils.Exceptions import OptimizationFailedError
from OptimizationProblems import initialize_optimization_problem
from OptimizationTask import optimization_task
from utils.Datatypes import OptimizationParameters


@pytest.fixture
def example_parameters():
    def _example_parameters(mRNA_seq):
        dna = mRNA_seq.replace('U', 'T')
        parameters = OptimizationParameters(
            input_mRNA=mRNA_seq,
            input_DNA=dna,
            five_end="ATG",
            three_end="CGG",
            avoid_codons=['AAA', 'AAG'],
            avoid_motifs=[],
            max_GC_content=0.9,
            min_GC_content=0.8,
            GC_window_size=30,
            usage_threshold=0.1,
            uridine_depletion=True,
            organism='h_sapiens',
            entropy_window=8,
            number_of_sequences=3,
            mfe_method='stem_loop',
            dinucleotides=False,
            codon_pair=False,
            CAI=False,
            location=(0, len(mRNA_seq) - len(mRNA_seq) % 3, 1),
            filename="optimization_results"
        )
        return parameters
    return _example_parameters


def test_optimization_failure_1(example_parameters):
    """Assert that optimization fails when conflicting parameters are given"""
    seq = "AGCAAAGAAGGCGGA"
    params = example_parameters(mRNA_seq=seq)
    optimization_problem = initialize_optimization_problem(params)
    try:
        sequence = optimization_task(optimization_problem)
        right_error_raised = False
    except OptimizationFailedError as e:
        right_error_raised = True
    except:
        right_error_raised = False
    assert right_error_raised
