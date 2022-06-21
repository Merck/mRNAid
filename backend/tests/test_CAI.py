from Evaluation import CAI
import pytest

test_cases = [('ATGAAGTCGCAATTCAGCTCGCACGTACTCCCGCTAAGCCGAAAGGTCCTATAATCTAGCCGGTCGGGTGTCTGAGATAACTATGCTAACCAGGCCTAACCGCGCGGTATTCAGCTAAGCACTCCGATCCCAAGAGCCAACCGCGAACCAAGTGAAGACTATATCTGTTCGTTCTTCACG', 0.63),
              ('GTAATAGGACTTCTCAAGCAGGTTATGTACCGTCATGTCTTGACCTCCTACGCTTAATCTCTTAGGGGCCCACGGACCTGCGTTCTTCGTCCGCATGACTTACTGCCACTCATCTGTCCGTCTCCTCCCCAGTTGAACCCACGATCGTGG', 0.62),
              ('CCGAAACAATTGGGACACTAGATACAGGTTAACTCCATGGCAGAGACCAATAAACGACCCTGGAAGATTGGCAGCCTTTGAAAATACACGGCGCGTTATACCTCTCAACCTCTGCTGCGCCATTGGCCAGATAGGTCCCCTCCTCTCAGCCCTAGGGCAAAGCTCGAACGTACTCTAGGTTACCCTTACTGCACTTAGATATTCTTCTCCCGGTGACTTGCCGATGATTCTACAAGGGTCGGCTGGGTCGATCCACGTGGTTACCGTGAT', 0.7),
              ('CTAAATGTGATTCCAGTGCGTTGATCGTCGGTTCCATTCACTCTCTCGCTCTATAGTGAGGTTGGTCATCGCATATAACTGCTACTCTGCCTATTGTACAAAACTATCTTGTTATGTTGCGACAACGCCAGATAGCATGTTGGTTTATAGACGTCTTGTTTGCGGGCTAAGGGATACAGAACTGTTGAATGATATCAATCTGCGATCGAGTCGCTTCATAAAGTGTGCGTCTGTCGACTGAGCTGTGGTCGCTGGATGCTCAGTTCTGGT', 0.6)]

@pytest.mark.parametrize("seq", test_cases)
def test_CAI(seq):
    assert round(CAI(seq[0], 'h_sapiens'), 2) == seq[1]