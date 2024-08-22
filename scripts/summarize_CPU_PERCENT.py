import argparse
import glob

def lines_to_vec(file_str, header=True):
    lines = file_str.split('\n')
    if header:
        del lines[0]
    ret =[float(l) for l in lines if l.strip() != '']    

    return ret
        
parser = argparse.ArgumentParser()

parser.add_argument('files_prefix', help='CPU percent file for a single process')
parser.add_argument('--no-header', action='store_false', dest='header', help='if file does not have the header in first line')
parser.add_argument('--function', dest='function', default='mean', help='function to computate data')
args=parser.parse_args()

files_prefix=args.files_prefix
header = args.header


files = glob.glob(f'{files_prefix}*.txt')



lists={}

for fn in files:
    with open(fn) as f:
        file_str = f.read()
    lists[fn] = lines_to_vec(file_str,header=True)
    

for fn in lists:
    print(fn, lists[fn])
    print('=======================================')