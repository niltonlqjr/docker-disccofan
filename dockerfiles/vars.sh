VOLUME_DIR="$(realpath $(pwd))/.."                      # Mappped volume
WORK_DIR="$(realpath $(pwd))/.."                        # Work dir
CONTAINER_CMD="docker"                                  # Container application
BUILD_CMD="build"                                       # Container application build command
RUN_CMD="run"                                           # Container application run command
DOCKERFILE_NAME="${WORK_DIR}/dockerfiles/Dockerfile"    # dockerfile name
CONTEXT_PATH="../"                                      # dockerfile context path
CONTAINER_IMAGE="disccofan:20.04"                       # Name of image to be generated


HOST_UID=$(id -u) # get user ID from system to use in docker 
HOST_GID=$(id -g) # get user ID from system to use in docker



