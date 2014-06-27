#!/usr/bin/python

import sys
import os
import numpy as np
import csv
import time
import datetime
from types import *

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
 
    outputpath = '/group/atlas/prj/xiaoxiao/CITI/output/'+outdir
    if outdir != '':
        if not os.path.exists(outputpath):
            os.makedirs(outputpath)


    reader = {}
    reader[month] = csv.DictReader(open('/group/atlas/prj/xiaoxiao/CITI/data/'+month+'-Citi_Bike_trip_data.csv'))

    reader["weather"] = csv.DictReader(open('/group/atlas/prj/xiaoxiao/CITI/data/Weather.csv'))

    f = ROOT.TFile(outputpath+'/'+month+'.root', "recreate")
    t = ROOT.TTree("citibike", "tree title")

    bike_id = np.zeros(1, dtype=float)
    trip_dur = np.zeros(1, dtype=float)
    #user_type = np.zeros(1, dtype=str)
    user_type = ROOT.std.vector( ROOT.std.string )()
    user_type.push_back('')
    user_birth = np.zeros(1, dtype=float)
    user_age = np.zeros(1, dtype=float)
    user_gender = np.zeros(1, dtype=float)
    
    start_station_id = np.zeros(1, dtype=float)
    #start_station_name = np.zeros(1, dtype=str)
    start_station_name = ROOT.std.vector( ROOT.std.string )()
    start_station_name.push_back('')
    start_station_lat = np.zeros(1, dtype=float)
    start_station_lon = np.zeros(1, dtype=float)
    start_y = np.zeros(1, dtype=float)
    start_m = np.zeros(1, dtype=float)
    start_d = np.zeros(1, dtype=float)
    start_h = np.zeros(1, dtype=float)
    start_min = np.zeros(1, dtype=float)
    start_s = np.zeros(1, dtype=float)
    start_w = np.zeros(1, dtype=float)  

    end_station_id = np.zeros(1, dtype=float)
    #end_station_name = np.zeros(1, dtype=str)
    end_station_name = ROOT.std.vector( ROOT.std.string )()
    end_station_name.push_back('')
    end_station_lat = np.zeros(1, dtype=float)
    end_station_lon = np.zeros(1, dtype=float)
    end_y = np.zeros(1, dtype=float)
    end_m = np.zeros(1, dtype=float)
    end_d = np.zeros(1, dtype=float)
    end_h = np.zeros(1, dtype=float)
    end_min = np.zeros(1, dtype=float)
    end_s = np.zeros(1, dtype=float)
    end_w = np.zeros(1, dtype=float)
    
    # weather condition
    max_temp = np.zeros(1, dtype=float)
    mean_temp = np.zeros(1, dtype=float)
    min_temp = np.zeros(1, dtype=float)
    max_wind_speed = np.zeros(1, dtype=float)
    mean_wind_speed = np.zeros(1, dtype=float)
    precipitation_in = np.zeros(1, dtype=float)
    max_humidity = np.zeros(1, dtype=float)
    mean_humidity = np.zeros(1, dtype=float)
    event_condition = ROOT.std.vector( ROOT.std.string )() 
    event_condition.push_back('')

    max_temp_15to = np.zeros(1, dtype=float)
    max_temp_25to = np.zeros(1, dtype=float)
    max_temp_35to = np.zeros(1, dtype=float)
    max_temp_45to = np.zeros(1, dtype=float)
    max_temp_55to = np.zeros(1, dtype=float)
    max_temp_65to = np.zeros(1, dtype=float)
    max_temp_75to = np.zeros(1, dtype=float)
    max_temp_85to = np.zeros(1, dtype=float)
    max_temp_95to = np.zeros(1, dtype=float)
    max_temp_20to = np.zeros(1, dtype=float)
    max_temp_30to = np.zeros(1, dtype=float)
    max_temp_40to = np.zeros(1, dtype=float)
    max_temp_50to = np.zeros(1, dtype=float)
    max_temp_60to = np.zeros(1, dtype=float)
    max_temp_70to = np.zeros(1, dtype=float)
    max_temp_80to = np.zeros(1, dtype=float)
    max_temp_90to = np.zeros(1, dtype=float)

    t.Branch('BikeId',  bike_id,   'BikeId/D')
    t.Branch('TripDuration',  trip_dur,   'TripDuration/D')
    t.Branch('UserType',  user_type) #, 'UserType/C')
    t.Branch('UserBirth', user_birth, 'UserBirth/D')
    t.Branch('UserAge', user_age, 'UserAge/D')
    t.Branch('UserGender',user_gender, 'UserGender/D')
    
    t.Branch('StartStationId', start_station_id, 'StartStationId/D')
    t.Branch('StartStationName', start_station_name) #, 'StartStationName/C')
    t.Branch('StartStationLat', start_station_lat, 'StartStationLat/D')
    t.Branch('StartStationLon', start_station_lon, 'StartStationLon/D')
    t.Branch('StartYear',  start_y,   'StartYear/D')
    t.Branch('StartMonth', start_m,   'StartMonth/D')
    t.Branch('StartDay',   start_d,   'StartDay/D')
    t.Branch('StartHour',  start_h,   'StartHour/D')
    t.Branch('StartMin',   start_min, 'StartMin/D')
    t.Branch('StartSec',   start_s,   'StartSec/D')
    t.Branch('StartWorkDay',   start_w,   'StartWorkDay/D')    

    t.Branch('EndStationId', end_station_id, 'EndStationId/D')
    t.Branch('EndStationName', end_station_name) #, 'EndStationName/C')
    t.Branch('EndStationLat', end_station_lat, 'EndStationLat/D')
    t.Branch('EndStationLon', end_station_lon, 'EndStationLon/D')
    t.Branch('EndYear',    end_y,   'EndYear/D')
    t.Branch('EndMonth',   end_m,   'EndMonth/D')
    t.Branch('EndDay',     end_d,   'EndDay/D')
    t.Branch('EndHour',    end_h,   'EndHour/D')
    t.Branch('EndMin',     end_min, 'EndMin/D')
    t.Branch('EndSec',     end_s,   'EndSec/D')
    t.Branch('EndWorkDay',   end_w,   'EndWorkDay/D')
    
    t.Branch('MaxTemp', max_temp, 'MaxTemp/D') 
    t.Branch('MeanTemp', mean_temp, 'MeanTemp/D')
    t.Branch('MinTemp', min_temp, 'MinTemp/D') 
    t.Branch('MaxWindSpeed', max_wind_speed, 'MaxWindSpeed/D')
    t.Branch('MeanWinSpeed', mean_wind_speed, 'MeanWinSpeed/D')
    t.Branch('Precipitation', precipitation_in, 'Precipitation/D')
    t.Branch('MaxHumidity', max_humidity, 'MaxHumidity/D')
    t.Branch('MeanHumidity', mean_humidity, 'MeanHumidity/D')
    t.Branch('Events', event_condition)

    t.Branch('MaxTemp15to', max_temp_15to, 'MaxTemp15to/D')
    t.Branch('MaxTemp25to', max_temp_25to, 'MaxTemp25to/D')
    t.Branch('MaxTemp35to', max_temp_35to, 'MaxTemp35to/D')
    t.Branch('MaxTemp45to', max_temp_45to, 'MaxTemp45to/D')
    t.Branch('MaxTemp55to', max_temp_55to, 'MaxTemp55to/D')
    t.Branch('MaxTemp65to', max_temp_65to, 'MaxTemp65to/D')
    t.Branch('MaxTemp75to', max_temp_75to, 'MaxTemp75to/D')
    t.Branch('MaxTemp85to', max_temp_85to, 'MaxTemp85to/D')
    t.Branch('MaxTemp95to', max_temp_95to, 'MaxTemp95to/D')
    t.Branch('MaxTemp20to', max_temp_20to, 'MaxTemp20to/D')
    t.Branch('MaxTemp30to', max_temp_30to, 'MaxTemp30to/D')
    t.Branch('MaxTemp40to', max_temp_40to, 'MaxTemp40to/D')
    t.Branch('MaxTemp50to', max_temp_50to, 'MaxTemp50to/D')
    t.Branch('MaxTemp60to', max_temp_60to, 'MaxTemp60to/D')
    t.Branch('MaxTemp70to', max_temp_70to, 'MaxTemp70to/D')
    t.Branch('MaxTemp80to', max_temp_80to, 'MaxTemp80to/D')
    t.Branch('MaxTemp90to', max_temp_90to, 'MaxTemp90to/D')
    

    MeanTemp = {}
    MaxTemp = {}
    MinTemp = {}
    MaxWindSpeed = {}
    MeanWindSpeed = {}
    PrecipitationIn = {}
    MaxHumidity = {}
    MeanHumidity = {}
    Events = {}

    for row in reader['weather']:
        MaxTemp[row['EST']] = row['Max TemperatureF']
        MeanTemp[row['EST']] = row['Mean TemperatureF']
        MinTemp[row['EST']] = row['Min TemperatureF']
        MaxWindSpeed[row['EST']] = row['Max Wind SpeedMPH']
        MeanWindSpeed[row['EST']] = row['Mean Wind SpeedMPH']
        PrecipitationIn[row['EST']] = row['PrecipitationIn']
        MaxHumidity[row['EST']] = row['Max Humidity']
        MeanHumidity[row['EST']] = row['Mean Humidity']    
        Events[row['EST']] = row['Events']

        whatTemp = convertFloat(row['Max TemperatureF'])

        if whatTemp>=15 and whatTemp<20:
            max_temp_15to[0] +=1
        elif whatTemp>=20 and whatTemp<25:
            max_temp_20to[0] +=1
        elif whatTemp>=25 and whatTemp<30:
            max_temp_25to[0] +=1
        elif whatTemp>=30 and whatTemp<35:
            max_temp_30to[0] +=1
        elif whatTemp>=35 and whatTemp<40:
            max_temp_35to[0] +=1
        elif whatTemp>=40 and whatTemp<45:
            max_temp_40to[0] +=1
        elif whatTemp>=45 and whatTemp<50:
            max_temp_45to[0] +=1
        elif whatTemp>=50 and whatTemp<55:
            max_temp_50to[0] +=1
        elif whatTemp>=55 and whatTemp<60:
            max_temp_55to[0] +=1
        elif whatTemp>=60 and whatTemp<65:
            max_temp_60to[0] +=1
        elif whatTemp>=65 and whatTemp<70:
            max_temp_65to[0] +=1
        elif whatTemp>=70 and whatTemp<75:
            max_temp_70to[0] +=1
        elif whatTemp>=75 and whatTemp<80:
            max_temp_75to[0] +=1
        elif whatTemp>=80 and whatTemp<85:
            max_temp_80to[0] +=1
        elif whatTemp>=85 and whatTemp<90:
            max_temp_85to[0] +=1
        elif whatTemp>=90 and whatTemp<95:
            max_temp_90to[0] +=1
        elif whatTemp>=95 and whatTemp<100:
            max_temp_95to[0] +=1

        

    for row in reader[month]:
    
        print row
        # get variables
        bikeId = row['bikeid']
        tripDur = row['tripduration']
        userType = row['usertype']
        if row['birth year'] != '\N':
            userBirth = row['birth year']
        else:
            userBirth = 2014
        userGen = row['gender'] 
    
        tStart = time.strptime(row['starttime'], "%Y-%m-%d %H:%M:%S")
        tStop = time.strptime(row['stoptime'], "%Y-%m-%d %H:%M:%S")

        dStart = datetime.date(tStart[0], tStart[1], tStart[2]).weekday()
        dStop = datetime.date(tStop[0], tStop[1], tStop[2]).weekday()    

        startStationId = row['start station id']
        startStationName = row['start station name']
        startStationLat = row['start station latitude']
        startStationLon = row['start station longitude']
    
        endStationId = row['end station id']
        endStationName = row['end station name']
        endStationLat = row['end station latitude']
        endStationLon = row['end station longitude']


        # weather index
        raw_date = str(tStart[0]) + '-' + str(tStart[1]) + '-' + str(tStart[2])
        maxTemp = convertFloat(MaxTemp[raw_date])
        meanTemp = convertFloat(MeanTemp[raw_date])
        minTemp = convertFloat(MinTemp[raw_date])
        maxWindSpeed = convertFloat(MaxWindSpeed[raw_date])
        meanWindSpeed = convertFloat(MeanWindSpeed[raw_date])
        precipitationIn = convertFloat(PrecipitationIn[raw_date])
        maxHumidity = convertFloat(MaxHumidity[raw_date])
        meanHumidity = convertFloat(MeanHumidity[raw_date])  
        events = Events[raw_date]    

        # fill variables
        bike_id[0] =  bikeId
        trip_dur[0] = tripDur
        user_type[0] = userType
        user_birth[0] = userBirth
        user_age[0] = 2014 - float(userBirth)
        user_gender[0] = userGen
    
        start_y[0] = tStart[0]
        start_m[0] = tStart[1]
        start_d[0] = tStart[2]
        start_h[0] = tStart[3]
        start_min[0] = tStart[4]
        start_s[0] = tStart[5]
        start_w[0] = dStart

        end_y[0] = tStop[0]
        end_m[0] = tStop[1]
        end_d[0] = tStop[2]
        end_h[0] = tStop[3]
        end_min[0] = tStop[4]
        end_s[0] = tStop[5]
        end_w[0] = dStop

        start_station_id[0] = startStationId
        start_station_name[0] = startStationName
        start_station_lat[0] = startStationLat
        start_station_lon[0] = startStationLon
    
        end_station_id[0] = endStationId
        end_station_name[0] = endStationName
        end_station_lat[0] = endStationLat
        end_station_lon[0] = endStationLon
    

        max_temp[0] = maxTemp
        mean_temp[0] = meanTemp
        min_temp[0] = minTemp
        max_wind_speed[0] = maxWindSpeed
        mean_wind_speed[0] = meanWindSpeed
        precipitation_in[0] = precipitationIn
        max_humidity[0] = maxHumidity
        mean_humidity[0] = meanHumidity
        event_condition[0] = events
    
        t.Fill()

        ## items() function returns a list of (key,value) tuples
        #for column, value in row.items():
            #print column, value
        #    result.setdefault(column, []).append(value)
    f.Write()
    f.Close()

if __name__ == '__main__':
    main()

