#!/bin/sh
cd `dirname $0` || exit 1
/home/ubuntu/anaconda3/envs/comp30830/bin/python3.6 Current_Weather.py >> run.log 2>&1     
/home/ubuntu/anaconda3/envs/comp30830/bin/python3.6 BikeStations.py >> run.log 2>&1        
/home/ubuntu/anaconda3/envs/comp30830/bin/python3.6 forecast_bikestation.py >> run.log 2>&1