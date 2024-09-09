# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/nkort/UCI DA Class Folder/Homework/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#homepage
@app.route("/")
def homepage():
    """List all available API routes."""
    return (
        f"<u><strong>Available Routes:</strong></u><br/>"
        f'<a href="/api/v1.0/precipitation">Precipitation</a><br/>'
        f'<a href="/api/v1.0/station">Stations</a><br/>'
        f'<a href="/api/v1.0/tobs">Tobs</a><br/>'
        f'<a href="/api/v1.0/<start>">/api/v1.0/&lt;start&gt;</a><br/>'
        f'replace &lt;start&gt; with a date | YYYY-MM-DD<br/>'
        f'<a href="/api/v1.0/<start>/<end>">/api/v1.0/&lt;start&gt;/&lt;end&gt;</a><br/>'
        f'replace &lt;start&gt; and &lt;end&gt; with dates | YYYY-MM-DD/YYYY-MM-DD'
    )
#precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

   # Design a query to retrieve the last 12 months of precipitation data 
    # Starting from the most recent data point in the database. 
    rec_date_row = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Calculate the date one year from the last date in data set.
    if rec_date_row:
        rec_date = rec_date_row[0]
        end_date = dt.datetime.strptime(rec_date, '%Y-%m-%d')
        start_date = end_date - dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores
    # Sort the dataframe by date    
        query = text("""
            SELECT date, prcp
            FROM measurement
            WHERE date BETWEEN :start_date AND :end_date
            ORDER BY date ASC
            """)
        
    prcp_df = pd.read_sql(query, engine, params={'start_date': start_date, 'end_date': end_date}).dropna()
    prcp_df.columns = ['date','prcp']
    prcp_data = prcp_df.to_dict(orient='records')

    session.close()

    return jsonify(prcp_data)

@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    query = text(""" 
            SELECT station
            FROM Measurement
            GROUP BY station
            """)

    # Extracting the station names from the query result
    stations_df = pd.read_sql(query,engine)
    stations_df.columns = ['station']
    stations_data = stations_df.to_dict(orient='records')

    session.close()
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
    query = text(""" 
            SELECT station, COUNT(*) AS count
            FROM Measurement
            GROUP BY station
            ORDER BY count DESC
            """)
    stations_df = pd.read_sql(query,engine)

    # Using the most active station id
    most_active_station = stations_df.iloc[0]['station']
    rec_date_row = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# Calculate the date one year from the last date in data set.
    if rec_date_row:
        rec_date = rec_date_row[0]
        end_date = dt.datetime.strptime(rec_date, '%Y-%m-%d')
        start_date = end_date - dt.timedelta(days=366)
# Query the last 12 months of temperature observation data for this station
        query_temp_observations = text("""
            SELECT date, tobs
            FROM Measurement
            WHERE station = :station
            AND date BETWEEN :start_date AND :end_date
    """)

    df_temp_observations = pd.read_sql(query_temp_observations, engine, params={'station': most_active_station, 'start_date': start_date, 'end_date': end_date}).dropna()
    df_temp_observations_data = df_temp_observations.to_dict(orient='records')

    session.close()
    return jsonify(df_temp_observations_data)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
    

    if end:
        # If both start and end dates are provided
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        # If only the start date is provided
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).all()

    # Close the session
    session.close()

    # Extract the result and structure the response
    temp_data = {
        "Instructions" : "Replace <start> and <end> with dates | YYYY-MM-DD/YYYY-MM-DD",
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)