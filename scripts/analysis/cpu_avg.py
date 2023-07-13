# Given a folder with cpu.csv files generated with the monitor.sh script
# this script returns a processed folder of those files plus another file
# summary_cpu_run.csv which contains a summary of the cpu usage and the temperature
# of the cores on each run
import numpy as np
import os
import sys
import pandas as pd
import datetime
from scipy.integrate import trapz

def clean_df(folder_path):
	file_count = 0
	folder_name = os.path.basename(folder_path)
	if folder_name == 'cpu_mem':
		results_path = os.path.join(folder_path, 'processed')
		# Check if the 'processed' folder exists
		if os.path.exists(results_path) and os.path.isdir(results_path):
			print("Program aborted. 'processed' folder already exists.")
			return 0
		else:
			files = os.listdir(folder_path)
			os.makedirs(results_path, exist_ok=True)
			for file_name in files:
				if file_name.startswith("cpu"):
					# Loop over fixed file
					file_count += 1
					temp_cont = 0
					file_path = os.path.abspath(os.path.join(folder_path, file_name))
					df = pd.read_csv(file_path)
					# Timestamp to DateTime object
					df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y%m%d-%H:%M:%S') + datetime.timedelta(hours=2)

					# extract the temperature column as a series
					for column in df.columns:
						if str(column).startswith('temp'):
							temp_cont += 1
							temp_column = df[column]
							temp_values = temp_column.str.extract(r'(\d+\.\d+)')    # extract the numerical value using a regular expression
							temp_values = temp_values[0].astype(float)              # convert the extracted values to float
							df['cpu'+str(temp_cont)+'_temp'] = temp_values          # add the extracted temperature values as a new column to the DataFrame
							df = df.drop(column, axis=1)         					# drop the original temperature columns

					# write the updated DataFrame to a new .csv file
					output_file_path = os.path.join(results_path, file_name)
					df.to_csv(output_file_path, index=False)
	else:
		print("Provided folder is not 'cpu_mem' folder.")
		return 0
	print(f"{file_count} CPU files analysed.")
	return results_path

def filter_short_runs(folder_path):
	files = os.listdir(folder_path)
	removed_files = 0
	for file_name in files:
		if file_name.startswith("cpu"):
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			df = pd.read_csv(file_path)    
			# get start and end
			datetime_start = pd.to_datetime(df['Timestamp'].iloc[0])
			datetime_end = pd.to_datetime(df['Timestamp'].iloc[-1])
			# Calculate the time difference between 'Datetime Start' and 'Datetime End'
			time_elapsed = datetime_end - datetime_start
			# Filter out rows where the time elapsed is less than 15 minutes
			if time_elapsed <= datetime.timedelta(minutes=14):
				# Add SHORT so we don't analyze them further
				results_path = os.path.join(folder_path, "SHORT_" + file_name)
				df.to_csv(results_path, index=False)
				os.remove(os.path.join(folder_path, file_name))
				removed_files += 1
				print(f"File too short: {file_name}, Run time: {time_elapsed}")
	print(f"{removed_files} shorter than 15 minutes.")

def shorten_runs(folder_path, minutes):
	files = os.listdir(folder_path)
	for file_name in files:
		if file_name.startswith("cpu"):
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			df = pd.read_csv(file_path)    
			# Convert 'Datetime Start' and 'Datetime End' columns to datetime objects
			df['Timestamp'] = pd.to_datetime(df['Timestamp'])
			datetime_start = df['Timestamp'].iloc[0]
			cutoff_time = datetime_start + datetime.timedelta(minutes=minutes)
			filtered_df = df[df['Timestamp'] <= cutoff_time]
			# print(f"{datetime_start} : {cutoff_time}")
			# print(df[df['Timestamp'] <= cutoff_time])
			results_path = os.path.join(folder_path, file_name)
			os.remove(results_path)
			filtered_df.to_csv(results_path, index=False)

def remove_outliers(folder_path, verbose=False):
	files = os.listdir(folder_path)
	file_count = 0
	for file_name in files:
		if file_name.startswith("cpu"):
			# Loop over fixed files
			file_count += 1
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			df = pd.read_csv(file_path)

			# Calculate statistical measures
			mean = df['%usr'].mean()
			std = df['%usr'].std()
			if verbose: print(f"[Before]\nMean: {mean}\nStd: {std}")
			threshold = 3 * std # Define threshold for outliers
			outliers = df[(df['%usr'] < mean - threshold) | (df['%usr'] > mean + threshold)]
			# Q1 = df['%usr'].quantile(0.25)
			# Q3 = df['%usr'].quantile(0.75)
			# IQR = Q3 - Q1			
			# threshold = 1.5 * IQR # Define threshold for outliers
			# Identify outlier rows
			# outliers = df[(df['%usr'] < Q1 - threshold) | (df['%usr'] > Q3 + threshold)]
			print(f"Num of outliers deleted: {len(outliers)}")
			# Remove outlier rows
			df = df.drop(outliers.index)	
			mean = df['%usr'].mean()
			std = df['%usr'].std()
			if verbose: print(f"[After]\nMean: {mean}\nStd: {std}")
			results_path = os.path.join(folder_path, file_path)

			# Save the processed DataFrame to a new CSV file
			df.to_csv(results_path, index=False)

def get_avg_temp(df):
	temp_cont = 0
	temp_tot = 0
	for column in df.columns:
		if str(column).startswith('cpu'):
			temp_cont += 1
			temp_tot += df[column].mean()
	return temp_tot/temp_cont

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

def summary_cpu_csv(folder_path):
	files = os.listdir(folder_path)
	data = []
	for file_name in files:
		if file_name.startswith("cpu"):
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			df = pd.read_csv(file_path)
			# get values
			avgUSR = df['%usr'].mean()
			avgSYS = df['%sys'].mean()
			avgUSED = 100 - df['%Idle'].mean()
			avgTEMP = get_avg_temp(df)
			datetime_start = df['Timestamp'].iloc[0]
			datetime_end = df['Timestamp'].iloc[-1]
			GL, workload, VUs = get_attributes_from_title(file_name)
			data.append([datetime_start, datetime_end, GL, workload, VUs, avgUSED, avgUSR, avgSYS, avgTEMP])

			# Save the DataFrame to a new .csv file
	return pd.DataFrame(data, columns=['Datetime Start', 'Datetime End', 'GL', 'Workload (%)', 'VUs (#)', '%USEDavg', '%USERavg', '%SYSavg', 'tempCPUavg'])


# MAIN LOGIC
if len(sys.argv) < 2: # Check if the folder path argument is provided
	print("Please provide the folder path as a command-line argument.")
	sys.exit(1)

folder_path = sys.argv[1]

if not os.path.exists(folder_path): # Check if the folder exists
	print("The specified folder does not exist.")
	sys.exit(1)

# Clean and process data
results_path = clean_df(folder_path) # remove degree symbols + adjust datetime to proper format in new folder 'processed'
if results_path != 0:
	filter_short_runs(results_path)
	remove_outliers(results_path, verbose=False)
	shorten_runs(results_path, 15) # limit the time of the run to the first 15'
	output_df = summary_cpu_csv(results_path)
	sorted_df = output_df.sort_values(by='Datetime Start')
	parent_folder = os.path.dirname(folder_path)
	sorted_df.to_csv(os.path.join(parent_folder, "cpu_summary_run.csv"), index=False)
