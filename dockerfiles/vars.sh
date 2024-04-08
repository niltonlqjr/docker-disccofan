CONTAINER_CMD="docker"              # Container application
BUILD_CMD="build"                   # Container application build command
RUN_CMD="run"                       # Container application run command
DOCKERFILE_NAME="Dockerfile"        # dockerfile name
DOCKERFILE_PATH="."                 # dockerfile path
CONTAINER_IMAGE="disccofan:20.04"   # Name of image to be generated
VOLUME_DIR="$(realpath $(pwd))/.."  # Mappped volume
WORK_DIR="$(realpath $(pwd))/.."    # Work dir

HOST_UID=$(id -u)
HOST_GID=$(id -g)

CONTAINER_BUILD_ARGS="--build-arg UID=$HOST_UID --build-arg GID=$HOST_GID "

