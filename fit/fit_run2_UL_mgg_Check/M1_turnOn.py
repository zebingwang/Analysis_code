
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
mvaCut = {'M1':0.955, 'M2':0.98, 'M3':0.985, 'M4':0.98, 'M5':0.985, 'M6':0.99, 'M7':0.985, 'M8':0.99, 'M9':0.99, 'M10':0.99, 'M15':0.99, 'M20':0.99, 'M25':0.985, 'M30':0.98}
#mvaCut = 0.1

BDT_filename="/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/weight/UL/model_ALP_BDT_param.pkl"


model = pickle.load(open(BDT_filename, 'rb'))

############################
myfile = TFile('/publicfs/cms/user/wangzebing/ALP/Analysis_out/UL/run2/ALP_data.root')
#myfile = TFile('/publicfs/cms/user/wangzebing/ALP/Analysis_out/UL/run2/ALP_DYJetsToLL.root')
mychain = myfile.Get('passedEvents')
entries = mychain.GetEntriesFast()
print entries

histos_ALP= TH1F('ALP_m', 'ALP_m', 50,  0., 35.)

for jentry in range(entries):
    nb = mychain.GetEntry(jentry)
    if mychain.passChaHadIso: continue
    if mychain.passNeuHadIso: continue
    if mychain.passdR_gl: continue
    if mychain.passHOverE: continue
    if mychain.H_m<95. or mychain.H_m>180.: continue
    #if mychain.H_m>115. and mychain.H_m<135.: continue


    param = (mychain.ALP_m - float(mass))/mychain.H_m
    MVA_list = [mychain.pho1Pt, mychain.pho1R9, mychain.pho1IetaIeta55, mychain.pho1PIso_noCorr ,mychain.pho2Pt, mychain.pho2R9, mychain.pho2IetaIeta55,mychain.pho2PIso_noCorr,mychain.ALP_calculatedPhotonIso, mychain.var_dR_Za, mychain.var_dR_g1g2, mychain.var_dR_g1Z, mychain.var_PtaOverMh, mychain.H_pt, param]
    MVA_value = model.predict_proba(MVA_list)[:, 1]
    if MVA_value < mvaCut["M"+str(mass)]:continue
    #if MVA_value < mvaCut:continue


    histos_ALP.Fill(mychain.ALP_m,mychain.factor*mychain.pho1SFs*mychain.pho2SFs)
    
    

c = TCanvas("c","c")
c.cd()
histos_ALP.GetYaxis().SetTitle('Events / (%.2f GeV)' %histos_ALP.GetBinWidth(1))
histos_ALP.GetXaxis().SetTitle('m(h) GeV')
histos_ALP.Draw("HIST")
#c.SaveAs("mass1_dataCR_neu"+str(mvaCut)+".png".format(mass))
c.SaveAs("mass{0}.png".format(mass))
#c.SaveAs("mass{0}_DY.png".format(mass))
