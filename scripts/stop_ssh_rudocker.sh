dir_script=$1

pass=$2

script=run-container-host-non-interative.sh
time=3

if [ -z $1 ]
then
    echo "Usage: $0 directory password"
    echo "where <directory> is the directory that contains scritp to start container"
    exit 1
fi

if [ -z $2 ]
then
    echo "Usage: $0 directory password"
    exit 1
fi

if [ ! -f "${dir_script}/${script}" ]
then
    echo "file ${dir_script}/${script} not found"
    exit 1
fi


echo "stopping ssh service, changing directory to '${dir_script}' and running script in ${time} seconds"
for i in `seq ${time} -1 1`
do
    sleep 1
    echo "$i seconds"
done

echo ${pass} | sudo -S service ssh stop 
cd ${dir_script} 
./${script}
