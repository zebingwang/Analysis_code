
#############################
from ROOT import *
import os
import sys
import numpy as np
from array import array
import math

from xgboost import XGBClassifier
import pickle

#############################

import argparse
parser = argparse.ArgumentParser(description="Prepare flashggFinalFit workspace: signal Fit")
parser.add_argument("-m", "--mass", dest="mass", type=float, default=1.0, help="ALP mass")
parser.add_argument('--interp', dest='interp', action='store_true', default=False, help='interpolation?')
args = parser.parse_args()

mass = int(args.mass)
mvaCuts = {}

mvaCuts['norm'] = {11:0.99, 12:0.99, 13:0.99, 14:0.99, 16:0.99, 17:0.99, 18:0.99, 19:0.99, 21:0.99, 22:0.99, 23:0.985, 24:0.985, 26:0.985, 27:0.985, 28:0.98, 29:0.98}
mvaCuts['left'] = {11:0.99, 12:0.99, 13:0.99, 14:0.99, 16:0.99, 17:0.99, 18:0.99, 19:0.99, 21:0.99, 22:0.99, 23:0.99, 24:0.99, 26:0.985, 27:0.985, 28:0.985, 29:0.985}
mvaCuts['right'] = {11:0.99, 12:0.99, 13:0.99, 14:0.99, 16:0.99, 17:0.99, 18:0.99, 19:0.99, 21:0.985, 22:0.985, 23:0.985, 24:0.985, 26:0.98, 27:0.98, 28:0.98, 29:0.98}



BDT_filename="/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/weight/UL/model_ALP_BDT_param.pkl"


model = pickle.load(open(BDT_filename, 'rb'))

def hist2graph(hist, mva_low = 0.1):
    
    Nbins = hist.GetNbinsX()
    bin_x_low = hist.FindBin(mva_low)
    xaxis = hist.GetXaxis()

    bin_x_Center=[]
    bin_y=[]
    for x in range(Nbins+1):
        # remove BDT score less than mva_low
        if x < bin_x_low: continue
        bin_x_Center.append(xaxis.GetBinCenter(x))
        bin_y.append(hist.GetBinContent(x))

    graph = TGraph(Nbins-bin_x_low+1, np.array(bin_x_Center), np.array(bin_y))

    return graph

def smooth(graph, hist, mva_low = 0.1):
    h_smooth = TH1F(hist.GetName()+"_smooth",hist.GetName()+"_smooth",hist.GetNbinsX(),0.0,1.0)
    h_smooth_up = TH1F(hist.GetName()+"_smooth_up",hist.GetName()+"_smooth_up",hist.GetNbinsX(),0.0,1.0)
    h_smooth_dn = TH1F(hist.GetName()+"_smooth_dn",hist.GetName()+"_smooth_dn",hist.GetNbinsX(),0.0,1.0)

    smoother = TGraphSmooth()
    g_smooth = smoother.SmoothSuper(graph)

    xaxis = hist.GetXaxis()
    x = array('d', [0])
    y = array('d', [0])

    for i in range(1, hist.GetNbinsX()+1):

        h_x = xaxis.GetBinCenter(i)

        if i < hist.FindBin(mva_low):
            y[0] = 0.0
        else:
            g_smooth.GetPoint(i,x,y)

        h_smooth.SetBinContent(i,y[0])

    for i in range(1, hist.GetNbinsX()+1):

        if i < hist.FindBin(mva_low):
            y[0] = 0.0
        else:
            y = h_smooth.GetBinContent(i)

        #print y
        #print np.sqrt(y)

        if y>=0.:
            h_smooth_up.SetBinContent(i,y+np.sqrt(y))
            if (y-np.sqrt(y))>0.: h_smooth_dn.SetBinContent(i,y-np.sqrt(y))
            else: h_smooth_dn.SetBinContent(i,0.)
        else:
            h_smooth_up.SetBinContent(i,0.)
            h_smooth_dn.SetBinContent(i,0.)


            

    return [h_smooth, h_smooth_up, h_smooth_dn]



############################
myfile = TFile('/publicfs/cms/user/wangzebing/ALP/Analysis_out/UL/run2/ALP_DYJetsToLL.root')
mychain = myfile.Get('passedEvents')
entries = mychain.GetEntriesFast()
print entries

histos = {}
updates=0

for m in mvaCuts['norm']:
    histos[m] = TH1F('hist_'+str(m), 'hist_'+str(m), 200,  0., 1.)

for jentry in range(entries):
    nb = mychain.GetEntry(jentry)
    #if jentry > 1000: break

    finished = 100*(float(jentry)/float(entries))
    if divmod(finished, 5)[0] == updates and round(divmod(finished, 5)[1],3) == 0:
        updates += 1
        print '{0}%'.format(round(finished,2))

    if not mychain.passChaHadIso: continue
    if not mychain.passNeuHadIso: continue
    if not mychain.passdR_gl: continue
    if not mychain.passHOverE: continue
    #if mychain.H_m<95. or mychain.H_m>180.: continue
    if mychain.H_m<115. or mychain.H_m>135.: continue

    for m in mvaCuts['norm']:
        param = (mychain.ALP_m - float(m))/mychain.H_m
        MVA_list = [mychain.pho1Pt, mychain.pho1R9, mychain.pho1IetaIeta55, mychain.pho1PIso_noCorr ,mychain.pho2Pt, mychain.pho2R9, mychain.pho2IetaIeta55,mychain.pho2PIso_noCorr,mychain.ALP_calculatedPhotonIso, mychain.var_dR_Za, mychain.var_dR_g1g2, mychain.var_dR_g1Z, mychain.var_PtaOverMh, mychain.H_pt, param]
        MVA_value = model.predict_proba(MVA_list)[:, 1]

        histos[m].Fill(MVA_value, mychain.factor*mychain.pho1SFs*mychain.pho2SFs)

graph = {}
hist_smooth = {}
bkg_smooth = {}
print ['left', 'norm', 'right']

for m in mvaCuts['norm']:
    graph[m] = hist2graph(histos[m], 0.01)
    hist_smooth[m] = smooth(graph[m], histos[m], 0.01)
    bkg_smooth = []
    for b in ['left', 'norm', 'right']:
        bkg_smooth.append(hist_smooth[m][0].Integral(int(mvaCuts[b][m]/0.005),200))

    print "mass: ",m,bkg_smooth
    


