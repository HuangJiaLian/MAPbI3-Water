#!/bin/bash
DValue=82
size=900

cp ../../../02_relax/final_000.png legend.png



for num in 64 128 256 512 1024 2048
do
echo "Processing frame $num"
#convert R_$num.png -density $DValue -resize $sizex$size R_$num_.png
convert frame_$num.png -density $DValue -resize $sizex$size -gravity North -pointsize 125 -annotate +0+10 "t = $num fs"  R_$num\_.png
done


# Legend 
convert legend.png -rotate 90 -resize 80% legend_r.png
convert -size $((2 * $(identify -format "%w" legend_r.png)))x$(identify -format "%h" legend_r.png) xc:none background.png
convert legend_r.png background.png +append legend_rn.png
offset_y=172
offset_x=150
convert -pointsize 100 legend_rn.png -gravity NorthEast\
        -annotate -$offset_x+5 Pb \
        -annotate -$offset_x+$((20 + 1 * $offset_y))  I \
        -annotate -$offset_x+$((20 + 2 * $offset_y))  N \
        -annotate -$offset_x+$((20 + 3 * $offset_y))  C \
        -annotate -$offset_x+$((20 + 4 * $offset_y))  H \
        legend_rn_noted.png
# open legend_rn_noted.png

convert R_64_.png R_128_.png R_256_.png R_512_.png R_1024_.png R_2048_.png +append R.png
convert G_64.png G_128.png G_256.png G_512.png G_1024.png G_2048.png +append G.png
convert Dg_64.png Dg_128.png Dg_256.png Dg_512.png Dg_1024.png Dg_2048.png +append Dg.png
convert Ang_64.png Ang_128.png Ang_256.png Ang_512.png Ang_1024.png Ang_2048.png +append Ang.png


convert R.png G.png  -append row12.png
convert row12.png legend_rn_noted.png -gravity West  +append row12_legend.png

# Append all
convert row12_legend.png Dg.png Ang.png  -append all_m.png

#convert -pointsize 20 -fill black -draw 'text 270, 460 "a"' $calculation_type/all.png $calculation_type/all_with_labels.png 
#
open all_m.png
