from utils.Exceptions import WrongCharSequenceError
from utils.RequestParser import RequestParser
import pytest
from tests.test_request_parsing import MockRequest

def assert_wrong_char(example_parameters, sequences):
    request = MockRequest(**example_parameters, sequences=sequences)
    parser = RequestParser(request)
    try:
        parameters = parser.parse()
    except WrongCharSequenceError as e:
        right_error_raised = True
    else:
        right_error_raised = False
    assert right_error_raised

@pytest.fixture
def example_parameters():
    return {
        "config": {
            "avoid_codons": [],
            "avoided_motifs": [],
            "codon_usage_frequency_threshold": 0.1,
            "max_GC_content": 0.6,
            "GC_window_size": 30,
            "min_GC_content": 0.4,
            "organism": 'h_sapiens',
            "entropy_window": 6,
            "number_of_sequences": 5
        },
        "dinucleotides": False,
        "match_codon_pair": False,
        "uridine_depletion": True,
        "faster_MFE_algorithm": False,
        "precise_MFE_algorithm": False,
        "CAI": False,
        "file_name": "test",
    }


def test_RNA_seq_wrong_char(example_parameters):
    """Assert that RNA sequence contains only allowd characters"""
    sequences = {"five_end_flanking_sequence": "AGAACCGCACTCGGGAGGTTAAGCCGTCAATAACAATGACTCAAAGCCAAATGGTACTTGATAAGCGCAGCGTGGTGT",
                 "gene_of_interest": "bbbbbbbbbbbbbbbbbb",
                 "three_end_flanking_sequence": "CATCGCGGGAATGCTACCTAGACTTGGGGTAAGTCGATCCAGTGTCCC"}
    assert_wrong_char(example_parameters, sequences)


def test_five_end_seq_wrong_char(example_parameters):
    """Assert that five flanking sequence contains only allowd characters"""
    sequences = {"five_end_flanking_sequence": "wwwwwwwww!",
                 "gene_of_interest": "CAGATCCGCATATGTCCTACTTCTGTCGGTGAG",
                 "three_end_flanking_sequence": "CATCGCGGGAATGCTACCTAGACTTGGGGTAAGTCGATCCAGTGTCCC"}
    assert_wrong_char(example_parameters, sequences)


def test_three_end_seq_wrong_char(example_parameters):
    """Assert that three flanking sequence contains only allowd characters"""
    sequences = {"five_end_flanking_sequence": "AGAACCGCACTCGGGAGGTTAAGCCGTCAATAACAATGACTCAAAGCCAAATGGTACTTGATAAGCGCAGCGTGGTGT",
                 "gene_of_interest": "CAGATCCGCATATGTCCTACTTCTGTCGGTGAG",
                 "three_end_flanking_sequence": "klkklkK"}
    assert_wrong_char(example_parameters, sequences)