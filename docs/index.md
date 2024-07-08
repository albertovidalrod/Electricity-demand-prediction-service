# Introduction

Welcome to the project documentation for the electricity demand prediction service! This is my first end-to-end MLOps project and I wanted to document the different parts of the project and not just the code.  

The goal of this project is to build an automated MLOps pipeline to:

* Fetch data from two APIs, transform it and store in a feature store
* Re-train a machine learning model (algorithm is yet to be determined) to predict electricity demand given a set of inputs
* Serve the trained model as a prediction service
* Monitor the performance of the model and the data and trigger the re-training of the model if required

I will be using Machine Learning Engineering in Action by Ben Wilson Currently to guide me in the process of building an end-to-end pipeline. Currently, I'm working on the experimentation stage.

