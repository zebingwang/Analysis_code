
#############################
from ROOT import *

from xgboost import XGBClassifier
import pickle

#############################

import argparse
parser = argparse.ArgumentParser(description="Prepare flashggFinalFit workspace: signal Fit")
parser.add_argument("-m", "--mass", dest="mass", type=float, default=1.0, help="ALP mass")
parser.add_argument('--interp', dest='interp', action='store_true', default=False, help='interpolation?')
args = parser.parse_args()

mass = int(args.mass)
#mvaCut = {'M1':0.955, 'M2':0.98, 'M3':0.985, 'M4':0.98, 'M5':0.985, 'M6':0.99, 'M7':0.985, 'M8':0.99, 'M9':0.99, 'M10':0.99, 'M15':0.99, 'M20':0.99, 'M25':0.985, 'M30':0.98}
mvaCut = 0.5

BDT_filename="/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/weight/UL/model_ALP_BDT_param.pkl"


model = pickle.load(open(BDT_filename, 'rb'))

############################
myfile_data = TFile('/publicfs/cms/user/wangzebing/ALP/Analysis_out/UL/run2/ALP_data.root')
mychain_data = myfile_data.Get('passedEvents')
entries_data = mychain_data.Getentries_dataFast()
print entries_data

myfile_DY = TFile('/publicfs/cms/user/wangzebing/ALP/Analysis_out/UL/run2/ALP_DYJetsToLL.root')
mychain_DY = myfile_DY.Get('passedEvents')
entries_DY = mychain_DY.Getentries_dataFast()

histos_H_data= TH1F('H_m', 'H_m', 50,  95., 180.)
histos_H_DY= TH1F('H_m', 'H_m', 50,  95., 180.)

Stack_H_DY= THStack('H_m', 'H_m')

for jentry in range(entries_data):
    nb = mychain_data.GetEntry(jentry)
    if not mychain_data.passChaHadIso: continue
    if not mychain_data.passNeuHadIso: continue
    if not mychain_data.passdR_gl: continue
    if not mychain_data.passHOverE: continue
    if mychain_data.H_m<95. or mychain_data.H_m>180.: continue
    #if mychain_data.H_m>115. and mychain_data.H_m<135.: continue


    param = (mychain_data.ALP_m - float(mass))/mychain_data.H_m
    MVA_list = [mychain_data.pho1Pt, mychain_data.pho1R9, mychain_data.pho1IetaIeta55, mychain_data.pho1PIso_noCorr ,mychain_data.pho2Pt, mychain_data.pho2R9, mychain_data.pho2IetaIeta55,mychain_data.pho2PIso_noCorr,mychain_data.ALP_calculatedPhotonIso, mychain_data.var_dR_Za, mychain_data.var_dR_g1g2, mychain_data.var_dR_g1Z, mychain_data.var_PtaOverMh, mychain_data.H_pt, param]
    MVA_value = model.predict_proba(MVA_list)[:, 1]
    #if MVA_value < mvaCut["M"+str(mass)]:continue
    if MVA_value < mvaCut:continue


    histos_H_data.Fill(mychain_data.H_m,mychain_data.factor*mychain_data.pho1SFs*mychain_data.pho2SFs)
 
for ientry in range(entries_DY):
    nb = mychain_DY.GetEntry(ientry)
    if not mychain_DY.passChaHadIso: continue
    if not mychain_DY.passNeuHadIso: continue
    if not mychain_DY.passdR_gl: continue
    if not mychain_DY.passHOverE: continue
    if mychain_DY.H_m<95. or mychain_DY.H_m>180.: continue
    #if mychain_DY.H_m>115. and mychain_DY.H_m<135.: continue


    param = (mychain_DY.ALP_m - float(mass))/mychain_DY.H_m
    MVA_list = [mychain_DY.pho1Pt, mychain_DY.pho1R9, mychain_DY.pho1IetaIeta55, mychain_DY.pho1PIso_noCorr ,mychain_DY.pho2Pt, mychain_DY.pho2R9, mychain_DY.pho2IetaIeta55,mychain_DY.pho2PIso_noCorr,mychain_DY.ALP_calculatedPhotonIso, mychain_DY.var_dR_Za, mychain_DY.var_dR_g1g2, mychain_DY.var_dR_g1Z, mychain_DY.var_PtaOverMh, mychain_DY.H_pt, param]
    MVA_value = model.predict_proba(MVA_list)[:, 1]
    #if MVA_value < mvaCut["M"+str(mass)]:continue
    if MVA_value < mvaCut:continue


    histos_H_DY.Fill(mychain_DY.H_m,mychain_DY.factor*mychain_DY.pho1SFs*mychain_DY.pho2SFs)
    

c = TCanvas("c","c")
c.cd()
Stack_H_DY.Add(histos_H_DY)
histos_H_data.GetYaxis().SetTitle('Events / (%.2f GeV)' %histos_H_data.GetBinWidth(1))
histos_H_data.GetXaxis().SetTitle('m(h) GeV')
histos_H_data.Draw("PE")
Stack_H_DY.Draw("HISTSAME")
histos_H_data.Draw("PE")
c.SaveAs("mass{0}_BDTcut{1}.png".format(mass,mvaCut))
