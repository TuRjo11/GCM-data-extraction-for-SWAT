import pandas as pd
import os
from typing import List

def load_and_process_precip_data(precip_path: str, coords_path: str, output_folder: str, output_filename: str = "processed_precip_data.xlsx") -> None:
    """
    Loads precipitation and coordinates data, processes them, and saves the filtered precipitation data to an Excel file.

    Args:
        precip_path (str): Path to the precipitation data Excel file.
        coords_path (str): Path to the coordinates data Excel file.
        output_folder (str): Directory to save the output file.
        output_filename (str): Name of the output Excel file. Defaults to 'processed_precip_data.xlsx'.

    Returns:
        None
    """
    # Load precipitation data
    precip_data = pd.read_excel(precip_path, header=None)
    
    # Load coordinates data
    coords_data = pd.read_excel(coords_path, header=None)
    
    # Extract longitudes and latitudes from the coordinates data
    longitudes = coords_data.iloc[0, 3:].dropna().values
    latitudes = coords_data.iloc[1, 3:].dropna().values

    # Set the multi-index headers for longitude and latitude from precipitation data
    precip_longitudes = precip_data.iloc[0, 3:].values  # Longitude from the precipitation dataset
    precip_latitudes = precip_data.iloc[1, 3:].values  # Latitude from the precipitation dataset

    # Create a DataFrame for easy matching
    header_df = pd.DataFrame({
        'longitude': precip_longitudes,
        'latitude': precip_latitudes
    })

    # Find columns that match the coordinates data
    matched_columns = header_df[(header_df['longitude'].isin(longitudes)) & (header_df['latitude'].isin(latitudes))]

    # Identify the corresponding column indices
    matched_indices = matched_columns.index + 3  # Adjust to account for the first 3 columns (Year, Month, Day)

    # Extract the relevant precipitation data
    precip_cleaned = precip_data.iloc[2:, matched_indices]

    # Add Year, Month, and Day columns
    precip_cleaned.insert(0, 'Year', precip_data.iloc[2:, 0].values)
    precip_cleaned.insert(1, 'Month', precip_data.iloc[2:, 1].values)
    precip_cleaned.insert(2, 'Day', precip_data.iloc[2:, 2].values)

    # Construct final DataFrame with header rows
    final_data = pd.concat([pd.DataFrame([[None, None, None] + list(matched_columns['longitude'])]),
                            pd.DataFrame([[None, None, None] + list(matched_columns['latitude'])]),
                            precip_cleaned])

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the final DataFrame to an Excel file
    output_path = os.path.join(output_folder, output_filename)
    final_data.to_excel(output_path, index=False, header=False)
    
    print(f"File saved to {output_path}")

# Example usage:
input_excel_path = r"D:\Turjo\data\GCM\__Brhamaputta__\Brahmaputra\BCC-CSM2-MR\ssp585\PrecipData.xlsx"  
coords_path = r"D:\Turjo\data\GCM\to filter the GCM coordinates.xlsx"
output_excel_folder = r"D:\Turjo\data\GCM\__Brhamaputta__\Brahmaputra\BCC-CSM2-MR\ssp585\PRECIP"
base_name = os.path.splitext(os.path.basename(input_excel_path))[0]
output_excel_path = os.path.join(output_excel_folder, f'{base_name}_T_filtered.xlsx')

load_and_process_precip_data(input_excel_path, coords_path, output_excel_folder, output_excel_path)
