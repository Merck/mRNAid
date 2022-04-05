import json

from utils.Datatypes import OptimizationParameters
from utils.Exceptions import SequenceLengthError, EmptySequenceError, \
    EntropyWindowError, NoGCError, NumberOfSequencesError, WrongCharSequenceError, RangeError, SpeciesError
from utils.Logger import MyLogger

# Setting up a logger
logger = MyLogger(__name__)


class RequestParser(object):
    """This class parses the input request and returns a set of
    parameters necessary to perform the optimization task """

    def __init__(self, request):
        self.data = json.loads(request.get_data())
        logger.info(self.data)

    def parse(self) -> OptimizationParameters:

        def seq_char_check(seq, seq_name):
            """Function to check if allowed characters are used"""
            if not set(seq) <= set("TAGC"):
                raise WrongCharSequenceError(seq_name)

        # --- Get the input sequences ---
        input_mRNA = self.data['sequences']['gene_of_interest'].upper().replace('T', 'U')
        input_DNA = input_mRNA.replace('U', 'T')
        if not input_mRNA:
            raise EmptySequenceError('RNA')
        if len(input_DNA) % 3:
            raise SequenceLengthError('Input RNA')
        seq_char_check(input_DNA, seq_name="RNA")
        five_end = self.data['sequences']['five_end_flanking_sequence'].upper().replace('U', 'T')
        if not five_end:
            raise EmptySequenceError('Five prime flanking')
        seq_char_check(five_end, seq_name="Five prime flanking")
        three_end = self.data['sequences']['three_end_flanking_sequence'].upper().replace('U', 'T')
        if not three_end:
            raise EmptySequenceError('Three prime flanking')
        seq_char_check(three_end, seq_name="Three prime flanking")

        # --- Get the list of avoided codons ---
        avoid_motifs = self.data['config']['avoided_motifs']

        # --- Get GC related parameters ---
        max_GC_content = self.data['config']['max_GC_content']
        min_GC_content = self.data['config']['min_GC_content']
        GC_window_size = self.data['config']['GC_window_size']
        if max_GC_content is None:
            logger.error('No max GC content defined')
            raise NoGCError()
        elif min_GC_content is None:
            logger.error('No min GC content defined')
            raise NoGCError()
        elif not GC_window_size:
            logger.warning('No GC window size defined or set to 0. Window GC optimization will not be performed.')
        elif max_GC_content > 1 or max_GC_content < 0:
            raise RangeError('Max GC content can be only in a range of 0 to 1!')
        elif min_GC_content > 1 or min_GC_content < 0:
            raise RangeError('Min GC content content can be only in a range of 0 to 1!')
        elif min_GC_content > max_GC_content:
            raise RangeError("Min GC content connot be higher than max GC content")
        else:
            pass

        # --- Get the threshold for usage frequency of codons ---
        usage_threshold = self.data['config']['codon_usage_frequency_threshold']
        if usage_threshold is None:
            logger.warning('Usage threshold is not defined')
        elif usage_threshold > 1 or usage_threshold < 0:
            raise RangeError('Codon usage frequency threshold can be only in a range of 0 to 1!')
        else:
            pass

        # --- Get the uridine depletion boolean value ---
        uridine_depletion = self.data['uridine_depletion']

        # --- Get the organism ---
        organism = self.data['config']['organism']
        if organism.lower() in ["h_sapiens", "sapiens", "human", "homo_sapiens", "h sapiens", "homo sapiens"]:
            organism = "h_sapiens"
        elif organism.lower() in ["m_musculus", "mouse", "mus_musc", "mus_musculus", "mus", "mus musculus", "m musculus", "mus musc"]:
            organism = "m_musculus"
        else:
            raise SpeciesError("Invalid organism {} is provided!".format(organism))

        # --- Get the entropy window value ---
        entropy_window = self.data['config']['entropy_window']
        if not entropy_window:
            logger.warning('Entropy window is not defined or is zero')
            raise EntropyWindowError()
        elif entropy_window < 0:
            logger.warning('Entropy window is negative, meaning is ambiguous.')
            raise EntropyWindowError()

        # --- Get the number of sequences required by user ---
        number_of_sequences = self.data['config']['number_of_sequences']
        if not number_of_sequences or number_of_sequences < 0:
            logger.error('Number of sequences for the output is not defined or negative!')
            raise NumberOfSequencesError()

        # --- Get the filename to produce the report ---
        filename = self.data['file_name']
        if not filename:
            filename = 'optimization_results'

        # --- Get the algorithm for MFE estimation ---
        precise_MFE_algorithm = self.data['precise_MFE_algorithm']
        if precise_MFE_algorithm is None:
            logger.warning('Algorithm for MFE is not specified! Switching to the default one...')
            precise_MFE_algorithm = False

        if precise_MFE_algorithm:
            mfe_method = 'RNAfold'
        else:
            mfe_method = 'stem-loop'

        # --- Get the dinucleotides usage boolean value ---
        dinucleotides = self.data['dinucleotides']
        if dinucleotides is None:
            logger.warning('Dinucleotides optimization option is not specified! Setting it to False')
            dinucleotides = False

        # --- Get the codon pair usage boolean value ---
        codon_pair = self.data['match_codon_pair']
        if codon_pair is None:
            logger.warning('Codon pair usage option is not specified! Setting it to False')
            codon_pair = False

        # --- Get the CAI optimization boolean value
        CAI = self.data['CAI']
        if CAI is None:
            logger.warning('CAI optimization is not specified! Setting it to False')
            CAI = False

        # --- Combining all the parameters together ---
        return OptimizationParameters(input_mRNA=input_mRNA,
                                      input_DNA=input_DNA,
                                      five_end=five_end,
                                      three_end=three_end,
                                      avoid_motifs=avoid_motifs,
                                      max_GC_content=max_GC_content,
                                      min_GC_content=min_GC_content,
                                      GC_window_size=GC_window_size,
                                      usage_threshold=usage_threshold,
                                      uridine_depletion=uridine_depletion,
                                      organism=organism,
                                      entropy_window=entropy_window,
                                      number_of_sequences=number_of_sequences,
                                      filename=filename,
                                      mfe_method=mfe_method,
                                      dinucleotides=dinucleotides,
                                      codon_pair=codon_pair,
                                      CAI=CAI,
                                      location=(0, len(input_mRNA) - len(input_mRNA) % 3, 1))
