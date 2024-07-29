FILE='teste.jpg'
FACTOR=2

if [[ ! -z $1 ]];
then
    FILE=$1
fi
if [[ ! -z $2 ]];
then
    FACTOR=$2
fi
EXT_OUT=`echo "$1" | awk '{n=split($1,A,"."); print A[n]}'`
if [[ ! -z $3 ]];
then
    EXT_OUT=$3
fi

echo "./downscale -o ${FILE}_DS_${FACTOR}.${EXT_OUT} -f ${FACTOR},${FACTOR} ${FILE}"

./downscale -o ${FILE}_DS_${FACTOR}.${EXT_OUT} -f ${FACTOR},${FACTOR} ${FILE} 
