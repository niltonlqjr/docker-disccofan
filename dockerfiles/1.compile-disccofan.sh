source ./vars.sh

#shell commands to build disccofan  
BUILD_DISCCOFAN_CMD="git clone https://github.com/niltonlqjr/disccofan.git && cd disccofan && make"

${CONTAINER_CMD} ${RUN_CMD} --rm \
  --env "HOME=$VOLUME_DIR" \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir ${VOLUME_DIR} \
  --volume ${VOLUME_DIR}:${VOLUME_DIR} \
  ${CONTAINER_IMAGE} sh -c "${BUILD_DISCCOFAN_CMD}"