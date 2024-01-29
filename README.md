# Introduction
The Electricity Demand Prediction Service is an innovative solution designed to forecast electricity demand for the upcoming days with precision and reliability. Leveraging historical data from the National Grid API and weather information obtained through the Met Office API, this service utilizes advanced machine learning algorithms to generate accurate predictions tailored to the specific needs of energy providers, grid operators, and stakeholders in the power industry.

## Key Features:
* Data Integration: Fetches historical electricity demand data from the National Grid API and past weather data, as well as weather predictions, from the Met Office API. Integrates seamlessly with these APIs to ensure access to up-to-date and relevant information.

* Machine Learning Modeling: Employs sophisticated machine learning techniques to analyze historical electricity demand patterns in conjunction with weather conditions. Develops predictive models capable of forecasting electricity demand for the next few days with high accuracy and confidence.

* MLOps Pipeline: Implements a robust MLOps (Machine Learning Operations) pipeline to automate the process of model training, evaluation, deployment, and monitoring. Ensures seamless integration of machine learning models into operational workflows, enabling continuous improvement and optimization.

* Scalability and Flexibility: Designed to scale effortlessly, the service can adapt to varying levels of demand and data volume. Whether hosted on a local server or in the cloud, it offers the flexibility to meet the evolving needs of energy markets and grid management.

* Monitoring and Alerting: Implements comprehensive monitoring and alerting mechanisms to track model performance, detect anomalies, and notify stakeholders of potential issues or deviations. Enables proactive intervention and decision-making to maintain the reliability and efficiency of energy systems.

# Installation and usage
This project is still in the early stages. Currently, only the capability for fetching data is implemented.
Python 3.11.4 is used for this project. After installing the python packages in `requirements.txt`, weather data can be fetched using:

```
cd src/data_fetch_scripts
python fetch_weather_data.py
```


# Project wiki
A dedicated wiki has been created for this project. The home page can be found [here](https://github.com/albertovidalrod/Electricity-demand-prediction-service/wiki). The wiki will be used to document the project, including requirements, architecture and more. Currently, the following sections are available:
* [Architecture and tools](https://github.com/albertovidalrod/Electricity-demand-prediction-service/wiki/Architecture-and-tools)
* [Ideas](https://github.com/albertovidalrod/Electricity-demand-prediction-service/wiki/Ideas)

# Data sources
## Met Office API
The MET Office API is used to fetch historic hourly weather data.
* [API overview](https://www.metoffice.gov.uk/services/data/datapoint/api-reference#overview)
* [API documentation - PDF](https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/data/datapoint_api_reference.pdf)
* [API documentation - hourly observations](https://www.metoffice.gov.uk/services/data/datapoint/uk-hourly-site-specific-observations)