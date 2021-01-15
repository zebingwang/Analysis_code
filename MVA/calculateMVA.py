#!/usr/bin/env python

from ROOT import TMVA, TFile, TString
from array import array
from subprocess import call
from os.path import isfile


def calMVA(weight_path, var_value):

    # Setup TMVA
    TMVA.Tools.Instance()
    TMVA.PyMethodBase.PyInitialize()
    reader = TMVA.Reader("Color:Silent")

    # Load data
    variables = ['pho1Pt','pho1R9','pho1IetaIeta','pho1HOE','pho1CIso','pho1NIso','pho1PIso','pho2Pt','pho2R9','pho2IetaIeta','pho2HOE','pho2CIso','pho2NIso','pho2PIso']
    branches = {}
    for var in variables:
        branches[var] = array('f', [-999])
        reader.AddVariable(var, branches[var])
        branches[var][0] = var_value[var]

    # Book methods
    reader.BookMVA('BDT method', TString('/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/weight/TMVAClassification_BDT_NTree150_nCut15.weights.xml'))

    value = reader.EvaluateMVA('BDT method')
    return value
