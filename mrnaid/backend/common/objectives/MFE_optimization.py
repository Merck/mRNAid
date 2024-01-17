from objectives.MFE import MFE
from dnachisel import (Specification, SpecEvaluation, Location, DnaOptimizationProblem)
from utils.Logger import MyLogger
import RNA

logger = MyLogger(__name__)


class MinimizeMFE(Specification):
    """Minimize absolute value of MFE in the entropy window"""

    def __init__(self, five_end: str, entropy_window: int, boost: float = 10.0, mfe_method: str = "stem-loop") -> None:
        super().__init__()
        self.boost = boost
        self.five_end = five_end
        self.mfe_method = mfe_method
        self.entropy_window = entropy_window

    def localized(self, location, problem=None):
        return self.copy_with_changes(location=location)

    def evaluate(self, problem: DnaOptimizationProblem) -> SpecEvaluation:
        """Return MFE score for the problem' sequence in entropy window"""
        sequence = problem.sequence
        mfe_estimator = MFE()
        loc = Location(0, self.entropy_window)
        try:
            if self.mfe_method == "stem-loop":
                mfe = mfe_estimator.estimate(self.five_end + sequence[:self.entropy_window])
            elif self.mfe_method == "RNAfold":
                _, mfe = RNA.fold(self.five_end + sequence[:self.entropy_window])
            else:
                logger.warning(f'MFE method {self.mfe_method} is unknown! Switching to default one')
                _, mfe = RNA.fold(self.five_end + sequence[:self.entropy_window])
        except Exception as e:
            logger.error(f'Error when calling MFE.estimate {str(e)}')
        score = 100*mfe
        return SpecEvaluation(
            self, problem,
            score=score,
            locations=[loc],
            message="MFE score: {}".format(score)
        )

    def __str__(self) -> str:
        """String representation."""
        return "MinimizeMFE"
