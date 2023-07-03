#!/bin/bash
# $1 <SUT>, $2 <path/to/results>, $3 <workload>,  $4 <VUs>, $5 <run_nr>
timestamp_file=$(date +"%Y%m%d-%H%M%S")

pgrep -f \"start_Rittal.sh\" | xargs kill
tmux kill-window
cd $2
/usr/bin/python3 ~/THESIS/master-project-def/scripts/preprocessing/output_2_csv.py $1 $2 $3 $4 $5
rm $2/energy*.log
