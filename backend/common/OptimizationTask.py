from dnachisel import DnaOptimizationProblem
from utils.Logger import MyLogger
from utils.Exceptions import OptimizationFailedError

logger = MyLogger(__name__)


def optimization_task(problem: DnaOptimizationProblem) -> str:
    """
    Try to resolve constraints and optimize given problem, catch exceptions, if any.
    :param problem: DnaOptimizationProblem with specified constraints and objectives
    :return: optimized sequence
    """

    try:
        # Resolve constrains
        problem.resolve_constraints()
        # Optimize
        problem.optimize()

        print(problem.constraints_text_summary())
        print(problem.objectives_text_summary())

        # Optimized sequence
        optimized = problem.sequence.replace('T', 'U')
        print("Optimized mRNA sequence:{}".format(optimized))
        logger.debug("Optimized mRNA sequence:{}".format(optimized))
    except Exception as e:
        logger.error(e.message)
        raise OptimizationFailedError()
    else:
        return optimized
