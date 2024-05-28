"""
This module contains the ElectricityDataTransform, which includes the transformations
performed to the electricity demand data parquet files
"""
import datetime

import holidays
import numpy as np
import pandas as pd

class ElectricityDataTransform:
    """
    The methods in this class are used to transform the weather data before
    it is passed to the feature store

    Methods:
        * transform_data
        * get_england_bank_holidays
        * modify_date
    """

    @staticmethod
    def transform_data(file_path: str) -> pd.DataFrame:
        """
        Transform electricity demand data by:
        - Remove unnecessary columns
        - Removing duplicate values
        - Removing NaN values
        - Adding bank holidays to the dataframe
        - Generate a timestamp in the format day + hour
        - Set the timestamp as the index of the dataframe

        Args:
            * file_path (str): file path

        Returns:
            * pd.DataFrame: dataframe containing transformed data
        """
        df = pd.read_parquet(path=file_path)
        # Remove unnecessary columns
        cols_to_keep = ["settlement_date", "settlement_period", "tsd"]
        df = df[cols_to_keep]
        # Drop rows with nan values
        df = df.dropna()
        # Drop duplicated rows
        df = df.drop_duplicates()
        # Get the bank holidays and add them to the dataframe
        holiday_dates = ElectricityDataTransform.get_england_bank_holidays(2024)
        df["is_holiday"] = df["settlement_date"].apply(
            lambda x: pd.to_datetime(x) in holiday_dates
        )
        df["is_holiday"] = df["is_holiday"].astype(int)

        df = ElectricityDataTransform.modify_date(df)
        # Set the date as the index and sort it in case something had gone wrong
        df.set_index("settlement_date", inplace=True)
        df.sort_index(inplace=True)

        return df


    @staticmethod
    def get_england_bank_holidays(years: int) -> list[np.datetime64]:
        """
        Extract bank holidays in England for the specified years

        Args:
            * years (int): years for which bank holidays are to be extracted

        Returns:
            * list[np.datetime64]: list of bank holidays
        """
        # Extract bank holidays in England
        bank_holiday_england = holidays.UK(
            subdiv="England", years=years, observed=True
        ).items()

        # Create empty lists to store data
        holiday_names = []
        holiday_dates = []
        holiday_names_observed = []
        holiday_dates_observed = []


        for date, name in sorted(bank_holiday_england):
            holiday_dates.append(date)
            holiday_names.append(name)

            holiday_names_observed.append(name)
            holiday_dates_observed.append(np.datetime64(date))

            # Pop the previous value as observed bank holidays takes place later
            if "Observed" in name:
                holiday_dates_observed.pop()
                holiday_names_observed.pop()

        return holiday_dates_observed

    @staticmethod
    def modify_date(df_original: pd.DataFrame) -> pd.DataFrame:
        """
        Modify the date in the original dataframe. The new date is in the
        format day + hour

        Args:
            df_original (pd.DataFrame): original electricity demand data

        Returns:
            * pd.DataFrame: electricity demand dataframe with new date format
        """
        # Create a copy of the original dataframe to avoid making
        # changes to the original dataframe
        df = df_original.copy()
        # Keep only the "on the hour" samples as these are the only available timestamps
        # in the weather data files
        df = df[df["settlement_period"] % 2 == 1]
        # Encode settlement period as 1-24 since even numbers from 1-48 are removed
        df["settlement_period"] = (np.ceil(df["settlement_period"] / 2)).astype(int)

        # Apply lambda function to turn settlement period into hours.
        # Settlement period equal to 0 corresponds with 00:00:00 and each
        # settlement period adds 30 minutes until settlement period 48, which
        # corresponds with 23:30:00
        hour = (df["settlement_period"]).apply(
            lambda x: str(datetime.timedelta(hours=x-1))
        )
        # Fix encoding of midnight values
        hour[hour == "1 day, 0:00:00"] = "0:00:00"
        # Create a new column containing the data as day + hour
        df["settlement_date"] = pd.to_datetime(
            (df["settlement_date"] + " " + hour)
        )

        return df
