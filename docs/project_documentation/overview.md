# Overview

Welcome to the project documentation for the electricity demand prediction service! This is my first end-to-end MLOps project and I wanted to document the different parts of the project and not just the code.  

Initially, I wanted to implement the fancy features from MLOps pipelines such as feature stores, CI pipelines or a prediction service before having carried out the essential steps such as deciding which model I will be using. That's why I'm using the book [Machine Learning Engineering in Action](https://github.com/BenWilson2/ML-Engineering) by Ben Wilson to guide my project planning and implementation process.

The goal of this project is to build an automated MLOps pipeline to:

* Fetch data from two APIs, transform it and store in a feature store
* Re-train a machine learning model (algorithm is yet to be determined) to predict electricity demand given a set of inputs
* Serve the trained model as a prediction service
* Monitor the performance of the model and the data and trigger the re-training of the model if required

These ideas are captured by the following diagram:
![MLOps_pipeline](https://cloud.google.com/static/architecture/images/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning-3-ml-automation-ct.svg)

*Automated MLOps pipeline. Source: [Google MLOps](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)*

The above diagram shows a fully automated MLOps pipeline and that's the ultimate goal, but the pipeline will be built iteratively and the first iterations won't include as many features

## Previous work and project motivation
This project is the continuation of a notebook a created on time series analysis and prediction as part of an ML course. The notebook, [available on Kaggle](https://www.kaggle.com/code/albertovidalrod/uk-electricity-consumption-prediction-time-series), uses past electricity demand data and other features, such as time of the day and day of the year, to analyse the performance of different ML models and make predictions on the hold-out set. 

That project helped me get a really good insight on the dataset, such as the different seasonal patterns, and the different models use, e.g. SARIMA models couldn't capture the complexity of the data and therefore won't be considered as possible ML models for this project. However, there were two questions I didn't answer as part of that project (not that it was meant to be an introductory project on time series analysis):

* What if I added other features such as temperature and weather conditions? Would it improve the accuracy of the predictions?
* After building an ML model that can make predictions of future electricity demand, can I create a dashboard to visualise the model performance and serve the predictions using an API?

The [National Grid](https://www.nationalgrid.com), the energy company that manages the electricity grid in the UK and whose data I use, has its own prediction service. The goal of this project isn't to create a prediction service that can compete with that of the National Grid, but to build on previous work and challenge myself to build and end-to-end MLOps platform. 

