import pandas as pd
import sys
import os
import matplotlib.pyplot as plt


def combine_files(folder_path, output_file_path):
    # Read the 'energy' and 'cpu' files into separate DataFrames
    energy_file_path = 'total_energy_per_run.csv'
    cpu_file_path = 'cpu_summary_run.csv'

    energy_df = pd.read_csv(os.path.abspath(os.path.join(folder_path, energy_file_path)))
    cpu_df = pd.read_csv(os.path.abspath(os.path.join(folder_path, cpu_file_path)))

    # Sort both DataFrames based on 'DatetimeStart' column
    energy_df.sort_values('Datetime Start', inplace=True)
    cpu_df.sort_values('Datetime Start', inplace=True)

    # Create a new column in 'energy' DataFrame to store 'cpu' values
    cpu_df['Energy (J)'] = None

    # Iterate over 'energy' DataFrame rows
    for idx, cpu_row in cpu_df.iterrows():
        cpu_start = cpu_row['Datetime Start']
        cpu_end = cpu_row['Datetime End']

        # Find the corresponding 'cpu' row where 'DatetimeStart' falls within the range
        energy_row = energy_df[(energy_df['Datetime Start'] <= cpu_start) & (energy_df['Datetime End'] >= cpu_start)]

        if not energy_row.empty:
            energy_value = energy_row['Energy (J)'].iloc[0]
            cpu_df.at[idx, 'Energy (J)'] = energy_value

    # Save the combined DataFrame to a new CSV file
    cpu_df.to_csv(os.path.abspath(os.path.join(folder_path, output_file_path)), index=False)
    print("Combined file saved successfully.")
    return cpu_df

def create_plot(combined_df):
    # Extract the relevant columns
    cpu_values = combined_df['%USEDavg']
    energy_values = combined_df['Energy (J)']

    # Create the plot
    plt.scatter(cpu_values, energy_values)
    plt.xlabel('%CPU load')
    plt.ylabel('Energy (J)')
    plt.title('Energy vs. CPU Load') # TODO denote which GL and so on

    # Set the x-axis and y-axis limits
    plt.xlim(0, 100)
    plt.ylim(0, 200000)

    # Show the plot
    plt.show()

# MAIN LOGIC
if len(sys.argv) < 2: # Check if the folder path argument is provided
	print("Please provide the folder path as a command-line argument.")
	sys.exit(1)

folder_path = sys.argv[1]

if not os.path.exists(folder_path): # Check if the folder exists
	print("The specified folder does not exist.")
	sys.exit(1)

# MATCH CPU/ENERGY and create summary of experiment
output_file_path = f'experiment_analysis_{os.path.basename(folder_path)}.csv'
combined_data_file = combine_files(folder_path,  output_file_path)

# create_plot(combined_data_file)
