# Architecture

## Requirements

## High-level architecture

## Data ingestion and feature store
The data ingestion process is very simple for this project as it only requires fetching data from two APIs using the `requests` package. No real time data will be used for the prediction service, in fact, only the weather data will be used for online inference. Electricity demand data will only be used for training purposes. The data is currently stored locally using parquet files, although it may be stored in the cloud in the future.

The data is transformed before being passed to a feature store. A feature store is a centralised repository for storing, managing, and serving machine learning features or attributes used for training predictive models. The developers of Feast, an open-sourced feature store, wrote a [great article](https://feast.dev/blog/what-is-a-feature-store/) that explains feature stores in depth.

At the start of this project, I came across the idea of features platforms, which build on feature stores and add feature transform pipelines. This functionality can be achieved by combining feature stores with feature transformation pipelines in Spark or Pandas, albeit not that scalable. Since this project will only transform data coming from two sources, a feature store is enough.

The architecture of the data ingestion and the feature store is as follows:

![feature_store_diagram drawio](https://github.com/albertovidalrod/Electricity-demand-prediction-service/assets/130750341/f7287554-269b-44e9-8ac0-d2061a71d8b1)

*Data ingestion and feature store - Generated using draw.io*



## Tools

## Data Management
* [Git LFS](https://git-lfs.com). Git LFS is the tool currently used for data management since it's very easy to integrate with GitHub and GitHub Actions.
* [Data Version Control](https://dvc.org). 

## Data ingestion and feature store
* Data transformation. The choice hasn't been made yet. Two different alternatives are considered:
  * Pandas
  * Apache beam
* [Feast](https://feast.dev) for feature store. The choice isn't definitive, but Feast is the preferred choice since it's open-sourced