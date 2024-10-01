import pandas as pd
import os

# Directory containing the input CSV files
input_directory = r"D:\Turjo\data\GCM\__Brhamaputta__\Brahmaputra\BCC-CSM2-MR\ssp585\TEMP\Year_2020s\CSV"
#r"D:\Turjo\data\Weather data\NASA POWER TEMP(max,min)\Amalshid Model\Combined Subbasin CSVs"

# Initialize an empty list to store dataframes
data_frames = []

# Iterate through each file in the directory
for filename in os.listdir(input_directory):
    # Check if the file is a CSV
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(input_directory, filename)
        
        # Extract the station name from the file name (without extension)
        station_id = filename.split('_')[2]
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Add a column for the station name
        df['Station'] = station_id
        
        # Append the dataframe to the list
        data_frames.append(df)

# Concatenate all the dataframes into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Reorder the columns to match the desired output

#combined_df = combined_df[['Date', 'Station', 'PCP']] #when extracting precipitation
combined_df = combined_df[['Date', 'Station', 'TMPmax', 'TMPmin']] #when extracting temperature

# Save the combined dataframe to a new CSV file
output_file = r"D:\Turjo\data\GCM\__Brhamaputta__\Brahmaputra\swat-weatherdatabase-v01803\ExInputs\tmp.csv"
combined_df.to_csv(output_file, index=False)


