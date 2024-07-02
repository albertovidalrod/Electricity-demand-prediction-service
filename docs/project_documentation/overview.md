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
This 
