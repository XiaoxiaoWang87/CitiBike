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
    if style == 2:
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

    if style == 2:
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
