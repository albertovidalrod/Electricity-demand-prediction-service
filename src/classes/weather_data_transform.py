"""
This module contains the WeatherDataTransform, which contains the transformations
performed to the weather data parquet files
"""
import datetime

import pandas as pd

class WeatherDataTransform:
    """


    Methods:
        * transform_individual_locations
    """

    @staticmethod
    def transform_individual_locations(file_path: str) -> pd.DataFrame:
        df = pd.read_parquet(path=file_path)
        # Remove unnecessary columns
        cols_to_keep = ["day", "minutes_after_midnight", "temperature", "weather"]
        df = df[cols_to_keep]
        # Drop rows with nan values
        df = df.dropna()
        # Drop duplicated rows
        df = df.drop_duplicates()
        # Change column types
        date_cols = "day"
        numeric_cols = [col for col in df.columns if col not in date_cols]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
        # Create date column that combines day and minutes_after_midnight
        df["day"] = df["day"].apply(lambda x: x.replace("Z", ""))
        df["hour_number"] = (df['minutes_after_midnight']/60).astype(int)
        df["hour"] = (df["hour_number"]).apply(
            lambda x: str(datetime.timedelta(hours=x))
        )
        df["date"] = pd.to_datetime(
            (df["day"] + " " + df["hour"])
        )
        # Set the date as the new index
        df.set_index("date", inplace=True)
        # Map the weather column using common values to reduce the number of total values
        weather_dict_mapping = {
            0: 0,
            1: 1,
            2: 2,
            3: 2,
            4: 3,
            5: 4,
            6: 5,
            7: 6,
            8: 7,
            9: 8,
            10: 8,
            11: 9,
            12: 8,
            13: 10,
            14: 10,
            15: 10,
            16: 11,
            17: 11,
            18: 11,
            19: 12,
            20: 12,
            21: 12,
            22: 13,
            23: 13,
            24: 13,
            25: 14,
            26: 14,
            27: 14,
            28: 15,
            29: 15,
            30: 15
        }
        df["weather"] = df["weather"].map(weather_dict_mapping)

        return df

    @staticmethod
    def generate_all_information_df():
        print("To do")
