basePath=PDOSs
relaxPath=VacancyLevels
sourcePath=../../6_Writing/dos/cp2k-full/cp2k_dos_222

# 1. Prepare calculation files
for vacancyLevel in 0 1 2 3 4 5 6
do
    # Create path for each vacancy level
    mkdir -p ${basePath}/level${vacancyLevel}

    # Obtain the last frame and name it as MAPbI3-pos-last.xyz (extractLast is a program in dailybin)
    extractLast ${relaxPath}/level${vacancyLevel}/MAPbI3-pos-1.xyz > ${basePath}/level${vacancyLevel}/MAPbI3-pos-last.xyz
    
    # Input file to calculate PDOS
    cp ${sourcePath}/input.inp ${basePath}/level${vacancyLevel}/

    # Prepare the test and submit script for cluster
    echo 'module load cp2k && mpirun -n 2 cp2k.popt -i input.inp' > ${basePath}/level${vacancyLevel}/runTest.sh
    chmod +x ${basePath}/level${vacancyLevel}/runTest.sh
    cp submit.sh ${basePath}/level${vacancyLevel}/
    # Change calculation time
    sed -i '' 's/--time=72:00:00/--time=12:00:00/g' ${basePath}/level${vacancyLevel}/submit.sh
    sed -i '' 's/--ntasks-per-node=24/--ntasks-per-node=12/g' ${basePath}/level${vacancyLevel}/submit.sh
    sed -i '' 's/mpirun -n 24/mpirun -n 12/g' ${basePath}/level${vacancyLevel}/submit.sh
done




# 2. Upload to Triton
if [ ! -f UpPDOS.flag ]; then
    echo 'Uploading file to cluster ...'
    zip -r ${basePath}.zip ${basePath}
    scp ${basePath}.zip huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/
    touch UpPDOS.flag
fi




# # 3. Test and submit on Trion 



# # 4. Download the Calculation results from cluster when completed
rsync -Pr huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/${basePath} .