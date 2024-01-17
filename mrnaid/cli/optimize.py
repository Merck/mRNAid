import json

import click
import os
import sys

from mrnaid import __version__

# Add mrnaid.backend.common directory to python path to enable local imports
mrnaid_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
common_path = os.path.join(mrnaid_path, 'backend', 'common')
sys.path.append(common_path)

def optimize(
    input_mrna: str,
    five_end: str,
    three_end: str,
    number_of_sequences=3,
    avoid_motifs=None,
    max_gc_content=0.7,
    min_gc_content=0.3,
    gc_window_size=100,
    usage_threshold=0.1,
    organism='h_sapiens',
    entropy_window=30,
    mfe_method='stem-loop',
    dinucleotides=False,
    codon_pair=False,
    disable_cai=False,
    disable_uridine_depletion=False,
):
    """
    Optimize a given mRNA sequence.

    This function adjusts the input mRNA sequence based on various parameters like GC content,
    codon usage, and avoidance of certain motifs to enhance its stability and translational efficiency.

    Parameters:
    - input_mrna (str): The original mRNA sequence to be optimized.
    - five_end (str): Sequence to be added at the 5' end of the mRNA.
    - three_end (str): Sequence to be added at the 3' end of the mRNA.
    - number_of_sequences (int, optional): The number of optimized sequences to generate. Default is 3.
    - avoid_motifs (list of str, optional): Motifs to be avoided in the optimized mRNA sequence.
    - max_gc_content (float, optional): Maximum allowable GC content in the sequence. Default is 0.7.
    - min_gc_content (float, optional): Minimum allowable GC content in the sequence. Default is 0.3.
    - gc_window_size (int, optional): Size of the window used to calculate GC content. Default is 100 nucleotides.
    - usage_threshold (float, optional): Threshold for codon usage frequency. Default is 0.1 (10%).
    - organism (str, optional): Target organism for codon usage optimization. Default is 'h_sapiens' (human).
    - entropy_window (int, optional): Size of the window used to calculate sequence entropy. Default is 30.
    - mfe_method (str, optional): Method used for minimum free energy calculation. Default is 'stem-loop', more precise slower option is 'RNAfold'.
    - dinucleotides (bool, optional): Whether to consider dinucleotide optimization. Default is False.
    - codon_pair (bool, optional): Whether to optimize based on codon pair usage. Default is False.
    - disable_cai (bool, optional): If True, disables codon adaptation index optimization. Default is False.
    - disable_uridine_depletion (bool, optional): If True, disables uridine depletion optimization. Default is False.

    Returns:
    JSON-like data structure with current configuration and output list of optimized mRNA sequences and their properties.

    Notes:
    - The function assumes input sequences are in standard RNA nucleotide format (A, U, G, C).
    - The optimization is tailored for the specified organism's codon usage and RNA processing mechanisms.
    """
    from mrnaid.backend.flask_app.tasks import optimization_evaluation_task
    result_str = optimization_evaluation_task(parameters=dict(
        input_mRNA=input_mrna,
        input_DNA=input_mrna.replace('U', 'T'),
        five_end=five_end,
        three_end=three_end,
        avoid_motifs=avoid_motifs or [],
        max_GC_content=max_gc_content,
        min_GC_content=min_gc_content,
        GC_window_size=gc_window_size,
        usage_threshold=usage_threshold,
        uridine_depletion=not disable_uridine_depletion,
        organism=organism,
        entropy_window=entropy_window,
        number_of_sequences=number_of_sequences,
        mfe_method=mfe_method,
        dinucleotides=dinucleotides,
        codon_pair=codon_pair,
        CAI=not disable_cai,
        filename='unused',
        location=(0, len(input_mrna) - len(input_mrna) % 3, 1),
    ))
    return json.loads(result_str)


@click.command(name='optimize')
# Required arguments
@click.option('--output', required=True)
@click.option('--input-mRNA', required=True, help='Input mRNA sequence')
@click.option('--five-end', required=True, help='')
@click.option('--three-end', required=True, help='')
# Optional arguments
@click.option('--number-of-sequences', default=3, type=int, help='')
@click.option('--avoid-motifs', default='', help='')
@click.option('--max-GC-content', default=0.7, type=float, help='')
@click.option('--min-GC-content', default=0.3, type=float, help='')
@click.option('--GC-window-size', default=100, type=int, help='')
@click.option('--usage-threshold', default=0.1, type=float, help='')
@click.option('--organism', default='h_sapiens', help='')
@click.option('--entropy-window', default=30, type=int, help='')
@click.option('--mfe-method', default='stem-loop', help='stem-loop or RNAfold')
@click.option('--dinucleotides', default=False, is_flag=True, help='')
@click.option('--codon-pair', default=False, is_flag=True, help='')
@click.option('--disable-uridine-depletion', default=True, is_flag=True, help='')
@click.option('--disable-CAI', is_flag=True, default=True, help='Do not use Codon Adaptation Index')
def optimize_cli(output, **parameters):
    print(f"""
            _____  _   _          _     _ 
           |  __ \| \ | |   /\   (_)   | |
  _ __ ___ | |__) |  \| |  /  \   _  __| |
 | '_ ' _ \|  _  /|     | / /\ \ | |/ _  |
 | | | | | | | \ \| |\  |/ ____ \| | (_| |
 |_| |_| |_|_|  \_\_| \_/_/    \_\_|\__,_|
                             version {__version__}
===========================================
""")
    with open(output, 'wt') as f:
        # parse list of motifs from string
        parameters['avoid_motifs'] = [m.strip() for m in parameters.get('avoid_motifs', '').split(',') if m.strip()]
        # generate results
        result = optimize(**parameters)
        # save results
        json.dump(result, f, indent=2)
        f.write('\n')

    num_sequences = parameters['number_of_sequences']
    print('')
    print(f'Saved {num_sequences} optimized sequences in JSON format to: {output}')
    print('')

