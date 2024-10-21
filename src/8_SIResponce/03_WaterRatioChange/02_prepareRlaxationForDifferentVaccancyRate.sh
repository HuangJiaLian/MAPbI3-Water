basePath=VacancyLevels


# Step 1: Calculation file parepare
# Input file source
sourcePath=/Users/mac/Github/UM_ClusterBak/Github/MAPbI3_Water/5_water/03_water_opt
dir=222

for vacancyLevel in 0 1 2 3 4 5 6
do
    mkdir -p ${basePath}/level${vacancyLevel}
    # Rename the xyz file, so that I don't need to change in the input file
    cp Water_cluster222_VacancyLevel${vacancyLevel}.xyz ${basePath}/level${vacancyLevel}/Water_cluster222.xyz
    cp ${sourcePath}/cluster_${dir}_water_big_box_nofix/input.inp ${basePath}/level${vacancyLevel}/

    # Increase the max iteration steps to ensure the structures are optimized
    sed -i '' 's/MAX_ITER 200/MAX_ITER 1000/g' ${basePath}/level${vacancyLevel}/input.inp
    echo 'module load cp2k && mpirun -n 2 cp2k.popt -i input.inp' > ${basePath}/level${vacancyLevel}/runTest.sh
    chmod +x ${basePath}/level${vacancyLevel}/runTest.sh
    cp submit.sh ${basePath}/level${vacancyLevel}/
done



# 2. Upload to Triton
if [ ! -f UpRlaxed.flag ]; then
    echo 'Uploading file to cluster ...'
    zip -r ${basePath}.zip ${basePath}
    scp ${basePath}.zip huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/
    touch UpRlaxed.flag
fi



# 3. Test and Run on Trion 
# Test and submit on Triton
#   25001313 batch-csl    relax  huangj4 PD       0:00      1 (Resources)
#   25001319 batch-csl    relax  huangj4 PD       0:00      1 (Priority)
#   25001321 batch-csl    relax  huangj4 PD       0:00      1 (Priority)
#   25001325 batch-csl    relax  huangj4 PD       0:00      1 (Priority)
#   25001329 batch-csl    relax  huangj4 PD       0:00      1 (Priority)
#   25001309 batch-mil    relax  huangj4  R       1:16      1 milan8
#   25001307 batch-mil    relax  huangj4  R       7:40      1 milan14


# 4. Download the Calculation results from cluster when completed
rsync -Pr huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/${basePath} .

