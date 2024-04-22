source ./vars.sh

#args used to run container
CONTAINER_RUN_ARGS="-it --rm"

${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} \
  --env "SHELL=/bin/bash" \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir ${VOLUME_DIR} \
  --volume ${VOLUME_DIR}:${VOLUME_DIR} \
  ${CONTAINER_IMAGE}
