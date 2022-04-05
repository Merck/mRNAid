from pydantic import BaseModel
from typing import List, Tuple


class OptimizationParameters(BaseModel):
    """Class for keeping all the input parameters for the optimization problem"""
    input_mRNA: str
    input_DNA: str
    five_end: str
    three_end: str
    avoid_motifs: List[str]
    max_GC_content: float
    min_GC_content: float
    GC_window_size: int
    usage_threshold: float
    uridine_depletion: bool
    organism: str
    entropy_window: int
    number_of_sequences: int
    filename: str
    mfe_method: str
    dinucleotides: bool
    codon_pair: bool
    CAI: bool
    location: Tuple[int, int, int]


class SequenceProperties(BaseModel):
    """Class for keeping track of sequence properties after evaluation"""
    seqID: str
    RNASeq: str
    DNASeq: str
    RNA_structure: str
    A_ratio: float
    TU_ratio: float
    G_ratio: float
    C_ratio: float
    AT_ratio: float
    GC_ratio: float
    MFE: float
    MFE_5: float
    score: float
    CAI: float


class EvaluationResults(BaseModel):
    """Class collecting the evaluation results together"""
    input: SequenceProperties
    optimized: List[SequenceProperties]
