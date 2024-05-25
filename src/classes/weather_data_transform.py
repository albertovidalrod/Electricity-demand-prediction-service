"""
This module contains the WeatherDataTransform, which includes the transformations
performed to the weather data parquet files
"""
import datetime

import pandas as pd

class WeatherDataTransform:
    """
    The methods in this class are used to transform the weather data before
    it is passed to the feature store

    Methods:
        * transform_individual_locations
        * generate_all_information_df
        * calculate_scaled_temperature
        * get_max_weather
    """

    @staticmethod
    def transform_individual_locations(file_path: str) -> pd.DataFrame:
        """
        Transform data from individual weather stations using pandas to:
        - Remove duplicate values
        - Remove NaN values
        - Generate a timestamp in the format day + hour
        - Changes column data types
        - Set the timestamp as the index of the dataframe
        - Map the weather types 

        Args:
            * file_path (str): file path

        Returns:
            * pd.DataFrame: dataframe containing transformed data
        """
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
    def generate_all_information_df(df_dict: dict[pd.DataFrame]) -> pd.DataFrame:
        """
        Generate a dataframe containing the combined information from individual
        weather stations. The data is combined using the population scaling, i.e.
        ratio of location population to total population.

        Args:
            * df_dict (dict[pd.DataFrame]): dictionary of dataframes containing
                information about individual weather stations

        Returns:
            * pd.DataFrame: dataframe containing scaled data
        """
        # Create a dict containing the population in millions
        # of the closest big city
        area_population = {
            "crossby_df": 0.9, # Liverpool
            "bingley_df": 0.8, # Leeds
            "rostherne_df": 2.9, # Manchester
            "watnall_df": 0.8, # Nottingham
            "coleshill_df": 4.3, # Birmingham
            "heathrow_df": 9.5, # London
            "thorney_df": 1.5 # Southampton and Portsmouth
        }
        total_population = sum([value for value in area_population.values()])
        # Calculate population ratio for each of the locations
        population_scaling = {
            key:value/total_population for (key, value) in area_population.items()
        }
        
        # Find the common indices
        indices_list = [df.index for df in df_dict.values()]
        common_indices = sorted(list(set(indices_list[0]).intersection(*indices_list[1:])))
        # Keep the common indices for each of the dataframes
        df_dict = {df_name:df.loc[common_indices] for (df_name,df) in df_dict.items()}

        # Extract scaled temperature across all the locations
        scaled_temperature = WeatherDataTransform.calculate_scaled_temperature(
            df_dict, population_scaling
        )

        # Initialize an empty DataFrame to store the "weather" column from each DataFrame
        weather_df = pd.DataFrame()
        # Iterate over each key-value pair in df_dict
        for df_name, df in df_dict.items():
            # Concatenate the "weather" column from the current DataFrame to weather_df
            weather_df[df_name] = df['weather']
        # Create a column containing the weather value with the highest weight
        max_weather = weather_df.apply(
            WeatherDataTransform.get_max_weather,
            axis=1, 
            population_scaling=population_scaling
        )

        # Create a dataframe that combines the scaled temperature
        # and the highest weighted weather value
        df_combined = pd.DataFrame(
            {
                "temperature": scaled_temperature,
                "weather": max_weather
            }
        )

        return df_combined

    @staticmethod
    def calculate_scaled_temperature(
            df_dict: dict[pd.DataFrame],
            population_scaling: dict[float]
    ) -> pd.Series:
        """
        Calculate the scaled temperature using temperature data from different
        locations and their population scaling weights

        Args:
            * df_dict (dict[pd.DataFrame]): dictionary of dataframes containing
                information about individual weather stations
            * population_scaling (dict[float]): population for different locations
                measured in millions of citizens

        Returns:
            * pd.Series: scaled temperature according to population scaling weights
        """
        scaled_temperature_all = 0
        # Iterate over each key-value pair in df_dict
        for df_name, df in df_dict.items():
            # Multiply the "temperature" column by the scaling factor for the current DataFrame
            scaled_temperature = df['temperature'] * population_scaling[df_name]
            # Add the scaled temperature to the total sum
            scaled_temperature_all += scaled_temperature

        return scaled_temperature_all
    
    @staticmethod
    def get_max_weather(
            weather_vals: pd.Series, population_scaling: dict[float]
    ) -> list:
        """
        Determine the max weather occurrence for a given timestamp. Uses the 
        their population scaling weights to determine the max weather.
        

        Args:
            * weather_vals (pd.Series): weather values for all the locations at
                a given timestamp
            * population_scaling (dict[float]): population for different locations
                measured in millions of citizens

        Returns:
            * int: weather value with the maximum weight
        """
        weather_aggregates = []
        unique_weathers = set(weather_vals)
        # For each weather value, find the locations where it occurs and multiply it
        # by the corresponding population scaling to determine the overall weight
        # of each weather value
        for weather in unique_weathers:
            weather_locations = weather_vals[weather_vals == weather].index.to_list()
            aggregate = sum(
                [
                    population_scaling[location] for location in weather_locations
                    if location in population_scaling
                ]
            )
            weather_aggregates.append(aggregate)
        # Retrieve the weather value with the highest weight
        index_max = weather_aggregates.index(max(weather_aggregates))
        max_weather = list(unique_weathers)[index_max]

        return max_weather