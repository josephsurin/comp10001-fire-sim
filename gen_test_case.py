#!/usr/bin/python

import argparse

ex = '''
example:
    python gen_test_case 5 out.txt
'''

parser = argparse.ArgumentParser(description='Fire model test case generator', epilog=ex, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('count', default=4, type=int, help='Number of test cases to generate')
parser.add_argument('outfile', default='out.txt', type=str, help='Filename of output file')

args = parser.parse_args()

from fire_sim import random_model
from libg import run_model

outtext = ''

for i in range(args.count):
    print('Generating random test case', i)
    f_grid, h_grid, i_threshold, w_direction, burn_seeds = random_model()
    final_state, burn_count = run_model([r[:] for r in f_grid], h_grid, i_threshold, w_direction, burn_seeds[::])
    outstring = 'test_run_model([{},{},{},{},{}], [{},{}])'.format(f_grid, h_grid, i_threshold, '"{}"'.format(w_direction) if w_direction else None, burn_seeds, final_state, burn_count)
    outtext += outstring + '\n'

with open(args.outfile, 'w') as f:
    print('Writing', args.count, 'test cases to', args.outfile)
    f.write(outtext)
