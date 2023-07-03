#!/bin/bash
while true; do
    read -p "Enter the CPU load (0-100%): " parameter
    if [[ "$parameter" =~ ^[0-9]+$ ]] && (( parameter >= 0 && parameter <= 100 )); then
        break
    else
        echo "Invalid input. Please try again."
    fi
done
nohup ./stress-x.sh $parameter >> ../results/experiment.log & pid1=$!
nohup ./monitor.sh $parameter >> ../results/experiment.log & pid2=$!
wait $pid1
kill $pid2