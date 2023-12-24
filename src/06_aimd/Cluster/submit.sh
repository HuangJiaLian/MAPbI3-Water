#!/bin/bash -l

#SBATCH --job-name              8ps-cluster
#SBATCH --partition             iampe-fast
#SBATCH --nodes                 1
#SBATCH --tasks-per-node        96
#SBATCH --time                  120:00:00
#SBATCH --mem                   300G
#SBATCH --output                %j.out
#SBATCH --error                 %j.err
#SBATCH --mail-type=ALL 
#SBATCH --mail-user=jiehuang@um.edu.mo 

# asks SLURM to send the USR1 signal 120 seconds before end of the time limit
#SBATCH --signal=B:USR1@120

source /etc/profile
source /etc/profile.d/modules.sh
# source /data/home/jiehuang/.jackprograms/cp2k-7.1/tools/toolchain/install/setup
source /data/home/jiehuang/.jackprograms/cp2k-2022.2/tools/toolchain/install/setup

# define the handler function
# note that this is not executed here, but rather
# when the associated signal is sent
your_cleanup_function()
{
    echo "function your_cleanup_function called at $(date)"
    # do whatever cleanup you want here
    pkill -u endcut
}

# call your_cleanup_function once we receive USR1 signal
trap 'your_cleanup_function' USR1

# your cp2k program goes below
# export OMP_NUM_THREADS=1
ulimit -s unlimited
NP=$(($SLURM_NTASKS_PER_NODE * $SLURM_JOB_NUM_NODES))

mpirun -mca pml ucx -mca btl ^uct -np $NP cp2k.popt -i input.inp
