#!/bin/bash

calculation_type=nofix

sizes=(222 333 444)
labels=('(a)' '(b)' '(c)')
labelIs=('(a)' '(b)' '(c)')
labelFs=('(d)' '(e)' '(f)')

pSize=80
offSet=60


# Add label to the right bottom of each images
for i in $(seq 0 2)
do 
  convert -pointsize $pSize init_${sizes[$i]}.png -gravity SouthEast -annotate +$offSet+$offSet ${labelIs[$i]}  init_${sizes[$i]}_l.png
  convert -pointsize $pSize final_${sizes[$i]}.png -gravity SouthEast -annotate +$offSet+$offSet ${labelFs[$i]}  final_${sizes[$i]}_l.png
done

# Make two lists containing [a, b, c] and [d, e, f]
for i in {2..4}; do imgIlist+=(init_$i$i$i\_l.png);imgFlist+=(final_$i$i$i\_l.png);done

# Append each list
convert ${imgIlist[@]} +append init_all.png
convert ${imgFlist[@]} +append final_all.png


# Append all
convert init_all.png final_all.png -append MAPbI3_Water.png

convert -rotate 90 -resize 50% init_111.png init_111_.png
convert -size $(identify -format "%wx%h" init_111_.png) xc:none background.png
convert init_111_.png background.png +append init_111_new.png



# Add legend 
convert -pointsize $((pSize * 70 / 100)) init_111_new.png -gravity NorthEast\
        -annotate -70+20 Pb \
        -annotate -70+$((20 + 1 * 85))  I \
        -annotate -70+$((20 + 2 * 85))  O \
        -annotate -70+$((20 + 3 * 85))  N \
        -annotate -70+$((20 + 4 * 85))  C \
        -annotate -70+$((20 + 5 * 85))  H \
        init_111_noted.png
convert init_111_noted.png MAPbI3_Water.png -gravity West +append Figure1.png

rm *l.png background.png  *new.png *noted.png init_111_.png MAPbI3_Water.png


