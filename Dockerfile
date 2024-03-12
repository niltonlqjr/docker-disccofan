FROM ubuntu:20.04

RUN apt-get install libomp-dev libfreeimage3 libfreeimage-dev -y

#instalar zlib (dependencia para o cftisio)
#tar xf zlib-1.3.1.tar.gz
#cd zlib-1.3.1
#./configure
#make test
#make install

#instalar cfitsio
#tar xf cfitsio-4.4.0.tar.gz
#cd cfitsio-4.4.0
#./configure
#make
#make install

#instalar hdf5
#tar xf hdf5-1.14.3.tar.gz
#cd hdf5-1.14.3
#make
#make install

#instalar mpi
#
