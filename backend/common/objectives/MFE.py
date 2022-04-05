from utils.Logger import MyLogger

logger = MyLogger(__name__)


class MFE():
    """This class implements the MFE prediction using a correlated stem–loop prediction.
    The method is described in Nucleic Acids Research, 2013, Vol. 41, No. 6 e73: 'mRNA secondary 
    structure optimization using a correlated stem–loop prediction'  """
    def __init__(self):
        pass

    def get_energy(self, seq1: str, seq2: str) -> float:
        """Calculation of contribution of each binding pair"""

        bond_energy = 0
        for i in range(len(seq1)):
            try:
                if [seq1[i], seq2[i]] in [['G', 'C'], ['C', 'G']]:
                    e = 3.12
                elif [seq1[i], seq2[i]] in [['A', 'T'], ['T', 'A']]:
                    e = 1
                elif [seq1[i], seq2[i]] in [['G', 'T'], ['T', 'G']]:
                    e = 1
                else:
                    e = 0
            except Exception as exception:
                #TODO: Explore why this exception happens 
                if str(exception) == "string index out of range":
                    e = 0
                    logger.error(f'{str(exception)}')
                    logger.debug(f'i: {i}, len(seq1): {len(seq1)}, len(seq2): {len(seq2)}')
                else:
                    #TODO: implement proper error handling
                    raise ValueError(str(exception))
            bond_energy = bond_energy + e

        return bond_energy

    def estimate(self, sequence: str) -> float:
        """Main method to get the estimation of the MFE"""

        sequence_size = len(sequence)
        iblock_size = 2 # <-- initial block size
        fblock_size = sequence_size/2 # <-- final block size
        loop_size = 3 # <-- minimum loop size
        c_energy = 0 # <-- cumulative energy

        for i in range(2):
            b = iblock_size
            while (b < fblock_size) and (sequence_size > loop_size + 2*b + 1): #  <-- Beware of never ending loop with celery!
                b += 1
                sub_seq1 = sequence[0:b]
                sub_seq2 = sequence[loop_size + b:loop_size + 2*b]
                energy = self.get_energy(sub_seq1, sub_seq2)
                c_energy = c_energy + energy
            sequence = sequence[::-1]

        return -c_energy/sequence_size
