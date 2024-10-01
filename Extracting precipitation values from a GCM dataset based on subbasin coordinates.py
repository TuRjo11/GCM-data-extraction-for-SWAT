import os
import pandas as pd
import numpy as np
import warnings
from typing import Tuple

# Suppress specific warnings from openpyxl
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Define the date range for precipitation extraction (Change these variables as needed)
START_YEAR = 2015
END_YEAR = 2040

def find_nearest_indices(latitudes: np.ndarray, longitudes: np.ndarray, target_lat: float, target_lon: float) -> Tuple[int, int]:
    """
    Function to find the nearest latitude and longitude indices.

    Args:
        latitudes (np.ndarray): Array of latitude values.
        longitudes (np.ndarray): Array of longitude values.
        target_lat (float): Target latitude to match.
        target_lon (float): Target longitude to match.

    Returns:
        Tuple[int, int]: Indices of the nearest latitude and longitude.
    """
    lat_diff = np.abs(latitudes - target_lat)
    lon_diff = np.abs(longitudes - target_lon)
    nearest_lat_idx = lat_diff.argmin()
    nearest_lon_idx = lon_diff.argmin()
    return nearest_lat_idx, nearest_lon_idx

def extract_precipitation_for_subbasins(centroids_subbasins_df: pd.DataFrame, 
                                        precip_data_df: pd.DataFrame, 
                                        output_folder: str, 
                                        start_year: int = START_YEAR, 
                                        end_year: int = END_YEAR) -> None:
    """
    Extract precipitation data for subbasins from 1 to 27 and save each subbasin's data to CSV files.

    Args:
        centroids_subbasins_df (pd.DataFrame): DataFrame containing subbasin centroids (latitude and longitude).
        precip_data_df (pd.DataFrame): DataFrame containing precipitation data.
        output_folder (str): Directory to save the output CSV files.
        start_year (int, optional): Start year for data extraction. Defaults to START_YEAR.
        end_year (int, optional): End year for data extraction. Defaults to END_YEAR.

    Returns:
        None
    """
    # Extract latitudes and longitudes from precipitation data
    precip_latitudes = precip_data_df.iloc[0, 3:].values
    precip_longitudes = pd.to_numeric(precip_data_df.columns[3:].str.extract(r'(\d+\.\d+)')[0])

    # Filter precipitation data for the specified date range
    date_range_filter = (precip_data_df.iloc[:, 0] >= start_year) & (precip_data_df.iloc[:, 0] <= end_year)
    date_range_data = precip_data_df[date_range_filter]

    # Iterate through each subbasin (1 to 27)
    for subbasin_id in range(1, 28):
        # Get latitude and longitude for the current subbasin
        subbasin_data = centroids_subbasins_df[centroids_subbasins_df['Subbasin'] == subbasin_id]
        subbasin_lat = round(subbasin_data['Lat'].values[0], 3)
        subbasin_lon = round(subbasin_data['Long_'].values[0], 3)

        # Find the nearest indices for latitude and longitude
        nearest_lat_idx, nearest_lon_idx = find_nearest_indices(precip_latitudes, precip_longitudes, subbasin_lat, subbasin_lon)

        # Extract precipitation data for the nearest location over the specified date range
        precip_date_range_data = date_range_data.iloc[:, nearest_lon_idx + 3]  # Offset by 3 to get the correct column

        # Extract the year, month, and day columns
        years = date_range_data.iloc[:, 0]
        months = date_range_data.iloc[:, 1]
        days = date_range_data.iloc[:, 2]

        # Combine year, month, and day into a YYYY-MM-DD format
        dates = pd.to_datetime({'year': years, 'month': months, 'day': days}).dt.strftime('%Y-%m-%d')

        # Create a DataFrame with date and precipitation data
        subbasin_precip_data = pd.DataFrame({
            'Date': dates,
            'PCP': precip_date_range_data.values
        })

        # Construct the output filename and save the data to CSV
        output_filename = os.path.join(output_folder, f'stationn_Subbasin_{subbasin_id}_data.csv')
        subbasin_precip_data.to_csv(output_filename, index=False)

    print(f"Precipitation data for all subbasins from {start_year} to {end_year} has been saved in {output_folder}")

# Define file paths
centroids_subbasins_path = "D:/Turjo/Model with Amalshid/Data/centroids_subbasins.xlsx"
precip_data_filtered_path = "D:/Turjo/data/GCM/__Brhamaputta__/Brahmaputra/BCC-CSM2-MR/ssp585/PRECIP/PrecipData_T_filtered.xlsx"
output_folder = "D:/Turjo/data/GCM/__Brhamaputta__/Brahmaputra/BCC-CSM2-MR/ssp585/PRECIP/Year_2020s/CSV"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the datasets
centroids_subbasins_df = pd.read_excel(centroids_subbasins_path)
precip_data_filtered_df = pd.read_excel(precip_data_filtered_path)

# Run the script to extract precipitation data for subbasins 1 to 27 for the specified date range
extract_precipitation_for_subbasins(centroids_subbasins_df, precip_data_filtered_df, output_folder)
