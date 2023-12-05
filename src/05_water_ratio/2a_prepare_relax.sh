basePath=VacancyLevels


# Step 1: Calculation file parepare
for vacancyLevel in 0 1 2 3 4 5 6
do
    mkdir -p ${basePath}/level${vacancyLevel}
    # Rename the xyz file, so that I don't need to change in the input file
    cp Water_cluster222_VacancyLevel${vacancyLevel}.xyz ${basePath}/level${vacancyLevel}/Water_cluster222.xyz
    cp relax_input.inp ${basePath}/level${vacancyLevel}/


    echo 'module load cp2k && mpirun -n 2 cp2k.popt -i input.inp' > ${basePath}/level${vacancyLevel}/runTest.sh
    chmod +x ${basePath}/level${vacancyLevel}/runTest.sh
    cp relax_submit.sh ${basePath}/level${vacancyLevel}/
done



# 2. Upload to Triton
if [ ! -f UpRlaxed.flag ]; then
    echo 'Uploading file to cluster ...'
    zip -r ${basePath}.zip ${basePath}
    scp ${basePath}.zip huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/
    touch UpRlaxed.flag
fi



# 3. Test and Run on Trion 



# 4. Download the Calculation results from cluster when completed
rsync --exclude='*RESTART*' --exclude='*.out' --exclude='*.Hessian' --exclude='*.restart*' -Pr huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/${basePath} .

