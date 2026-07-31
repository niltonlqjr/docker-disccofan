np=200
hf=host/slots_lins.txt
grid_comma=10,20,1
grid=$(echo ${grid_comma} | awk -F',' '{print $1"_"$2"_"$3}')
in_prefix=host/gigapixel_img/PHR1A/200_tiles/dim_${grid}/IMG_PHR1A__${grid}
out_prefix=host/gigapixel_img/PHR1A/200_tiles_filtered/dim_${grid}/IMG_PHR1A__${grid}
in_type=JP2


mpirun -np ${np} --hostfile ${hf} disccofan/disccofan -g ${grid} --inprefix ${in_prefix} --intype ${in_type} --outprefix ${out_prefix} --infile 1 --overlap 0