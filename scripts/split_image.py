import skimage
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('filename', type = str)
parser.add_argument('--grid', '-g', dest='grid_dim', default='2,2,1', type=str)
parser.add_argument('--output-prefix', '-o', dest='output_prefix', default='',type=str)
args=parser.parse_args()

filename = args.filename
grid_str = args.grid_dim
in_prefix, ext = os.path.splitext(filename)

grid_x, grid_y, grid_z = grid_str

im = skimage.io.imread(filename)

print(im)



'''

código em C que divide os tiles entre os processos
grid: vetor de 3 dimensoes (X,Y,Z)
    X é a quantidade de partes da imagem na horizontal
    Y é a quantidade de partes da imagem na vertical
    Z é a profundidade (neste caso não está sendo levanda em conta)
myrank_arr: vetor de 3 dimensoes (X,Y,Z)
    for (i = 0; i < 2; i++){
      dims[i]  = dims_T[i]/grid[i];
      offsets[i] = myrank_arr[i] * dims[i];
      if (myrank_arr[i] < (int) (dims_T[i]%grid[i])) {
        dims[i]++;
        offsets[i] += myrank_arr[i];
      } else {
    	offsets[i] += (dims_T[i]%grid[i]);
      }
      if((offsets[i] > 0) && overlap){
        offsets[i]--;
        dims[i]++;
      }
      if((dims[i] + offsets[i] != dims_T[i]) && overlap) {
	    dims[i]++;
      }
    }
'''
