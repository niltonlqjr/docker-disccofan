import skimage as sk
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', type = str)
parser.add_argument('--factor', '-f', dest='downsample_factor', default='2,2', type=str)
parser.add_argument('--output-file', '-o', dest='output_file', default='ds.jpg',type=str)
parser.add_argument('--verbose', dest='verbose', action='store_true')
args=parser.parse_args()

filename = args.filename
dsf_str = args.downsample_factor
verbose = args.verbose
out_name = args.output_file

in_prefix, ext = os.path.splitext(filename)

factor = tuple(int(x) for x in dsf_str.split(','))

im = sk.io.imread(filename)

ds = sk.transform.downscale_local_mean(im,factor)
ds = np.round(ds)
ds = ds.astype(np.uint8)

sk.io.imsave(out_name,ds)