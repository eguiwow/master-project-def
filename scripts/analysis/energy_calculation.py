# Given a folder with energy.csv files generated with the Rittal system
# This script returns a processed folder of those files plus another file
# total_energy_per_run.csv which contains a summary of the total energy of each run
import numpy as np
import os
import sys
import pandas as pd
from scipy.integrate import trapz

def fix_headers_energy_files(folder_path):
	files = os.listdir(folder_path)
	energy_files = False
	for file_name in files:
		if file_name.startswith("energy"):
			# DEALING WITH THE MISSING HEADERS
			energy_files = True
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			# Define the new header row
			new_header = ['Date', 'Time', 'Index', 'Phase', 'Volts', 'Amps', 'Watts', 'noidea']  # Specify the new header names

			# Read the original CSV file
			with open(file_path, 'r') as file:
				lines = file.readlines()[1:] # skip the first row

			# Add the new header row at the beginning
			lines.insert(0, ','.join(new_header) + '\n')

			# Write the modified lines to a new file
			with open(file_path, 'w') as file:
				file.writelines(lines)
	if energy_files:
		print("Header of energy files modified")
		return True
	else:
		print("No energy files in the folder. Aborting.")
		return False

def clean_df_and_timestamp(folder_path):
	files = os.listdir(folder_path)
	results_path = os.path.join(folder_path, 'processed')
	os.makedirs(results_path, exist_ok=True)
	for file_name in files:
		if file_name.startswith("energy"):
			# Loop over fixed files
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			df = pd.read_csv(file_path)
			df.dropna(subset=['Watts'], inplace=True) # remove rows with NaN values in the 'Watts' column (6)
			df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
			df['Timestamp'] = (df['Datetime'] - df['Datetime'].iloc[0]).dt.total_seconds()
			
			output_file_path = os.path.join(results_path, file_name)
			df.to_csv(output_file_path, index=False)
	return results_path

def get_energy_from_df(df):
	timestamp = np.array(df['Timestamp'])
	watts = np.array(df['Watts'], dtype=float)
	return trapz(watts, timestamp)

def get_attributes_from_title(title: str):
	substrings = title.split('_')[1].split('-')
	GL = substrings[0]
	workload = substrings[1]
	VUs = ""
	try:
		VUs = substrings[2]
	except:
		# print("VUs was not provided in the file's name")
		pass

	return GL, workload, VUs

def calc_energy_from_csv(folder_path):
	files = os.listdir(folder_path)
	data = []
	file_count = 0
	for file_name in files:
		if file_name.startswith("energy"):
			# Loop over fixed files
			file_count += 1
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			df = pd.read_csv(file_path)
			energy = get_energy_from_df(df)
			datetime_start = df['Datetime'].iloc[0]
			datetime_end = df['Datetime'].iloc[-1]
			GL, workload, VUs = get_attributes_from_title(file_name)
			data.append([datetime_start, datetime_end, GL, workload, VUs, energy])

	print(f"{file_count} Energy files analysed.")
	# Save the DataFrame to a new .csv file
	return pd.DataFrame(data, columns=['Datetime Start', 'Datetime End', 'GL', 'Workload (%)', 'VUs (#)', 'Energy (J)'])


# MAIN LOGIC

if len(sys.argv) < 2: # Check if the folder path argument is provided
    print("Please provide the folder path as a command-line argument.")
    sys.exit(1)

folder_path = sys.argv[1]

if not os.path.exists(folder_path): # Check if the folder exists
    print("The specified folder does not exist.")
    sys.exit(1)

# Clean and process data
if fix_headers_energy_files(folder_path):
	results_path = clean_df_and_timestamp(folder_path)
	output_df = calc_energy_from_csv(results_path)
	sorted_df = output_df.sort_values(by='Datetime Start')
	sorted_df.to_csv(os.path.join(results_path, "total_energy_per_run.csv"), index=False)	
