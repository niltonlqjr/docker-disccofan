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

ADD ../FreeImage3180.zip /dependencies/FreeImage3180.zip
ADD ../cfitsio-4.4.0.tar.gz /dependencies/cfitsio-4.4.0.tar.gz
ADD ../hdf5-1.14.3.tar.gz /dependencies/hdf5-1.14.3.tar.gz
ADD ../openmpi-3.0.6.tar.gz /dependencies/openmpi-3.0.6.tar.gz
ADD ../zlib-1.3.1.tar.gz /dependencies/zlib-1.3.1.tar.gzs

ENV LANG en_US.utf8

WORKDIR /dependencies

#instalar free image do codigo fonte
RUN unzip FreeImage3180.zip \
    && cd FreeImage \
    && make CXXFLAGS="-std=c++11 -O3 -fPIC -fexceptions -fvisibility=hidden -Wno-ctor-dtor-privacy -D__ANSI__ -I. -ISource -ISource/Metadata -ISource/FreeImageToolkit -ISource/LibJPEG -ISource/LibPNG -ISource/LibTIFF4 -ISource/ZLib -ISource/LibOpenJPEG -ISource/OpenEXR -ISource/OpenEXR/Half -ISource/OpenEXR/Iex -ISource/OpenEXR/IlmImf -ISource/OpenEXR/IlmThread -ISource/OpenEXR/Imath -ISource/OpenEXR/IexMath -ISource/LibRawLite -ISource/LibRawLite/dcraw -ISource/LibRawLite/internal -ISource/LibRawLite/libraw -ISource/LibRawLite/src -ISource/LibWebP -ISource/LibJXR -ISource/LibJXR/common/include -ISource/LibJXR/image/sys -ISource/LibJXR/jxrgluelib" \
    && make install

# #instalar zlib (dependencia para o cftisio)
# RUN tar xf zlib-1.3.1.tar.gz \
#     && cd zlib-1.3.1 \
#     && make install 

# #instalar cfitsio
# RUN tar xf cfitsio-4.4.0.tar.gz \
#     && cd cfitsio-4.4.0 \
#     && ./configure \
#     && make \
#     && make install 

# #instalar hdf5
# RUN tar xf hdf5-1.14.3.tar.gz \
#     && cd hdf5-1.14.3 \
#     &&  ./configure --prefix=/usr/local/hdf5 \
#     && make \
#     && make install

# #instalar mpi
# RUN tar xf openmpi-3.0.6.tar.gz \
#     && cd openmpi-3.0.6 \
#     && ./configure \
#     && make \
#     && make install

# RUN mkdir -p /disccofan

USER nonroot

WORKDIR /home/nonroot


