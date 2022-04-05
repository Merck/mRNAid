from tests.test_request_parsing import MockRequest
from utils.RequestParser import RequestParser


def test_correct_parsing():
    """Test if the request JSON is parsed correctly"""
    config = {
        "avoid_codons": ["ATG"],
        "avoided_motifs": [],
        "codon_usage_frequency_threshold": 0.1,
        "max_GC_content": 0.7,
        "GC_window_size": 30,
        "min_GC_content": 0.3,
        "organism": 'h_sapiens',
        "entropy_window": 6,
        "number_of_sequences": 5
    }
    dinucleotides = False
    uridine_depletion = False
    faster_MFE_algorithm = False
    filename = 'test'
    sequences = {"five_end_flanking_sequence": "ACG",
                 "gene_of_interest": "AGCAAAGAAGGCGGA",
                 "three_end_flanking_sequence": "ACG"}
    request = MockRequest(config=config,
                          dinucleotides=dinucleotides, uridine_depletion=uridine_depletion,
                          faster_MFE_algorithm=faster_MFE_algorithm, file_name=filename, sequences=sequences)
    parser = RequestParser(request)

    try:
        params = parser.parse()
    except Exception as e:
        print(f'Exception is {e}')
        success = False
    else:
        success = True

    assert success
    assert params.input_mRNA == "AGCAAAGAAGGCGGA"
    assert len(params.avoid_motifs) == 0
    assert len(params.avoid_codons) == 1 and params.avoid_codons[0] == "ATG"
    assert params.max_GC_content == 0.7
    assert params.min_GC_content == 0.3
    assert params.GC_window_size == 30
    assert params.usage_threshold == 0.1
    assert not params.uridine_depletion
    assert params.organism == 'h_sapiens'
    assert params.entropy_window == 6
    assert params.number_of_sequences == 5
    assert params.filename == 'test'
    assert params.mfe_method == 'RNAfold'
    assert not params.dinucleotides
