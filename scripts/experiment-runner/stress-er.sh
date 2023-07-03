#!/bin/bash
# $1 = load; $2 = time in s
echo "Experiment test..."

echo "CPU Load: $1 %"
stress-ng -c 0 -l $1 -t ${2}s
