import os
import csv
import sys
import subprocess
import datetime
from pathlib import Path

# Arguments:
# $1 <GLX>
# $2 <path/to/results>
# $3 <workload>
# $4 <VUs>

def txt_2_table(file_in):
    data = []
    try:
        with open(file_in, 'r') as f_in:
            for line in f_in:
                fields = line.split()
                data.append(fields)
    except FileNotFoundError:
        print(f"'{file_in}' not present. Aborting")
    return data

def table_2_csv(table, filename, path_results):
    if len(table) != 0:
        os.chdir(path_results) # cd to the folder in which the results are
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time", "Index", "Watts", "Volts", "Amps"])
            writer.writerows(table)
    else:
        print("Data was not provided. Output energy file not generated.")


timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
server_name = sys.argv[1]
path_results = Path(sys.argv[2])
workload = None; VUs = None; run_nr = None
try:
    workload = sys.argv[3]
except IndexError as e:
    print(f"Workload not provided to output2scv.py")
try:
    VUs = sys.argv[4]
except IndexError as e:
    print(f"VUs not provided to output2scv.py")   

try:
    run_nr = sys.argv[5]
except IndexError as e:
    print(f"run_nr not provided to output2scv.py")

if run_nr is not None:
    new_filename = run_nr + 'energy_' + server_name + '-' + workload + '-' + VUs + '_' + timestr + '.csv'
else:
    if workload is not None and VUs is None:
        new_filename = 'energy_' + server_name + '-' + workload + '_' + timestr + '.csv'
    elif workload is not None and VUs is not None:
        new_filename = 'energy_' + server_name + '-' + workload + '-' + VUs + '_' + timestr + '.csv'
    else:
        new_filename = 'energy_' + server_name + '_' + timestr + '.csv'
table = txt_2_table('energy' + server_name + '.log')
table_2_csv(table, new_filename, path_results)
        