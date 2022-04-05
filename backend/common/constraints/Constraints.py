from typing import List, Union, Tuple

from dnachisel import Specification, AvoidPattern, EnzymeSitePattern, EnforceGCContent, EnforceTranslation, \
    AvoidRareCodons
from constraints.UridineDepletion import UridineDepletion


class Constraints(object):

    def __init__(self, avoid_motifs: List[str], uridine_depletion: bool,
                 min_GC_content: int, max_GC_content: int, organism: str, usage_threshold: float,
                 location: Union[None, Tuple]) -> None:
        self.avoid_motifs = avoid_motifs
        self.uridine_depletion = uridine_depletion
        self.min_GC_content = min_GC_content
        self.max_GC_content = max_GC_content
        self.organism = organism
        self.usage_threshold = usage_threshold
        self.location = location

    def create_constraints(self) -> List[Specification]:
        """
        Create a list of constraints based on parameters.
        EnforceTranslation is added always, the others only if the corresponding parameter is set.
        """
        constraints_list = []
        for motif in self.avoid_motifs:
            try:
                constraints_list.append(AvoidPattern(EnzymeSitePattern(motif), location=self.location))
            except KeyError:
                motif = motif.replace('U', 'T')
                constraints_list.append(AvoidPattern(motif, location=self.location))
        constraints_list.append(EnforceGCContent(mini=self.min_GC_content, maxi=self.max_GC_content, location=self.location))
        if self.uridine_depletion:
            constraints_list.append(UridineDepletion(location=self.location))
        constraints_list.append(EnforceTranslation(genetic_table='Standard',
                                                   location=self.location))  # need different table for different species
        if self.usage_threshold:
            constraints_list.append(
                AvoidRareCodons(min_frequency=self.usage_threshold, species=self.organism, location=self.location))

        return constraints_list
