dir=$1
file_cmd=$2
pass=$3

if [ -z $1 ]
then
    echo "Usage: $0 < directory > <comand file> <password>"
    echo "where:" 
    echo "   <directory> is the directory that contains scritp to start exec-host.sh"
    echo "   <comand file> is the file containing the commands to execute"
    echo "   <password> is the password"
    exit 1
fi

if [ -z $2 ]
then
    echo "Usage: $0 < directory > <comand file> <password>"
    echo "where:" 
    echo "   <directory> is the directory that contains scritp to start exec-host.sh"
    echo "   <comand file> is the file containing the commands to execute"
    echo "   <password> is the password"
    exit 1
fi

if [ -z $3 ]
then
    echo "Usage: $0 < directory > <comand file> <password>"
    echo "where:" 
    echo "   <directory> is the directory that contains scritp to start exec-host.sh"
    echo "   <comand file> is the file containing the commands to execute"
    echo "   <password> is the password"
    exit 1
fi

if [ ! -f "${dir}/exec-host.sh" ]
then
    echo "file ${dir}/exec-host.sh not found"
    exit 1
fi

${dir}/exec-host.sh ${file_cmd} ${pass} &
