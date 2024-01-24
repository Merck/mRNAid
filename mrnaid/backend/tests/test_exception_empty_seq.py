import pytest
from tests.test_request_parsing import MockRequest
from utils.Exceptions import EmptySequenceError
from utils.RequestParser import RequestParser


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
        "uridine_depletion": True,
        "faster_MFE_algorithm": False
    }


def test_empty_seq(example_parameters):
    sequences = {"five_end_flanking_sequence": "ACG",
                 "gene_of_interest": "",
                 "three_end_flanking_sequence": "ACG"}
    request = MockRequest(**example_parameters, sequences=sequences)
    parser = RequestParser(request)
    try:
        parameters = parser.parse()
    except EmptySequenceError as e:
        right_error_raised = True
    except Exception as e:
        right_error_raised = False
    else:
        right_error_raised = False
    assert right_error_raised


def test_empty_five_end(example_parameters):
    sequences = {"five_end_flanking_sequence": "",
                 "gene_of_interest": "AAAGGGCCCTTT",
                 "three_end_flanking_sequence": "ACG"}
    request = MockRequest(**example_parameters, sequences=sequences)
    parser = RequestParser(request)
    try:
        parameters = parser.parse()
    except EmptySequenceError as e:
        right_error_raised = True
    except Exception as e:
        right_error_raised = False
    else:
        right_error_raised = False
    assert right_error_raised


def test_empty_three_end(example_parameters):
    sequences = {"five_end_flanking_sequence": "ATG",
                 "gene_of_interest": "AAAGGGCCCTTT",
                 "three_end_flanking_sequence": ""}
    request = MockRequest(**example_parameters, sequences=sequences)
    parser = RequestParser(request)
    try:
        parameters = parser.parse()
    except EmptySequenceError as e:
        right_error_raised = True
    except Exception as e:
        right_error_raised = False
    else:
        right_error_raised = False
    assert right_error_raised
