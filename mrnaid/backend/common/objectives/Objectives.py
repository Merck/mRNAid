from typing import List, Union, Tuple

from dnachisel import *
from objectives.Codon_pair_usage import MatchTargetCodonPairUsage
from objectives.Dinucleotide_usage import MatchTargetPairUsage
from objectives.MFE_optimization import MinimizeMFE
from utils.Logger import MyLogger
from utils.Exceptions import UnsupportedOptimizationError

# Setting up a logger
logger = MyLogger(__name__)


class Objectives(object):

    def __init__(self, entropy_window: int, organism: str, location: Union[None, Tuple], min_GC_content: int,
                 max_GC_content: int, GC_window_size: int, five_end: str, mfe_method: str, optimization_criterion: str) -> None:
        self.entropy_window = entropy_window
        self.organism = organism
        self.location = location
        self.min_GC_content = min_GC_content
        self.max_GC_content = max_GC_content
        self.GC_window_size = GC_window_size
        self.five_end = five_end
        self.mfe_method = mfe_method
        self.optimization_criterion = optimization_criterion

    def create_objectives(self) -> List[Specification]:
        """
        Create a list of objectives based on parameters.
        MinimizeMFE is added always, the others only if the corresponding parameter is set.
        MatchTargetCodonUsage is added when neither dinucleotides nor codon_pair is set. The three are mutually exclusive.
        """
        objectives = []
        objectives.append(MinimizeMFE(self.five_end, self.entropy_window, mfe_method=self.mfe_method))

        if self.GC_window_size:
            objectives.append(
                EnforceGCContent(mini=self.min_GC_content, maxi=self.max_GC_content, window=self.GC_window_size,
                                 location=self.location))


        if self.optimization_criterion == 'codon_usage':
            objectives.append(MatchTargetCodonUsage(species=self.organism, location=self.location))
        elif self.optimization_criterion == 'cai':
            objectives.append(MaximizeCAI(species=self.organism))
        elif self.optimization_criterion == 'dinucleotides':
            objectives.append(MatchTargetPairUsage(species=self.organism))
        elif self.optimization_criterion == 'codon_pair':
            objectives.append(MatchTargetCodonPairUsage(species=self.organism))
        else:
            logger.error(f'Unknown optimization criterion: {self.optimization_criterion}')
            raise UnsupportedOptimizationError(f'Unknown optimization criterion: {self.optimization_criterion}')

        return objectives
