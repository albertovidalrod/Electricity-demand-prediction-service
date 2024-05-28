"""
This module transforms electricity demand data before sending data to the feature store
"""
import os
import sys

# Add the parent directory to the Python path to import WeatherData class
CURRENT_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.normpath(os.path.dirname(CURRENT_DIR))
sys.path.append(parent_dir)

from classes.electricity_data_transform import ElectricityDataTransform
from classes.utils import Utils

def main(current_dir: str) -> None:
    """
    Transform electricity demand data and generate a file containing the transformed data

    Args:
        * current_dir (str): file's current directory
    """
    config_dir = os.path.join(current_dir, os.path.normpath("../../config"))
    config = Utils.read_json_files(config_dir=config_dir)
    data_dir = os.path.join(
        current_dir,
        os.path.normpath(f"../../{config['DATA_DIR']}/{config['ELECTRICITY_DATA_DIR']}")
    )

    df = ElectricityDataTransform.transform_data(
        os.path.join(data_dir, "historic_demand_year_2024.parquet")
    )

    df.to_parquet(os.path.join(data_dir, "electricity_data_transformed.parquet"))




if __name__ == "__main__":
    CURRENT_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    main(current_dir=CURRENT_DIR)