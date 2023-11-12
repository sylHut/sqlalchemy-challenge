# Import the dependencies.
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask , jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# 1./
@app.route("/")
def welcome():
    return (f"Welcome to sqlalchemy-challenge Page <br/>"
           f" ------------------------------------ <br/>"
           f" List of Available Routes <br/>"
           f" ------------------------- <br/>"
           f"/api/v1.0/precipitation <br/>"
           f"/api/v1.0/stations <br/>"
           f"/api/v1.0/tobs <br/>"
           f"/api/v1.0/yyyy-mm-dd <br/>"
           f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd <br/>")

           
# 2./api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(measurement.date , measurement.prcp).\
    filter(measurement.date >= '2016-08-23', measurement.date <= '2017-08-23').\
    order_by(measurement.date).all()
    prdict = {date : x for date , x in results}
    return jsonify(prdict)


# 3./api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    result = session.query(station.station).all()
    st_list = list(np.ravel(result))
    return jsonify (st_list)


# 4./api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days= 365)
    year_temp = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= year_ago, measurement.station == 'USC00519281').\
         order_by(measurement.tobs).all()
    yr_temp = {date : t for date , t in year_temp}
    return jsonify(yr_temp)


# 5./api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route ("/api/v1.0/<start>")
@app.route ("/api/v1.0/<start>/<end>")
def cal_temps(start=None,end=None):
    if not end:
        result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

        temps = list(np.ravel(result))
        s_min = temps[0]
        s_avg = temps[1]
        s_max = temps[2]
        s_dict = {'TMIN': s_min, 'TAVG': s_avg, 'TMAX': s_max}
        return jsonify (s_dict)
    
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start, measurement.date <= end).all()
    
    temps = list(np.ravel(result))
    se_min = temps[0]
    se_avg = temps[1]
    se_max = temps[2]
    se_dict = {'TMIN': se_min, 'TAVG': se_avg, 'TMAX': se_max}
    return jsonify (se_dict)
           
            
# Define main behavior
if __name__ == "__main__":
   app.run(debug=True)



