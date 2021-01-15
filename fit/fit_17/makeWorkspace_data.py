
#############################
from ROOT import *

from xgboost import XGBClassifier
import pickle

BDT_filename="/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/weight/nodR/model_ALP_massindependent_2017.pkl"
mvaCut = 0.8571
model = pickle.load(open(BDT_filename, 'rb'))

#############################

myfile = TFile('/publicfs/cms/user/wangzebing/ALP/Analysis_out/17/massInde/ALP_data.root')
mychain = myfile.Get('passedEvents')
entries = mychain.GetEntriesFast()
print entries


w = RooWorkspace("CMS_hza_workspace")

Sqrts = RooRealVar("Sqrts","Sqrts",13)
CMS_hza_mass = RooRealVar("CMS_hza_mass","CMS_hza_mass",15,0.8,40)

getattr(w,'import')(Sqrts)
getattr(w,'import')(CMS_hza_mass)


data_mass_cat0 = RooDataSet("data_mass_cat0","data_mass_cat0",RooArgSet(CMS_hza_mass))

for jentry in range(entries):
    nb = mychain.GetEntry(jentry)
    if not mychain.passChaHadIso: continue
    if not mychain.passNeuHadIso: continue
    if not mychain.passdR_gl: continue
    if not mychain.passHOverE: continue
    if mychain.H_m>130. or mychain.H_m<118.: continue

    MVA_list = [mychain.pho1Pt, mychain.pho1eta, mychain.pho1phi, mychain.pho1R9, mychain.pho1IetaIeta55 ,mychain.pho2Pt, mychain.pho2eta, mychain.pho2phi, mychain.pho2R9, mychain.pho2IetaIeta55,mychain.ALP_calculatedPhotonIso, mychain.var_dR_g1Z, mychain.var_Pta, mychain.var_MhMZ, mychain.H_pt ]
    MVA_value = model.predict_proba(MVA_list)[:, 1]
    if MVA_value < mvaCut:continue
    if mychain.ALP_m < 0.8: continue
    #print mychain.ALP_dR

    CMS_hza_mass.setVal(mychain.ALP_m)
    data_mass_cat0.add(RooArgSet(CMS_hza_mass))


#getattr(w,'import')(data_mass_cat0)
getattr(w,'import')(data_mass_cat0)


w.writeToFile("ALP_data_bkg_workspace.root")
del w
