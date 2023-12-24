calculation_type=ab_energy_final

sizes=(222 333 444) 
water_numbs=(156 370 891) 

for i in ${!sizes[@]}
do
    size=${sizes[$i]}
    water_num=${water_numbs[$i]}
    echo "########### ${size} ${water_num} ##############"
    cluster_water_log=${calculation_type}/Cluster_${size}/MAPbI3_Water.log
    cluster_log=${calculation_type}/Cluster_${size}/MAPbI3.log
    water_log=${calculation_type}/Cluster_${size}/Water.log
    E_total=$(grep "Total energy: " ${cluster_water_log} | awk '{print $3}' | tail -n 1)
    E_cluster=$(grep "Total energy: " ${cluster_log} | awk '{print $3}' | tail -n 1)
    E_water=$(grep "Total energy: " ${water_log} | awk '{print $3}' | tail -n 1)
    echo Cluster${size}  E_total in a.u. ${E_total}
    echo Cluster${size}  E_cluster in a.u. ${E_cluster}
    echo Cluster${size}  E_water in a.u. ${E_water}
    E_absorb=$(echo "$E_total - $E_cluster - $E_water" | bc)
    echo Cluster${size} E_absorb in a.u. ${E_absorb}
    E_absorb_per_water=$(echo "scale=4; $E_absorb / $water_num" | bc)
    echo Cluster${size} E_absorb per water in a.u. ${E_absorb_per_water}
done
