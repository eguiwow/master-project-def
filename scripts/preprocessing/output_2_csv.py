import os
import csv
import sys
import subprocess
import datetime

def txt_2_table(file_in):
    data = []
    with open(file_in, 'r') as f_in:
        for line in f_in:
            fields = line.split()
            data.append(fields)
    return data

def table_2_csv(table, filename):
    os.chdir('/home/ander/results')
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Time", "Index", "Watts", "Volts", "Amps"])
        writer.writerows(table)

server_name = sys.argv[1]

timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
new_filename = 'energy_' + server_name + '_' + timestr + '.csv'
os.chdir('/home/ander/results')
table = txt_2_table('energy' + server_name + '.log')
table_2_csv(table, new_filename)

#cmd = 'scp ander@145.108.225.16:~/results/' +new_filename+ '/home/ander/thesis/results/'+new_filename
#retcode = subprocess.call(cmd,shell=True)