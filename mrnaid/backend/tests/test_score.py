from utils.Evaluation import Evaluation
from utils.Datatypes import OptimizationParameters
import pytest


@pytest.fixture
def example_parameters():
    def _example_parameters(mRNA_seq, entropy_window):
        dna = mRNA_seq.replace('U', 'T')
        parameters = OptimizationParameters(
            input_mRNA=mRNA_seq,
            input_DNA=dna,
            five_end="ATG",
            three_end="CGG",
            avoid_codons=[],
            avoid_motifs=[],
            max_GC_content=0.7,
            min_GC_content=0.3,
            GC_window_size=30,
            usage_threshold=0.1,
            uridine_depletion=True,
            organism='h_sapiens',
            entropy_window=entropy_window,
            number_of_sequences=3,
            mfe_method='stem_loop',
            dinucleotides=False,
            location=(0, len(mRNA_seq) - len(mRNA_seq) % 3, 1),
            filename="optimization_results"
        )
        return parameters
    return _example_parameters


def test_ranking(example_parameters):
    """Check if the sequences are ranked properly by the Evaluation class"""
    seq_in = "AUGCCUGCGGAUCCGAGAAACGCCGGAAAGGACAAAGGAAAUCUUCAGAUGGAGCUCCAGAACUUGCUCACUUCCGCAAGAAUAAGGAAGAUGGAGUACGAAGCAAUAGUGGAAGAGCUUGAGGAAGACGAGCUCAAAUACGACCUCUUUGAGUACCAAGACUACCUUGAAAAUUACAUUAUGCCCUACGUUGAAAGAGCUUACAAAAACGGCAGUAAAGAACUGAUAGGAAUGGCGGAGGAAGUAAAGAGUAUAUUUGAAGAAAUUAUUGAUAUGAUAAAGGCGAGAAUAGAAAAGAAGUGA"
    seq1 = "AUGCCGGCGGACCCAAGAAACGCCGGCAAGGACAAGGGAAACUUGCAGAUGGAGCUGCAGAACUUGUUGACCUCCGCCCGAAUCAGGAAGAUGGAAUACGAAGCAAUAGUAGAGGAGCUGGAGGAAGACGAGCUGAAAUACGACCUCUUCGAGUACCAAGACUACCUCGAAAACUACAUCAUGCCCUACGUGGAACGCGCCUACAAAAACGGCUCAAAAGAGCUGAUAGGGAUGGCGGAGGAGGUCAAGAGCAUCUUCGAAGAGAUCAUCGACAUGAUAAAGGCACGGAUAGAAAAGAAAUGA"
    seq2 = "AUGCCAGCAGACCCGCGGAACGCCGGCAAGGACAAAGGAAACCUGCAGAUGGAACUGCAGAACUUGCUCACCUCCGCACGAAUAAGGAAGAUGGAGUACGAGGCAAUAGUGGAGGAGCUGGAGGAAGACGAGUUGAAAUACGACCUCUUCGAGUACCAAGACUACCUGGAAAACUACAUCAUGCCCUACGUCGAAAGAGCGUACAAAAACGGCUCAAAAGAACUGAUAGGGAUGGCCGAGGAAGUAAAGAGCAUCUUCGAAGAGAUCAUCGACAUGAUCAAGGCCCGCAUAGAGAAGAAGUGA"
    seq3 = "AUGCCGGCAGACCCACGAAACGCCGGCAAGGACAAAGGGAACCUGCAGAUGGAGCUGCAGAACUUGCUGACCUCCGCACGCAUAAGGAAGAUGGAGUACGAAGCAAUCGUGGAAGAGCUGGAGGAAGACGAGUUGAAAUACGACCUCUUCGAGUACCAAGACUACCUCGAAAACUACAUCAUGCCCUACGUCGAAAGAGCCUACAAAAACGGCAGCAAAGAACUGAUCGGAAUGGCCGAGGAGGUAAAGUCAAUAUUCGAGGAGAUCAUCGACAUGAUAAAGGCGCGGAUAGAAAAGAAGUGA"
    optimized = [seq1, seq2, seq3]
    parameters = example_parameters(seq_in, 10)

    evaluator = Evaluation(optimized, parameters)

    seq0_properties = evaluator.get_seq_properties("seq0", seq_in)
    seq1_properties = evaluator.get_seq_properties("seq1", seq1)
    seq2_properties = evaluator.get_seq_properties("seq2", seq2)
    seq3_properties = evaluator.get_seq_properties("seq3", seq3)

    # Sequence 1 is the best one
    assert seq0_properties.score < seq1_properties.score
    assert seq0_properties.score < seq2_properties.score
    assert seq0_properties.score < seq3_properties.score
    assert seq1_properties.score > seq2_properties.score
    assert seq2_properties.score > seq3_properties.score


def test_ranking_w_longer_window(example_parameters):
    """Check if the sequences are ranked properly by the Evaluation class"""
    seq_in = "AUGCCUGCGGAUCCGAGAAACGCCGGAAAGGACAAAGGAAAUCUUCAGAUGGAGCUCCAGAACUUGCUCACUUCCGCAAGAAUAAGGAAGAUGGAGUACGAAGCAAUAGUGGAAGAGCUUGAGGAAGACGAGCUCAAAUACGACCUCUUUGAGUACCAAGACUACCUUGAAAAUUACAUUAUGCCCUACGUUGAAAGAGCUUACAAAAACGGCAGUAAAGAACUGAUAGGAAUGGCGGAGGAAGUAAAGAGUAUAUUUGAAGAAAUUAUUGAUAUGAUAAAGGCGAGAAUAGAAAAGAAGUGA"
    seq1 = "AUGCCAGCAGACCCAAGAAAUGCAGGAAAAGACAAAGGAAAUCUGCAGAUGGAGCUCCAGAACUUGCUUACCUCCGCUCGGAUAAGGAAGAUGGAGUACGAAGCGAUCGUGGAGGAGCUUGAGGAAGACGAGCUGAAGUAUGAUCUCUUUGAGUACCAAGAUUACCUGGAGAACUAUAUUAUGCCCUACGUGGAACGAGCUUAUAAAAACGGCAGCAAGGAACUGAUAGGGAUGGCCGAGGAGGUCAAGUCUAUCUUCGAAGAAAUCAUUGAUAUGAUUAAGGCCCGCAUCGAAAAGAAAUGA"
    seq2 = "AUGCCAGCAGACCCAAGAAAUGCAGGAAAAGACAAAGGAAAUUUGCAGAUGGAGCUGCAGAACCUGCUCACCUCCGCCCGGAUAAGGAAGAUGGAGUACGAAGCUAUCGUGGAAGAGCUUGAGGAAGAUGAACUGAAAUACGACCUCUUCGAAUAUCAAGAUUACCUCGAGAACUAUAUUAUGCCUUACGUCGAGCGCGCGUAUAAGAACGGCUCUAAAGAGCUGAUCGGGAUGGCUGAAGAAGUUAAGAGCAUCUUUGAGGAGAUUAUUGAUAUGAUCAAGGCCCGAAUAGAGAAGAAGUGA"
    seq3 = "AUGCCAGCAGACCCAAGAAAUGCAGGAAAAGACAAAGGAAAUCUCCAGAUGGAGCUGCAGAACUUGCUUACCUCCGCCCGAAUUAGGAAGAUGGAGUACGAAGCCAUCGUAGAAGAGCUUGAGGAGGACGAGCUCAAGUAUGAUCUGUUUGAAUACCAAGAUUAUCUGGAGAACUAUAUUAUGCCCUACGUUGAACGGGCUUACAAAAACGGCUCUAAGGAACUGAUCGGGAUGGCUGAGGAGGUCAAAAGCAUAUUCGAAGAGAUUAUCGAUAUGAUCAAGGCGCGCAUAGAAAAGAAGUGA"
    optimized = [seq1, seq2, seq3]
    parameters = example_parameters(seq_in, 40)

    evaluator = Evaluation(optimized, parameters)

    seq0_properties = evaluator.get_seq_properties("seq0", seq_in)
    seq1_properties = evaluator.get_seq_properties("seq1", seq1)
    seq2_properties = evaluator.get_seq_properties("seq2", seq2)
    seq3_properties = evaluator.get_seq_properties("seq3", seq3)

    # Sequence 1 is the best one
    assert seq0_properties.score < seq1_properties.score
    assert seq0_properties.score < seq2_properties.score
    assert seq0_properties.score < seq3_properties.score
    assert seq1_properties.score > seq2_properties.score
    assert seq2_properties.score > seq3_properties.score


def test_gc_score(example_parameters):
    """Check if the sequences with optimal GC content are ranked higher than sequences with extreme GC content"""
    seq_gc = "GCCGGCCCCCGGTGCGACGAGGTGAGCCCCTGGAGCCGG"
    seq_at = "TGATTCATCAAAATGAACACTTACATCACTAAATGAAAA"
    seq_opt = "CGGTGAGACAAACTGAACTGGTTCGGCTACGAGAAACTG"
    seqs = [seq_gc, seq_opt]
    parameters = example_parameters(seq_at, 5)

    evaluator = Evaluation(seqs, parameters)

    seq_opt_properties = evaluator.get_seq_properties("seq_opt", seq_opt)
    seq_gc_properties = evaluator.get_seq_properties("seq_gc", seq_gc)
    seq_at_properties = evaluator.get_seq_properties("seq_at", seq_at)

    assert seq_opt_properties.score > seq_at_properties.score
    assert seq_opt_properties.score > seq_gc_properties.score


