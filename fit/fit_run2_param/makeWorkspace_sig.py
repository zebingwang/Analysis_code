
#############################
from ROOT import *

from xgboost import XGBClassifier
import pickle


#############################
import argparse
parser = argparse.ArgumentParser(description="Prepare flashggFinalFit workspace: signal Fit")
parser.add_argument("-m", "--mass", dest="mass", type=float, default=1.0, help="ALP mass")
parser.add_argument("-dm", "--shift", dest="shift", type=float, default=5, help="shift ALP mass")
args = parser.parse_args()

mass = int(args.mass)
shift = int(args.shift)

BDT_filename="/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/weight/nodR/model_ALP_BDT_param_runII.pkl"
mvaCuts = {1:0.94, 5:0.945, 15:0.97, 30:0.97}
mvaCut = mvaCuts[mass]
model = pickle.load(open(BDT_filename, 'rb'))

####################
lumi = {'16':35.9, '17':41.5, '18':56.9}
for year in ['16','17','18']:

    print "prepare year: "+year

    filename = '/publicfs/cms/user/wangzebing/ALP/Analysis_out/'+year+'/massInde/ALP_M{0}.root'.format(mass)
    myfile = TFile(filename)
    if myfile:
        print "open " + filename + " success!"
    else:
        print filename + " does not exist!"
        sys.exit(0)
    mychain = myfile.Get('passedEvents')
    entries = mychain.GetEntriesFast()
    print "Entries: ",entries

    for mass_H in [125 - shift, 125, 125 + shift]:
        print "[[ INFO ]] prepare ALP mass: {0}".format(mass_H)
        w = RooWorkspace("CMS_hza_workspace")

        Sqrts = RooRealVar("Sqrts","Sqrts",13)
        IntLumi = RooRealVar("IntLumi","IntLumi", lumi[year])
        CMS_hza_mass = RooRealVar("CMS_hza_mass","CMS_hza_mass",mass_H,110.,180.)
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

        dataset = RooDataSet("ggh_{0}_13TeV_cat0".format(mass_H),"ggh_{0}_13TeV_cat0".format(mass_H), ArgSet, "CMS_hza_weight")
        #dataset_WithoutWeight = RooDataSet("dataset_WithoutWeight","dataset_WithoutWeight", ArgSet)

        #dataset.Print("v")
        #dataset_WithoutWeight.Print("v")
        #print type(ArgSet)
        #print "#"*51

        for jentry in range(entries):
            nb = mychain.GetEntry(jentry)
            if not mychain.passChaHadIso: continue
            if not mychain.passNeuHadIso: continue
            if not mychain.passdR_gl: continue
            if not mychain.passHOverE: continue
            if mychain.H_m>180. or mychain.H_m<110.: continue

            param = (mychain.ALP_m - mass)/mychain.H_m
            MVA_list = [mychain.pho1Pt, mychain.pho1eta, mychain.pho1phi, mychain.pho1R9, mychain.pho1IetaIeta55, mychain.pho1PIso_noCorr ,mychain.pho2Pt, mychain.pho2eta, mychain.pho2phi, mychain.pho2R9, mychain.pho2IetaIeta55,mychain.pho2PIso_noCorr,mychain.ALP_calculatedPhotonIso, mychain.var_dR_Za, mychain.var_dR_g1g2, mychain.var_dR_g1Z, mychain.var_PtaOverMh, mychain.H_pt, param]
            MVA_value = model.predict_proba(MVA_list)[:, 1]
            if MVA_value < mvaCut:continue
            #if mychain.passBDT < 0.5: continue
            #if mychain.ALP_m < 0.8: continue
            #if mychain.ALP_m > 40.: continue

            CMS_hza_mass.setVal(mychain.H_m + mass_H - 125.0)
            CMS_hza_weight.setVal(mychain.factor*mychain.pho1SFs_dR0P15*mychain.pho2SFs_dR0P15)
            dataset.add(ArgSet,mychain.factor*mychain.pho1SFs_dR0P15*mychain.pho2SFs_dR0P15)
            #dataset_WithoutWeight.add(ArgSet)

        dataset.Print("v")
        #dataset_WithoutWeight.Print("v")
        print type(ArgSet)
        print "#"*51

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

        w.writeToFile("ALP_data_sig_Am{0}_Hm{1}_{2}_workspace.root".format(mass,mass_H,year))
        del w

#raw_input()
