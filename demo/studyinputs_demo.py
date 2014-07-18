import numpy as np
import array

import ROOT
from ROOT import *

import AtlasStyle
import PlottingUtls as Plt


class Hist:
    def __init__(self, name):
        self.h_trip_duration = TH1F(name+"_trip_duration", name+"_trip_duration", 30, 0, 4800)
        self.h_startwhichday = TH1F(name+"_startwhichday", name+"_startwhichday", 7, 0, 7)
        self.h_starthour = TH1F(name+"_starthour", name+"_starthour", 24, 0, 24)
        self.h_meantemp = TH1F(name+"_meantemp", name+"_meantemp", 10, 0, 90)
        self.h_meanwindspeed = TH1F(name+"_meanwindspeed", name+"_meanwindspeed", 13, 0, 13)
        self.h_meanhumidity = TH1F(name+"_meanhumidity", name+"_meanhumidity", 14, 0, 90)

def main():

    hist = {}

    hist['signal'] = Hist('signal')
    hist['background'] = Hist('background')
    
    
    f = TFile("../output/demo/data.root")
    
    tree = f.Get('citibike_train')

    for e in tree:
        if e.UserType == 1:
            hist['signal'].h_trip_duration.Fill(e.TripDuration, 1) 
            hist['signal'].h_starthour.Fill(e.StartHour, 1)
            hist['signal'].h_startwhichday.Fill(e.StartWhichDay, 1)
            hist['signal'].h_meantemp.Fill(e.MeanTemp, 1)
            hist['signal'].h_meanwindspeed.Fill(e.MeanWindSpeed,1)
            hist['signal'].h_meanhumidity.Fill(e.MeanHumidity, 1)
        elif e.UserType == 0:
            hist['background'].h_trip_duration.Fill(e.TripDuration, 1)  
            hist['background'].h_starthour.Fill(e.StartHour,1)    
            hist['background'].h_startwhichday.Fill(e.StartWhichDay, 1)
            hist['background'].h_meantemp.Fill(e.MeanTemp, 1)
            hist['background'].h_meanwindspeed.Fill(e.MeanWindSpeed,1)
            hist['background'].h_meanhumidity.Fill(e.MeanHumidity,1)


    Plt.DrawMultiPadHist(hist['signal'], hist['background'], "Customer (signal)", "Subscriber (background)", "Arbitrary Unit", True, False, "plots/MVA_Inputs.pdf")


if __name__ == '__main__':
    main()
