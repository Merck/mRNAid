from utils.RequestParser import RequestParser
from utils.Exceptions import SpeciesError
import pytest
from tests.test_request_parsing import MockRequest


@pytest.fixture
def example_parameters():
    def _example_parameters(organism):
        return {
            "config": {
                "avoid_codons": [],
                "avoided_motifs": [],
                "codon_usage_frequency_threshold": 0.1,
                "max_GC_content": 0.7,
                "GC_window_size": 30,
                "min_GC_content": 0.3,
                "organism": organism,
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


def test_correct_organism_human(example_parameters):
    """Assert correct human organism name is given"""
    organism_var = ["h_sapiens", "sapiens", "human", "homo_sapiens", "h sapiens", "homo sapiens", "H sapiens", "Homo Sapiens", "H_sapiens"]
    for organism in organism_var:
        organism_parametrs = example_parameters(organism=organism)
        request = MockRequest(**organism_parametrs)
        parser = RequestParser(request)
        parameters = parser.parse()
        assert parameters.organism == "h_sapiens"


def test_correct_organism_mouse(example_parameters):
    """Assert correct mouse organism name is given"""
    organism_var = ["m_musculus", "mouse", "mus_musc", "mus_musculus", "mus", "mus musculus", "m musculus", "M_musculus", "Mus Musculus"]
    for organism in organism_var:
        organism_parametrs = example_parameters(organism=organism)
        request = MockRequest(**organism_parametrs)
        parser = RequestParser(request)
        parameters = parser.parse()
        assert parameters.organism == "m_musculus"


def test_species_error_input(example_parameters):
    """Assert SpeciesError is raised when invalid organism is given"""
    request = MockRequest(**example_parameters(organism="wrong_organism"))
    parser = RequestParser(request)
    try:
        parameters = parser.parse()
    except SpeciesError as e:
        right_error_raised = True
    else:
        right_error_raised = False
    assert right_error_raised
