# Copy legend image
cp ../../7_Structure_evolution/cluster/dgraph/legend_rn_noted.png legend.png

numbers=(1 60 120 180 240)
concatenated_images=""
for num in "${numbers[@]}"
do
    frame_number_text="$((num*100/240))%"
    convert frame_${num}.png -gravity south -pointsize 300 -annotate +0+10 "${frame_number_text}" frame_${num}_annotated.png
    concatenated_images+="frame_${num}_annotated.png "
done

convert legend.png -resize 250% ${concatenated_images} -gravity west +append opt_process.png

# I also want to compare when water are added
# numbers=(1 41 82 123 164)
numbers=(1 91 181 271 361)
concatenated_images=""
for num in "${numbers[@]}"
do
    frame_number_text="$((num*100/361))%"
    convert frame_water100p${num}.png -gravity south -pointsize 300 -annotate +0+10 "${frame_number_text}" frame_water100p${num}_annotated.png
    concatenated_images+="frame_water100p${num}_annotated.png "
done

convert legend.png -resize 250% ${concatenated_images} -gravity west +append opt_process_water100p.png



# Convert opt_process.png to white background
convert opt_process.png -background white -alpha remove -alpha off opt_process_white.png

# Add black box edges around opt_process_white.png
convert opt_process_white.png -bordercolor black -border 5x5 opt_process_black.png

# Add legend text (a) at the right bottom corner of opt_process_black.png
# convert opt_process_black.png -gravity southeast -pointsize 300 -annotate +10+10 "(a)" opt_process_black_annotated.png

# Convert opt_process_water100p.png to white background
convert opt_process_water100p.png -background white -alpha remove -alpha off opt_process_water100p_white.png

# Add black box edges around opt_process_water100p_white.png
convert opt_process_water100p_white.png -bordercolor black -border 5x5 opt_process_water100p_black.png

# Add legend text (b) at the right bottom corner of opt_process_water100p_black.png
# convert opt_process_water100p_black.png -gravity southeast -pointsize 300 -annotate +10+10 "(b)" opt_process_water100p_black_annotated.png

# Append the two images vertically
convert opt_process_black.png opt_process_water100p_black.png -append opt_process_compare.png


