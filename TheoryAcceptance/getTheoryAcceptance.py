####################################################
####################################################

import os
import sys
import numpy as np

#sys.path.insert(0, '%s/lib' % os.getcwd())
from ROOT import *
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from scipy import interpolate
import math


def getVariableHistsEventsNumber_weight(Tree,varName,weight,cut=''):

    #Make a canvas to do the work on
    canvas = TCanvas(varName,varName,1000,800)

    #Extract the relevant variable from the trees
    Tree.Draw("{0}>>tree{0}".format(varName),"{0}*({1})".format(weight,cut))
    Hist = gDirectory.Get("tree{0}".format(varName))

    canvas.Clear()

    return Hist.Integral()

def main():

    mass_list = [1,2,3,4,5,6,7,8,9,10,15,20,25,30]
    years = ['16', '16APV', '17', '18']
    
    path_basic = '/publicfs/cms/user/wangzebing/ALP/Analysis_code/TheoryAcceptance/output/'

    acc = []

    for m in mass_list:
        
        file_name = path_basic+str(m)+'.root'
        
        file = TFile(file_name)
        filesTree = file.Get("passedEvents")

        dem_acceptance = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt_acceptance", "1","1")

        num_acceptance = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt_acceptance", "1", "pho1Pt_acceptance>0")

        acceptance = float(num_acceptance)/float(dem_acceptance)
        acc.append(acceptance)

    acc_norm = [item / acc[-1] for item in acc]

    func_pol3 = np.polyfit(mass_list,acc_norm,3)
    acc_fit_pol3 = np.poly1d(func_pol3)
    print acc_fit_pol3[1]
    print acc_fit_pol3
    func_pol2 = np.polyfit(mass_list,acc_norm,2)
    acc_fit_pol2 = np.poly1d(func_pol2)
    m = range(1,31)
    acc_pre_pol2 = acc_fit_pol2(m)
    acc_pre_pol3 = acc_fit_pol3(m)
    
    plt.xlabel('m(a) GeV')
    plt.ylabel('Theory Acceptance')

    plt.plot(mass_list, acc_norm, "o", c="black", label="data")
    plt.plot(m, acc_pre_pol2, "-", c="red", label="pol2")
    plt.plot(m, acc_pre_pol3, "-", c="blue", label="pol3")
    
    plt.grid()
    plt.legend(fontsize=8)
    plt.savefig('./results/Theory_acc.png')
    plt.close('all')
    



main()