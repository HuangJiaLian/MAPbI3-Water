mkdir -p 222 333 444 

sourcePath=/Users/mac/Github/UM_ClusterBak/Github/MAPbI3_Water/5_water/03_water_opt

dir=222
cp ${sourcePath}/cluster_${dir}_water_big_box_nofix/input.inp $dir/. 
cp ${sourcePath}/cluster_${dir}_water_big_box_nofix/Water_cluster${dir}.xyz $dir/.

dir=333
cp ${sourcePath}/cluster_${dir}_water_no_fix/input.inp $dir/. 
cp ${sourcePath}/cluster_${dir}_water_no_fix/Water_cluster${dir}.xyz $dir/.

dir=444
cp ${sourcePath}/cluster_${dir}_water_iampe_nofix/input.inp $dir/. 
cp ${sourcePath}/cluster_${dir}_water_iampe_nofix/Water_cluster${dir}.xyz $dir/.

# for dir in 222 333 444
# do
#   cd $dir
#   # Perform operations here
#   cp ${sourcePath}/cluster_${dir}_water_big_box_nofix/input.inp $dir/. 
#   cp ${sourcePath}/cluster_${dir}_water_big_box_nofix/Water_cluster${dir}.xyz .
#   cd ..
# done
