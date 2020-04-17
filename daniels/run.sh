snakemake -s /shahlab/archive/pye/BIOF-150/Snakefile -C lib_path=$1 --cluster 'qsub -V -hard -q shahlab.q -l h_vmem=12G -S /bin/bash -o tmp_out -e tmp_err' -j 512 -q -k 
