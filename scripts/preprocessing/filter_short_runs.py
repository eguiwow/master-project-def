import pandas as pd
from datetime import datetime, timedelta
import glob

# Get a list of all CSV files in the current directory
csv_files = glob.glob("*.csv")

# Loop over each CSV file
for file in csv_files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file)    
    # Convert 'Datetime Start' and 'Datetime End' columns to datetime objects
    df['Datetime Start'] = pd.to_datetime(df['Datetime Start'])
    df['Datetime End'] = pd.to_datetime(df['Datetime End'])
    # Calculate the time difference between 'Datetime Start' and 'Datetime End'
    df['Time Elapsed'] = df['Datetime End'] - df['Datetime Start']
    # Filter out rows where the time elapsed is less than 15 minutes
    df = df[df['Time Elapsed'] >= timedelta(minutes=14)]
    # Remove the 'Time Elapsed' column
    df = df.drop('Time Elapsed', axis=1)
    # Save the modified DataFrame back to a CSV file
    df.to_csv(f"FILTERED_{file}", index=False)
