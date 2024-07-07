# Ideas

## How to implement the prediction
In previous analysis, I've used features such as hour of the day and day of the year to predict the electricity demand. These features are great because the strong seasonalities in electricity demand help make decent predictions, but it isn't enough to make accurate predictions. The goal of this project is to add some of the most important features when it comes to electricity demand: weather data and weather forecasts.

It looks simple in theory, just add values like the hourly temperature or the overall weather condition, e.g. sunny or cloudy. In practice, it's more complicated since the data from the National Grid is at national level. The temperature, most likely, won't be the same in London and Manchester, and the same can be said about weather condition.

To address this issue, some ideas are suggested:

* Let's predict Wales and England demand instead of National demand or TSD
* Let's use an weighed-average temperature based on population of the area, e.g. if London has 10% of the population, then london_temp*0.1
* Try to use an "average" climate condition: e.g. cloudy, sunny... It could be encoded as
a number, but it wouldn't make much sense in real life

The goal is to encode the weather conditions as a single value for the entire territory instead of different values for different locations. This would increase the number of features very quickly, leading to a more complex model, as well as the possibility of adding non-informative features.

## Data management
The project is in the early stages and optimal data management strategy is yet to be determined. In its final form, the project will use two API services to pull information periodically, but for now, the data from both sources will be stored in parquet files. The National Grid makes the historic data available and it isn't necessary to pull data every day (currently, it's done weekly). However, it seems that the data from the Met Office is only available for the last 24 hours. Therefore, it needs to be fetched daily. 

To do so, different options are considered:
* Keep track of the data using Git LFS, create a branch for data updates and merge it with develop (or master) periodically. This is the preferred option.
* Similar to the previous option, but pulling the data directly into the workflow. Since daily data updates are required, it may make the develop branch and other branches quite messy
* Reference the data using Git LFS. Specific versions or commits of the data can be directly referenced in the code.
* use a different tool such as Data Version Control.


The data used in the project is tabular for both sources and it will stored in parquet files for now.  
