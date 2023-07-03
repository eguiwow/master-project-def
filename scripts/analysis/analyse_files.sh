#!/bin/bash
# $1 <path/to/results>
/home/eguiwow/.virtualenvs/thesis/bin/python /home/eguiwow/THESIS/master-project-def/scripts/analysis/energy_calculation.py $1/energy
/home/eguiwow/.virtualenvs/thesis/bin/python /home/eguiwow/THESIS/master-project-def/scripts/analysis/cpu_avg.py $1/cpu_mem
echo "CPU and ENERGY analysed".