#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --time=5-00:00:00  # Job time allocation
#SBATCH --mem=30G          # Memory
#SBATCH -J relax    # Job name
#SBATCH -o relax.log      # Output file

# Load environment
module load cp2k

export OMP_NUM_THREADS=1

# Calculate total number of processes
TOTAL_TASKS=$((SLURM_NNODES * SLURM_NTASKS_PER_NODE))

# Print job info
echo "Job ID: "$SLURM_JOB_ID
echo "Job Name: "$SLURM_JOB_NAME


# Remember some metadata
echo -e "Run start: "`date` >> ./metadata.txt
echo -e "   Job ID: "$SLURM_JOB_ID >> ./metadata.txt
echo -e "   Job Name: "$SLURM_JOB_NAME >> ./metadata.txt
echo -e "   Comment: CP2K Structure Relaxation Calculate" >> ./metadata.txt


# Run 
mpirun -n $TOTAL_TASKS cp2k.psmp -i input.inp -o output.log