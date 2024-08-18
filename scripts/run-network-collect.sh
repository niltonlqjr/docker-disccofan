dims=('1 2' '3 4' '5 6')
lim=`expr ${#dims[@]} - 1`

cur_dir=`pwd`
script=$cur_dir/net_collect.py
NUM_EXECS=5

OUT_PREFIX=/home/mpi/host/results-disccofan

for i in `seq 0 $lim`
do
    dim=${dims[$i]}
    d1=`echo $dim | awk '{split($0,a," "); print a[1]}'`
    d2=`echo $dim | awk '{split($0,a," "); print a[2]}'`
    num_proc=`expr ${d1} '*' ${d2}`
    for PROC_PER_HOST in `seq 1 12`
    do
        mkdir -p ${OUT_PREFIX}/dim_${d1}-${d2}-1/proc_per_host${PROC_PER_HOST}/
        for ((exec=1;$exec<=3;exec+=1))
        do
            output_complete_dir=${OUT_PREFIX}/dim_${d1}-${d2}-1/proc_per_host${PROC_PER_HOST}
            echo "grid: ${d1},${d2},1 => np: ${num_proc}, per host: ${PROC_PER_HOST}, ${exec}"
            sudo python3 $script -o ${output_file_name}/network_out_exec${exec}.txt -i 0.5 disccofan
        done
    done
done

