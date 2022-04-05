from dnachisel import DnaOptimizationProblem
from dnachisel.Location import Location
from common.constraints.UridineDepletion import UridineDepletion


def test_uridine_depletion_with_occurrences():
    """Check if breach locations are correctly identified"""
    uridine_depletion = UridineDepletion()
    sequence = "AATCTAGTCCCTACGTGA"
    problem = DnaOptimizationProblem(sequence, [uridine_depletion])
    evaluation = uridine_depletion.evaluate(problem)
    assert len(evaluation.locations) == 2
    assert str(evaluation.locations[0]) == str(Location(0, 3, 1))
    assert str(evaluation.locations[1]) == str(Location(9, 12, 1))


def test_uridine_depletion_no_occurence():
    """Check if breach locations are correctly identified (none in this case)"""
    uridine_depletion = UridineDepletion()
    sequence = "AAGCTAGTCCCAACGTGA"
    problem = DnaOptimizationProblem(sequence, [uridine_depletion])
    evaluation = uridine_depletion.evaluate(problem)
    assert len(evaluation.locations) == 0
    assert evaluation.score == 0


def test_uridine_depletion_optimization_results():
    """Check if the uridine depletion is correctly applied during optimization (no U at third position in any codon)"""
    # optimization
    uridine_depletion = UridineDepletion()
    sequence = "AATCTAGTCCCTACGTGA"
    problem = DnaOptimizationProblem(sequence, [uridine_depletion])
    problem.resolve_constraints()
    problem.optimize()
    optimized_sequence = problem.sequence

    # evaluation
    for_evaluation = DnaOptimizationProblem(optimized_sequence, [uridine_depletion])
    evaluation = uridine_depletion.evaluate(for_evaluation)
    for i in range(0, len(optimized_sequence) - 2, 3):
        assert optimized_sequence[i + 2] != "T"
    assert len(evaluation.locations) == 0
    assert evaluation.score == 0
