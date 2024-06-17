import skimage
import numpy as np
import argparse
import os

def copia_trecho(image, yini,yfim,xini,xfim,zini,zfim):
    deltay = yfim-yini
    deltax = xfim-xini
    deltaz = zfim-zini
    if verbose:
        print('delta:',deltay,deltax,deltaz)
        print(yini,yfim,xini,xfim,zini,zfim)
    ret=np.zeros(deltay*deltax*deltaz)
    ret = ret.reshape(deltay,deltax,deltaz)
    ret[:,:,:] = image[yini:yfim,xini:xfim,zini:zfim]
    return ret.astype(np.uint8)

def print_mat(im,dim):
    for i in range(len(im)):
        for j in range(len(im[i])):
            if dim == 3:
                print('({:3d}, {:3d}, {:3d})'.format(im[i,j,0],im[i,j,1],im[i,j,2]),end='')
            elif dim == 2:
                print('{:4d}'.format(im[i,j]),end='')
        print('')

parser = argparse.ArgumentParser()
parser.add_argument('filename', type = str)
parser.add_argument('--grid', '-g', dest='grid_dim', default='3,2,1', type=str)
parser.add_argument('--output-prefix', '-o', dest='output_prefix', default='teste',type=str)
parser.add_argument('--verbose', dest='verbose', action='store_true')
args=parser.parse_args()

filename = args.filename
grid_str = args.grid_dim
verbose = args.verbose
in_prefix, ext = os.path.splitext(filename)
out_prefix = args.output_prefix
grid_dims = np.array([int(i) for i in grid_str.split(',')],dtype=np.int64)
grid_dims[0], grid_dims[1] = grid_dims[1], grid_dims[0]

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
if verbose:
    print(dims)
    print(im.shape)

    print_mat(im, 3)

#cart_prod=cartesian_prod(offsets)

yinc=dims[0]
xinc=dims[1]
zinc=dims[2]

count=0

y=0
while y < im.shape[0]:
    yini = y-1 if y >= 1 else y 
    yfim = y+yinc+1 if y+yinc+1 < im.shape[0] else im.shape[0]
    '''
    if y == 0:
        if yfim < im.shape[0]:
            yfim+=1
    if yfim == im.shape[0]:
        if yini > 0:
            yini -=1
    '''
    x=0
    while x < im.shape[1]:
        xini = x-1 if x >= 1 else x 
        xfim = x+xinc+1 if x+xinc+1 < im.shape[1] else im.shape[1]
        '''
        if x == 0:
            if xfim < im.shape[1]:
                xfim+=1
        if xfim == im.shape[1]:
            if xini > 0:
                xini -=1
        '''
        z=0
        while z < im.shape[2]:
            zini = z-1 if z >= 1 else z 
            zfim = z+zinc+1 if z+zinc+1 < im.shape[2] else im.shape[2]
            '''
            if z == 0:
                if zfim < im.shape[2]:
                    zfim+=1
            if zfim == im.shape[2]:
                if zini > 0:
                    zini -=1
            '''
            im_out = copia_trecho(im,
                                  yini,yfim,
                                  xini,xfim,
                                  zini,zfim)
            im_out=skimage.color.rgb2gray(im_out)
            im_out *= 255
            im_out=im_out.astype(np.uint8)
            imname = f'{out_prefix}-{count}{ext}'
            if verbose:
                print(imname)
                print_mat(im_out,2)
                print(im_out.shape)
            skimage.io.imsave(imname,im_out)
            count+=1
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
