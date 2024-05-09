source ./vars.sh
arg=$1
if [ $arg == "nompirun" ]
then
    echo "Building a docker image to a machine that WILL NOT RUN mpirun command"
elif [ $arg == "mpirun" ]
then
    echo "Building a docker image to a machine WILL RUN mpirin command"
    DOCKERFILE_NAME='Dockerfile.mpirun'
else
    echo "Invalid Argumments"
    echo "Usage:"
    echo "$0 <mpirun | nompirun>"
    echo "if mpirun argumment is used then the docker image will be build to a machine that will run mpirun command"
    echo "if nompirun argumment is used the dockerimage will be build to a machine that will NOT run mpirun command"
    exit 1
fi

#args used to build dockerfile
CONTAINER_BUILD_ARGS="--build-arg UID=$HOST_UID --build-arg GID=$HOST_GID --build-arg VOLUME_DIR=$VOLUME_DIR"

${CONTAINER_CMD} ${BUILD_CMD} ${CONTAINER_BUILD_ARGS} -t ${CONTAINER_IMAGE} -f ${DOCKERFILE_NAME} ${CONTEXT_PATH}