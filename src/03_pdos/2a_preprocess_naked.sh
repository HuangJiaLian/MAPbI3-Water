#!/bin/bash
# Using Python 2 
eval "$(conda shell.bash hook)"
conda activate py2

calculation_type=PDOSNaked234
echo $calculation_type
# Out loop
for size in 222 333 444
do
cp get-smearing-pdos.py  $calculation_type/Cluster_$size/
cp pdos.py $calculation_type/Cluster_$size/
cd $calculation_type/Cluster_$size/
# Inner loop
for i in 1 2 3 4 5 
do 
    echo MAPbI3_DOS-ALPHA_k$i-1.pdos
    python get-smearing-pdos.py MAPbI3_DOS-ALPHA_k$i-1.pdos
    mv smeared.dat smeared_alpha_$i.dat

    echo MAPbI3_DOS-BETA_k$i-1.pdos
    python get-smearing-pdos.py MAPbI3_DOS-BETA_k$i-1.pdos
    mv smeared.dat smeared_beta_$i.dat

    python get-smearing-pdos.py MAPbI3_DOS-ALPHA_k$i-1.pdos MAPbI3_DOS-BETA_k$i-1.pdos
    mv smeared.dat smeared_both_$i.dat
done
cd ../../
done

# Change back to base env
eval "$(conda shell.bash hook)"
conda activate base
