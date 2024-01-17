from tests.test_request_parsing import MockRequest
from utils.RequestParser import RequestParser


def test_parse_incomplete_parameters():
    config = {
        "avoid_codons": [],
        "max_GC_content": 0.7,
        "GC_window_size": 30,
        "min_GC_content": 0.3,
        "entropy_window": 6,
        "number_of_sequences": 5
    }
    sequences = {
        "five_end_flanking_sequence": "AAA",
        "gene_of_interest": "AAAGGGCCCTTT",
        "three_end_flanking_sequence": "AAA"
    }
    request = MockRequest(config=config, sequences=sequences, faster_MFE_algorithm=False)

    parser = RequestParser(request)
    try:
        parameters = parser.parse()
        right_error_raised = False
    except KeyError as e:
        right_error_raised = True
    except:
        right_error_raised = False
    assert right_error_raised
