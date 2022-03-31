'''
Created on 22 Jan 2017

@author: aonghus
'''
import platform
import os
from flask import Flask, render_template, request
from flask.helpers import url_for
from jinja2 import Template
from sqlalchemy import create_engine, engine
import pandas as pd
from datetime import datetime
import time

import requests
import json
from pymysql import connect

def main():
    print("The platform is", platform.platform())
    return

app = Flask(__name__)

@app.route('/t')
def indexFrame():
    return app.send_static_file('index.html')

@app.route('/test')
def test():
    return app.send_static_file('test.html')

@app.route('/')
def get_dt():
    return render_template("tindex.html")

@app.route('/prediction/<int:station_id>')
def get_prediction(station_id):
    engine = create_engine("mysql+pymysql://admin:a123456789@database.c9wohqhfjk3g.eu-west-1.rds.amazonaws.com/project",echo=True)
    sql = f"""
        SELECT number, lastupdate, available_bikes FROM project.bikestation_predict
        where number = {station_id}
    """
    df = pd.read_sql_query(sql, engine)
    return df.to_json(orient = 'records')


@app.route('/occupancy/<int:station_id>')
def get_occupancy(station_id):
    # engine = create_engine("mysql+pymysql://root:root@localhost/project",echo=True)
    engine = create_engine("mysql+pymysql://admin:a123456789@database.c9wohqhfjk3g.eu-west-1.rds.amazonaws.com/project",echo=True)
    sql = f"""
        SELECT number, last_update, available_bikes, available_bike_stands FROM project.bikestation
        where number = {station_id}
    """
    df = pd.read_sql_query(sql, engine)
    # res_df = df.set_index('lastupdate').resample('1d').mean()
    # df['lastupdate'] = pd.to_datetime(df['lastupdate'])
    # res_df['lastupdate'] = res_df.index
    return df.to_json(orient = 'records')
    # return res_df.to_json(orient = 'records')

@app.route('/stations')
def stations():
    engine = create_engine("mysql+pymysql://admin:a123456789@database.c9wohqhfjk3g.eu-west-1.rds.amazonaws.com/project",echo=True)
    left = str(int(time.time() - 4000)*1000)
    sql = f"""
        SELECT * FROM project.bikestation
        where last_update > {left}
    """
    df = pd.read_sql_query(sql, engine)
    # df = pd.read_sql_table("bikestation", engine)
    return df.to_json(orient="records")


#get request from client
@app.route('/', methods=['GET', 'POST'])
def get_request():
    key = request.args.get('key', '')
    print(key)

#send a dict(as jason) to client
    d = dict(name='wwww')
    return d

if __name__ == '__main__':
    main()
    try:
        # pid = os.fork()
        pid = 1
        if pid == 0:
            print("this is child process")
            # data collection 
        else:
            print("this is parent process")
            app.run(debug=True, port=5000)
    except OSError:
        pass
        
