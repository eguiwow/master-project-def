import pandas as pd

# Read the CSV file into a dataframe
df = pd.read_csv('cpu_summary_run.csv')

# Convert the columns to datetime format
df['Datetime Start'] = pd.to_datetime(df['Datetime Start'], format='%Y%m%d-%H:%M:%S')
df['Datetime End'] = pd.to_datetime(df['Datetime End'], format='%Y%m%d-%H:%M:%S')

# Convert the columns to the desired format
df['Datetime Start'] = df['Datetime Start'].dt.strftime('%d/%m/%Y %H:%M')
df['Datetime End'] = df['Datetime End'].dt.strftime('%d/%m/%Y %H:%M')

# Store the new dataset with the same name
#df.to_csv('cpu_summary_run.csv')
df.to_csv('cpu_summary_run_2.csv')

