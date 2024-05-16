#############################################################################
#                                                                           #
# Run a docker container with environmnet variables needed to disccofan.    #
# Also maps /home/mpi/host from container to user home                           #
#                                                                           #
#############################################################################

#import some common variables to build container
source ./vars.sh

ip=$1

# args used to run container


RUNNING=`docker ps -a |grep ${CONTAINER_NAME} | awk -F\  '{print $NF}'`

if [ -z $RUNNING ]
then
    RUN_CMD="run"
    CONTAINER_RUN_ARGS="-it --name ${CONTAINER_NAME} "
    VOLUME_ARG="--volume ${HOME}:/home/mpi/host"
    COMMAND_TO_EXEC=""
    CONTAINER=$CONTAINER_IMAGE

    # arg to use network of host machine
    # to use this configuration, the machine must have a mpi user that is can
    # connect to other cluster machines through ssh with public private key.
    NETWORK_ARG="--network bridge"
else
    RUN_CMD="exec"
    CONTAINER_RUN_ARGS="-it"
    VOLUME_ARG=""
    COMMAND_TO_EXEC="/bin/bash"
    CONTAINER=$CONTAINER_NAME

    NETWORK_ARG=""
fi

#run container
echo "START"
${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_ARG}\
  --env "SHELL=/bin/bash" \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir /home/mpi \
  ${VOLUME_ARG} \
  ${CONTAINER} \
  ${COMMAND_TO_EXEC}

#import some common variables to build container
source ./vars.sh

# args used to run container
CONTAINER_RUN_ARGS="-it --rm --name ${CONTAINER_NAME}"

RUNNING=`docker ps -a |grep ${CONTAINER_NAME} | awk -F\  '{print $NF}'`

if [ -z $RUNNING ]
then
    RUN_CMD="run"
else
    RUN_CMD="exec"
fi

# port used to ssh and mpi. These ports are setted in Dockerfile (in this 
# directory) during container building
NETWORK_ARG="-p 2222:22 -p 52000-52300:52000-52300"




#run container
${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_ARG}\
  --env "SHELL=/bin/bash" \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir /home/mpi \
  --volume ${HOME}:/home/mpi/host \
  ${CONTAINER_IMAGE}
