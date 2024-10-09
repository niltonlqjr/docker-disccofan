source vars_experiments.sh

script=/home/mpi/net_collect.py
OUT_PREFIX=/home/mpi/host/results-disccofan

for i in `seq 0 $lim`
do
    dim=${dims[$i]}
    d1=`echo $dim | awk '{split($0,a," "); print a[1]}'`
    d2=`echo $dim | awk '{split($0,a," "); print a[2]}'`
    num_proc=`expr ${d1} '*' ${d2}`
    mkdir -p ${OUT_PREFIX}/dim_${d1}-${d2}-1
    for ((exec=1;$exec<=$NUM_EXECS;exec+=1))
    do
        output_complete_dir=${OUT_PREFIX}/dim_${d1}-${d2}-1/
        echo "grid: ${d1},${d2},1 => np: ${num_proc}, ${exec}"
        sudo python3 $script -o ${output_complete_dir}/network_out_exec${exec}.txt -i 0.5 disccofan
        sleep 5
    done
done

