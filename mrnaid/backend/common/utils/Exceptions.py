class SequenceLengthError(Exception):
    """ This exception is raised when the input sequences have incorrect length"""

    def __init__(self, sequence_type):
        self.sequence_type = sequence_type
        self.message = "{} sequence with size not multiple of 3".format(self.sequence_type)
        super().__init__(self.message)


class OptimizationFailedError(Exception):
    """This exception is raised when the number of attempts is exceeded and no optimized
    sequences have been returned"""

    def __init__(self):
        self.message = 'Not possible to optimize with given parameters. Please try other ones.'
        super().__init__(self.message)


class EmptySequenceError(Exception):
    """This exception is raised when the input RNA or five and three flanking sequences are empty"""

    def __init__(self, sequence_type):
        self.sequence_type = sequence_type
        self.message = '{} sequence is not provided!'.format(sequence_type)
        super().__init__(self.message)


class WrongCharSequenceError(Exception):
    """This exception is raised when the input RNA or five and three flanking sequences contains forbidden characters"""

    def __init__(self, sequence_type):
        self.message = '{} sequence can only have "A", "T", "U", "G", "C" characters!'.format(sequence_type)
        super().__init__(self.message)


class RangeError(Exception):
    """This exception is raised when the min, max GC content or codon usage frequency threshold exceeds allowed range"""

    def __init__(self, message):
        super().__init__(message)


class EntropyWindowError(Exception):
    """This exception is raised when the entropy window is not defined by user"""

    def __init__(self):
        self.message = 'Entropy window is negative or not provided!'
        super().__init__(self.message)


class NoGCError(Exception):
    """This error is raised when the max or min GC is not provided by user"""

    def __init__(self):
        self.message = 'Max or Min GC content is not provided!'
        super().__init__(self.message)


class SpeciesError(Exception):
    """This error is raised when an invalid species is provided by user"""

    def __init__(self, message):
        super().__init__(message)


class NumberOfSequencesError(Exception):
    """This error is raised when user didn't input the number of sequences they
    want to see in the output """

    def __init__(self):
        self.message = 'Number of sequences in the output is not defined or negative!'
        super().__init__(self.message)


class IncompatibleOptimizationError(Exception):
    """This error is raised when incompatible strategies for codon optimization"""

    def __init__(self):
        self.message = 'Incompatible optimization strategies are selected for optimization!'
        super().__init__(self.message)
