"""
This module fetches weather data from the MetOffice API
"""

from pathlib import Path

from classes.weather_data_api import WeatherData
from config import settings


def main() -> None:
    """
    Fetch weather data from the Met Office API and store it in the data directory.
    """
    root = Path(__file__).parent.parent.parent
    data_dir = (
        root / settings.directories.data_dir / settings.directories.weather_data_dir
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

    weather_data = WeatherData(data_dir=str(data_dir), response_format="json")

    for location in interest_locations:
        weather_data.gather_and_merge_data(location_id=location, mode="past_data")


if __name__ == "__main__":
    main()
