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

# arg to use network of host machine
# to use this configuration, the machine must have a mpi user that is can
# connect to other cluster machines through ssh with public private key.
NETWORK_ARG="--network host"


#run container
${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_ARG}\
  --env "SHELL=/bin/bash" \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir /home/mpi \
  --volume ${HOME}:/home/mpi/host \
  ${CONTAINER_IMAGE}
