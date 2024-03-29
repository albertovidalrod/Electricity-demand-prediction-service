"""
This module contains the WeatherData class, which fetches data using the Met Office API
"""

import os
from typing import Tuple, Literal
import requests
from dotenv import load_dotenv

import pandas as pd


class WeatherData:
    """
    This class includes several function to fetch data from the Met Office API and
    save to the specified directory

    Methods:
        * gather_location_data
        * gather_and_merge_data
    """

    def __init__(self, response_format: str, data_dir: str = None) -> None:
        """
        Initialise the WeatherData class.

        Args:
            * response_format (str): Format of the response from the API.
            * data_dir (str): Directory where data will be stored.
                Default to None
        """
        self.data_dir = data_dir
        self.response_format = response_format
        self.url_basic = "http://datapoint.metoffice.gov.uk/public/data"

        # Load environment variables
        load_dotenv()
        self.met_office_api_key = os.getenv("MET_OFFICE_API_KEY")

    def gather_location_data(
        self, location_id: str, mode: Literal["forecast", "past_data"]
    ) -> Tuple[pd.DataFrame, str]:
        """
        Gather weather data for a specified location using MET Office's API.

        Args:
            * location_id (str): Specified location ID.
            * mode (str): gather data mode, either past data or forecast

        Returns:
            * location_data_df (pd.DataFrame): DataFrame containing weather information.
            * location_name (str): Name of the location.
        """

        if mode not in ["forecast", "past_data"]:
            raise ValueError("'mode' can only be 'forecast' or 'past_data'")

        if mode == "forecast":
            wx_type = "fcs"
            resolution = "3hourly"
        else:
            wx_type = "obs"
            resolution = "hourly"

        # Construct the URL using variables and parameters
        url = (
            f"{self.url_basic}/val/wx{wx_type}/all/{self.response_format}/"
            f"{location_id}?res={resolution}&key={self.met_office_api_key}"
        )

        # Make a GET request to the constructed URL
        response = requests.get(url=url, timeout=10)

        # Parse the response JSON
        response_json = response.json()

        # Extract relevant data from the JSON response
        data = response_json["SiteRep"]["DV"]["Location"]["Period"]

        # Extract location name from the response and convert to lowercase
        location_name = (
            response_json["SiteRep"]["DV"]["Location"]["name"].lower().replace(" ", "_")
        )

        # Initialize lists to store data
        location_id_list = []
        day = []
        wind_direction = []
        wind_gust = []
        wind_speed = []
        humidity = []
        pressure = []
        weather = []
        visibility = []
        temperature = []
        dew_point = []
        minutes_after_midnight = []
        
        # Convert to list if not already a list
        if not isinstance(data, list):
            data = [data]
        # Loop through data and extract required information
        for item in data:
            try:
                for sample in item["Rep"]:
                    # Define a list of all keys you want to ensure are present
                    # in the final dictionary
                    all_keys = ["D", "G", "H", "P", "S", "T", "V", "W", "Pt", "Dp", "$"]
                    # Create a new dictionary with keys from sample and corresponding values
                    # from the input dictionary (data).If a key is missing in the sample
                    # dictionary, set its value to None
                    sample = {key: sample.get(key, None) for key in all_keys}

                    # Append data to respective lists
                    location_id_list.append(response_json["SiteRep"]["DV"]["Location"]["i"])
                    day.append(item["value"])
                    wind_direction.append(sample["D"])
                    wind_gust.append(sample["G"])
                    humidity.append(sample["H"])
                    pressure.append(sample["P"])
                    wind_speed.append(sample["S"])
                    temperature.append(sample["T"])
                    visibility.append(sample["V"])
                    weather.append(sample["W"])
                    dew_point.append(sample["Dp"])
                    minutes_after_midnight.append(sample["$"])
            except KeyError as e:
                # Handle the KeyError
                print(f"KeyError occurred: {e}")
            except:
                print("Another error occurred")

        # Check if the extracted location ID matches the specified ID
        if not set(location_id_list) == {location_id}:
            raise ValueError("Location ID doesn't match specified ID value")

        # Create a pandas DataFrame from the extracted data
        location_data_df = pd.DataFrame(
            data={
                "location_id": location_id,
                "day": day,
                "minutes_after_midnight": minutes_after_midnight,
                "temperature": temperature,
                "weather": weather,
                "humidity": humidity,
                "wind_direction": wind_direction,
                "wind_gust": wind_gust,
                "wind_speed": wind_speed,
                "pressure": pressure,
                "visibility": visibility,
                "dew_point": dew_point,
            }
        )

        return location_data_df, location_name

    def gather_and_merge_data(
        self, location_id: str, mode: Literal["forecast", "past_data"]
    ) -> pd.DataFrame:
        """
        This function gathers weather data for a specified location, merge with
        existing data (if any), and save the merged data to CSV and Parquet files.

        Args:
            * location_id (str): Specified location ID.

        Returns:
            * all_data_no_dup_df (pd.DataFrame): Merged DataFrame with no duplicate
                entries.
        """

        # Gather new data and location name
        new_data_df, location_name = self.gather_location_data(
            location_id=location_id, mode=mode
        )

        # Read existing data from Parquet file
        file_dir = os.path.normpath(
            f"{self.data_dir}/{location_id}_{location_name}_weather_data.parquet"
        )
        old_data_df = pd.read_parquet(file_dir)

        # Concatenate old and new data
        all_data_df = pd.concat([old_data_df, new_data_df], axis=0, ignore_index=True)

        # Remove duplicate entries
        all_data_no_dup_df = all_data_df.drop_duplicates(keep="last").reset_index(
            drop=True
        )

        # Save data in parquet file
        all_data_no_dup_df.to_parquet(file_dir, index=False)

        return all_data_no_dup_df
