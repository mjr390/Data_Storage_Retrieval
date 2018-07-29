import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to the home page for the project!"


@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page")
    from datetime import timedelta
    # Calculate the date 1 year ago from today (find 1 year from last day in data instead)
    Measurement_dates = session.query(Measurement)
    dates_list = []
    for row in Measurement_dates:
        dates_list.append(row.date)
    last_day_in_data = max(dates_list)
    las = dt.datetime.strptime(last_day_in_data, '%Y-%m-%d')
    one_year_before_last_day = las- timedelta(days=365)
    date_and_scores = session.query(Measurement).\
    filter(Measurement.date <= las).filter(Measurement.date >= one_year_before_last_day) 

    to_df_dates = []
    to_df_prcp = []
    for row in date_and_scores:
        to_df_dates.append(row.date)
        to_df_prcp.append(row.prcp)
    dictionary = dict(zip(to_df_dates, to_df_prcp))
    return(jsonify(dictionary))

#return list of uniqe stations in json form
@app.route("/api/v1.0/stations") 
def stations():
    Measurement_dates = session.query(Measurement)
    stations_list = []
    for row in Measurement_dates:
        stations_list.append(row.station)
    unique_stations = []
    for i in stations_list:
        if i not in unique_stations:
            unique_stations.append(i)     
    return(jsonify(unique_stations)) 

#return a JSON list of tobs for past year
@app.route("/api/v1.0/tobs")
def tobs():
    x=1         


if __name__ == "__main__":
    app.run(debug=True)       