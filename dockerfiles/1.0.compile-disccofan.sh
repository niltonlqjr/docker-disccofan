source ./vars.sh

#shell commands to build disccofan  
BUILD_DISCCOFAN_CMD="git clone https://github.com/niltonlqjr/disccofan.git && cd disccofan && make"



${CONTAINER_CMD} ${RUN_CMD} --rm \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir ${WORK_DIR} \
  --volume ${WORK_DIR}:/home/mpi/host \
  ${CONTAINER_IMAGE} sh -c "${BUILD_DISCCOFAN_CMD}"