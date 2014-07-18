#!/usr/bin/python

import sys
import os
import numpy as np
import csv

import ROOT
from ROOT import *
import AtlasStyle

import matplotlib
import matplotlib.pyplot as plt

gROOT.Reset();
gROOT.SetStyle("ATLAS");

def set_palette(name='palette', ncontours=999):
    """Set a color palette from a given RGB list
    stops, red, green and blue should all be lists of the same length
    see set_decent_colors for an example"""

    if name == "gray" or name == "grayscale":
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
    # elif name == "whatever":
        # (define more palettes)
    else:
        # default palette, looks cool
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [0.00, 0.00, 0.87, 1.00, 0.51]
        green = [0.00, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

    s = np.array(stops, dtype=float)
    r = np.array(red, dtype=float)
    g = np.array(green, dtype=float)
    b = np.array(blue, dtype=float)

    npoints = len(s)
    TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    gStyle.SetNumberContours(ncontours)

def DrawTwoHistOverlay(h1, h2, h1_legend='', h2_legend='', x_title='', y_title='', norm=False, log=False, style=0, path='test.pdf'):

    c = ROOT.TCanvas("c", "c", 800,600)
    c.cd()

    if log==True:
        c.SetLogy()

    if norm==True:
        h1.Sumw2()
        h1.Scale(1.0/h1.Integral())
        h2.Sumw2()
        h2.Scale(1.0/h2.Integral())

    h1.GetXaxis().SetTitle(x_title);
    h1.GetYaxis().SetTitle(y_title);
    h1.GetYaxis().SetTitleOffset(1.7)
    h1.GetYaxis().SetTitleSize(0.045)

    if h1.GetMaximum() > h2.GetMaximum():
        max = h1.GetMaximum()
    else:
        max = h2.GetMaximum()

    if log==False:
        h1.GetYaxis().SetRangeUser(0,1.65*max)
    else:
        h1.GetYaxis().SetRangeUser(0.0001,20*max)

    #h1.SetMarkerSize(1.3)
    if style == 3:
        h1.SetLineColor(kBlue-9)
        h1.SetFillColor(kBlue-9)
        h1.SetFillStyle(3001)
        h1.SetLineWidth(2)
    elif style == 2:
        h1.SetMarkerColor(1)
        h1.SetLineColor(1)
    else:
        h1.SetMarkerColor(1)
        h1.SetLineColor(1)
    h1.SetLineWidth(2)

    if style == 0 or  style == 2:
        #h1.SetLineStyle(2)
        h1.SetLineStyle(1)
        h1.Draw("hist")
    else:
        h1.SetLineStyle(1)
        h1.Draw("hist")

    #h2.SetMarkerSize(1.3)
 
    if style == 3:
        h2.SetLineColor(kRed-7)
        h2.SetFillColor(kRed-7)
        h2.SetFillStyle(3003)
        h2.SetLineWidth(2)
        h2.SetLineStyle(1)
    elif style == 2:
        h2.SetMarkerColor(8)
        h2.SetLineColor(8)
    else:
        h2.SetMarkerColor(2)
        h2.SetLineColor(2)
    h2.SetLineWidth(2)

    if style == 0 or style == 2:
        #h2.SetLineStyle(2)
        h2.SetLineStyle(1)
        h2.Draw("hist same")
    else:
        h2.SetLineStyle(1)
        h2.Draw("hist same")

    if log==False and (style==0 or style==2):
        leg = TLegend(0.15,0.55,0.40,0.80);
    elif style==3:
        leg = TLegend(0.5,0.75,0.90,0.90)
    else:
        leg = TLegend(0.65,0.55,0.90,0.80)
    leg.SetBorderSize(0);
    leg.SetFillColor(kWhite);
    ##leg.SetFillStyle(0);
    leg.SetLineColor(1);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    ##leg.SetTextFont(47);
    ##leg.SetTextSize(2);
    leg.AddEntry(h1,h1_legend,"l");
    leg.AddEntry(h2,h2_legend,"l");
    leg.Draw("same");

    labelSize = 0.0375
    upScale = 0.75
    labelATLAS = TLatex(0.18,0.88-0.01,"#bf{Citi} Bike Analysis");
    labelATLAS.SetNDC();
    labelATLAS.SetTextFont(42);
    labelATLAS.SetTextSize(labelSize/upScale);
    labelATLAS.SetLineWidth(2);
    labelATLAS.Draw("same")

    if style == 1:
        line1 = TLine(20,0,20,0.05)
        line1.SetLineColor(kBlack)
        line1.SetLineStyle(2)
        line1.SetLineWidth(1)

        line2 = TLine(30,0,30,0.05)
        line2.SetLineColor(kBlack)
        line2.SetLineStyle(2)
        line2.SetLineWidth(1)

        line3 = TLine(40,0,40,0.05)
        line3.SetLineColor(kBlack)
        line3.SetLineStyle(2)
        line3.SetLineWidth(1)

        line4 = TLine(50,0,50,0.05)
        line4.SetLineColor(kBlack)
        line4.SetLineStyle(2)
        line4.SetLineWidth(1)

        line5 = TLine(60,0,60,0.05)
        line5.SetLineColor(kBlack)
        line5.SetLineStyle(2)
        line5.SetLineWidth(1)
      
        line1.Draw("same")
        line2.Draw("same")
        line3.Draw("same")
        line4.Draw("same")
        line5.Draw("same")

    c.Print(path)

    c.Close()



def DrawFourHistOverlay(h1, h2, h3, h4, h1_legend='', h2_legend='', h3_legend='', h4_legend='', x_title='', y_title='', norm=False, log=False, style=0, path='test.pdf'):

    c = ROOT.TCanvas("c", "c", 800,600)
    c.cd()

    if log==True:
        c.SetLogy()

    if norm==True:
        h1.Sumw2()
        h1.Scale(1.0/h1.Integral())
        h2.Sumw2()
        h2.Scale(1.0/h2.Integral())
        h3.Sumw2()
        h3.Scale(1.0/h3.Integral())
        h4.Sumw2()
        h4.Scale(1.0/h4.Integral())        

    h1.GetXaxis().SetTitle(x_title);
    h1.GetYaxis().SetTitle(y_title);
    h1.GetYaxis().SetTitleOffset(1.7)
    h1.GetYaxis().SetTitleSize(0.045)
    if log==False:
        h1.GetYaxis().SetRangeUser(0,1.65*h1.GetMaximum())
    else:
        h1.GetYaxis().SetRangeUser(0.0001,20*h1.GetMaximum())
    h1.SetMarkerSize(1.3)
    h1.SetMarkerColor(1)
    h1.SetLineColor(1)
    h1.SetLineWidth(2)
    h1.SetLineStyle(2)
    h1.Draw("hist")

    h2.SetMarkerSize(1.3)
    h2.SetMarkerColor(2)
    h2.SetLineColor(2)
    h2.SetLineWidth(2)
    h2.SetLineStyle(2)
    h2.Draw("hist same")

    h3.SetMarkerSize(1.3)
    h3.SetMarkerColor(4)
    h3.SetLineColor(4)
    h3.SetLineWidth(2)
    h3.SetLineStyle(2)
    h3.Draw("hist same")

    h4.SetMarkerSize(1.3)
    h4.SetMarkerColor(6)
    h4.SetLineColor(6)
    h4.SetLineWidth(2)
    h4.SetLineStyle(2)
    h4.Draw("hist same")

    if log==False:
        leg = TLegend(0.15,0.55,0.40,0.80);
    else:
        leg = TLegend(0.65,0.55,0.90,0.80)
    leg.SetBorderSize(0);
    leg.SetFillColor(kWhite);
    ##leg.SetFillStyle(0);
    leg.SetLineColor(1);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    ##leg.SetTextFont(47);
    ##leg.SetTextSize(2);
    leg.AddEntry(h1,h1_legend,"l");
    leg.AddEntry(h2,h2_legend,"l");
    leg.AddEntry(h3,h3_legend,"l");
    leg.AddEntry(h4,h4_legend,"l");
    leg.Draw("same");

    labelSize = 0.0375
    upScale = 0.75
    labelATLAS = TLatex(0.18,0.88-0.01,"#bf{Citi} Bike Analysis");
    labelATLAS.SetNDC();
    labelATLAS.SetTextFont(42);
    labelATLAS.SetTextSize(labelSize/upScale);
    labelATLAS.SetLineWidth(2);
    labelATLAS.Draw("same")

    c.Print(path)
    c.Close()


def DrawMultiPadHist(h1_group, h2_group, h1_legend='', h2_legend='', y_title='', norm=False, log=False, path="test.pdf"):

    c = ROOT.TCanvas("c", "c", 1900,800)
    c.Divide(3,2)

    leg = {}
    labelATLAS = {}

    for key1, h1 in h1_group.__dict__.iteritems():
        for key2, h2 in h2_group.__dict__.iteritems():
            if key1!=key2:
                continue
            print key1
            if key1 == 'h_trip_duration':
                c.cd(1)
                x_title = 'Trip Duration [s]' 
            elif key1 == 'h_startwhichday':
                c.cd(2)
                x_title = 'Trip Start Day [Mon-Sun]' 
            elif key1 == 'h_starthour':
                c.cd(3)
                x_title = 'Trip Start Hour [0-24]'
            elif key1 == 'h_meantemp':
                c.cd(4)
                x_title = 'Mean Temperature [F]'
            elif key1 == 'h_meanwindspeed':
                c.cd(5)
                x_title = 'Mean Wind Speed [MPH]'
            elif key1 == 'h_meanhumidity':
                c.cd(6)
                x_title = 'Mean Humidity [%]'

            if log==True:
                c.SetLogy()

            if norm==True:
                h1.Scale(1.0/h1.Integral())
                h2.Scale(1.0/h2.Integral())

            h1.GetXaxis().SetTitle(x_title);
            h1.GetYaxis().SetTitle(y_title);
            h1.GetYaxis().SetTitleOffset(1.7)
            h1.GetYaxis().SetTitleSize(0.045)

            if h1.GetMaximum() > h2.GetMaximum():
                max = h1.GetMaximum()
            else:
                max = h2.GetMaximum()

            if log==False:
                h1.GetYaxis().SetRangeUser(0,1.65*max)
            else:
                h1.GetYaxis().SetRangeUser(0.0001,20*max)

            #trans_blue = GetColorTransparent(kBlue-9, 0.3)
            #h1.SetMarkerSize(1.3)
            #h1.SetMarkerColor(trans_blue)
            h1.SetLineColor(kBlue-9)
            h1.SetFillColor(kBlue-9)
            h1.SetFillStyle(3001)
            #h1.SetFillColorAlpha(trans_blue, 0.35)
            h1.SetLineWidth(2)

            h1.SetLineStyle(1)
            h1.Draw("hist")
 
            #kRed-7 = GetColorTransparent(kRed-7, 0.3)
            #h2.SetMarkerSize(1.3)
            #h2.SetMarkerColor(kRed-7)
            h2.SetLineColor(kRed-7)
            h2.SetFillColor(kRed-7)
            h2.SetFillStyle(3003)
            #h2.SetFillColorAlpha(trans_red, 0.35)
            h2.SetLineWidth(2)

            h2.SetLineStyle(1)
            h2.Draw("hist same")

            leg[key1] = TLegend(0.5,0.75,0.90,0.90)
            leg[key1].SetBorderSize(0);
            leg[key1].SetFillColor(kWhite);
            ##leg[key1].SetFillStyle(0);
            leg[key1].SetLineColor(1);
            leg[key1].SetLineStyle(1);
            leg[key1].SetLineWidth(1);
            ##leg[key1].SetTextFont(47);
            ##leg[key1].SetTextSize(2);
            leg[key1].AddEntry(h1,h1_legend,"l");
            leg[key1].AddEntry(h2,h2_legend,"l");
            leg[key1].Draw("same");


            labelSize = 0.0375
            upScale = 0.75
            labelATLAS[key1] = TLatex(0.18,0.88-0.01,"#bf{Citi} Bike Analysis");
            labelATLAS[key1].SetNDC();
            labelATLAS[key1].SetTextFont(42);
            labelATLAS[key1].SetTextSize(labelSize/upScale);
            labelATLAS[key1].SetLineWidth(2);
            labelATLAS[key1].Draw("same")

    c.Update()

    c.Print(path)

    c.Close()


def Draw2DHist(h1, h1_legend='', x_title='', y_title='', norm=False, log=False, style=0, path='test.pdf'):

    c = ROOT.TCanvas("c", "c", 650,600)
    c.cd()

    set_palette('none',255)

    c.SetLeftMargin(0.15)
    c.SetRightMargin(0.15)

    if log==True:
        c.SetLogy()

    if norm==True:
        h1.Sumw2()
        h1.Scale(1.0/h1.Integral())

    h1.GetXaxis().SetTitle(x_title);
    h1.GetYaxis().SetTitle(y_title);
    h1.GetYaxis().SetTitleOffset(1.8)
    h1.GetYaxis().SetTitleSize(0.045)
    #TGaxis.SetMaxDigits(1)

    if log==False:
        h1.GetYaxis().SetRangeUser(0,1.65*h1.GetMaximum())
    else:
        h1.GetYaxis().SetRangeUser(0.0001,20*h1.GetMaximum())
    #h1.SetMarkerSize(1.3)
    h1.SetLineWidth(2)
    if style == 0:
        h1.SetLineStyle(2)
        h1.Draw("colz")


    if log==False and style==0:
        leg = TLegend(0.15,0.55,0.40,0.80);
    else:
        leg = TLegend(0.65,0.55,0.90,0.80)
    #leg.SetBorderSize(0);
    #leg.SetFillColor(kWhite);
    ###leg.SetFillStyle(0);
    #leg.SetLineColor(1);
    #leg.SetLineStyle(1);
    #leg.SetLineWidth(1);
    ###leg.SetTextFont(47);
    ###leg.SetTextSize(2);
    #leg.AddEntry(h1,h1_legend,"l");
    #leg.Draw("same");

    labelSize = 0.0375
    upScale = 0.75
    labelATLAS = TLatex(0.18,0.88-0.01,"#bf{Citi} Bike Analysis");
    labelATLAS.SetNDC();
    labelATLAS.SetTextFont(42);
    labelATLAS.SetTextSize(labelSize/upScale);
    labelATLAS.SetLineWidth(2);
    labelATLAS.Draw("same")

    c.Print(path)
    c.Close()


def DrawGraphOverlay(glist, llist, x_title='', y_title='', path='test.pdf'):

    c = ROOT.TCanvas("c", "c", 900,500)
    c.cd()

    #c.SetLeftMargin(0.15)
    #c.SetRightMargin(0.15)

    c.SetGrid()
    #c.SetGridy()

    mg = ROOT.TMultiGraph()

    i = 0
    for g in glist:
        if i!=9:
            g.SetLineColor(i+1)
        else:
            g.SetLineColor(38)
        g.SetLineWidth(2)
        #if i==0:
        #    g.GetXaxis().SetTitle(x_title);
        #    g.GetYaxis().SetTitle(y_title);
        i +=1
        mg.Add(g)
    #SetTitleOffset(1.8)
    #SetTitleSize(0.045)
    #SetLineWidth(2)
    mg.Draw("AC")
    mg.GetXaxis().SetTitle(x_title)
    mg.GetYaxis().SetTitle(y_title)
    #mg.GetYaxis().SetTitleSize(0.04)
    mg.GetXaxis().SetRangeUser(0,6)
    mg.GetYaxis().SetRangeUser(-20,12)
    gPad.Modified()

    leg = TLegend(0.15,0.55,0.45,0.15);
    leg.SetBorderSize(0);
    leg.SetFillColor(kWhite);
    ##leg.SetFillStyle(0);
    leg.SetLineColor(1);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    ##leg.SetTextFont(47);
    ##leg.SetTextSize(2);
    leg.AddEntry(glist[0],llist[0],"l");
    leg.AddEntry(glist[1],llist[1],"l");
    leg.AddEntry(glist[2],llist[2],"l");
    leg.AddEntry(glist[3],llist[3],"l");
    leg.AddEntry(glist[4],llist[4],"l");
    leg.AddEntry(glist[5],llist[5],"l");
    leg.AddEntry(glist[6],llist[6],"l");
    leg.AddEntry(glist[7],llist[7],"l");
    leg.AddEntry(glist[8],llist[8],"l");
    leg.AddEntry(glist[9],llist[9],"l");
    leg.Draw("same");
    

    labelSize = 0.0375
    upScale = 0.75
    labelATLAS = TLatex(0.18,0.88-0.01,"#bf{Citi} Bike Analysis");
    labelATLAS.SetNDC();
    labelATLAS.SetTextFont(42);
    labelATLAS.SetTextSize(labelSize/upScale);
    labelATLAS.SetLineWidth(2);
    labelATLAS.Draw("same")

    c.Print(path)
    c.Close()


def DrawPieChart(counts, names, colors, explode, small, path):
    plt.clf() 
    if small == True:
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(12,6)
    matplotlib.rcParams['font.size'] = 16
    plt.pie(counts, explode=explode, labels=names, colors=colors,
            autopct='%1.1f%%', shadow=True)#, startangle=90)
    plt.axis('equal')
    plt.savefig(path)



def DrawROCcurve(h_sig_1, h_bkg_1, h_name_1, h_sig_2, h_bkg_2, h_name_2, h_sig_3, h_bkg_3, h_name_3, ben_effS, ben_bkgR, ben_name, x_name, y_name, path):

    effS_1 = []
    bkgR_1 = []

    for i in range(1, h_sig_1.GetNbinsX()+1):
        effS_1.append(h_sig_1.GetBinContent(i))
        bkgR_1.append(1 - h_bkg_1.GetBinContent(i))
    array_effS_1 = np.array(effS_1)
    array_bkgR_1 = np.array(bkgR_1)

    effS_2 = []
    bkgR_2 = []
    for i in range(1, h_sig_2.GetNbinsX()+1):
        effS_2.append(h_sig_2.GetBinContent(i))
        bkgR_2.append(1 - h_bkg_2.GetBinContent(i))
    array_effS_2 = np.array(effS_2)
    array_bkgR_2 = np.array(bkgR_2)

    effS_3 = []
    bkgR_3 = []
    for i in range(1, h_sig_3.GetNbinsX()+1):
        effS_3.append(h_sig_3.GetBinContent(i))
        bkgR_3.append(1 - h_bkg_3.GetBinContent(i))
    array_effS_3 = np.array(effS_3)
    array_bkgR_3 = np.array(bkgR_3)


    effS_b = []
    bkgR_b = []
    effS_b.append(ben_effS)
    bkgR_b.append(ben_bkgR)
    array_effS_b = np.array(effS_b)
    array_bkgR_b = np.array(bkgR_b)


    c = ROOT.TCanvas("c", "c", 800,600)
    c.cd()
    c.SetGrid()

    g1 = TGraph(len(effS_1), array_effS_1, array_bkgR_1)
    g1.Sort()
    g1.SetMarkerStyle(20)
    g1.SetMarkerSize(0.6)
    g1.SetMarkerColor(kBlue-6)#10)
    g1.SetLineColor(kBlue-6)#10)    
    g1.SetLineWidth(3)

    g1.GetXaxis().SetLimits(0,1.0)
    g1.GetXaxis().SetRangeUser(0,1.0)
    g1.GetYaxis().SetRangeUser(0,1.0)
    g1.GetXaxis().SetTitle(x_name)
    g1.GetYaxis().SetTitle(y_name)
    g1.Draw("AC")

    g2 = TGraph(len(effS_2), array_effS_2, array_bkgR_2)
    g2.Sort()
    g2.SetMarkerStyle(20)
    g2.SetMarkerSize(0.6)
    g2.SetMarkerColor(kGreen-9) #10)
    g2.SetLineColor(kGreen-9) #10)
    g2.SetLineWidth(3)

    g2.Draw("C");

    g3 = TGraph(len(effS_3), array_effS_3, array_bkgR_3)
    g3.Sort()
    g3.SetMarkerStyle(20)
    g3.SetMarkerSize(0.6)
    g3.SetMarkerColor(kYellow-6)#10)
    g3.SetLineColor(kYellow-6)#10)
    g3.SetLineWidth(3)
    g3.Draw("C");

    gb = TGraph(len(effS_b), array_effS_b, array_bkgR_b)
    gb.SetMarkerStyle(29)
    gb.SetMarkerSize(3)
    gb.SetMarkerColor(kRed-7)

    gb.Draw("P");
    

    leg = TLegend(0.15,0.25,0.48,0.50);
    leg.SetBorderSize(0);
    leg.SetFillColor(kWhite);
    ##leg.SetFillStyle(0);
    leg.SetLineColor(1);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    ##leg.SetTextFont(47);
    ##leg.SetTextSize(2);
    leg.AddEntry(g1,h_name_1, "l")
    leg.AddEntry(g2,h_name_2, "l")
    leg.AddEntry(g3,h_name_3, "l")
    leg.AddEntry(gb,ben_name, "p")

    leg.Draw("same")

    labelSize = 0.035
    upScale = 0.75
    labelATLAS = TLatex(0.5,0.25,"#bf{Citi} Bike Analysis");
    labelATLAS.SetNDC();
    labelATLAS.SetTextFont(42);
    labelATLAS.SetTextSize(labelSize/upScale);
    labelATLAS.SetLineWidth(2);
    labelATLAS.Draw("same")


    c.Print(path)

    c.Close()

