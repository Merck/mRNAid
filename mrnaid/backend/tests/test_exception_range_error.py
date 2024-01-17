from utils.Exceptions import RangeError
from utils.RequestParser import RequestParser
import pytest
from tests.test_request_parsing import MockRequest

def assert_range_error(request):
    parser = RequestParser(request)
    try:
        parameters = parser.parse()
    except RangeError as e:
        right_error_raised = True
    else:
        right_error_raised = False
    assert right_error_raised

@pytest.fixture
def example_parameters():
    def _example_parameters(max_GC_content, min_GC_content, codon_usage):
        return {
        "config": {
            "avoid_codons": [],
            "avoided_motifs": [],
            "codon_usage_frequency_threshold": codon_usage,
            "max_GC_content": max_GC_content,
            "GC_window_size": 30,
            "min_GC_content": min_GC_content,
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
        "sequences": {
            "five_end_flanking_sequence": "AGAACCGCACTCGGGAGGTTAAGCCGTCAATAACAATGACTCAAAGCCAAATGGTACTTGATAAGCGCAGCGTGGTGT",
            "gene_of_interest": "ATACTTTTCTGCATCGACTAAGTCTGAACGGAGAACCCGGAAACATATGTTGCTTCAGAACGCCGAGATTACTGCGTTTAGACTCAAACGAGAAGCGCCCCGCTCGTGTTATCTTCCAACTACCACGTATGTGTTGGACTGTTAGTGCACTTCAGATTGGTCCAAAACACCCTAGATGCTGAACCTGTACCCAGTAAGAAGTACGTAGTCGTTACAAGCAAACCCTAGCTTAGTAAAGGAAGCGCGTCTTACGTGTATGGTGGTTATCTTCCACCGTTGGACTTACGCGATTTGTGGAAATTACTTGCTTGCGTTGCTACGGGATTGAGAAAGCTTGCATATTGGGGGGTCAGACCCGTCATACAGGCCATCATGTCGGAAGGGCAGGTTCCATTGCCAGGTAGCTCCACCGCCCTGACGGGTTTCCAGGCACAGGTATACTCTCATACCAACAAAGCGCTTTCTGGGACTCGACGACACCAGGCCACGCGATGCTTCTCTAGATTCTCTGCGTTCGCTGTTGCATGCAGCCTCGCCTCGTTGAAGATGAGTATACAAACCCTGAACTGGGTGGTCCGATTGCTTGTAGGGTACACAACATGAGGGCGCACAAGCCCGGCGGGCCAATCCTTGATCACAACATATTCTACCTTCACTCCGCCAGACTGCGACCGCGTCAGTGTAAGCCCAAGTTTCGTGTTAGAAATACCACATGAATCGCGATTAACGGAGCACACGGCGCACGACGTCGATCCCTACTTAAGGGGTGTTTGACTCTCACAGTATGTTTATGCTCCGTACAGGCGCCCTAGTCGCAAGAAAGCCACTATGCTTGCTAATTTTTTCTTTGGCACGAACGTGCTTTCTAACTGGTAGATCCTATACTAGGCCTACTCGCTA",
            "three_end_flanking_sequence": "CATCGCGGGAATGCTACCTAGACTTGGGGTAAGTCGATCCAGTGTCCC"
        }
    }
    return _example_parameters


def test_max_GC_higher_1(example_parameters):
    """Assert that max GC content doen`t exceed 100%"""
    request = MockRequest(**example_parameters(1.2, 0.4, 0.1))
    assert_range_error(request)


def test_max_GC_less_0(example_parameters):
    """Assert that max GC content isn`t negative"""
    request = MockRequest(**example_parameters(-2.3, 0.4, 0.1))
    assert_range_error(request)


def test_min_GC_higher_1(example_parameters):
    """Assert that min GC content doen`t exceed 100%"""
    request = MockRequest(**example_parameters(0.7, 1.4, 0.1))
    assert_range_error(request)


def test_min_GC_less_0(example_parameters):
    """Assert that min GC content isn`t negative"""
    request = MockRequest(**example_parameters(0.7, -0.4, 0.1))
    assert_range_error(request)


def test_codon_usage_higher_1(example_parameters):
    """Assert that codon usage frequency threshold doen`t exceed 100%"""
    request = MockRequest(**example_parameters(0.7, 0.4, 3))
    assert_range_error(request)

def test_codon_usage_less_0(example_parameters):
    """Assert that codon usage frequency threshold isn`t negative"""
    request = MockRequest(**example_parameters(0.7, 0.4, -0.1))
    assert_range_error(request)


def test_max_GC_less_min_GC(example_parameters):
    """Assert that max GC content is higher than min GC content"""
    request = MockRequest(**example_parameters(0.1, 0.4, 0.1))
    assert_range_error(request)