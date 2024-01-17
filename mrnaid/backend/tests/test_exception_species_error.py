from OptimizationProblems import initialize_optimization_problem
from OptimizationTask import optimization_task
from utils.Datatypes import OptimizationParameters
from utils.Exceptions import SpeciesError


def test_species_error():
    mRNA_seq = "AAUCAAAUAGGGUUAAGUCUAGGAUUGUUAGUCUGCUAAGGUCUGCAGUUACUGUGUCUACUGAUGAUAGUUCGCAUUGACAAU"
    dna = mRNA_seq.replace('U', 'T')
    parameters = OptimizationParameters(
        input_mRNA=mRNA_seq,
        input_DNA=dna,
        five_end="ATG",
        three_end="CGG",
        avoid_codons=['AAA', 'AAG'],
        avoid_motifs=[],
        max_GC_content=0.7,
        min_GC_content=0.3,
        GC_window_size=30,
        usage_threshold=0.1,
        uridine_depletion=True,
        organism='wrong_organism',
        entropy_window=8,
        number_of_sequences=3,
        mfe_method='stem_loop',
        dinucleotides=False,
        CAI=False,
        codon_pair=False,
        location=(0, len(mRNA_seq) - len(mRNA_seq) % 3, 1),
        filename="optimization_results"
    )

    try:
        optimization_problem = initialize_optimization_problem(parameters)
        sequence = optimization_task(optimization_problem)
    except SpeciesError as e:
        right_error_raised = True
    except Exception as e:
        print(e)
        right_error_raised = False
    else:
        right_error_raised = False
    assert right_error_raised
