# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################


# 1. Homepage
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"To find min temp, the avg temp, and the max temp for a specified start, type below the start date after v1.0/<br/>"
        f"/api/v1.0/<start><br/>"
        f"To find min temp, the avg temp, and the max temp for a specified start and end, type below the start date after v1.0/ followed by a / then the end date <br/>"
        f"/api/v1.0/<start>/<end>"
    )


# 2. Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the results from the precipitation analysis"""
    prev_year = '2016-08-23'
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).\
        order_by(Measurement.date.asc()).all()

    session.close()

    # Convert list of tuples into normal list
    prcp_last_year = list(np.ravel(results))

    return jsonify(prcp_last_year)


# 3. Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station_list():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)


# 4. Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the results from the station analysis"""
    prev_year = '2016-08-23'
    
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).\
        order_by(Measurement.date.asc()).all()

    session.close()

    # Convert list of tuples into normal list
    most_active_station_temp = list(np.ravel(results))

    return jsonify(most_active_station_temp)


# 5. Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

# Start point
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the results from the station analysis"""
    sel = [
        func.min(Measurement.tobs).label("TMIN"),
        func.avg(Measurement.tobs).label("TAVG"),
        func.max(Measurement.tobs).label("TMAX")
        ]

    results = session.query(*sel).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    temp_start = list(np.ravel(results))

    return jsonify(temp_start)

# Start and end point
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the results from the station analysis"""
    sel = [
        func.min(Measurement.tobs).label("TMIN"),
        func.avg(Measurement.tobs).label("TAVG"),
        func.max(Measurement.tobs).label("TMAX")
        ]

    results = session.query(*sel).\
        filter((Measurement.date >= start) & (Measurement.date <= end)).all()

    session.close()

    # Convert list of tuples into normal list
    temp_start_end = list(np.ravel(results))

    return jsonify(temp_start_end)


if __name__ == "__main__":
    app.run(debug=True)