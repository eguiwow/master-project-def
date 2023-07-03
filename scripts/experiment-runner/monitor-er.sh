#!/bin/bash
# $1 <GLX>; $2 <workload>; $3 <VUs>; $4 <run_nr>

folder_path="/home/ander/results"

# Create the results folder if it does not exist
if [ ! -d "$folder_path" ]; then
    mkdir -p "$folder_path"
fi

echo "Logging the measurements..."
interval=9
timestamp_file=$(date +"%Y%m%d-%H%M%S")

# TEMPERATURE HEADERS
cpu_cores=$(nproc)  # Get the number of CPU cores
temp_headers=""

for ((i=1; i<=($cpu_cores/2); i++))
do
    temp_headers+="tempCPU$i,"
done

temp_headers=${temp_headers%?} # Remove last comma

#Headers for csv. Check whether VUs was provided or not
if [ -z "$3" ]; then
    echo "Timestamp,%usr,%sys,%IOwait,%Idle,$temp_headers" >> $folder_path/${4}cpu_${1}-${2}_$timestamp_file.csv
    echo "Timestamp,Used,Available" >> $folder_path/${4}mem_${1}-${2}_$timestamp_file.csv
else
    echo "Timestamp,%usr,%sys,%IOwait,%Idle,$temp_headers" >> $folder_path/cpu_${1}-${2}-${3}_$timestamp_file.csv
    echo "Timestamp,Used,Available" >> $folder_path/${4}mem_${1}-${2}-${3}_$timestamp_file.csv
fi

while true; do
    timestamp=$(date +"%Y%m%d-%T")
    if [ "$1" = "GL5" ] || [ "$1" = "GL6" ]; then # GL5 or GL6 so we change the parameters
        cpu_data=$(mpstat 1 1| awk 'FNR == 4 {print $4 "," $6 "," $7 "," $13 ","}')
    else
        cpu_data=$(mpstat 1 1| awk 'FNR == 4 {print $3 "," $5 "," $6 "," $12 ","}')
    fi
    mem_data=$(free -m | awk 'FNR == 2 {print $3 "," $7}')
    temp_data=$(sensors | awk 'BEGIN{RS="\n"; line=""} /^Core [0-9]:/ {line = line $3 ","} END{print line}')

    temp_data=${temp_data%,} # remove last comma

    if [ -z "$3" ]; then # if VUs is sent, then add it to the title of the file
        echo "$timestamp,$cpu_data$temp_data" >> $folder_path/${4}cpu_${1}-${2}_$timestamp_file.csv
        echo "$timestamp,$mem_data" >> $folder_path/${4}mem_${1}-${2}_$timestamp_file.csv
    else
        echo "$timestamp,$cpu_data$temp_data" >> $folder_path/${4}cpu_${1}-${2}-${3}_$timestamp_file.csv
        echo "$timestamp,$mem_data" >> $folder_path/${4}mem_${1}-${2}-${3}_$timestamp_file.csv
    fi
    sleep $interval #every 9s +1s of the mpstat instruction = 10s
done
