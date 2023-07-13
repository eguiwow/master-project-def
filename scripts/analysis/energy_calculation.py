# Given a folder with energy.csv files generated with the Rittal system
# This script returns a processed folder of those files plus another file
# total_energy_per_run.csv which contains a summary of the total energy of each run
import numpy as np
import os
import sys
import pandas as pd
from datetime import timedelta
from scipy.integrate import trapz

def clean_df_and_timestamp(folder_path):
	file_count = 0
	folder_name = os.path.basename(folder_path)
	if folder_name == 'energy':
		results_path = os.path.join(folder_path, 'processed')
		# Check if the 'processed' folder exists
		if os.path.exists(results_path) and os.path.isdir(results_path):
			print("Program aborted. 'processed' folder already exists.")
			return 0
		else:
			files = os.listdir(folder_path)
			os.makedirs(results_path, exist_ok=True)
			for file_name in files:
				if file_name.startswith("energy"):
					# Loop over fixed files
					file_count += 1
					file_path = os.path.abspath(os.path.join(folder_path, file_name))
					df = pd.read_csv(file_path)
					# Remove unuseful columns
					df = df.drop('Phase', axis=1)
					df = df.drop('Index', axis=1)
					df = df.drop('Volts', axis=1)
					df = df.drop('Amps', axis=1)
					df = df.drop('noidea', axis=1)
					df.dropna(subset=['Watts'], inplace=True) # remove rows with NaN values in the 'Watts' column (6)
					df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time']) # create a combined Datetime column
					df['Timestamp'] = (df['Datetime'] - df['Datetime'].iloc[0]).dt.total_seconds() # Span of time between rows

					# write the updated DataFrame to a new .csv file
					output_file_path = os.path.join(results_path, file_name)
					df.to_csv(output_file_path, index=False)
	else:
		print("Provided folder is not 'energy' folder.")
		return 0
	print(f"{file_count} CPU files analysed.")
	return results_path


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


def filter_short_runs(folder_path):
	files = os.listdir(folder_path)
	removed_files = 0
	for file_name in files:
		if file_name.startswith("energy"):
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			df = pd.read_csv(file_path)    
			# get start and end
			df['Datetime'] = pd.to_datetime(df['Datetime'])
			datetime_start = df['Datetime'].iloc[0]
			datetime_end = df['Datetime'].iloc[-1]
			# Calculate the time difference between 'Datetime Start' and 'Datetime End'
			time_elapsed = datetime_end - datetime_start
			# Filter out rows where the time elapsed is less than 15 minutes
			if time_elapsed <= timedelta(minutes=14):
				# Add SHORT so we don't analyze them further
				results_path = os.path.join(folder_path, "SHORT_" + file_name)
				df.to_csv(results_path, index=False)
				os.remove(os.path.join(folder_path, file_name))
				removed_files += 1
				print(f"File too short: {file_name}, Run time: {time_elapsed}")
	print(f"{removed_files} shorter than 15 minutes.")


def remove_outliers(folder_path, verbose=False):
	files = os.listdir(folder_path)
	file_count = 0
	for file_name in files:
		if file_name.startswith("energy"):
			# Loop over fixed files
			file_count += 1
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			df = pd.read_csv(file_path)

			# Calculate statistical measures
			mean = df['Watts'].mean()
			std = df['Watts'].std()
			if verbose: print(f"[Before]\nMean: {mean}\nStd: {std}")
			threshold = 3 * std # Define threshold for outliers
			outliers = df[(df['Watts'] < mean - threshold) | (df['Watts'] > mean + threshold)]

			# Q1 = df['Watts'].quantile(0.25)
			# Q3 = df['Watts'].quantile(0.75)
			# IQR = Q3 - Q1			
			# threshold = 1.5 * IQR # Define threshold for outliers
			# # Identify outlier rows
			# outliers = df[(df['Watts'] < Q1 - threshold) | (df['Watts'] > Q3 + threshold)]
			print(f"Num of outliers deleted: {len(outliers)}")
			# Remove outlier rows
			df = df.drop(outliers.index)
			mean = df['Watts'].mean()
			std = df['Watts'].std()
			if verbose: print(f"[After]\nMean: {mean}\nStd: {std}")
			results_path = os.path.join(folder_path, file_path)

			# Save the processed DataFrame to a new CSV file
			df.to_csv(results_path, index=False)


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
	filter_short_runs(results_path)
	remove_outliers(results_path, verbose=False)
	output_df = calc_energy_from_csv(results_path)
	sorted_df = output_df.sort_values(by='Datetime Start')
	parent_folder = os.path.dirname(folder_path)
	sorted_df.to_csv(os.path.join(parent_folder, "total_energy_per_run.csv"), index=False)	
