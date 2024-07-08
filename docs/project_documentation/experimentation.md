# Experimentation

## Introduction 
For this stage, I will use chapters 5 and 6 from the book Machine Learning Engineering in Action by Ben Wilson as reference material. Chapter 5 focuses on planning and researching and ML project and chapter 6 describes testing and evaluation of different ML models. Ben uses a examples in all the chapters and the example in this section of the book is a time series forecasting model and therefore what he describes is quite relevant for me.

Prior to describing my approach to the experimentation phase, it's worth noting in a [previous project available on Kaggle](https://www.kaggle.com/code/albertovidalrod/uk-electricity-consumption-prediction-time-series) I already did a lof of the work that a data scientist/ML engineer would do during the experimentation stage, such as data analysis and model benchmarking. 

## Planning
The research I conducted for my previous project on electricity demand forecasting was very helpful for this project. Since I worked on that project (mid 2022), there haven't been groundbreaking new techniques for time series forecasting. As part of that project, I used:

* [SARIMA models](https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html). Despite trying multiple combinations of hyperparameters, each of them leading to a more complex and bigger model, SARIMA couldn't capture the complexity of the data (see next section)
* [XGBoost](https://xgboost.readthedocs.io/en/stable/). XGBoost yielded the best results, but as proven by in this [Kaggle notebook](https://www.kaggle.com/code/carlmcbrideellis/extrapolation-do-not-stray-out-of-the-forest) by [Carl McBride Ellis](https://www.kaggle.com/carlmcbrideellis) a very respected member of the Kaggle community, gradient boosted frameworks, including XGBoost, cannot extrapolate and their performance decreases when the forecasting on unseen data.
* Linear Boost Regression - part of [Linear Trees](https://github.com/cerlymarco/linear-tree). I came across this python packages in a [Kaggle notebook](https://www.kaggle.com/code/carlmcbrideellis/multivariable-time-series-forecasting-linear-tree?scriptVersionId=165694964) also by [Carl McBride Ellis](https://www.kaggle.com/carlmcbrideellis). It offered the most promising results, but it was fairly slow to train on CPU (around 10 minutes per run for a simple model).
* [Prophet](https://facebook.github.io/prophet/docs/quick_start.html#python-api). The results were comparable to that of the other models, but I have since encountered some articles that discourage the use of Prophet.
* LSTM and Deep LSTM (using Keras). LSTM networks were the most accurate model, but also the one that took the longest to train despite having GPU acceleration enabled in Kaggle.Therefore, given the expensive computational requirements, it won't be used for this project.

The results I got (as of version 16) are as follows:

| Metric | XGBoost - Simple | XGBoost - CV & GS | Linear Boost | Prophet - Simple | Prophet - Holiday | Prophet - CV & GS | LSTM  | Deep LSTM |
|--------|-------------------|-------------------|--------------|------------------|-------------------|-------------------|-------|-----------|
| MAPE   | 8.91              | 7.34              | 8.63         | 9.37             | 9.36              | 9.36              | 7.39  | 7.22      |
| RMSE   | 3383.98           | 2670.52           | 3112.08      | 3262.10          | 3243.37           | 3241.11           | 2708.95 | 2594.04  |


## Analysis
The first step of the analysis stage is to visualise the data:
![electricity_demand_graph](https://raw.githubusercontent.com/albertovidalrod/Electricity-demand-prediction-service/create-documentation-mkdocs/media/images/electricity_demand_graph.png)


## Prototyping


## Evaluation
