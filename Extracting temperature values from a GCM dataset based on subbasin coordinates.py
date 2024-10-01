import os
import pandas as pd
import numpy as np
from typing import Tuple

# Define the date range for temperature extraction
START_YEAR = 2015
END_YEAR = 2040

def find_nearest_indices(latitudes: np.ndarray, longitudes: np.ndarray, target_lat: float, target_lon: float) -> Tuple[int, int]:
    """
    Function to find the nearest latitude and longitude indices.
    
    Args:
        latitudes (np.ndarray): Array of latitude values.
        longitudes (np.ndarray): Array of longitude values.
        target_lat (float): Target latitude to find the nearest value.
        target_lon (float): Target longitude to find the nearest value.
        
    Returns:
        Tuple[int, int]: Indices of the nearest latitude and longitude.
    """
    lat_diff = np.abs(latitudes - target_lat)
    lon_diff = np.abs(longitudes - target_lon)
    nearest_lat_idx = lat_diff.argmin()
    nearest_lon_idx = lon_diff.argmin()
    return nearest_lat_idx, nearest_lon_idx

def extract_temperature_for_subbasins(centroids_subbasins_df: pd.DataFrame, 
                                      tmax_data_df: pd.DataFrame, 
                                      tmin_data_df: pd.DataFrame, 
                                      output_folder: str, 
                                      start_year: int = START_YEAR, 
                                      end_year: int = END_YEAR) -> None:
    """
    Extract TMax and TMin data for subbasins from 1 to 27 and save each subbasin's data to CSV for the given date range.
    
    Args:
        centroids_subbasins_df (pd.DataFrame): DataFrame containing latitude and longitude for subbasins.
        tmax_data_df (pd.DataFrame): DataFrame containing Tmax temperature data.
        tmin_data_df (pd.DataFrame): DataFrame containing Tmin temperature data.
        output_folder (str): Directory to save the output CSV files.
        start_year (int): The start year for filtering the data. Defaults to START_YEAR.
        end_year (int): The end year for filtering the data. Defaults to END_YEAR.
        
    Returns:
        None
    """
    # Extract latitudes and longitudes from the Tmax data
    temp_latitudes = tmax_data_df.iloc[0, 3:].values
    temp_longitudes = pd.to_numeric(tmax_data_df.columns[3:].str.extract(r'(\d+\.\d+)')[0])

    # Filter temperature data for the specified date range
    date_range_filter = (tmax_data_df.iloc[:, 0] >= start_year) & (tmax_data_df.iloc[:, 0] <= end_year)
    tmax_date_range_data = tmax_data_df[date_range_filter]
    tmin_date_range_data = tmin_data_df[date_range_filter]

    # Loop through subbasins 1 to 27
    for subbasin_id in range(1, 28):
        # Get the latitude and longitude for the current subbasin
        subbasin_data = centroids_subbasins_df[centroids_subbasins_df['Subbasin'] == subbasin_id]
        subbasin_lat = round(subbasin_data['Lat'].values[0], 3)
        subbasin_lon = round(subbasin_data['Long_'].values[0], 3)

        # Find the nearest latitude and longitude in the temperature dataset
        nearest_lat_idx, nearest_lon_idx = find_nearest_indices(temp_latitudes, temp_longitudes, subbasin_lat, subbasin_lon)

        # Extract the Tmax and Tmin values for the nearest location in the date range
        tmax_values = tmax_date_range_data.iloc[:, nearest_lon_idx + 3]  # Adjust by 3 to get the correct column
        tmin_values = tmin_date_range_data.iloc[:, nearest_lon_idx + 3]  # Adjust by 3 to get the correct column

        # Extract the Year, Month, and Day columns
        years = tmax_date_range_data.iloc[:, 0]
        months = tmax_date_range_data.iloc[:, 1]
        days = tmax_date_range_data.iloc[:, 2]

        # Combine Year, Month, and Day into a YYYY-MM-DD date format
        dates = pd.to_datetime({'year': years, 'month': months, 'day': days}).dt.strftime('%Y-%m-%d')

        # Create a DataFrame with Date, TMax, and TMin data
        subbasin_temp_data = pd.DataFrame({
            'Date': dates,
            'TMPmax': tmax_values.values,
            'TMPmin': tmin_values.values
        })

        # Define the output filename and save the data to CSV
        output_filename = os.path.join(output_folder, f'stationn_Subbasin_{subbasin_id}_data.csv')
        subbasin_temp_data.to_csv(output_filename, index=False)

    print(f"Temperature data for all subbasins from {start_year} to {end_year} has been saved in {output_folder}")

# Define your file paths
tmax_data_path = "D:/Turjo/data/GCM/__Brhamaputta__/Brahmaputra/BCC-CSM2-MR/ssp585/TEMP/TMaxData_T_filtered.xlsx"
tmin_data_path = "D:/Turjo/data/GCM/__Brhamaputta__/Brahmaputra/BCC-CSM2-MR/ssp585/TEMP/TMinData_T_filtered.xlsx"
centroids_subbasins_path = "D:/Turjo/Model with Amalshid/Data/centroids_subbasins.xlsx"
output_folder = "D:/Turjo/data/GCM/__Brhamaputta__/Brahmaputra/BCC-CSM2-MR/ssp585/TEMP/Year_2020s/CSV"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the datasets
centroids_subbasins_df = pd.read_excel(centroids_subbasins_path)
tmax_data_df = pd.read_excel(tmax_data_path)
tmin_data_df = pd.read_excel(tmin_data_path)

# Run the script to extract temperature data for subbasins 1 to 27 for the specified date range
extract_temperature_for_subbasins(centroids_subbasins_df, tmax_data_df, tmin_data_df, output_folder)
