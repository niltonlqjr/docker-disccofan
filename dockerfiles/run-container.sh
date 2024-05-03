source ./vars.sh


#args used to run container
CONTAINER_RUN_ARGS="-it --rm"
NETWORK_PORT="-p 22:22 -p 52000-52032:52000-52032 -p 53000-53032:53000-53032"
#NETWORK_PORT="--network host"

${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_PORT}\
  --env "SHELL=/bin/bash" \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir ${HOME} \
  --volume ${HOME}:${HOME} \
  ${CONTAINER_IMAGE}
