import numpy as np
import array

import ROOT
from ROOT import *

import AtlasStyle
import PlottingUtls as Plt


class Hist:
    def __init__(self, name):
        self.h_bdt = TH1F(name+"_bdt", name+"_bdt", 30, -0.5, 0.28) #-0.25, 0.6)
        self.h_scan_bdt = TH1F(name+"_scan_bdt", name+"_scan_bdt", 30,  -0.5, 0.28) # -0.25, 0.6)
        self.h_trip_duration = TH1F(name+"_trip_duration", name+"_trip_duration", 30, 0, 4800)
        self.h_scan_trip_duration = TH1F(name+"_scan_trip_duration", name+"_scan_trip_duration", 30, 0, 4800)
        self.h_starthour = TH1F(name+"_starthour", name+"_starthour", 24, 0, 24)
        self.h_scan_starthour = TH1F(name+"_scan_starthour", name+"_scan_starthour", 24, 0, 24)

def Scan(h):
    h_scan = h.Clone()
    for i in range(1,h.GetNbinsX()+1):
        h_scan.SetBinContent(i, h.Integral(i, h.GetNbinsX())*1.0 / h.Integral(1, h.GetNbinsX()) )
    return h_scan


def main():

    reader = ROOT.TMVA.Reader()
    
    tripDuration = array.array('f',[0])
    startWhichDay = array.array('f',[0])
    startHour = array.array('f',[0])
    meanTemp = array.array('f',[0])
    meanWindSpeed = array.array('f',[0])
    meanHumidity = array.array('f',[0])

    reader.AddVariable("TripDuration", tripDuration)
    reader.AddVariable('StartWhichDay', startWhichDay)
    reader.AddVariable('StartHour', startHour)
    reader.AddVariable('MeanTemp', meanTemp)
    reader.AddVariable('MeanWindSpeed', meanWindSpeed)
    reader.AddVariable('MeanHumidity', meanHumidity)
    
    reader.BookMVA("BDT","weights/TMVAClassification_BDT.weights.xml")
    
    hist = {}

    hist['signal'] = Hist('signal')
    hist['background'] = Hist('background')
    
    
    f = TFile("../output/demo/data.root")
    
    tree = f.Get('citibike_evaluate')
    
    for e in tree:

        tripDuration[0] = e.TripDuration
        startWhichDay[0] = e.StartWhichDay
        startHour[0] = e.StartHour
        meanTemp[0] = e.MeanTemp
        meanWindSpeed[0] = e.MeanWindSpeed
        meanHumidity[0] = e.MeanHumidity     

        BDT = reader.EvaluateMVA("BDT")

        if e.UserType == 1:
            hist['signal'].h_bdt.Fill(BDT,1)
            hist['signal'].h_trip_duration.Fill(e.TripDuration, 1) 
            hist['signal'].h_starthour.Fill(e.StartHour,1)

        elif e.UserType == 0:
            hist['background'].h_bdt.Fill(BDT,1)
            hist['background'].h_trip_duration.Fill(e.TripDuration, 1)  
            hist['background'].h_starthour.Fill(e.StartHour,1)    


    hist['signal'].h_scan_bdt = Scan(hist['signal'].h_bdt)
    hist['signal'].h_scan_trip_duration = Scan(hist['signal'].h_trip_duration)
    hist['signal'].h_scan_starthour = Scan(hist['signal'].h_starthour)

    hist['background'].h_scan_bdt = Scan(hist['background'].h_bdt)
    hist['background'].h_scan_trip_duration = Scan(hist['background'].h_trip_duration)
    hist['background'].h_scan_starthour = Scan(hist['background'].h_starthour)


    benchmark_effS = 0 #0.55 
    benchmark_bkgS = 0 #0.26
    file = open('benchmark.txt', 'r')
    l = 0
    for line in file:
        if l == 0:
            benchmark_effS = float(line)
        else:
            benchmark_bkgR = float(line)
        l = l+1

    Plt.DrawROCcurve(hist['signal'].h_scan_bdt, hist['background'].h_scan_bdt, "Boost Decision Tree", hist['signal'].h_scan_trip_duration, hist['background'].h_scan_trip_duration, "Trip Duration", hist['signal'].h_scan_starthour, hist['background'].h_scan_starthour, "Trip Start Hour", benchmark_effS, benchmark_bkgR, "Cut Combination", "#varepsilon_{customers}", "1 - #varepsilon_{subscribers (i.e. rejection factor)}", "plots/MVA_ROC.pdf")

    Plt.DrawTwoHistOverlay(hist['signal'].h_bdt, hist['background'].h_bdt, "Customer (signal)", "Subscriber (background)", "BDT Score", "Arbitrary Unit", True, False, 3, "plots/MVA_BDT.pdf")


if __name__ == '__main__':
    main()
