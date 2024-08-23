import argparse
import glob
import utils

import matplotlib.pyplot as plt
import numpy as np
    
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('directory',
                    help='directory containing files')
parser.add_argument('--regular-expr', '-r', type=str, dest='regular_expr', default='mem_out_*.txt',
                    help='regular expression to filenames')
parser.add_argument('--output-figure', '-o', dest='out_name', default='cpu_usage_per_cpu.png',
                    help='figure name output')
parser.add_argument('--no-header', action='store_false', dest='header',
                    help='if file does not have the header in first line')
parser.add_argument('--column', '-c', dest='column', default=0, type=int,
                    help='column that will be plotted')

args=parser.parse_args()

directory = args.directory
regular_expr = args.regular_expr
header = args.header
fig_name = args.out_name
column = args.column

files = glob.glob(f'{directory}/{regular_expr}')


cpu_usage={}

col_type = [float for i in range(11)]

for fn in files:
    with open(fn) as f:
        file_str = f.read()
    all_data = utils.text_table_to_data(file_str, colum_types=col_type, header=header)
    cpu_usage[fn] = [d[column] for d in all_data]

for fn in cpu_usage:
    print(fn, cpu_usage[fn], len(cpu_usage[fn]))
    print('=======================================')
    plt.plot(cpu_usage[fn])
    

print(fig_name)
plt.savefig(f'{fig_name}', dpi=200)