#!/bin/bash
# 10s of stress; 5s of sleep
declare -i CONT=1
echo "Experiment test..."
for i in {0..10..1}
do
  echo "CPU Load: $1 %"
  printf "State before run #%d:" $CONT
  stress-ng -c 0 -l $1 -t 10s
  printf "State after run #%d:" $CONT
  uptime
  let CONT++
  echo "Cooling time of 5s"
  sleep 5s
done