
#############################
from ROOT import *

from xgboost import XGBClassifier
import pickle

#############################

import argparse
parser = argparse.ArgumentParser(description="Prepare flashggFinalFit workspace: signal Fit")
parser.add_argument("-m", "--mass", dest="mass", type=float, default=1.0, help="ALP mass")
args = parser.parse_args()

mass = int(args.mass)

BDT_filename="/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/weight/nodR/model_ALP_BDT_param_2017.pkl"
mvaCuts = {5:0.985, 15:0.98, 30:0.975}
mvaCut = mvaCuts[mass]
model = pickle.load(open(BDT_filename, 'rb'))

############################
myfile = TFile('/publicfs/cms/user/wangzebing/ALP/Analysis_out/17/massInde/ALP_data.root')
mychain = myfile.Get('passedEvents')
entries = mychain.GetEntriesFast()
print entries


w = RooWorkspace("CMS_hza_workspace")

Sqrts = RooRealVar("Sqrts","Sqrts",13)
CMS_hza_mass = RooRealVar("CMS_hza_mass","CMS_hza_mass",125.,110.,180.)

getattr(w,'import')(Sqrts)
getattr(w,'import')(CMS_hza_mass)


data_mass_cat0 = RooDataSet("data_mass_cat0","data_mass_cat0",RooArgSet(CMS_hza_mass))

for jentry in range(entries):
    nb = mychain.GetEntry(jentry)
    if not mychain.passChaHadIso: continue
    if not mychain.passNeuHadIso: continue
    if not mychain.passdR_gl: continue
    if not mychain.passHOverE: continue
    if mychain.H_m<110. or mychain.H_m>180.: continue

    param = (mychain.ALP_m - mass)/mychain.H_m
    #MVA_list = [mychain.pho1Pt, mychain.pho1eta, mychain.pho1phi, mychain.pho1R9, mychain.pho1IetaIeta55 ,mychain.pho2Pt, mychain.pho2eta, mychain.pho2phi, mychain.pho2R9, mychain.pho2IetaIeta55,mychain.ALP_calculatedPhotonIso, mychain.var_dR_g1Z, mychain.var_Pta, mychain.var_MhMZ, mychain.H_pt, param]
    MVA_list = [mychain.pho1Pt, mychain.pho1eta, mychain.pho1phi, mychain.pho1R9, mychain.pho1IetaIeta55, mychain.pho1PIso_noCorr ,mychain.pho2Pt, mychain.pho2eta, mychain.pho2phi, mychain.pho2R9, mychain.pho2IetaIeta55,mychain.pho2PIso_noCorr,mychain.ALP_calculatedPhotonIso, mychain.var_dR_Za, mychain.var_dR_g1g2, mychain.var_dR_g1Z, mychain.var_PtaOverMh, mychain.H_pt, param]
    MVA_value = model.predict_proba(MVA_list)[:, 1]
    if MVA_value < mvaCut:continue
    #if mychain.passBDT < 0.5: continue
    #if mychain.H_m < 110.: continue
    #if mychain.H_m > 180.: continue
    #print mychain.ALP_dR

    #print mychain.H_m

    CMS_hza_mass.setVal(mychain.H_m)
    data_mass_cat0.add(RooArgSet(CMS_hza_mass))


#getattr(w,'import')(data_mass_cat0)
getattr(w,'import')(data_mass_cat0)


w.writeToFile("ALP_data_bkg_Am{0}_workspace.root".format(mass))
del w
