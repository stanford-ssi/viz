#!/bin/bash

dir=../../IREC_2018_data/

cat bno_accel.html > "$dir/motion.html"
cat mma.html bno_gyro.html >> "$dir/motion.html"
cat header.html | cat - "$dir/motion.html" > temp && mv temp "$dir/motion.html"
