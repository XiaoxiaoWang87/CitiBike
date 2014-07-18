#!/usr/bin/python

import sys
import os

import csv
from types import *

import time
import datetime
import random
from random import randint

import pandas as pd
import numpy as np
import ROOT

def convertFloat(s):
    try:
        float(s)
        return float(s)
    except ValueError:
        return -999
    return float(s)


def main():
    if len(sys.argv) > 1:
        month = sys.argv[1]
    else:
        month = 'test'

    if len(sys.argv) > 2:
        outdir = sys.argv[2]
    else:
        outdir = ''

    print 'Run: ', month
    print 'OutDir: ', outdir
 
    outputpath = '/group/atlas/prj/xiaoxiao/CITI/output/demo/'+outdir
    if outdir != '':
        if not os.path.exists(outputpath):
            os.makedirs(outputpath)


    df = {}
    df[month] = pd.read_csv('/group/atlas/prj/xiaoxiao/CITI/data/'+month+'-Citi_Bike_trip_data.csv')

    df["weather"] = pd.read_csv('/group/atlas/prj/xiaoxiao/CITI/data/Weather.csv')


    f = ROOT.TFile(outputpath+'/'+month+'.root', "recreate")
    tree = {}
    tree['train'] = ROOT.TTree("citibike_train", "tree title")
    tree['evaluate'] = ROOT.TTree("citibike_evaluate", "tree title")

    # define variable getter
    user_type = np.zeros(1, dtype=float)

    trip_dur = np.zeros(1, dtype=float)
    
    start_h = np.zeros(1, dtype=float)
    start_w = np.zeros(1, dtype=float)

    start_station_lat = np.zeros(1, dtype=float)
    start_station_lon = np.zeros(1, dtype=float)
    end_station_lat = np.zeros(1, dtype=float)
    end_station_lon = np.zeros(1, dtype=float)


    # weather condition
    mean_temp = np.zeros(1, dtype=float)
    mean_wind_speed = np.zeros(1, dtype=float)
    mean_humidity = np.zeros(1, dtype=float)


    # define variable
    for k, t in tree.items():
        t.Branch('UserType',  user_type, 'UserType/D')

        t.Branch('TripDuration',  trip_dur,   'TripDuration/D')
        t.Branch('StartWhichDay',   start_w,   'StartWhichDay/D') 
        t.Branch('StartHour',  start_h,   'StartHour/D')
   
        t.Branch('StartStationLat', start_station_lat, 'StartStationLat/D')
        t.Branch('StartStationLon', start_station_lon, 'StartStationLon/D')
        t.Branch('EndStationLat', end_station_lat, 'EndStationLat/D')
        t.Branch('EndStationLon', end_station_lon, 'EndStationLon/D')

        t.Branch('MeanTemp', mean_temp, 'MeanTemp/D')
        t.Branch('MeanWindSpeed', mean_wind_speed, 'MeanWindSpeed/D')
        t.Branch('MeanHumidity', mean_humidity, 'MeanHumidity/D')


    MeanTemp = {}
    MeanWindSpeed = {}
    MeanHumidity = {}

    for index, row in df['weather'].iterrows():
        MeanTemp[row['EST']] = row['Mean TemperatureF']
        MeanWindSpeed[row['EST']] = row['Mean Wind SpeedMPH']
        MeanHumidity[row['EST']] = row['Mean Humidity']


    for index, row in df[month].iterrows():

        #print row        

        # randomly sample 1/100 of the total data
        r = randint(1,100)
        if r!=1 and r!=2:
            continue

        # clean unphysical trip duration entries
        tripDur = row['tripduration']
        if tripDur > 6000:
            continue    

        userType = row['usertype']

        tStart = time.strptime(row['starttime'], "%Y-%m-%d %H:%M:%S")
        tStop = time.strptime(row['stoptime'], "%Y-%m-%d %H:%M:%S")

        dStart = datetime.date(tStart[0], tStart[1], tStart[2]).weekday()
        dStop = datetime.date(tStop[0], tStop[1], tStop[2]).weekday()    

        startStationLat = row['start station latitude']
        startStationLon = row['start station longitude']
        endStationLat = row['end station latitude']
        endStationLon = row['end station longitude']


        # weather index
        raw_date = str(tStart[0]) + '-' + str(tStart[1]) + '-' + str(tStart[2])
        # clean unphysical weather entries
        if np.isnan(MeanWindSpeed[raw_date]) or MeanWindSpeed[raw_date]<0 or np.isnan(MeanTemp[raw_date]) or np.isnan(MeanHumidity[raw_date]):
            continue

        meanTemp = convertFloat(MeanTemp[raw_date])
        meanWindSpeed = convertFloat(MeanWindSpeed[raw_date])
        meanHumidity = convertFloat(MeanHumidity[raw_date])


        # fill variables
        if userType == 'Subscriber':
            user_type[0] = 0
        elif userType == 'Customer':
            user_type[0] = 1    

        trip_dur[0] = tripDur
        start_w[0] = dStart
        start_h[0] = tStart[3]

        start_station_lat[0] = startStationLat
        start_station_lon[0] = startStationLon
    
        end_station_lat[0] = endStationLat
        end_station_lon[0] = endStationLon


        mean_temp[0] = meanTemp
        mean_wind_speed[0] = meanWindSpeed
        mean_humidity[0] = meanHumidity
    
        if r == 1:
            tree['train'].Fill()
        elif r == 2:
            tree['evaluate'].Fill()

        #random.seed(tripDur*endStationLon)

    f.Write()
    f.Close()

if __name__ == '__main__':
    main()

