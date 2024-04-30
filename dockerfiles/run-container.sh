source ./vars.sh

IP=$1

echo $IP

#args used to run container
CONTAINER_RUN_ARGS="-it --rm"
NETWORK_PORT="-p ${IP}:2222:22 -p ${IP}10000-10031:10000-10031"
#NETWORK_PORT="--network host"

${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_PORT}\
  --env "SHELL=/bin/bash" \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir ${VOLUME_DIR} \
  --volume ${VOLUME_DIR}:${VOLUME_DIR} \
  ${CONTAINER_IMAGE}
