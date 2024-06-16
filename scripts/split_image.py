import skimage
import numpy as np
import argparse
import os

def copia_trecho(image, yini,yfim,xini,xfim,zini,zfim):
    deltay = yfim-yini
    deltax = xfim-xini
    deltaz = zfim-zini
    ret=np.zeros(deltay*deltax*deltaz)
    ret = ret.reshape(deltay,deltax,deltaz)
    for i in range(yini,yfim):
        for j in range(xini,xfim):
            for k in range(zini,zfim):
                ret[i-yini,j-xini,k-zini] = image[i,j,k]
    return ret.astype(np.uint8)

parser = argparse.ArgumentParser()
parser.add_argument('filename', type = str)
parser.add_argument('--grid', '-g', dest='grid_dim', default='3,2,1', type=str)
parser.add_argument('--output-prefix', '-o', dest='output_prefix', default='teste',type=str)
args=parser.parse_args()

filename = args.filename
grid_str = args.grid_dim
in_prefix, ext = os.path.splitext(filename)
out_prefix = args.output_prefix
grid_dims = np.array([int(i) for i in grid_str.split(',')],dtype=np.int64)

ndims = len(grid_dims)
im = skimage.io.imread(filename)

if len(im.shape) != ndims:
    print("Invalid dimensions")
    exit()

dims = np.zeros(ndims, dtype=np.int64)
#offsets=np.zeros(np.cumprod(grid_dims)[-1],dtype=np.int64)
#offsets=offsets.reshape(np.flip(grid_dims))
offsets = [None for i in range(ndims)]


for d in range(ndims):
    dims[d] = int(im.shape[d])//grid_dims[d]
    offsets[d] = np.arange(grid_dims[d])*dims[d]

print(dims)
print(im.shape)


cart_prod=cartesian_prod(offsets)

yinc=dims[0]
xinc=dims[1]
zinc=dims[2]

y=0
while y < im.shape[0]:
    yini = y-1 if y > 1 else y 
    yfim = y+yinc if y+yinc < im.shape[0] else im.shape[0]
    x=0
    while x < im.shape[1]:
        xini = x-1 if x > 1 else x 
        xfim = x+xinc if x+xinc < im.shape[1] else im.shape[1]
        z=0
        while z < im.shape[2]:
            zini = z-1 if z > 1 else z 
            zfim = z+zinc if z+zinc < im.shape[2] else im.shape[2]
            
            im_out = copia_trecho(im,
                                  yini,yfim,
                                  xini,xfim,
                                  zini,zfim)
            imname = f'{out_prefix}-{y}-{x}-{z}{ext}'
            skimage.io.imsave(imname,im_out)
            print(im_out.shape)
            z+=zinc
        x+=xinc
    y+=yinc



#while z < len(im.shape[2])
#    z+=

'''
image.c
Linhas: 488 - 504
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
