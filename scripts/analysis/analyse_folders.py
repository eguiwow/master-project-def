import subprocess
import sys
import os

def analyse_folders(folder_path):
    scripts_path = r"C:\MT\THESIS\master-project-def\scripts\analysis"
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            folder_cpu = os.path.join(item_path, "cpu_mem")
            folder_energy = os.path.join(item_path, "energy")
            subprocess.run(['python', scripts_path + r'\cpu_avg.py', folder_cpu])
            subprocess.run(['python', scripts_path + r'\energy_calculation.py', folder_energy])
            subprocess.run(['python', scripts_path + r'\match_analysis.py', item_path])


# MAIN LOGIC
if len(sys.argv) < 2: # Check if the folder path argument is provided
	print("Please provide the folder path as a command-line argument.")
	sys.exit(1)

folder_path = sys.argv[1]

if not os.path.exists(folder_path): # Check if the folder exists
	print("The specified folder does not exist.")
	sys.exit(1)
        

analyse_folders(folder_path)