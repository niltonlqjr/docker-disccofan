dims=( '4 4' '8 4' '8 6' '8 8' '10 8' '12 8' '14 8' '16 8' '12 12' '16 10' '16 11' '16 12' )
lim=`expr ${#dims[@]} - 1`

NUM_EXECS=3

INP_DIR=/home/mpi/host/split

HF_DIR=/home/mpi/host/hostfile

for i in `seq 0 $lim`
do
    dim=${dims[$i]}
    d1=`echo $dim | awk '{split($0,a," "); print a[1]}'`
    d2=`echo $dim | awk '{split($0,a," "); print a[2]}'`
    in_prefix_img=${INP_DIR}/dim_${d1}-${d2}-1/IMG_PHR1A__${d1}_${d2}_1
    PROC_PER_HOST=`expr i + 1`
    HOSTFILE=${HF_DIR}/hosts_lins_${PROC_PER_HOST}proc.txt
    for ((exec=1;$exec<=$NUM_EXECS;exec+=1))
    do
        num_proc=`expr ${d1} '*' ${d2}`
        echo "grid: ${d1},${d2},1 => np: ${num_proc}, per host: ${PROC_PER_HOST}, exec=${exec}"
        mpirun -np ${num_proc} --hostfile ${HOSTFILE} ./disccofan -g ${d1},${d2},1 --inprefix ${in_prefix_img} --intype JP2 --infile 1 --overlap 0
        sleep 5
    done
done

