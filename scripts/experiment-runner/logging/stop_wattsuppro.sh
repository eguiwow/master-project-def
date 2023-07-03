#!/bin/bash
timestamp_file=$(date +"%Y%m%d-%H%M%S")

pgrep -f \"start_wattsuppro.sh\" | xargs kill

/usr/bin/python3 /home/ander/scripts/output_2_csv.py $1
mv /home/ander/results/energy$1.log /home/ander/results/energy_${1}_$timestamp_file.log
rm -r /home/ander/results/energy*.log

# GL2 == /dev/ttyUSB0
# GL3 == /dev/ttyUSB2
# GL4 == /dev/ttyUSB1