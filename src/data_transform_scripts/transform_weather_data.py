"""
This module transforms weather data before sending data to the feature store
"""
import os
import sys

import pandas as pd

# Add the parent directory to the Python path to import WeatherData class
CURRENT_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.normpath(os.path.dirname(CURRENT_DIR))
sys.path.append(parent_dir)

from classes.weather_data_transform import WeatherDataTransform
from classes.utils import Utils

def main(current_dir: str) -> None:
    """
    Transform weather data for individual locations and generate a file containing the
    combined data

    Args:
        * current_dir (str): file's current directory
    """
    config_dir = os.path.join(current_dir, os.path.normpath("../../config"))
    config = Utils.read_json_files(config_dir=config_dir)
    data_dir = os.path.join(
        current_dir,
        os.path.normpath(f"../../{config['DATA_DIR']}/{config['WEATHER_DATA_DIR']}")
    )
    # Extract filenames from data directory
    sorted_filenames = sorted(
        [file.split(".")[0] for file in os.listdir(os.path.normpath(data_dir))
         if ".parquet" in file and "transformed" not in file]
    )
    # Transform data from the individual locations and save it to a new parquet file
    for file in sorted_filenames:
        # Define file paths to load and save
        file_path = os.path.join(os.path.normpath(data_dir), f"{file}.parquet")
        save_path = os.path.join(os.path.normpath(data_dir), f"{file}_transformed.parquet")
        # Transform data
        df = WeatherDataTransform.transform_individual_locations(
            file_path=file_path
        )
        # Save transformed data
        df.to_parquet(save_path)
    # Extract filenames from transformed files
    sorted_transformed_filenames = sorted(
        [file for file in os.listdir(os.path.normpath(data_dir))
         if ".parquet" in file and "transformed" in file]
    )
    # Sort the files before loading them onto a dictionary
    sorted_transformed_file_dirs = [os.path.join(
        os.path.normpath(data_dir), file
    ) for file in sorted_transformed_filenames]
    # Create a dict containing one dataframe per file
    df_dict = {
        "crossby_df": pd.read_parquet(sorted_transformed_file_dirs[0]),
        "bingley_df": pd.read_parquet(sorted_transformed_file_dirs[1]),
        "rostherne_df": pd.read_parquet(sorted_transformed_file_dirs[2]),
        "watnall_df": pd.read_parquet(sorted_transformed_file_dirs[3]),
        "coleshill_df": pd.read_parquet(sorted_transformed_file_dirs[4]),
        "heathrow_df": pd.read_parquet(sorted_transformed_file_dirs[5]),
        "thorney_df": pd.read_parquet(sorted_transformed_file_dirs[6])
    }
    # Use transformed data to generate a new dataframe containing the combined data and
    # save it to a new parquet file
    df_combined = WeatherDataTransform.generate_all_information_df(
        df_dict
    )
    save_path = os.path.join(os.path.normpath(data_dir), "weather_data_combined.parquet")
    df_combined.to_parquet(save_path)



if __name__ == "__main__":
    CURRENT_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    main(current_dir=CURRENT_DIR)