from tests.test_request_parsing import MockRequest
from utils.Exceptions import EntropyWindowError
from utils.RequestParser import RequestParser


def test_neg_entropy_window():
    config = {
        "avoid_codons": ["ATG"],
        "avoided_motifs": [],
        "codon_usage_frequency_threshold": 0.1,
        "max_GC_content": 0.7,
        "GC_window_size": 30,
        "min_GC_content": 0.3,
        "organism": 'h_sapiens',
        "entropy_window": -6,
        "number_of_sequences": 5
    }
    dinucleotides = False
    uridine_depletion = True
    faster_MFE_algorithm = True
    filename = 'test'
    sequences = {"five_end_flanking_sequence": "ACG",
                 "gene_of_interest": "AGCAAAGAAGGCGGA",
                 "three_end_flanking_sequence": "ACG"}
    request = MockRequest(config=config,
                          dinucleotides=dinucleotides, uridine_depletion=uridine_depletion,
                          faster_MFE_algorithm=faster_MFE_algorithm, filename=filename, sequences=sequences)
    parser = RequestParser(request)

    try:
        parameters = parser.parse()
        right_error_raised = False
    except EntropyWindowError as e:
        right_error_raised = True
    except Exception as e:
        right_error_raised = False
    assert right_error_raised


def test_no_entropy_window():
    config = {
        "avoid_codons": ["ATG"],
        "avoided_motifs": [],
        "codon_usage_frequency_threshold": 0.1,
        "max_GC_content": 0.7,
        "GC_window_size": 30,
        "min_GC_content": 0.3,
        "organism": 'h_sapiens',
        "entropy_window": None,
        "number_of_sequences": 5
    }
    dinucleotides = False
    uridine_depletion = True
    faster_MFE_algorithm = True
    filename = 'test'
    sequences = {"five_end_flanking_sequence": "ACG",
                 "gene_of_interest": "AGCAAAGAAGGCGGA",
                 "three_end_flanking_sequence": "ACG"}
    request = MockRequest(config=config,
                          dinucleotides=dinucleotides, uridine_depletion=uridine_depletion,
                          faster_MFE_algorithm=faster_MFE_algorithm, filename=filename, sequences=sequences)
    parser = RequestParser(request)

    try:
        parameters = parser.parse()
        right_error_raised = False
    except EntropyWindowError as e:
        right_error_raised = True
    except Exception as e:
        right_error_raised = False
    assert right_error_raised
