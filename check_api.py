import httpx

from config import settings


def test_api_endpoint_accessible():
    response = httpx.get(
        url=f"{settings.weather_data.base_url}/point/hourly",
        headers={
            "apikey": settings.met_office.global_spot_api_key,
        },
        params={
            "dataSource": "BD1",
            "latitude": 51,
            "longitude": -0.1,
        },
        timeout=10.0,
    )

    data = response.json()
    pass


if __name__ == "__main__":
    test_api_endpoint_accessible()
