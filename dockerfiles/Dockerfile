FROM ubuntu:20.04 

ARG UID
ARG GID

RUN apt-get update \
    && apt-get install -y wget sudo locales unzip sudo build-essential \
    libomp-dev 

RUN addgroup --gid $GID nonroot  
RUN adduser --uid $UID --gid $GID --disabled-password --gecos "" nonroot 
RUN echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

RUN mkdir -p /dependencies

ADD deps/FreeImage3180.zip /dependencies/FreeImage3180.zip
#tar files are added as a filder
ADD deps/cfitsio-4.4.0.tar.gz /dependencies/
ADD deps/hdf5-1.14.3.tar.gz /dependencies/
ADD deps/openmpi-3.0.6.tar.gz /dependencies/
ADD deps/zlib-1.3.1.tar.gz /dependencies/

ENV LANG en_US.utf8

WORKDIR /dependencies

#instalar free image do codigo fonte
RUN unzip FreeImage3180.zip \
    && cd FreeImage \
    && make CXXFLAGS="-std=c++11 -O3 -fPIC -fexceptions -fvisibility=hidden -Wno-ctor-dtor-privacy -D__ANSI__ -I. -ISource -ISource/Metadata -ISource/FreeImageToolkit -ISource/LibJPEG -ISource/LibPNG -ISource/LibTIFF4 -ISource/ZLib -ISource/LibOpenJPEG -ISource/OpenEXR -ISource/OpenEXR/Half -ISource/OpenEXR/Iex -ISource/OpenEXR/IlmImf -ISource/OpenEXR/IlmThread -ISource/OpenEXR/Imath -ISource/OpenEXR/IexMath -ISource/LibRawLite -ISource/LibRawLite/dcraw -ISource/LibRawLite/internal -ISource/LibRawLite/libraw -ISource/LibRawLite/src -ISource/LibWebP -ISource/LibJXR -ISource/LibJXR/common/include -ISource/LibJXR/image/sys -ISource/LibJXR/jxrgluelib" \
    && make install

#instalar zlib (dependencia para o cftisio)
RUN cd zlib-1.3.1 \
    && ./configure \
    && make install 

#instalar cfitsio
RUN cd cfitsio-4.4.0 \
    && ./configure \
    && make \
    && make install 

#instalar hdf5
RUN cd hdf5-1.14.3 \
    &&  ./configure --prefix=/usr/local/hdf5 \
    && make \
    && make install

#instalar mpi
RUN cd openmpi-3.0.6 \
    && ./configure \
    && make \
    && make install

RUN mkdir -p /disccofan

USER nonroot

WORKDIR /home/nonroot


