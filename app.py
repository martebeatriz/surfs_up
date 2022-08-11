from flask import Flask, jsonify

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes.
Base = automap_base()

# the following code to reflect the database:
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# define our Flask app
app = Flask(__name__)

# define the starting point, also known as welcome route or root
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br/>
    Available Routes: <br/>
    /api/v1.0/precipitation <br/>
    /api/v1.0/stations <br/>
    /api/v1.0/tobs <br/>
    /api/v1.0/temp/start/end <br/>
    ''')

# create the route for the precipitation analysis
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) # calculates the last year available
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all() # write a query to get the date and precipitation 
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip) # Jsonify() is a function that converts the dictionary to a JSON file.

#create the stations route
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all() #create a query that gets the stations in our database
    stations = list(np.ravel(results)) # unravel results and convert them to a list
    return jsonify(stations=stations)

# return the temperature observations
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) #calc dates 
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all() #query the stations for their temps
    temps = list(np.ravel(results)) #unravel and list
    return jsonify(temps=temps)


#create route for the min, max, and avg temps 
    # have to provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None): #Set both parameters to none
    # create a query to select the min, ave, and max temps from our SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)] 

    # determine the starting and ending date
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate the temp min, ave, and max with the start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
