source ./vars.sh

#args used to run container
CONTAINER_RUN_ARGS="-it --rm"
NETWORK_PORT="-p 2222:22 -p 10000-10031:10000-10031"
#NETWORK_PORT="--network mpi_network"

${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_PORT}\
  --env "SHELL=/bin/bash" \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir ${VOLUME_DIR} \
  --volume ${VOLUME_DIR}:${VOLUME_DIR} \
  ${CONTAINER_IMAGE}
