import os
import paramiko
import subprocess

def get_credentials(host_name):
    # declare credentials
    host = os.getenv(f"{host_name}_H")
    username = os.getenv(f"{host_name}_U")
    password = os.getenv(f"{host_name}_P")

    if not password or not username or not host:
        raise Exception('No environment variables set for credentials')

    return host, username, password

# Open a terminal and execute a command in the local machine
def execute_command(command, wait):
    process = subprocess.Popen(command, shell=True, executable='/bin/bash')
    if wait: 
        process.communicate()
    return process


execute_command("cd ~/experiment-runner/ander/testing-stress && mkdir -p results/energy", True)
_, _, passwordGL5 = get_credentials("GL5")
retrieve_data_energy_command = f'sshpass -p "{passwordGL5}" scp -r /home/eguiwow/master-project-def/scripts/* ander@145.108.225.16:/home/ander/scripts/' #TODO get path via method
execute_command(retrieve_data_energy_command, False)
