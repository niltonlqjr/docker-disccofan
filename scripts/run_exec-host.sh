dir=$1
pass=$2


if [ -z $1 ]
then
    echo "Usage: $0 directory password"
    echo "where <directory> is the directory that contains scritp to start exec-host.sh"
    exit 1
fi

if [ -z $2 ]
then
    echo "Usage: $0 directory password"
    exit 1
fi

if [ ! -f "${dir}/exec-host.sh" ]
then
    echo "file ${dir}/exec-host.sh not found"
    exit 1
fi

cd ${dir}
echo ${pass} | sudo -S pwd
./exec-host.sh &