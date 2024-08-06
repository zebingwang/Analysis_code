#A script that will plot the desired distributions for both the signal tW and ttbar background for comparison.

#Import the root framework
from ROOT import *

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

mass = 'M1'
year = '17'

#The directory containing the scripts and trees
baseDir = "/publicfs/cms/user/wangzebing/ALP/NTuples/"

sigFileName_Rereco = "17/sig/HZA_"+mass+"_2017.root"
sigFileName_UL = "UL/"+year+"/sig/ntuple_"+mass+".root"

variablesToCompare = args.variables
#You can also edit this list to select the variables from within the script
variablesToCompare = [
"GENlep_pt",
"GENlep_eta",
"GENlep_phi",
"GENlep_mass",
"GENlep_id",
"lep_mass",
"lep_id",
"GENlep_RelIso",
"GENpho_pt",
"GENpho_eta",
"GENpho_phi",
"GENpho_energy"
]

var_log = [
"GENlep_mass",
"lep_mass"
]

rebinHists = args.rebinHists

#Make the output directory if it doesn't exist
if not os.path.exists("plot_compare_KineVar_RerecoUL_"+year+mass): os.mkdir("plot_compare_KineVar_RerecoUL_"+year+mass)


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

def getVariableHists(sigTree,bkgTree,varName,cut="EventWeight>0."):

    #print varName

    #Make a canvas to do the work on
    canvas = TCanvas(varName,varName,1000,800)

    #Extract the relevant variable from the trees

    bkgTree.Draw("{0}>>sig{0}".format(varName))
    bkgHist = gDirectory.Get("sig{0}".format(varName))

    #Get some properties so that we have matching histograms
    xMin = bkgHist.GetXaxis().GetXmin()
    xMax = bkgHist.GetXaxis().GetXmax()
    nBins = bkgHist.GetXaxis().GetNbins()

    sigTree.Draw("{0}>>bkg{0}({1},{2},{3})".format(varName,nBins,xMin,xMax))
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
    legend.AddEntry(sigHist,"Rereco","l")

    bkgHist.Scale(1./bkgHist.Integral())
    bkgHist.SetFillColor(0)
    bkgHist.SetLineColor(kRed)
    bkgHist.SetLineWidth(3)
    bkgHist.Rebin(rebinHists)
    bkgHist.Draw("sameHIST")
    legend.AddEntry(bkgHist,"UL","l")

    #Do a quick trick to make sure we see the entire distribution
    if bkgHist.GetMaximum() > sigHist.GetMaximum() : sigHist.SetMaximum(1.2*bkgHist.GetMaximum())

    legend.Draw("same")

    if args.calculateSeparation:
        separation = calculateSeparation(sigHist,bkgHist)
        print "Variable name: {0} \tSeparation: {1:.3f}".format(varName,separation)        #Add the separation to the plot:
        legend.AddEntry(0,"Sep: {0:.3f}".format(separation),"")

    canvas.SaveAs("plot_compare_KineVar_RerecoUL_"+year+mass+"/{0}_comp.png".format(varName))




def main():
    #Open the files to compare
    sigFile = TFile(baseDir+sigFileName_Rereco,"READ")
    bkgFile = TFile(baseDir+sigFileName_UL,"READ")

    #Get the trees to compare
    sigTree = sigFile.Ana.Get("passedEvents")
    bkgTree = bkgFile.Ana.Get("passedEvents")

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
