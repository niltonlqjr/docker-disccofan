import skimage
import numpy as np
import argparse
import os
import imageio.v3 as iio
import imageio_freeimage

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

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('filename', type = str)
parser.add_argument('--grid', '-g', dest='grid_dim', default='4,4,1', type=str,
                    help='the number of divisions for each dimension')
parser.add_argument('--output-prefix', '-o', dest='output_prefix', default='',type=str,
                    help='prefix of output (each part will be saved as <prefix>-i.<filename format>)')
parser.add_argument('--verbose', dest='verbose', action='store_true',
                    help='show messages during processing')
parser.add_argument('--library', '-l', dest='library', default='skimage',
                    help='library to read image [skimage | imageio]\n imageio uses freeimage')
args=parser.parse_args()

filename = args.filename
grid_str = args.grid_dim
verbose = args.verbose
plugin = args.library

in_prefix, ext = os.path.splitext(filename)


grid_name = grid_str.replace(',','_')
grid_name = '__'+grid_name

if args.output_prefix != '':
    out_prefix = args.output_prefix+grid_name
else:
    out_prefix = in_prefix+grid_name
    

grid_dims = np.array([int(i) for i in grid_str.split(',')],dtype=np.int64)
grid_dims[0], grid_dims[1] = grid_dims[1], grid_dims[0]

ndims = len(grid_dims)
if plugin == 'skimage':
    im = skimage.io.imread(filename)
elif plugin == 'imageio':
    im = iio.imread(filename,plugin='JP2-FI')
else:
    print("invalid plugin")
    exit()
    
if len(im.shape) != ndims:
    print("Invalid dimensions")
    exit()

dims_T = np.zeros(ndims, dtype=np.int64)
#offsets=np.zeros(np.cumprod(grid_dims)[-1],dtype=np.int64)
#offsets=offsets.reshape(np.flip(grid_dims))
#offsets = [None for i in range(ndims)]

offsets = np.zeros(len(grid_dims), dtype=np.int64)


for d in range(ndims):
    dims_T[d] = int(im.shape[d])#//grid_dims[d]
    offsets[d] = 0
if verbose:
    print('offsets:',offsets)
    print('dims_T:',dims_T)
    print(im.shape)
    #print_mat(im, 3)

count=0


dims = np.arange(ndims, dtype=np.int64)

for myrank in range(grid_dims[0]*grid_dims[1]*grid_dims[2]):
    myrank_2D = myrank % (grid_dims[1]*grid_dims[0]);
    myrank_arr = [myrank_2D % grid_dims[0], myrank_2D // grid_dims[0], myrank // (grid_dims[1]*grid_dims[0])]
    for i in range(2):
        dims[i]  = dims_T[i]//grid_dims[i]
        offsets[i] = myrank_arr[i] * dims[i]
        if myrank_arr[i] < dims_T[i]%grid_dims[i]:
            dims[i] += 1
            offsets[i] += myrank_arr[i]
        else:
            offsets[i] += dims_T[i]%grid_dims[i]
        if offsets[i] > 0:
            offsets[i] -= 1
            dims[i] += 1
        if dims[i] + offsets[i] != dims_T[i]:
            dims[i]+=1
    
    yini = offsets[0]
    xini = offsets[1]
    yfim = offsets[0] + dims[0]
    xfim = offsets[1] + dims[1]
    zini = 0
    zfim = im.shape[2]
    if verbose:
        print('y, x, z ranges:',yini,yfim,xini,xfim,zini,zfim)
    im_out = copia_trecho(im,
                          yini,yfim,
                          xini,xfim,
                          zini,zfim)
    
    imname = f'{out_prefix}-{myrank}{ext}'


    im_out=skimage.color.rgb2gray(im_out)
    im_out *= 255
    im_out=im_out.astype(np.uint8)
    
    if plugin == 'skimage':
        skimage.io.imsave(imname,im_out)
    elif plugin == 'imageio':
        iio.imwrite(imname,im_out,plugin='JP2-FI')
    
    if verbose:
        print(imname)
        print_mat(im_out,2)
        print(im_out.shape)
    
'''
image.c
Linhas: 488 - 504
código em C que divide os tiles entre os processos
grid: vetor de 3 dimensoes (X,Y,Z)
    X é a quantidade de partes da imagem na horizontal
    Y é a quantidade de partes da imagem na vertical
    Z é a profundidade (neste caso não está sendo levanda em conta)
myrank_arr: vetor de 3 dimensoes (X,Y,Z)

    dims_T[0] = FreeImage_GetWidth(dib);			    
    dims_T[1] = FreeImage_GetHeight(dib);
    if(grid[2] > 1){
      error("Ask distributionin depth but data is 2D");
      MPI_Abort(MPI_COMM_WORLD, 701);
    }
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
