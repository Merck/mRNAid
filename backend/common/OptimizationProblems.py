from constraints.Constraints import Constraints
from dnachisel import DnaOptimizationProblem
from dnachisel.Location import Location
from objectives.Objectives import Objectives
from utils.Datatypes import OptimizationParameters
from utils.Exceptions import SpeciesError


def initialize_optimization_problem(parameters: OptimizationParameters) -> DnaOptimizationProblem:
    """
    Combines all constraints and objectives together to create a list of DNA Optimization problems.
    :param parameters: optimization parameters
    :return: optimization problem object
    """

    constraints_creator = Constraints(parameters.avoid_motifs, parameters.uridine_depletion,
                                      parameters.min_GC_content, parameters.max_GC_content, parameters.organism,
                                      parameters.usage_threshold,
                                      Location(0, len(parameters.input_DNA)))
    try:
        constraints = constraints_creator.create_constraints()
    except FileNotFoundError as e:
        raise SpeciesError("No data provided for the organism {}".format(parameters.organism))

    # Create objectives
    objectives_creator = Objectives(parameters.entropy_window, parameters.organism,
                                    Location(0, len(parameters.input_DNA)), parameters.min_GC_content,
                                    parameters.max_GC_content, parameters.GC_window_size, parameters.five_end,
                                    parameters.mfe_method, parameters.dinucleotides, parameters.codon_pair,
                                    parameters.CAI)

    try:
        objectives = objectives_creator.create_objectives()
    except FileNotFoundError as e:
        raise SpeciesError("No data provided for the organism {}".format(parameters.organism))

    return DnaOptimizationProblem(sequence=parameters.input_DNA, constraints=constraints, objectives=objectives)
