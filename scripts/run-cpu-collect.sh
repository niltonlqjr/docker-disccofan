#dims=( '4 4' '8 4' '8 6' '8 8' '10 8' '12 8' '14 8' '16 8' '12 12' '16 10' '16 11' '16 12' )
#dims=('2 29' '4 29')
#dims=('1 124' '2 62' '31 4' '4 31' '62 2' '124 1')
dims=('4 4' '8 4' '8 8' '12 8' '12 12')

lim=`expr ${#dims[@]} - 1`

script=/home/mpi/cpu_collect.py
NUM_EXECS=3

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
        python3 $script -p -c ${output_complete_dir}/cpu_out_exec${exec}- -m ${output_complete_dir}/mem_out_exec${exec}- -i 0.5 disccofan
        sleep 5
    done
done

