"""
This module fetches weather data from the MetOffice API
"""

import os
import sys

# Add the parent directory to the Python path to import WeatherData class
CURRENT_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.normpath(os.path.dirname(CURRENT_DIR))
sys.path.append(parent_dir)

from classes.weather_data_api import WeatherData
from classes.utils import Utils


def main(current_dir: str) -> None:
    """
    This function fetches data from the Met Office API and stores it in the data
    directory

    Args:
        * current_dir (str): File's current directory
    """
    config_dir = os.path.join(current_dir, os.path.normpath("../../config"))
    config = Utils.read_json_files(config_dir=config_dir)
    data_dir = os.path.join(
        current_dir,
        os.path.normpath(f"../../{config['DATA_DIR']}/{config['WEATHER_DATA_DIR']}")
    )

    interest_locations = [
        "3772",  # Heathrow
        "3535",  # Coleshill, very close to Birmingham
        "3316",  # Crosby, very close to Liverpool
        "3351",  # closest to Manchester
        "3344",  # Bingley Samos, very close to Leeds
        "3872",  # Thorney Island, closest to Southampton and Portsmouth
        "3354",  # Watnall, very close to Nottingham
    ]

    weather_data = WeatherData(data_dir=data_dir, response_format="json")

    for location in interest_locations:
        weather_data.gather_and_merge_data(location_id=location, mode="past_data")


if __name__ == "__main__":
    main(current_dir=CURRENT_DIR)
