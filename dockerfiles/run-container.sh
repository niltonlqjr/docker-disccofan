#############################################################################
#                                                                           #
# Run a docker container with environmnet variables needed to disccofan.    #
# Also maps /home/mpi/host from container to user home                           #
#                                                                           #
#############################################################################

#import some common variables to build container
source ./vars.sh

# args used to run container
CONTAINER_RUN_ARGS="-it --rm"

# port used to ssh and mpi. These ports are setted in Dockerfile (in this 
# directory) during container building
NETWORK_PORT="-p 2222:22 -p 52000-52032:52000-52032 -p 53000-53032:53000-53032"
#NETWORK_PORT="--network host"


#run container
${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_PORT}\
  --env "SHELL=/bin/bash" \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir /home/mpi \
  --volume ${HOME}:/home/mpi/host \
  ${CONTAINER_IMAGE}
