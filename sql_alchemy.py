# Import dependencies 
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables (measurement and station)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# Flask routes

# Homepage route 
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaiian Climate API!<br/>"
        f"Available Routes:<br/>"
        f"Precipitation: <a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"Stations: <a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"Temperature Observations: <a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"Temperature Analysis from Start Date: <a href='/api/v1.0/yyyy-mm-dd'>/api/v1.0/yyyy-mm-dd</a><br/>"
        f"Temperature Analysis from Start to End Dates: <a href='/api/v1.0/yyyy-mm-dd/yyyy-mm-dd'>/api/v1.0/yyyy-mm-dd/yyyy-mm-dd</a><br/>"
    )

# Precipitation route 
@app.route("/api/v1.0/precipitation")
def precipitation():
# Session link from python to the database 
    session = Session(engine)
    
# Query to retrieve the data and precipitation scores 
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

# Close session
    session.close()

# Convert to list to jsonify 
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_list.append(prcp_dict)
    
    return jsonify(prcp_list)

# Stations route 
@app.route("/api/v1.0/stations")
def stations():
# Session link from python to the database 
    session = Session(engine)

# Query to retrieve the station list 
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

# Close session
    session.close()

# Convert to list to jsonify 
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude 
        station_dict["Elevation"] = elevation
        all_stations.append(station_dict)
    
    return jsonify(all_stations)

# Temperature observation route 
@app.route("/api/v1.0/tobs")
def tobs():

# Session link from python to the database 
    session = Session(engine)

# Query the dates and temperature observations of the most active station for the last year of data.
    one_year = dt.date (2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year).order_by(Measurement.date.desc()).all()

# Close session
    session.close()

# Convert to list to jsonify 
    year_tobs = []
    for date, prcp in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Precipitation"] = prcp
        year_tobs.append(tobs_dict)

    return jsonify(year_tobs)

# Start route 
@app.route("/api/v1.0/<start>")
def temp_start(start):

# Session link from python to the database 
    session = Session(engine)

# Query min, average, and max temp for a given start range 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

# Close session
    session.close()

# Convert to list to jsonify
    tobs_start = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_start.append(tobs_dict)

    return jsonify(tobs_start)

# Start and end route 
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):

# Session link from python to the database 
    session = Session(engine)

# Query min, average, and max temp for a given start and end range 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

# Close session
    session.close()

# Convert to list to jsonify
    tobs_start_end = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_start_end.append(tobs_dict)

    return jsonify(tobs_start_end)


if __name__ == '__main__':
    app.run(debug=True)