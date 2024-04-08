source ./vars.sh

${CONTAINER_CMD} ${RUN_CMD} -it --rm \
  --env "HOME=$VOLUME_DIR" \
  --env "SHELL=/bin/bash" \
  --workdir ${VOLUME_DIR} \
  --volume ${VOLUME_DIR}:${VOLUME_DIR} \
  ${CONTAINER_IMAGE}