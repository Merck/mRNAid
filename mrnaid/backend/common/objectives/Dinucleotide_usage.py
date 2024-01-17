import json
import os
from statistics import mean
from typing import Dict, List

from dnachisel import (DnaOptimizationProblem, SpecEvaluation, Location, Specification)
from dnachisel.biotools import group_nearby_indices
from utils.Logger import MyLogger

logger = MyLogger(__name__)

DEFAULT_BACKEND_OBJECTIVES_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
BACKEND_OBJECTIVES_DATA = os.environ.get('BACKEND_OBJECTIVES_DATA', DEFAULT_BACKEND_OBJECTIVES_DATA)

class MatchTargetPairUsage(Specification):
    """ This class is used to specify the objective to match the target
    usage of nucleotide pairs in organism. The pair usage table is taken
    from CoCoPUTs database: https://bigd.big.ac.cn/databasecommons/database/id/6462"""

    def __init__(self, pair_usage_table=None, location=None, species: str = 'h_sapiens'):
        super().__init__()

        if pair_usage_table is None:
            with open(os.path.join(BACKEND_OBJECTIVES_DATA, f'dinucleotides_usage_{species}.json'),
                      'r') as myfile:
                data = myfile.read()
            self.pair_usage_table = json.loads(data)
        else:
            self.pair_usage_table = pair_usage_table

        self.localization_group_spread = 5
        self.location = Location.from_data(location)

    def evaluate(self, problem: DnaOptimizationProblem) -> SpecEvaluation:
        """Return discrepancy score for the problem"""
        sequence = problem.sequence
        calculated_freqs = self.calculate_freqs(sequence)
        score = self.calculate_score(calculated_freqs)
        breaches = self.get_overrepresented_dinucleotides(sequence, calculated_freqs)

        return SpecEvaluation(
            self, problem,
            score=-score,
            locations=self.positions_to_locations(breaches),
            message=f"Dinucleotide score: {score}"
        )

    def __str__(self) -> str:
        """String representation."""
        return "MatchTargetPairUsage"

    def calculate_freqs(self, sequence: str) -> Dict[str, float]:
        """
        Calculate a dictionary of frequencies for each possible dinucleotide
        """
        total_number_of_dinuc = len(sequence) - 1
        calculated_freqs = {}

        counts = {}
        for i in range(0, len(sequence) - 1):
            counts[sequence[i:i + 2]] = counts.get(sequence[i:i + 2], 0) + 1
        for pair, _ in self.pair_usage_table.items():
            calculated_freqs[pair] = counts.get(pair, 0) / total_number_of_dinuc

        return calculated_freqs

    def calculate_score(self, calculated_freqs: Dict[str, float]) -> float:
        ratios = []
        for pair, fr in calculated_freqs.items():
            ratios.append(fr / self.pair_usage_table[pair])
        return mean([abs(1 - ratio) for ratio in ratios])

    def get_overrepresented_dinucleotides(self, sequence: str, freqs: Dict[str, float]) -> List[int]:
        dinuc_positions = {dinuc: [] for dinuc in self.pair_usage_table.keys()}
        for i in range(len(sequence) - 1):
            dinucleotide = sequence[i:i + 2]
            dinuc_positions[dinucleotide].append(i)
        nonoptimal = []
        for dinuc, freq in freqs.items():
            if freq > self.pair_usage_table[dinuc]:
                nonoptimal += dinuc_positions[dinuc]
        return nonoptimal

    def positions_to_locations(self, positions: List[int]) -> List[Location]:
        groups = group_nearby_indices(positions, max_group_spread=self.localization_group_spread)
        return [
            Location(group[0], group[-1] + 2, strand=1)
            for group in groups
        ]

    def localized(self, location, problem=None):
        return self.copy_with_changes(location=location)
