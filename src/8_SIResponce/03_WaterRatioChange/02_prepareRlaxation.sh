basePath=RelaxationWaterRatio
mkdir -p ${basePath}/mask0 ${basePath}/mask1

# xyz file
cp Water_cluster222_mask0.xyz ${basePath}/mask0/
cp Water_cluster222_mask1.xyz ${basePath}/mask1/

# cp2k input file
sourcePath=/Users/mac/Github/UM_ClusterBak/Github/MAPbI3_Water/5_water/03_water_opt
dir=222
cp ${sourcePath}/cluster_${dir}_water_big_box_nofix/input.inp ${basePath}/mask0/
cp ${sourcePath}/cluster_${dir}_water_big_box_nofix/input.inp ${basePath}/mask1/

# Change the xyz file name 
sed -i '' 's/Water_cluster222.xyz/Water_cluster222_mask0.xyz/g' ${basePath}/mask0/input.inp
sed -i '' 's/Water_cluster222.xyz/Water_cluster222_mask1.xyz/g' ${basePath}/mask1/input.inp


# Triton running test file
echo 'module load cp2k && mpirun -n 2 cp2k.popt -i input.inp' > ${basePath}/mask0/runTest.sh
echo 'module load cp2k && mpirun -n 2 cp2k.popt -i input.inp' > ${basePath}/mask1/runTest.sh
chmod +x ${basePath}/mask0/runTest.sh
chmod +x ${basePath}/mask1/runTest.sh
# Triton Submit file
cp ../02_RelaxNaked/222/submit.sh ${basePath}/mask0/submit.sh
cp ../02_RelaxNaked/222/submit.sh ${basePath}/mask1/submit.sh



# Upload to Triton

zip -r ${basePath}.zip ${basePath}
scp ${basePath}.zip huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/
