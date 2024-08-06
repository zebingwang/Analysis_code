#A script that will plot the desired distributions for both the signal tW and ttbar background for comparison.

#Import the root framework
from ROOT import *
from math import sqrt
import os,argparse

#Command line arguemnts
parser = argparse.ArgumentParser()

parser.add_argument("-v","--variables",default=["pho1Pt"],nargs="+",type=string,help="Space separated list of the variables to use")
parser.add_argument("-n","--normComparison",action="store_true",help="Make normalised comparisons between the tW signal and ttbar background for the desired distributions")
parser.add_argument("--stackPlots",action="store_true",help="Make data/MC plots for the desired distributions")
parser.add_argument("--makeLatexFile",action="store_true",help="Make a latex file that will display all the produced historgrans")
parser.add_argument("--calculateSeparation",action="store_true",help="If we are making the normalised comparison plots this argument will calculate the separation power of the variable")
parser.add_argument("--rebinHists",  dest="rebinHists", type=int, default=1, help="rebin hist")

args = parser.parse_args()

#Set up the style we want the plots to use
from plotStyleFile import setPlotStyle
setPlotStyle()

#This disables pop up xwindows
gROOT.SetBatch()


#The directory containing the scripts and trees
baseDir = "/publicfs/cms/user/wangzebing/ALP/Analysis_out/"

s = 5 # 1 for signal 2 for DY 3 for data
version = 'RerecoUL'
if s == 1:
    mass = 'M15'
    year = '17'

    sigFileName_Rereco = "Rereco/17/massInde/ALP_"+mass+".root"
    sigFileName_UL = "UL_v1/"+year+"/ALP_"+mass+".root"
elif s == 2:
    mass = 'DY'
    year = '18'

    sigFileName_Rereco = "Rereco/"+year+"/massInde/ALP_DYJetsToLL.root"
    sigFileName_UL = "UL_v1/"+year+"/ALP_DYJetsToLL.root"
elif s == 3:
    mass = 'data'
    year = '17'

    sigFileName_Rereco = "Rereco/"+year+"/massInde/ALP_data.root"
    sigFileName_UL = "UL_v1/"+year+"/ALP_data.root"
elif s ==4:
    mass = 'M1'
    year = '17'

    version = 'Rereco'

    sigFileName_Rereco = "Rereco/"+year+"/massInde/ALP_DYJetsToLL.root"
    sigFileName_UL = "Rereco/"+year+"/massInde/ALP_"+mass+".root"
else:
    mass = 'M15'
    year = '17'

    version = 'UL'

    sigFileName_Rereco = "UL/"+year+"/ALP_DYJetsToLL.root"
    sigFileName_UL = "UL/"+year+"/ALP_"+mass+".root"


variablesToCompare = args.variables
#You can also edit this list to select the variables from within the script
variablesToCompare = [
"pho1Pt",
"pho1R9",
"pho1IetaIeta55",
"pho1PIso_noCorr",
"pho2Pt",
"pho2R9",
"pho2IetaIeta55",
"pho2PIso_noCorr",
"ALP_calculatedPhotonIso",
"var_dR_Za",
"var_dR_g1g2",
"var_dR_g1Z",
"var_PtaOverMh",
"H_pt"
]

var_log = [
"GENlep_mass",
"lep_mass"
]

rebinHists = args.rebinHists

#Make the output directory if it doesn't exist
if not os.path.exists("plot_compare_BDTVar_"+version+"_"+year+mass): os.mkdir("plot_compare_BDTVar_"+version+"_"+year+mass)


def calculateSeparation(histArg1,histArg2):
    #Calculates the mathematical separation of the two histograms

    #Make copies so the scaling doesn't mess everyhting up
    (hist1,hist2) = (histArg1,histArg2)

    #Firstly make sure the integral of the histograms is unity
    hist1.Scale(1./hist1.Integral())
    hist2.Scale(1./hist2.Integral())

    #Now calculate the separation.
    sep = 0.
    for i in range(1,hist1.GetXaxis().GetNbins()+1):
        if not ( hist1.GetBinContent(i) + hist2.GetBinContent(i) ) == 0:
            sep+=((hist1.GetBinContent(i) - hist2.GetBinContent(i))*(hist1.GetBinContent(i) - hist2.GetBinContent(i)))/(hist1.GetBinContent(i) + hist2.GetBinContent(i))
    sep = sqrt(sep/2)
    return sep

def makeLegend():
    #Make a legend in the corner of the canvas
    legend = TLegend(0.8,0.92,0.9,0.7)
    legend.SetFillStyle(1001)
    legend.SetBorderSize(1)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetShadowColor(0)
    legend.SetFillColor(kWhite)

    return legend

def getVariableHists(sigTree,bkgTree,varName,cut="passChaHadIso&&passNeuHadIso&&passdR_gl&&passHOverE"):

    #print varName

    #Make a canvas to do the work on
    canvas = TCanvas(varName,varName,1000,800)

    #Extract the relevant variable from the trees

    bkgTree.Draw("{0}>>sig{0}".format(varName),"factor*pho1SFs*pho2SFs*({0})".format(cut))
    bkgHist = gDirectory.Get("sig{0}".format(varName))

    #Get some properties so that we have matching histograms
    xMin = bkgHist.GetXaxis().GetXmin()
    xMax = bkgHist.GetXaxis().GetXmax()
    nBins = bkgHist.GetXaxis().GetNbins()

    sigTree.Draw("{0}>>bkg{0}({1},{2},{3})".format(varName,nBins,xMin,xMax),"factor*pho1SFs*pho2SFs*({0})".format(cut))
    sigHist = gDirectory.Get("bkg{0}".format(varName))

    canvas.Clear()

    #tWHist.Scale(masterLumiScale)
    #ttbarHist.Scale(masterLumiScale)

    return (sigHist,bkgHist)


def makeComparisonPlot(sigHist1,bkgHist1,varName):

    #We will be making changes to these histograms, but we don't want them done universally, so here we'll copy them
    (sigHist,bkgHist) = (sigHist1,bkgHist1)

    #Make a canvas to do the work on
    canvas = TCanvas(varName+"_comp",varName+"_comp",1000,800)
    if varName in var_log: canvas.SetLogy()
    #Mke a legend
    legend = makeLegend()

    #Normalise the distributions and set their appropriate colours
    sigHist.Scale(1./sigHist.Integral())
    sigHist.SetFillColor(0)
    sigHist.SetLineColor(kBlue)
    sigHist.SetLineWidth(3)
    sigHist.Rebin(rebinHists)
    sigHist.Draw("HIST")
    sigHist.GetXaxis().SetTitle(varName)
    #legend.AddEntry(sigHist,"Rereco","l")
    legend.AddEntry(sigHist,"sig","l")

    bkgHist.Scale(1./bkgHist.Integral())
    bkgHist.SetFillColor(0)
    bkgHist.SetLineColor(kRed)
    bkgHist.SetLineWidth(3)
    bkgHist.Rebin(rebinHists)
    bkgHist.Draw("sameHIST")
    #legend.AddEntry(bkgHist,"UL","l")
    legend.AddEntry(bkgHist,"bkg","l")

    #Do a quick trick to make sure we see the entire distribution
    if bkgHist.GetMaximum() > sigHist.GetMaximum() : sigHist.SetMaximum(1.2*bkgHist.GetMaximum())

    legend.Draw("same")

    if args.calculateSeparation:
        separation = calculateSeparation(sigHist,bkgHist)
        print "Variable name: {0} \tSeparation: {1:.3f}".format(varName,separation)        #Add the separation to the plot:
        legend.AddEntry(0,"Sep: {0:.3f}".format(separation),"")

    canvas.SaveAs("plot_compare_BDTVar_"+version+"_"+year+mass+"/{0}_comp.png".format(varName))




def main():
    #Open the files to compare
    sigFile = TFile(baseDir+sigFileName_UL,"READ")
    bkgFile = TFile(baseDir+sigFileName_Rereco,"READ")

    #Get the trees to compare
    sigTree = sigFile.Get("passedEvents")
    bkgTree = bkgFile.Get("passedEvents")

    if not sigTree: print "open signal tree file fail."
    if not bkgTree: print "open background tree file fail."

    print variablesToCompare

    for var in variablesToCompare:
        #Draw the branches of the trees into histograms
        print "In var: "+var
        (sigHist,bkgHist) = getVariableHists(sigTree,bkgTree,var)

        if not sigHist: print "open signal file fail."
        if not bkgHist: print "open background file fail."

        if args.normComparison:
            makeComparisonPlot(sigHist,bkgHist,var)





if __name__ == "__main__":
    main()
