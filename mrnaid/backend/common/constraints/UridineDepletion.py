from dnachisel import DnaOptimizationProblem
from dnachisel.Location import Location
from dnachisel.Specification import SpecEvaluation
from dnachisel.builtin_specifications.CodonSpecification import CodonSpecification


class UridineDepletion(CodonSpecification):
    """
    Avoid codon with U in third position in the sequence.
    """

    def __init__(self, location=None, boost=1.0):
        self.boost = boost
        self.location = Location.from_data(location)

    def initialized_on_problem(self, problem: DnaOptimizationProblem, role="constraint"):
        """Get translation from the sequence if it is not already set."""
        return self._copy_with_full_span_if_no_location(problem)

    def localized_on_window(self, new_location, start_codon, end_codon):
        return self.copy_with_changes(location=new_location)

    def evaluate(self, problem: DnaOptimizationProblem) -> SpecEvaluation:
        location = (
            self.location
            if self.location is not None
            else Location(0, len(problem.sequence))
        )
        subsequence = location.extract_sequence(problem.sequence)
        errors_locations = [
            Location(i + location.start, i + 3 + location.start, 1)  # Safe to assume strand is always 1?
            for i in range(0, len(subsequence) - 2, 3)
            if subsequence[i + 2] == "T"
        ]
        return SpecEvaluation(
            self,
            problem,
            score=-len(errors_locations),
            locations=errors_locations,
            message="All OK."
            if len(errors_locations) == 0
            else "U in third position found at indices %s" % errors_locations,
        )

    def __str__(self) -> str:
        """Represent."""
        return "UridineDepletion"
