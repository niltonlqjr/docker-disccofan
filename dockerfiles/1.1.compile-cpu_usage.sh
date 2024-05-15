source ./vars.sh

#shell commands to build disccofan  
BUILD_CPU_USAGE_CMD="git clone https://github.com/niltonlqjr/cpu_usage.git && cd cpu_usage && make"

${CONTAINER_CMD} ${RUN_CMD} --rm \
  --env "LD_LIBRARY_PATH=/usr/local/hdf5/lib/:$LD_LIBRARY_PATH" \
  --workdir ${WORK_DIR} \
  --volume ${WORK_DIR}:/home/mpi/host \
  ${CONTAINER_IMAGE} sh -c "${BUILD_CPU_USAGE_CMD}"