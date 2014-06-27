#!/usr/bin/python

from __future__ import division
import sys
import os
import numpy as np
import csv
from collections import defaultdict
import operator

import ROOT
from ROOT import *
import AtlasStyle
import PlottingUtls as Plt

import matplotlib.pyplot as plt


class Hist:
    def __init__(self, name):
        self.h_ride_weekday = TH1F("ride_weekday", "ride_weekday", 24, 0, 24) 
        self.h_ride_weekend = TH1F("ride_weekend", "ride_weekend", 24, 0, 24)
        self.h_ride_customer_weekday = TH1F("ride_customer_weekday", "ride_customer_weekday", 24, 0, 24)
        self.h_ride_customer_weekend = TH1F("ride_customer_weekend", "ride_customer_weekend", 24, 0, 24)

        self.h_temp_rwday_weekday = TH1F("temp_rwday_weekday", "temp_rwday_weekday", 8, 20, 100);

        self.h_ride_annual_20to30_weekday = TH1F("ride_annual_20to30_weekday", "ride_annual_20to30_weekday", 24, 0, 24)

        self.h_duration_men = TH1F("duration_men", "duration_men", 20, 0, 60)
        self.h_duration_women = TH1F("duration_women", "duration_women", 20, 0, 60)
 
        self.h_age_men = TH1F("age_men", "age_men", 70, 15, 85)
        self.h_age_women = TH1F("age_women", "age_women", 70, 15, 85)

        self.h_ride_20to30_weekday = TH1F("ride_20to30_weekday", "ride_20to30_weekday", 24, 0, 24)
        self.h_ride_30to40_weekday = TH1F("ride_30to40_weekday", "ride_30to40_weekday", 24, 0, 24)
        self.h_ride_40to50_weekday = TH1F("ride_40to50_weekday", "ride_40to50_weekday", 24, 0, 24)
        self.h_ride_50to_weekday = TH1F("ride_50to_weekday", "ride_50to_weekday", 24, 0, 24)

        self.h2_ride_lat_lon_am_weekday = TH2F("ride_lat_lon_am_weekday", "ride_lat_lon_am_weekday", 35, -74.02, -73.96, 35, 40.675, 40.775)
        self.h2_ride_lat_lon_pm_weekday = TH2F("ride_lat_lon_pm_weekday", "ride_lat_lon_pm_weekday", 35, -74.02, -73.96, 35, 40.675, 40.775)

        self.g1_diff_weekday = TGraph()
        self.g2_diff_weekday = TGraph()
        self.g3_diff_weekday = TGraph()
        self.g4_diff_weekday = TGraph()
        self.g5_diff_weekday = TGraph()
        self.g6_diff_weekday = TGraph()
        self.g7_diff_weekday = TGraph()
        self.g8_diff_weekday = TGraph()
        self.g9_diff_weekday = TGraph()
        self.g10_diff_weekday = TGraph()

class Count:
    def __init__(self, name):
        self.men = 0
        self.women = 0

        self.below20 = 0
        self.from20to30 = 0
        self.from30to40 = 0
        self.from40to50 = 0
        self.from50to60 = 0
        self.from60above = 0

        self.subscriber = 0
        self.customer = 0

class StationInfo:
    def __init__(self, name, lon, lat):
        self.station = name
        self.longitude = lon
        self.latitude = lat
        self.annual_start_am_weekday = 0
        self.annual_end_am_weekday = 0
        self.customer_start_weekend = 0
        self.customer_end_weekend = 0

        self.start_weekday = [0]*12
        self.end_weekday = [0]*12
        self.diff_weekday = [0]*12

        self.incl_annual_start_am_weekday = 0
        self.incl_annual_start_pm_weekday = 0
        self.incl_annual_start_weekday = 0
        self.incl_annual_start_weekend = 0
 
        self.incl_annual_end_am_weekday = 0
        self.incl_annual_end_pm_weekday = 0
        self.incl_annual_end_weekday = 0
        self.incl_annual_end_weekend = 0

        self.incl_customer_start_weekday = 0
        self.incl_customer_start_weekend = 0
        self.incl_customer_end_weekday = 0
        self.incl_customer_end_weekend = 0


def calcPoissonCL(h):
    for b in xrange(1,h.GetNbinsX()+1):
        upper = h.GetBinContent(b) + sqrt(h.GetBinContent(b)+0.25) + 0.5
        lower = h.GetBinContent(b) - sqrt(h.GetBinContent(b)+0.25) + 0.5
        approx = sqrt(h.GetBinContent(b))
        h.SetBinError(b, approx)

def accumu(lis):
    total = 0
    new_lis=[]
    for x in lis:
        total += x
        new_lis.append(round(total,2))
    return new_lis


def getWeight(temp, e):
    #if temp>=15 and temp<20:
    #    return e.MaxTemp15to
    #elif temp>=20 and temp<25:
    #    return e.MaxTemp20to
    #elif temp>=25 and temp<30:
    #    return e.MaxTemp25to
    #elif temp>=30 and temp<35:
    #    return e.MaxTemp30to
    #elif temp>=35 and temp<40:
    #    return e.MaxTemp35to
    #elif temp>=40 and temp<45:
    #    return e.MaxTemp40to
    #elif temp>=45 and temp<50:
    #    return e.MaxTemp45to
    #elif temp>=50 and temp<55:
    #    return e.MaxTemp50to
    #elif temp>=55 and temp<60:
    #    return e.MaxTemp55to
    #elif temp>=60 and temp<65:
    #    return e.MaxTemp60to
    #elif temp>=65 and temp<70:
    #    return e.MaxTemp65to
    #elif temp>=70 and temp<75:
    #    return e.MaxTemp70to
    #elif temp>=75 and temp<80:
    #    return e.MaxTemp75to
    #elif temp>=80 and temp<85:
    #    return e.MaxTemp80to
    #elif temp>=85 and temp<90:
    #    return e.MaxTemp85to
    #elif temp>=90 and temp<95:
    #    return e.MaxTemp90to
    #elif temp>=95 and temp<100:
    #    return e.MaxTemp95to
    #else:
    #    return -1
    if temp>=15 and temp<20:
        return e.MaxTemp15to
    elif temp>=20 and temp<30:
        return e.MaxTemp20to + e.MaxTemp25to
    elif temp>=30 and temp<40:
        return e.MaxTemp30to + e.MaxTemp35to
    elif temp>=40 and temp<50:
        return e.MaxTemp40to + e.MaxTemp45to
    elif temp>=50 and temp<60:
        return e.MaxTemp50to + e.MaxTemp55to
    elif temp>=60 and temp<70:
        return e.MaxTemp60to + e.MaxTemp65to
    elif temp>=70 and temp<80:
        return e.MaxTemp70to + e.MaxTemp75to
    elif temp>=80 and temp<90:
        return e.MaxTemp80to + e.MaxTemp85to
    elif temp>=90 and temp<100:
        return e.MaxTemp90to + e.MaxTemp95to
    else:
        return -1



def main():
    if len(sys.argv) > 1:
        outdir = sys.argv[1]
    else:
        outdir = ''

    print 'OutDir: ', outdir

    outputpath = '/group/atlas/prj/xiaoxiao/CITI/plots/'+outdir
    if outdir != '':
        if not os.path.exists(outputpath):
            os.makedirs(outputpath)


    hist = {}
    count = {}
    hist['data'] = Hist('data')
    count['data'] = Count('data')

    sstat = {}

    unique_weekday = []
    unique_weekend = []

    # do error properly
    for key, h in hist['data'].__dict__.items(): #dir(hist['data']):
        if not key.startswith("__") and not key.startswith('g'): #if not callable(h) and not h.startswith("__"):
            #print key
            h.Sumw2() 

    file = {}
    file['data'] = TFile('../output/data.root')
    #file['data'] = TFile('../output/2014-02.root')
    #file['data'] = TFile('../output/test.root')

    tree = file['data'].Get('citibike')
    for e in tree:
        try:
            sstat[e.StartStationName[0]]
        except KeyError:
            sstat[e.StartStationName[0]] = StationInfo(e.StartStationName[0], e.StartStationLon, e.StartStationLat)
        try:
            sstat[e.EndStationName[0]]
        except KeyError:
            sstat[e.EndStationName[0]] = StationInfo(e.EndStationName[0], e.EndStationLon, e.EndStationLat)

        if e.EndWorkDay == 5 or e.EndWorkDay == 6:   # weekend
            if e.UserType[0]=="Subscriber":
                hist['data'].h_ride_weekend.Fill(e.EndHour, 1)
                sstat[e.StartStationName[0]].incl_annual_start_weekend +=1
                sstat[e.EndStationName[0]].incl_annual_end_weekend +=1
            elif e.UserType[0]=="Customer":
                hist['data'].h_ride_customer_weekend.Fill(e.EndHour, 1)
                sstat[e.StartStationName[0]].incl_customer_start_weekend +=1
                sstat[e.EndStationName[0]].incl_customer_end_weekend +=1
                if e.EndHour>=11 and e.EndHour<=17:
                    sstat[e.StartStationName[0]].customer_start_weekend +=1
                    sstat[e.EndStationName[0]].customer_end_weekend +=1
            unique_weekend.append(str(e.EndYear)+'-'+str(e.EndMonth)+'-'+str(e.EndDay))
        else:   # weekday
            if e.UserType[0]=="Subscriber":
                hist['data'].h_ride_weekday.Fill(e.EndHour, 1)
                sstat[e.StartStationName[0]].incl_annual_start_weekday +=1
                sstat[e.EndStationName[0]].incl_annual_end_weekday +=1      
            elif e.UserType[0]=="Customer":
                hist['data'].h_ride_customer_weekday.Fill(e.EndHour, 1)            
                sstat[e.StartStationName[0]].incl_customer_start_weekday +=1
                sstat[e.EndStationName[0]].incl_customer_end_weekday +=1

            if e.EndHour>=9 and e.EndHour<=11 and e.UserType[0]=="Subscriber":
                hist['data'].h2_ride_lat_lon_am_weekday.Fill(e.EndStationLon,e.EndStationLat, 1)
                sstat[e.StartStationName[0]].annual_start_am_weekday +=1
                sstat[e.EndStationName[0]].annual_end_am_weekday +=1
	    elif e.EndHour>=21 and e.EndHour<=23 and e.UserType[0]=="Subscriber":
                hist['data'].h2_ride_lat_lon_pm_weekday.Fill(e.EndStationLon,e.EndStationLat, 1)

            if e.StartHour>=6 and e.StartHour<=12 and e.UserType[0]=="Subscriber":
                sstat[e.StartStationName[0]].incl_annual_start_am_weekday +=1
            elif e.StartHour>=17 and e.StartHour<=23 and e.UserType[0]=="Subscriber":
                sstat[e.StartStationName[0]].incl_annual_start_pm_weekday +=1
            if e.EndHour>=6 and e.EndHour<=12 and e.UserType[0]=="Subscriber":
                sstat[e.EndStationName[0]].incl_annual_end_am_weekday +=1
            elif e.EndHour>=17 and e.EndHour<=23 and e.UserType[0]=="Subscriber":
                sstat[e.EndStationName[0]].incl_annual_end_pm_weekday +=1
            


            for i in range(12):
                if e.StartHour>=11+i*0.5 and e.StartHour<11+(i+1)*0.5:
                    sstat[e.StartStationName[0]].start_weekday[i] +=1

                if e.EndHour>=11+i*0.5 and e.EndHour<11+(i+1)*0.5:
                    sstat[e.EndStationName[0]].end_weekday[i] +=1


            #if e.UserType[0]=="Subscriber":
            weight = 1.0/getWeight(e.MaxTemp,e)
            hist['data'].h_temp_rwday_weekday.Fill(e.MaxTemp, weight)
         

            if e.UserAge>=20 and e.UserAge<30:
                hist['data'].h_ride_20to30_weekday.Fill(e.EndHour, 1) 
                if e.UserType[0] == "Subscriber":
                    hist['data'].h_ride_annual_20to30_weekday.Fill(e.EndHour, 1)          
            elif e.UserAge>=30 and e.UserAge<40:    
                hist['data'].h_ride_30to40_weekday.Fill(e.EndHour, 1)
            elif e.UserAge>=40 and e.UserAge<50:
                hist['data'].h_ride_40to50_weekday.Fill(e.EndHour, 1)            
            elif e.UserAge>=50:
                hist['data'].h_ride_50to_weekday.Fill(e.EndHour, 1) 
         
            unique_weekday.append(str(e.EndYear)+'-'+str(e.EndMonth)+'-'+str(e.EndDay))

        # Gender
        if e.UserGender == 2:
            count['data'].women = count['data'].women + 1
            hist['data'].h_duration_women.Fill(e.TripDuration/60.0, 1)
            hist['data'].h_age_women.Fill(e.UserAge, 1)
        elif e.UserGender == 1:
            count['data'].men = count['data'].men + 1
            hist['data'].h_duration_men.Fill(e.TripDuration/60.0, 1)
            hist['data'].h_age_men.Fill(e.UserAge, 1)    

        # Age
        if e.UserAge<20:
            count['data'].below20 = count['data'].below20 + 1
        elif e.UserAge>=20 and e.UserAge<30:
            count['data'].from20to30 = count['data'].from20to30 + 1
        elif e.UserAge>=30 and e.UserAge<40:
            count['data'].from30to40 = count['data'].from30to40 + 1
        elif e.UserAge>=40 and e.UserAge<50:
            count['data'].from40to50 = count['data'].from40to50 + 1
        elif e.UserAge>=50 and e.UserAge<60:
            count['data'].from50to60 = count['data'].from50to60 + 1
        elif e.UserAge>=60:
            count['data'].from60above = count['data'].from60above + 1
   
        # Type
        if e.UserType[0] == 'Subscriber':
            count['data'].subscriber = count['data'].subscriber + 1
        elif e.UserType[0] == 'Customer': 
            count['data'].customer = count['data'].customer + 1

        # Begin a time series analysis here: 
        #date = str(int(e.EndMonth))+'/'+str(int(e.EndDay))+'/'+str(int(e.EndYear))
        #if date not in count:
        #    count[date]=Count(date)
        #if e.UserGender==2:
        #    count[date].women = count[date].women + 1
        #elif e.UserGender==1:
        #    count[date].men = count[date].men + 1

    #file1 = open(outputpath+"/date.txt", "w")
    #file2 = open(outputpath+"/n_female_riders.txt", "w")
    #file3 = open(outputpath+"/n_male_riders.txt", "w")
    #for key in count.keys():
    #    if key=='data':
    #        continue
    #    else:
    #        file1.write(key + '\n')
    #        file2.write(str(count[key].women) + '\n')
    #        file3.write(str(count[key].men) + '\n')
    #file1.close()
    #file2.close()
    #file3.close()


    #Plt.DrawTwoHistOverlay(hist['data'].h_ride_weekday,hist['data'].h_ride_weekend, "Weekday", "Weekend", "Hour", "Number of Rides", False, False, 0, outputpath+"/DrawWeekdayWeekendOverlay.pdf")
    #Plt.DrawTwoHistOverlay(hist['data'].h_ride_weekday,hist['data'].h_ride_customer_weekday, "Subscriber", "Customer", "Hour", "Arbitrary Unit", True, False, 2, outputpath+"/DrawSubCusOverlayWeekday.pdf")
    #Plt.DrawTwoHistOverlay(hist['data'].h_ride_weekend,hist['data'].h_ride_customer_weekend, "Subscriber", "Customer", "Hour", "Arbitrary Unit", True, False, 2, outputpath+"/DrawSubCusOverlayWeekend.pdf")

    ##Plt.DrawTwoHistOverlay(hist['data'].h_duration_men,hist['data'].h_duration_women, "Men", "Women", "Trip Duration [min]", "Arbitrary Unit", True, True, 0, outputpath+"/CitiBikeTest2.pdf")
    
    ##Plt.DrawFourHistOverlay(hist['data'].h_ride_20to30_weekday,hist['data'].h_ride_30to40_weekday,hist['data'].h_ride_40to50_weekday,hist['data'].h_ride_50to_weekday, "20to30","30to40","40to50","50 above", "Hour", "Number of Rides", True, False, 0, outputpath+"/CitiBikeTest3.pdf")

    #Plt.DrawTwoHistOverlay(hist['data'].h_age_men,hist['data'].h_age_women, "Male Riders", "Female Riders", "Age", "Arbitrary Unit", True, False, 1, outputpath+"/DrawAge_OverlaySex.pdf")

    #Plt.Draw2DHist(hist['data'].h2_ride_lat_lon_am_weekday, "","Longitude", "Latitude", False, False, 0, outputpath+"/Draw2DAmWorkday.pdf")
    #Plt.Draw2DHist(hist['data'].h2_ride_lat_lon_pm_weekday, "","Longitude", "Latitude", False, False, 0, outputpath+"/Draw2DPmWorkday.pdf")

    #stats = defaultdict(list)
    #names = defaultdict(list)
    #colors = defaultdict(list)
    
    #Gender
    #stats['gender'].append(count['data'].men)
    #stats['gender'].append(count['data'].women)
    #names['gender'].append('Male Riders')
    #names['gender'].append('Female Riders')
    #colors['gender'].append('#00FFFF')
    #colors['gender'].append('#FF66FF')
    #Plt.DrawPieChart(stats['gender'], names['gender'], colors['gender'], [0,0], False, outputpath+"/PieGender.pdf")

    #Age
    #stats['age'].append(count['data'].below20)
    #stats['age'].append(count['data'].from20to30)
    #stats['age'].append(count['data'].from30to40)
    #stats['age'].append(count['data'].from40to50)
    #stats['age'].append(count['data'].from50to60)
    #stats['age'].append(count['data'].from60above)
    #names['age'].append('Below 20')
    #names['age'].append('20 to 30')
    #names['age'].append('30 to 40')
    #names['age'].append('40 to 50')
    #names['age'].append('50 to 60')
    #names['age'].append('60 Above')
    #colors['age'].append('#FFFFCC')
    #colors['age'].append('#FF6633')
    #colors['age'].append('#66FF99')
    #colors['age'].append('#0066FF')
    #colors['age'].append('#9999FF')
    #colors['age'].append('#FFFFFF')
    #Plt.DrawPieChart(stats['age'], names['age'], colors['age'], [0,0,0,0,0,0], False, outputpath+"/PieAge.pdf")
    
    #Type
    #stats['type'].append(count['data'].subscriber)
    #stats['type'].append(count['data'].customer)
    #names['type'].append('Annual Members')
    #names['type'].append('24-hour/7-day Pass Users')
    #colors['type'].append('#FFFFCC')
    #colors['type'].append('#FFFFFF')
    #Plt.DrawPieChart(stats['type'], names['type'], colors['type'], [0,0], True, outputpath+"/PieType.pdf")
    

    # Begin a counting analysis
    n_weekdays = len(set(unique_weekday))
    n_weekends = len(set(unique_weekend))

    list_objects = []
    for key, value in sstat.iteritems():
        value.annual_start_am_weekday = round(value.annual_start_am_weekday/n_weekdays/2.0, 2)
        value.annual_end_am_weekday = round(value.annual_end_am_weekday/n_weekdays/2.0, 2)
        value.customer_start_weekend = round(value.customer_start_weekend/n_weekends/6.0, 2)
        value.customer_end_weekend = round(value.customer_end_weekend/n_weekends/6.0, 2)

        value.incl_annual_start_am_weekday = round(value.incl_annual_start_am_weekday/n_weekdays/6.0, 2)
        value.incl_annual_start_pm_weekday = round(value.incl_annual_start_pm_weekday/n_weekdays/6.0, 2)
        value.incl_annual_start_weekday = round(value.incl_annual_start_weekday/n_weekdays/24.0, 2)
        value.incl_annual_start_weekend = round(value.incl_annual_start_weekend/n_weekends/24.0, 2)

        value.incl_annual_end_am_weekday = round(value.incl_annual_end_am_weekday/n_weekdays/6.0, 2)
        value.incl_annual_end_pm_weekday = round(value.incl_annual_end_pm_weekday/n_weekdays/6.0, 2)
        value.incl_annual_end_weekday = round(value.incl_annual_end_weekday/n_weekdays/24.0, 2)
        value.incl_annual_end_weekend = round(value.incl_annual_end_weekend/n_weekends/24.0, 2)

        value.incl_customer_start_weekday = round(value.incl_customer_start_weekday/n_weekdays/24.0, 2)
        value.incl_customer_start_weekend = round(value.incl_customer_start_weekend/n_weekends/24.0, 2)
        value.incl_customer_end_weekday  = round(value.incl_customer_end_weekday/n_weekdays/24.0, 2)
        value.incl_customer_end_weekend  = round(value.incl_customer_end_weekend/n_weekends/24.0, 2)


        for i in range(len(value.start_weekday)):
            value.start_weekday[i] = round(value.start_weekday[i]/n_weekdays, 2)
            value.end_weekday[i] = round(value.end_weekday[i]/n_weekdays, 2)
            value.diff_weekday[i] =  round(value.end_weekday[i] - value.start_weekday[i], 2) 
        value.diff_weekday = accumu(value.diff_weekday)

        list_objects.append(value)

    sorted_pop_annual_start_am_weekday = sorted(list_objects, key=lambda object: object.annual_start_am_weekday, reverse=True)
    sorted_pop_annual_end_am_weekday = sorted(list_objects, key=lambda object: object.annual_end_am_weekday, reverse=True)
    sorted_pop_customer_start_weekend = sorted(list_objects, key=lambda object: object.customer_start_weekend, reverse=True)
    sorted_pop_customer_end_weekend = sorted(list_objects, key=lambda object: object.customer_end_weekend, reverse=True)
 
    one_for_all = sorted(list_objects, key=lambda object: object.incl_annual_start_weekday, reverse=True)
   
    file_sorted_pop_annual_start_am_weekday = open(outputpath+"/sorted_pop_annual_start_am_weekday.txt", "w")
    file_sorted_pop_annual_end_am_weekday = open(outputpath+"/sorted_pop_annual_end_am_weekday.txt", "w")
    file_sorted_pop_customer_start_weekend = open(outputpath+"/sorted_pop_customer_start_weekend.txt", "w")
    file_sorted_pop_customer_end_weekend = open(outputpath+"/sorted_pop_customer_end_weekend.txt", "w")
    file_one_for_all = open(outputpath+"/one_for_all.txt", "w") 
   
    for attr, value in sorted_pop_annual_start_am_weekday[0].__dict__.iteritems():
        file_sorted_pop_annual_start_am_weekday.write(attr+",")
    file_sorted_pop_annual_start_am_weekday.write('\n') 
    for attr, value in sorted_pop_annual_end_am_weekday[0].__dict__.iteritems():
        file_sorted_pop_annual_end_am_weekday.write(attr+",")
    file_sorted_pop_annual_end_am_weekday.write('\n')
    for attr, value in sorted_pop_customer_start_weekend[0].__dict__.iteritems():
        file_sorted_pop_customer_start_weekend.write(attr+",")
    file_sorted_pop_customer_start_weekend.write('\n')
    for attr, value in sorted_pop_customer_end_weekend[0].__dict__.iteritems():
        file_sorted_pop_customer_end_weekend.write(attr+",")
    file_sorted_pop_customer_end_weekend.write('\n')

    for attr, value in one_for_all[0].__dict__.iteritems():
        if attr!='start_weekday' and attr!='end_weekday' and attr!='diff_weekday':
            file_one_for_all.write(attr+",")
    file_one_for_all.write('\n')

    for i in range(20):
        for attr, value in sorted_pop_annual_start_am_weekday[i].__dict__.iteritems():
            file_sorted_pop_annual_start_am_weekday.write(str(value)+',')
        file_sorted_pop_annual_start_am_weekday.write('\n')
        for attr, value in sorted_pop_annual_end_am_weekday[i].__dict__.iteritems():
            file_sorted_pop_annual_end_am_weekday.write(str(value)+',')
        file_sorted_pop_annual_end_am_weekday.write('\n')
        for attr, value in sorted_pop_customer_start_weekend[i].__dict__.iteritems():
            file_sorted_pop_customer_start_weekend.write(str(value)+',')
        file_sorted_pop_customer_start_weekend.write('\n')
        for attr, value in sorted_pop_customer_end_weekend[i].__dict__.iteritems():
            file_sorted_pop_customer_end_weekend.write(str(value)+',')
        file_sorted_pop_customer_end_weekend.write('\n')

    for obj in one_for_all:
        for attr, value in obj.__dict__.iteritems():
            if attr!='start_weekday' and attr!='end_weekday' and attr!='diff_weekday':
                file_one_for_all.write(str(value)+',')        
        file_one_for_all.write('\n')

    file_sorted_pop_annual_start_am_weekday.close()
    file_sorted_pop_annual_end_am_weekday.close()
    file_sorted_pop_customer_start_weekend.close()
    file_sorted_pop_customer_end_weekend.close()
    file_one_for_all.close()

    x = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
    y = []
    llist = []
    for i in range(10): 
        llist.append(sorted_pop_annual_end_am_weekday[i].station)
        temp = sorted_pop_annual_end_am_weekday[i].diff_weekday
        temp.insert(0, 0)
        y.append(np.asarray(temp))

    glist = []
    g1 = TGraph(13, x, y[0]) 
    g2 = TGraph(13, x, y[1])
    g3 = TGraph(13, x, y[2])
    g4 = TGraph(13, x, y[3])
    g5 = TGraph(13, x, y[4])
    g6 = TGraph(13, x, y[5])
    g7 = TGraph(13, x, y[6])
    g8 = TGraph(13, x, y[7])
    g9 = TGraph(13, x, y[8])
    g10 = TGraph(13, x, y[9])
    glist.append(g1)
    glist.append(g2)
    glist.append(g3)
    glist.append(g4)
    glist.append(g5)
    glist.append(g6)
    glist.append(g7)
    glist.append(g8)
    glist.append(g9)
    glist.append(g10)
    Plt.DrawGraphOverlay(glist, llist, "Number of Hours Since 11 a.m.", "Variations on Bicycle Availability", outputpath+"/DrawGraph.pdf")

    MyFile = ROOT.TFile("fit.root","RECREATE");
    calcPoissonCL(hist['data'].h_temp_rwday_weekday)
    hist['data'].h_temp_rwday_weekday.Write()
    MyFile.Close()

if __name__ == '__main__':
    main()
