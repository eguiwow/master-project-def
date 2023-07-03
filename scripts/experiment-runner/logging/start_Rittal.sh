#!/bin/bash
timestamp_file=$(date +"%Y%m%d-%H%M%S")
# INPUT $1 <server>, $2 <timeout>, $3 <path/to/results>, $4 userRittal, $5 passRittal
case "$1" in
  GL2)
    /home/eguiwow/.virtualenvs/thesis/bin/python3 ~/THESIS/Rittal_Power_Monitoring/rittal_aut_logs.py -p L2 -t $2 -s LTS -o $3/energy$1.log -U $4 -P $5
    ;;
  GL5)
    /home/eguiwow/.virtualenvs/thesis/bin/python3 ~/THESIS/Rittal_Power_Monitoring/rittal_aut_logs.py -p L3 -t $2 -s LTS -o $3/energy$1.log -U $4 -P $5
    ;;
  GL6)
    /home/eguiwow/.virtualenvs/thesis/bin/python3 ~/THESIS/Rittal_Power_Monitoring/rittal_aut_logs.py -p L1 -t $2 -s LTS -o $3/energy$1.log -U $4 -P $5
    ;;
  *)
    echo "Invalid parameter. Please choose from GL2, GL5, or GL6."
    exit 1
    ;;
esac

# GL2 == Phase 2
# GL5 == Phase 3
# GL6 == Phase 1