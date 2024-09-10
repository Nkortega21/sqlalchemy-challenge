# sqlalchemy-challenge
UCI Data Analyst Module 10 - sqlalchemy-challenge

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

For this this project I used 2 CSV files (hawaii_measurements & hawaii_station) as well as a SQLite file (hawaii) to perform my analysis inside of a Jupyter Notebook design a Climate App in Python 

Worked with Chris & Brendan
Used ChatGPT to help debug and assist with some coding

## Part 1: Analyze and Explore the Climate Data

### Exploratory Precipitation Analysis

Queried the measurement dataset to find the most recent date of data and queried the SQLite file to find a years worth of the most recent data. Created a line graph to visualize when precipitation was at its highest, so we can be sure to avoid the rainy season. Performed statistical analysis to calculate the counts, min, max, mean, standard deviation, 25% quantile, 50% quantile, and 75% quantile.

### Exploratory Station Analysis

Queried the station dataset to determine which stations are the most active. Used the most active station to calculate min,max, and avg temperatures of the data. Queried the SQLite file to find a years worth of the most recent data to get an up to date reference of the temperatures. Visualized the dataset with a histogram to determine what temperatures are most frequent throughout the year. 

## Part 2: Design Your Climate App

Created an app to more easily visualize the data from a browser via Jsonification. Created a list of routes with hyperlinks to make managing the app more navigatable.

### App Routes

**@app.route("/")**
This is the homepage that includes all of the available routes and some instructions.

**/api/v1.0/precipitation**
This page lists out all of the precipitation data for the most recent years worth of data in an easy to JSONified format.

**/api/v1.0/station**
This page lists out all of the available stations.

**/api/v1.0/tobs**
This page lists a years worth of the most recent data with the date and the corresponding temperatures.

**/api/v1.0/&lt;start&gt;**
_Instructions": "Replace &lt;start&gt; with date | YYYY-MM-DD_:
This page allows the user to do self exploratory analysis and calculate the mean, min, and max of the data. If there is no end date included it will calculate from the start date to the most recent date.

**/api/v1.0/<start>/<end>**
_Instructions": "Replace <start> and <end> with dates | YYYY-MM-DD/YYYY-MM-DD_:
This page allows the user to do self exploratory analysis and calculate the mean, min, and max of the data for a desired start and end date. 
