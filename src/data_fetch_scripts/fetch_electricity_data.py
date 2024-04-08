"""
This module fetches weather data from the NationalGrid API
"""
import os
import sys

# Add the parent directory to the Python path to import WeatherData class
CURRENT_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.normpath(os.path.dirname(CURRENT_DIR))
sys.path.append(parent_dir)

from classes.electricity_data_api import ElectricityData
from classes.utils import Utils


def main(current_dir: str) -> None:
    """
    This function fetches data from the National Grid API and stores it in the data
    directory

    Args:
        * current_dir (str): File's current directory
    """
    config_dir = os.path.join(current_dir, os.path.normpath("../../config"))
    config = Utils.read_json_files(config_dir=config_dir)
    data_dir = os.path.join(
        current_dir,
        os.path.normpath(f"../../{config['DATA_DIR']}/{config['ELECTRICITY_DATA_DIR']}")
    )

    electricity_data = ElectricityData(data_dir=data_dir)
    electricity_data.gather_historic_data()

if __name__ == "__main__":
    CURRENT_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    main(current_dir=CURRENT_DIR)
