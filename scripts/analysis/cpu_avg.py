# Given a folder with cpu.csv files generated with the monitor.sh script
# this script returns a processed folder of those files plus another file
# summary_cpu_run.csv which contains a summary of the cpu usage and the temperature
# of the cores on each run
import numpy as np
import os
import sys
import pandas as pd
from scipy.integrate import trapz

def clean_df(folder_path):
	files = os.listdir(folder_path)
	results_path = os.path.join(folder_path, 'processed')
	os.makedirs(results_path, exist_ok=True) # TODO should be created only if it's the good folder
	file_count = 0
	for file_name in files:
		if file_name.startswith("cpu"):
			# Loop over fixed file
			file_count += 1
			temp_cont = 0
			file_path = os.path.abspath(os.path.join(folder_path, file_name))
			df = pd.read_csv(file_path)
			# Change datetime format to match energy's
			df['Datetime Start'] = pd.to_datetime(df['Datetime Start'], format='%Y%m%d-%H:%M:%S')
			df['Datetime End'] = pd.to_datetime(df['Datetime End'], format='%Y%m%d-%H:%M:%S')
			df['Datetime Start'] = df['Datetime Start'].dt.strftime('%d/%m/%Y %H:%M')
			df['Datetime End'] = df['Datetime End'].dt.strftime('%d/%m/%Y %H:%M')

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
	
	print(f"{file_count} CPU files analysed.")
	return results_path

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

			# print(df.describe(include='all'))
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

results_path = clean_df(folder_path) # remove degree symbols + adjust datetime to proper format
output_df = summary_cpu_csv(results_path)
sorted_df = output_df.sort_values(by='Datetime Start')
sorted_df.to_csv(os.path.join(results_path, "cpu_summary_run.csv"), index=False)	

