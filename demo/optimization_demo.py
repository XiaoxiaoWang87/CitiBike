#!/usr/bin/python

import sys
import os
from math import *

import pandas as pd
import numpy as np
import ROOT

from collections import defaultdict


class Variable:
    def __init__(self, name):
        self.initVal = 0
        self.stepSize = 0
        self.minVal = 0
        self.maxVal = 0

class VariableVal:
    def __init__(self, name):
        self.val = []


sig_var = {}
sig_var['TripDuration'] = VariableVal('TripDuration')
sig_var['StartWhichDay'] = VariableVal('StartWhichDay')
sig_var['StartHour'] = VariableVal('StartHour')
sig_var['MeanTemp'] = VariableVal('MeanTemp')
bkg_var = {}
bkg_var['TripDuration'] = VariableVal('TripDuration')
bkg_var['StartWhichDay'] = VariableVal('StartWhichDay')
bkg_var['StartHour'] = VariableVal('StartHour')
bkg_var['MeanTemp'] = VariableVal('MeanTemp')



def fcn(npar, deriv, f, par, iflag):

    sig_counts = 0
    bkg_counts = 0

    for i in range(len(sig_var['TripDuration'].val)):
        if sig_var['TripDuration'].val[i] > par[0] and sig_var['StartWhichDay'].val[i] > par[1] and sig_var['MeanTemp'].val[i] > par[2] and sig_var['StartHour'].val[i] > par[3]:
            sig_counts = sig_counts + 1

    for i in range(len(bkg_var['TripDuration'].val)):
        if bkg_var['TripDuration'].val[i] > par[0] and bkg_var['StartWhichDay'].val[i] > par[1] and bkg_var['MeanTemp'].val[i] > par[2] and bkg_var['StartHour'].val[i] > par[3]:
            bkg_counts = bkg_counts + 1


    if sig_counts > 3000: #> 500:
        f[0] = -1.0 * float(sig_counts)/float(bkg_counts)
    else:
        f[0] = 0
        bkg_counts = 100000.

    print 'TripDuration: %0.f' % par[0]
    print 'StartWhichDay: %0.f' % par[1]
    print 'MeanTemp: %0.f' % par[2]
    print 'StartHour: %0.f' % par[3]

    print 'f: %0.2f' % f[0]

    s_b = float(sig_counts)/float(bkg_counts)
    print "Customer (signal) counts: %0.f, Subscriber (background) counts: %0.f, S/B: %0.2f" % (sig_counts, bkg_counts, s_b)


def PrintResult(results, n_sig, n_bkg):

    sig_counts = 0
    bkg_counts = 0

    for i in range(len(sig_var['TripDuration'].val)):
        if sig_var['TripDuration'].val[i] > results[0] and sig_var['StartWhichDay'].val[i] > results[1] and sig_var['MeanTemp'].val[i] > results[2] and sig_var['StartHour'].val[i] > results[3]:
            sig_counts = sig_counts + 1

    for i in range(len(bkg_var['TripDuration'].val)):
        if bkg_var['TripDuration'].val[i] > results[0] and bkg_var['StartWhichDay'].val[i] > results[1] and bkg_var['MeanTemp'].val[i] > results[2] and bkg_var['StartHour'].val[i] > results[3]:
            bkg_counts = bkg_counts + 1

    s_b = float(sig_counts)/float(bkg_counts)
    print "\nCustomer (signal) counts: %0.f, Subscriber (background) counts: %0.f, S/B: %0.2f" % (sig_counts, bkg_counts, s_b)
    print "Customer (signal) efficiency: %0.2f, Subscriber (background) rejection: %0.2f" % (float(sig_counts)/float(n_sig), 1-float(bkg_counts)/float(n_bkg))

    file = open("benchmark.txt", "w")
    file.write(str(float(sig_counts)/float(n_sig))+'\n')
    file.write(str(1-float(bkg_counts)/float(n_bkg))+'\n')
    file.close()


def main():
 
    file = ROOT.TFile.Open("../output/demo/data.root","READ")
    t = file.Get('citibike_evaluate')
    ROOT.gROOT.cd()
    sig_t = t.CopyTree("UserType == 1")
    bkg_t = t.CopyTree("UserType == 0")

    n_sig = 0
    for e1 in sig_t:
        n_sig = n_sig+1
        sig_var['TripDuration'].val.append(e1.TripDuration)
        sig_var['StartWhichDay'].val.append(e1.StartWhichDay)        
        sig_var['StartHour'].val.append(e1.StartHour)
        sig_var['MeanTemp'].val.append(e1.MeanTemp)
 
    n_bkg = 0
    for e2 in bkg_t:
        n_bkg = n_bkg+1
        bkg_var['TripDuration'].val.append(e2.TripDuration)
        bkg_var['StartWhichDay'].val.append(e2.StartWhichDay)
        bkg_var['StartHour'].val.append(e2.StartHour)
        bkg_var['MeanTemp'].val.append(e2.MeanTemp)



    npar = 2
    m = ROOT.TMinuit(npar)
    m.SetFCN(fcn)   


    var = {}
    var['TripDuration'] = Variable('TripDuration')
    var['StartWhichDay'] = Variable('StartWhichDay')
    var['StartHour'] = Variable('StartHour')
    var['MeanTemp'] = Variable('MeanTemp')

    var['TripDuration'].initVal = 100  #1000
    var['TripDuration'].stepSize = 100  #200
    var['TripDuration'].minVal = 0
    var['TripDuration'].maxVal = 8000

    var['StartWhichDay'].initVal = 0   #5  
    var['StartWhichDay'].stepSize = 1
    var['StartWhichDay'].minVal = 0
    var['StartWhichDay'].maxVal = 6

    var['StartHour'].initVal = 9    #9
    var['StartHour'].stepSize = 1
    var['StartHour'].minVal = 0
    var['StartHour'].maxVal = 23

    var['MeanTemp'].initVal =  0   #60
    var['MeanTemp'].stepSize = 5
    var['MeanTemp'].minVal = 0
    var['MeanTemp'].maxVal = 90


    c = 0
    for k, v in var.items():
        #print k
        m.DefineParameter(c, k , var[k].initVal, var[k].stepSize, var[k].minVal, var[k].maxVal)
        c = c + 1

    #m.FixParameter(0);
    #m.FixParameter(1);
    #m.FixParameter(2);
    #m.FixParameter(3);
    
    for i in range(5):
        m.mnsimp();
        m.mnimpr();

    #then use migrad to achieve better precision, notice the inputs should be close to minimum
    #m.Migrad();       # Minuit's best minimization algorithm
    #m.mnmnos();       # This is MINOS


    i = 0

    outpar = {}
    err = {}
    outpar = defaultdict(list)
    err = defaultdict(list)

    results = []

    
    print '\n\n******************' 
    print 'THE ANSWER IS: '

    for k, v in var.items():
        outpar[k].append(ROOT.Double(0))
        err[k].append(ROOT.Double(0))

        m.GetParameter(i,outpar[k][0],err[k][0]) 

        print '\n' + k + ': > %0.f' % outpar[k][0]

        results.append(outpar[k][0])
        i = i + 1

    PrintResult(results, n_sig, n_bkg)


if __name__ == '__main__':
    main()
