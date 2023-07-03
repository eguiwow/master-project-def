#!/bin/bash
# $1 = load; $2 = time in s
nohup ./stress-er.sh $1 $2 >> ../../results/experiment.log & pid1=$!
nohup ./monitor-er.sh $3 $1 >> ../../results/experiment.log & pid2=$!
wait $pid1
kill $pid2