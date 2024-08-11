FILE_CMD='../container_command.txt'

while true;
do
    sleep 1
    CMD=`cat ${FILE_CMD}`
    $CMD
    echo '' > ${FILE_CMD}
done