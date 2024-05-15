VOLUME_DIR="${HOME}"                # Mappped volume
WORK_DIR="${HOME}"                  # Directory that will be used to executables
CONTAINER_CMD="docker"              # Container application
BUILD_CMD="build"                   # Container application build command
RUN_CMD="run"                       # Container application run command
CONTEXT_PATH="../"                  # dockerfile context path
CONTAINER_IMAGE="disccofan:20.04"   # Name of image to be generated


HOST_UID=$(id -u) # get user ID from system to use in docker 
HOST_GID=$(id -g) # get user ID from system to use in docker



