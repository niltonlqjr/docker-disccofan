source ./vars.sh

if [ -n $1 ]
then
    echo "Building a docker image to a machine that WILL NOT RUN mpirun command"
else
    echo "Building a docker image to a machine WILL RUN mpirin command"
    DOCKERFILE_NAME='Dockerfile.mpirun'
fi

#args used to build dockerfile
CONTAINER_BUILD_ARGS="--build-arg UID=$HOST_UID --build-arg GID=$HOST_GID --build-arg VOLUME_DIR=$VOLUME_DIR"

${CONTAINER_CMD} ${BUILD_CMD} ${CONTAINER_BUILD_ARGS} -t ${CONTAINER_IMAGE} -f ${DOCKERFILE_NAME} ${CONTEXT_PATH}