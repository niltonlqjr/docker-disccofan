FILE_CMD=$1
pass=$2

if [ -z $1 ]
then
    echo "Usage: $0 <comand file> <password>"
    echo "where <command file> is the the file with command to be executed"
    exit 1
fi

if [ -z $2 ]
then
    echo "Usage: $0 <comand file> <password>"
    echo "where <command file> is the the file with command to be executed"
    exit 1
fi

echo ${pass} | sudo -S ls

while true;
do
    sleep 1
    CMD=`cat ${FILE_CMD}`
    $CMD
    echo '' > ${FILE_CMD}
    sudo -v
done