#!/bin/bash
timestamp_file=$(date +"%Y%m%d-%H%M%S")
# INPUT $1 <server> and $2 <timeout>
case "$1" in
  GL2)
    nohup /usr/bin/python3 /home/ander/wattsuppro_logger/WattsupPro.py -l -p /dev/ttyUSB0 -t $2 -o /home/ander/results/energy$1.log & pid1=$!
    ;;
  GL3)
    nohup /usr/bin/python3 /home/ander/wattsuppro_logger/WattsupPro.py -l -p /dev/ttyUSB2 -t $2 -o /home/ander/results/energy$1.log & pid1=$!
    ;;
  GL4)
    nohup /usr/bin/python3 /home/ander/wattsuppro_logger/WattsupPro.py -l -p /dev/ttyUSB1 -t $2 -o /home/ander/results/energy$1.log & pid1=$!
    ;;
  *)
    echo "Invalid parameter. Please choose from GL2, GL3, or GL4."
    exit 1
    ;;
esac

# GL2 == /dev/ttyUSB0
# GL3 == /dev/ttyUSB2
# GL4 == /dev/ttyUSB1