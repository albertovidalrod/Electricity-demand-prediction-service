# Introduction
The Electricity Demand Prediction Service is an an-to-end Machine Learning project with the aim to forecast electricity demand for the upcoming days with precision and serve the predictions using an API. The system will leverage historical data from the National Grid API and weather information obtained through the Met Office API to create the ML models.

## Key Features
The desired key features for this project are:

* Data Integration: Fetches historical electricity demand data from the National Grid API and past weather data, as well as weather predictions, from the Met Office API. Integrates seamlessly with these APIs to ensure access to up-to-date and relevant information.

* Machine Learning Modeling: Employs  machine learning techniques to analyze historical electricity demand patterns in conjunction with weather conditions. Develops predictive models capable of forecasting electricity demand for the next few days with high accuracy and confidence.

* MLOps Pipeline: Implements a robust MLOps (Machine Learning Operations) pipeline to automate the process of model training, evaluation, deployment, and monitoring

* Monitoring and Alerting: Implements comprehensive monitoring and alerting mechanisms to track model performance, detect anomalies, and notify stakeholders of potential issues or deviations. 

Note that some of this 

# Installation and usage
This project is still in the early stages. Currently, only the capability for fetching data is implemented.
Python 3.11.4 is used for this project. After installing the python packages in `requirements.txt`, weather data can be fetched using:

```
cd src/data_fetch_scripts
python fetch_weather_data.py
```

# Project documentation
My goal for this project is to go beyond writing the code to train ML models and creating the infrastructure to serve those models. My aim is to detail the different steps of the project (planning, experimentation, development and production) as well as more technical elements such as the system requirements and architecture.

The documentation can be found [here](https://albertovidalrod.github.io/Electricity-demand-prediction-service/project_documentation/architecture/). 