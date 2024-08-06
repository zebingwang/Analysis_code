####################################################
####################################################

import os
import sys
import numpy as np

sys.path.insert(0, '%s/lib' % os.getcwd())
from ROOT import *
from matplotlib import pyplot as plt
from scipy import interpolate
import math


def getVariableHistsEventsNumber_weight(Tree,varName,weight,cut):

    #Make a canvas to do the work on
    canvas = TCanvas(varName,varName,1000,800)

    #Extract the relevant variable from the trees
    Tree.Draw("{0}>>tree{0}".format(varName),"{0}*({1})".format(weight,cut))
    Hist = gDirectory.Get("tree{0}".format(varName))

    canvas.Clear()

    return Hist.Integral()


def printFile(year,results,pdf):
    file = open('./results/theory_'+year+'.txt', 'a')

    if pdf:
        file.write('pdf uncertainty\n')
    else:
        file.write('qcd uncertainty\n')
    title = "sample\t\tall_up\t\t\tall_dn\t\t\tPtEta_up\t\t\t\tPtEta_dn\t\t\tacceptance_up\t\t\tacceptance_dn"
    file.write(title + '\n')

    for m in results.keys():
        line = ""
        line = "M"+str(m)+"\t\t"
        for r in results[m]:
            line = line +str(r) +"\t\t"
        file.write(line + '\n')


def main():

    mass_list = [1,2,3,4,5,6,7,8,9,10,15,20,25,30]
    years = ['16', '16APV', '17', '18']
    
    path_basic = '/publicfs/cms/user/wangzebing/ALP/Analysis_code/TheoryUnc/output/'

    for y in years:
        results_pdf = {}
        results_qcd = {}
        for m in mass_list:
            
            file_name = path_basic+str(m)+'_'+y+'.root'
            
            file = TFile(file_name)
            filesTree = file.Get("passedEvents")

            dem_all = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt", "1","1")
            num_all_pdf_up = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt", "event_pdfweight_up","1")
            num_all_pdf_dn = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt", "event_pdfweight_dn","1")

            dem_acceptance = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt_acceptance", "1", "pho1Pt_acceptance>0")
            num_acceptance_pdf_up = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt_acceptance", "event_pdfweight_up", "pho1Pt_acceptance>0")
            num_acceptance_pdf_dn = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt_acceptance", "event_pdfweight_dn", "pho1Pt_acceptance>0")

            all_pdf_up = num_all_pdf_up/dem_all
            all_pdf_dn = num_all_pdf_dn/dem_all

            acceptance_pdf_up = num_acceptance_pdf_up/dem_acceptance
            acceptance_pdf_dn = num_acceptance_pdf_dn/dem_acceptance

            final_pdf_up =  math.sqrt(abs(pow(acceptance_pdf_up-1,2) - pow(all_pdf_up-1,2)))
            final_pdf_dn =  math.sqrt(abs(pow(1-acceptance_pdf_dn,2) - pow(1-all_pdf_dn,2)))

            results_pdf[m] = [all_pdf_up, all_pdf_dn, acceptance_pdf_up, acceptance_pdf_dn, final_pdf_up, final_pdf_dn]

            ## qcd
            num_all_qcd_up = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt", "event_qcdweight_up","1")
            num_all_qcd_dn = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt", "event_qcdweight_dn","1")

            num_acceptance_qcd_up = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt_acceptance", "event_qcdweight_up", "pho1Pt_acceptance>0")
            num_acceptance_qcd_dn = getVariableHistsEventsNumber_weight(filesTree, "pho1Pt_acceptance", "event_qcdweight_dn", "pho1Pt_acceptance>0")

            all_qcd_up = num_all_qcd_up/dem_all
            all_qcd_dn = num_all_qcd_dn/dem_all

            acceptance_qcd_up = num_acceptance_qcd_up/dem_acceptance
            acceptance_qcd_dn = num_acceptance_qcd_dn/dem_acceptance

            final_qcd_up =  math.sqrt(abs(pow(acceptance_qcd_up-1,2) - pow(all_qcd_up-1,2)))
            final_qcd_dn =  math.sqrt(abs(pow(1-acceptance_qcd_dn,2) - pow(1-all_qcd_dn,2)))

            results_qcd[m] = [all_qcd_up, all_qcd_dn, acceptance_qcd_up, acceptance_qcd_dn, final_qcd_up, final_qcd_dn]


            #output = "Total events: ", dem_all, ", all_up: ", all_up, ", all_dn: ", all_dn, "; Events after accptance cut: ", dem_acceptance, ", acceptance_up: ", acceptance_up, ", acceptance_dn: ", acceptance_dn, "; Final acceptance: Up: ", final_up, ", Dn: ", final_dn
            #print ' '.join(map(str,output))

        printFile(y,results_pdf,1)
        printFile(y,results_qcd,0)
main()