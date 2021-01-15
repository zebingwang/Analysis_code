
#############################
from ROOT import *

from xgboost import XGBClassifier
import pickle

BDT_filename="/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/weight/nodR/model_ALP_massindependent.pkl"
mvaCut = 0.8675
model = pickle.load(open(BDT_filename, 'rb'))
#############################
import argparse
parser = argparse.ArgumentParser(description="Prepare flashggFinalFit workspace: signal Fit")
parser.add_argument("-m", "--mass", dest="mass", type=float, default=1.0, help="ALP mass")
parser.add_argument("-dm", "--shift", dest="shift", type=float, default=1.0, help="shift ALP mass")
args = parser.parse_args()

mass = int(args.mass)
shift = int(args.shift)

filename = '/publicfs/cms/user/wangzebing/ALP/Analysis_out/17/massInde/ALP_M{0}.root'.format(mass)
myfile = TFile(filename)
if myfile:
    print "open " + filename + " success!"
else:
    print filename + " does not exist!"
    sys.exit(0)
mychain = myfile.Get('passedEvents')
entries = mychain.GetEntriesFast()
print "Entries: ",entries

for mass_shift in [mass - shift, mass, mass + shift]:
    print "[[ INFO ]] prepare ALP mass: {0}".format(mass_shift)
    w = RooWorkspace("CMS_hza_workspace")

    Sqrts = RooRealVar("Sqrts","Sqrts",13)
    IntLumi = RooRealVar("IntLumi","IntLumi",41.5)
    CMS_hza_mass = RooRealVar("CMS_hza_mass","CMS_hza_mass",mass_shift,0.8,40)
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

    dataset = RooDataSet("ggh_{0}_13TeV_cat0".format(mass_shift),"ggh_{0}_13TeV_cat0".format(mass_shift), ArgSet, "CMS_hza_weight")
    #dataset_WithoutWeight = RooDataSet("dataset_WithoutWeight","dataset_WithoutWeight", ArgSet)

    dataset.Print("v")
    #dataset_WithoutWeight.Print("v")
    print type(ArgSet)
    print "#"*51

    for jentry in range(entries):
        nb = mychain.GetEntry(jentry)
        if not mychain.passEleVeto: continue
        if not mychain.passChaHadIso: continue
        if not mychain.passNeuHadIso: continue
        if not mychain.passdR_gl: continue
        if not mychain.passHOverE: continue
        if mychain.H_m>130. or mychain.H_m<118.: continue

        MVA_list = [mychain.pho1Pt, mychain.pho1eta, mychain.pho1phi, mychain.pho1R9, mychain.pho1IetaIeta55 ,mychain.pho2Pt, mychain.pho2eta, mychain.pho2phi, mychain.pho2R9, mychain.pho2IetaIeta55,mychain.ALP_calculatedPhotonIso, mychain.var_dR_g1Z, mychain.var_Pta, mychain.var_MhMZ, mychain.H_pt ]
        MVA_value = model.predict_proba(MVA_list)[:, 1]
        if MVA_value < mvaCut:continue
        if mychain.ALP_m < 0.8: continue

        CMS_hza_mass.setVal(mychain.ALP_m + mass_shift - mass)
        CMS_hza_weight.setVal(mychain.factor)
        dataset.add(ArgSet,mychain.factor)
        #dataset_WithoutWeight.add(ArgSet)

    c1 = TCanvas("c1","With Weight")
    massDist = CMS_hza_mass.frame(RooFit.Title("CMS_hza_mss"))
    dataset.plotOn(massDist)
    massDist.Draw()
    '''
    c2 = TCanvas("c2","Without Weight")
    massDist2 = CMS_hza_mass.frame(RooFit.Title("CMS_hza_mss"))
    dataset_WithoutWeight.plotOn(massDist2)
    massDist2.Draw()
    '''
    getattr(w,'import')(dataset)
    #getattr(w,'import')(dataset_WithoutWeight)

    w.writeToFile("ALP_data_sig_m{0}_workspace.root".format(mass_shift))
    del w

#raw_input()
