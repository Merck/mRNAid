import json
import os
from statistics import mean
from typing import Dict, List

from dnachisel import (DnaOptimizationProblem, SpecEvaluation, Location, Specification)
from utils.Logger import MyLogger

logger = MyLogger(__name__)

DEFAULT_BACKEND_OBJECTIVES_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
BACKEND_OBJECTIVES_DATA = os.environ.get('BACKEND_OBJECTIVES_DATA', DEFAULT_BACKEND_OBJECTIVES_DATA)


class MatchTargetCodonPairUsage(Specification):
    """ This class is used to specify the objective to match the target
    usage of codon pairs in organism. The pair usage table is taken
    from CoCoPUTs database"""

    def __init__(self, pair_usage_table: Dict[str, float] = None, location: Location = None, species: str = 'h_sapiens'):
        super().__init__()

        if pair_usage_table is None:
            with open(os.path.join(BACKEND_OBJECTIVES_DATA, f'codon_pair_usage_{species}.json'),
                      'r') as myfile:
                data = myfile.read()
            self.pair_usage_table = json.loads(data)
        else:
            self.pair_usage_table = pair_usage_table

        self.location = Location.from_data(location)

    def evaluate(self, problem: DnaOptimizationProblem) -> SpecEvaluation:
        """Return discrepancy score for the problem"""
        sequence = problem.sequence
        calculated_freqs = self.calculate_freqs(sequence)
        score = self.calculate_score(calculated_freqs)
        breaches = self.get_overrepresented_codon_pairs(sequence, calculated_freqs)

        return SpecEvaluation(
            self, problem,
            score=-score,
            locations=breaches,
            message=f"Codon pair score: {score}"
        )

    def __str__(self) -> str:
        """String representation."""
        return "MatchTargetCodonPairUsage"

    def calculate_freqs(self, sequence: str) -> Dict[str, float]:
        """
        Calculate a dictionary of frequencies for each possible codon pair
        """
        number_of_codon_pairs = len(sequence)/3 - 1
        calculated_freqs = {}

        counts = {}
        for i in range(0, len(sequence) - 3, 3):
            counts[sequence[i:i + 6]] = counts.get(sequence[i:i + 6], 0) + 1
        for pair, _ in counts.items():
            calculated_freqs[pair] = counts.get(pair, 0) / number_of_codon_pairs

        return calculated_freqs

    def calculate_score(self, calculated_freqs: Dict[str, float]) -> float:
        ratios = []
        for pair, fr in calculated_freqs.items():
            table_frequency = self.pair_usage_table[pair]
            ratios.append(table_frequency / fr)
        return mean([abs(1 - ratio) for ratio in ratios])

    def get_overrepresented_codon_pairs(self, sequence: str, calculated_freqs: Dict[str, float]) -> List[Location]:
        pairs = [sequence[i:i + 6] for i in range(0, len(sequence) - 3, 3)]
        pair_positions = {pair: [] for pair in pairs}
        for i in range(0, len(sequence) - 3, 3):
            pair = sequence[i:i + 6]
            pair_positions[pair].append(Location(i, i+6, strand=1))
        nonoptimal = []
        for pair, freq in calculated_freqs.items():
            if freq > self.pair_usage_table[pair]:
                nonoptimal += pair_positions[pair]
        return nonoptimal

    def localized(self, location, problem=None):
        return self.copy_with_changes(location=location)

