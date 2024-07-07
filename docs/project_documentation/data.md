# Data

This project uses two different data sources:

* Historic electricity consumption in the UK from the National Grid
* Weather data from the MET Office.

## Electricity demand data
The historic electricity demand data is collated by National Grid, who operate the electricity grid in the UK. The data spans from 2009 to the current date and it can be accessed using [their API](https://www.nationalgrideso.com/data-portal/historic-demand-data). The data is often updated on a daily basis, but the update frequency isn't a problem since this dataset is only used for training and testing of ML models and not for inference. All the data is available and therefore the data can be accessed when needed. 
![Electricity Demand Sample](https://raw.githubusercontent.com/albertovidalrod/Electricity-demand-prediction-service/create-documentation-mkdocs/media/images/electricity_demand_sample.png)


The dataset contains a total of 21 columns such as total electricity demand, renewable energy capacity, interconnector flow, etc ( a description of all the columns can be found [here](https://www.nationalgrideso.com/data-portal/historic-demand-data/historic_demand_data_2024)). However, only three columns are used as part of model training:

* SETTLEMENT_DATE. The date the historic outturn occurred.
* SETTLEMENT_PERIOD. The half hourly period for the historic outturn occurred. Settlement period 1 runs from 00:00-00:30.
* ENGLAND_WALES_DEMAND. England and Wales Demand, as ND above but on an England and Wales basis
    * ND is described as "Great Britain generation requirement and is equivalent to the Initial National Demand Outturn (INDO) and National Demand Forecast as published on BM Reports. National Demand is the sum of metered generation, but excludes generation required to meet station load, pump storage pumping and interconnector exports. National Demand is calculated as a sum of generation based on National Grid ESO operational generation metering"


Out of those three columns, ENGLAND_WALES_DEMAND is the target, i.e. the value the model will predict, and the other two columns are simply used to assemble a date column that includes both the day and the hour. The date is then used to generated some predictive features such as the day of the week or the week of the year. However, no electricity demand data is used for the prediction service.

## Weather data
Weather data is collected daily all over the UK by the [Met Office](https://www.metoffice.gov.uk). Their [API](https://www.metoffice.gov.uk/services/data/datapoint/api-reference#overview) provides a lot of data, but only the [hourly site-specific observations](https://www.metoffice.gov.uk/services/data/datapoint/uk-hourly-site-specific-observations) are required for training and testing ML models.

Hourly site-specific observations include 10 features, such as temperature, wind direction and pressure. However, only two features are used for model training:

* Temperature
* Weather type (see more in [Annex A](#annex-a-weather-types))

Unlike the historic electricity demand data, the hourly site-specific observations are only available for the last 24 hours. Therefore, a script is daily run using Github actions to fetch the daily data and store in a parquet file. The downside of this approach is that historic data isn't available. The earliest the script was run was 26/01/2024, which means that only data from 26/01/2024 will be used to train the model.

### Weather data for model prediction
The weather features mentioned in the previous section, i.e. temperature and weather type, will also be used as part of the predictions service. Met Office provides weather data forecast for the next five days with time steps being daily or every three hours. 

Since the project is still in the early stages of development, a decision has not been made regarding the data that will be used for the prediction service, but most likely it will use the weather forecast data in intervals of three hours.


### Annex A: Weather types
The original "weather type" in the data provided by the Met Office uses numbers to encode different weather types as follows:

| Code | Description                    |
|------|--------------------------------|
| 0    | Clear night                    |
| 1    | Sunny day                      |
| 2    | Partly cloudy (night)          |
| 3    | Partly cloudy (day)            |
| 4    | Not used                       |
| 5    | Mist                           |
| 6    | Fog                            |
| 7    | Cloudy                         |
| 8    | Overcast                       |
| 9    | Light rain shower (night)      |
| 10   | Light rain shower (day)        |
| 11   | Drizzle                        |
| 12   | Light rain                     |
| 13   | Heavy rain shower (night)      |
| 14   | Heavy rain shower (day)        |
| 15   | Heavy rain                     |
| 16   | Sleet shower (night)           |
| 17   | Sleet shower (day)             |
| 18   | Sleet                          |
| 19   | Hail shower (night)            |
| 20   | Hail shower (day)              |
| 21   | Hail                           |
| 22   | Light snow shower (night)      |
| 23   | Light snow shower (day)        |
| 24   | Light snow                     |
| 25   | Heavy snow shower (night)      |
| 26   | Heavy snow shower (day)        |
| 27   | Heavy snow                     |
| 28   | Thunder shower (night)         |
| 29   | Thunder shower (day)           |
| 30   | Thunder?                       |


As can be seen, some of the values are the same for night and day. In order to reduce the complexity of this feature, the data encoding was modified to the following:

| Code | Description      |
|------|------------------|
| 0    | Clear night      |
| 1    | Sunny day        |
| 2    | Partly cloudy    |
| 3    | Not used         |
| 4    | Mist             |
| 5    | Fog              |
| 6    | Cloudy           |
| 7    | Overcast         |
| 8    | Light rain       |
| 9    | Drizzle          |
| 10   | Heavy rain       |
| 11   | Sleet            |
| 12   | Hail             |
| 13   | Light snow       |
| 14   | Heavy snow       |
| 15   | Thunder          |

