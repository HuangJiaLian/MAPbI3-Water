basePath=PreviousOpt

# 1. Prepare calculation files
for num in 222 333 444
do
    # Prepare the test and submit script for cluster
    echo 'module load cp2k && mpirun -n 2 cp2k.popt -i input.inp' > ${basePath}/cluster_${num}/runTest.sh
    chmod +x ${basePath}/cluster_${num}/runTest.sh
done




# 2. Upload to Triton
if [ ! -f UpCheckP.flag ]; then
    echo 'Uploading file to cluster ...'
    zip -r ${basePath}.zip ${basePath}
    scp ${basePath}.zip huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/
    touch UpCheckP.flag
fi




# # 3. Test and submit on Trion 



# # 4. Download the Calculation results from cluster when completed
# rsync -Pr huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/${basePath} .