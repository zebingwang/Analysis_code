
#############################
from ROOT import *

from xgboost import XGBClassifier
import pickle

BDT_filename="/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/weight/nodR/model_ALP_massindependent.pkl"
mvaCut = 0.8556
model = pickle.load(open(BDT_filename, 'rb'))
#############################

myfile = TFile('/publicfs/cms/user/wangzebing/ALP/Analysis_out/17/sample_M30/ALP_M15.root')
mychain = myfile.Get('passedEvents')
entries = mychain.GetEntriesFast()
print "Entries: ",entries


w = RooWorkspace("CMS_hza_workspace")

Sqrts = RooRealVar("Sqrts","Sqrts",13)
IntLumi = RooRealVar("IntLumi","IntLumi",41.5)
CMS_hza_mass = RooRealVar("CMS_hza_mass","CMS_hza_mass",15,0.8,40)
CMS_hza_weight = RooRealVar("CMS_hza_weight","CMS_hza_weight",-100000,1000000)


getattr(w,'import')(Sqrts)
getattr(w,'import')(IntLumi)
getattr(w,'import')(CMS_hza_mass)
getattr(w,'import')(CMS_hza_weight)

ArgSet = RooArgSet("args")
ArgSet.add(CMS_hza_mass)
ArgSet.add(CMS_hza_weight)
print "#"*51
ArgSet.Print("v")
print "#"*51

ggh_14_13TeV_cat0 = RooDataSet("ggh_14_13TeV_cat0","ggh_14_13TeV_cat0", ArgSet, "CMS_hza_weight")
#ggh_14_13TeV_cat0_WithoutWeight = RooDataSet("ggh_14_13TeV_cat0_WithoutWeight","ggh_14_13TeV_cat0_WithoutWeight", ArgSet)

ggh_14_13TeV_cat0.Print("v")
#ggh_14_13TeV_cat0_WithoutWeight.Print("v")
print type(ArgSet)
print "#"*51

for jentry in range(entries):
    nb = mychain.GetEntry(jentry)
    if mychain.Z_dR < -90: continue
    if mychain.dR_pho < 0.02: continue
    if not mychain.passHOverE: continue
    if mychain.H_pho_veto>130. or mychain.H_pho_veto<118.: continue

    MVA_list = [mychain.pho1IetaIeta55, mychain.pho1PIso_noCorr, mychain.pho2IetaIeta55, mychain.pho2PIso_noCorr, mychain.ALP_calculatedPhotonIso, mychain.var_PtaOverMh, mychain.var_MhMZ, mychain.var_dR_g1g2]
    MVA_value = model.predict_proba(MVA_list)[:, 1]
    if MVA_value < mvaCut:continue
    if mychain.ALP_dR < 0.8: continue

    CMS_hza_mass.setVal(mychain.ALP_dR-1.0)
    CMS_hza_weight.setVal(mychain.factor)
    ggh_14_13TeV_cat0.add(ArgSet,mychain.factor)
    #ggh_14_13TeV_cat0_WithoutWeight.add(ArgSet)

c1 = TCanvas("c1","With Weight")
massDist = CMS_hza_mass.frame(RooFit.Title("CMS_hza_mss"))
ggh_14_13TeV_cat0.plotOn(massDist)
massDist.Draw()
'''
c2 = TCanvas("c2","Without Weight")
massDist2 = CMS_hza_mass.frame(RooFit.Title("CMS_hza_mss"))
ggh_14_13TeV_cat0_WithoutWeight.plotOn(massDist2)
massDist2.Draw()
'''
getattr(w,'import')(ggh_14_13TeV_cat0)
#getattr(w,'import')(ggh_14_13TeV_cat0_WithoutWeight)

w.writeToFile("ALP_data_sig_m14_workspace.root")

del w
#raw_input()
