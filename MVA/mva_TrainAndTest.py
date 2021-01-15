import ROOT as rt
from root_numpy import root2array, tree2array
#from root_pandas import read_root
import h5py

import numpy as np
import numpy.lib.recfunctions as nlr
import pandas as pd
import os, sys
from matplotlib import pyplot as plt
import math

from sklearn.metrics import accuracy_score, roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier
from xgboost import plot_tree

import pickle

def convert(tree):
    feature = tree2array(tree,
                        branches = id_variables+wt_variables + variables,
                        selection = 'Z_pho_veto>-90 && passChaHadIso && passNeuHadIso && passdR_gl && passdR_gg && passHOverE')
    return feature

def convert_ntuple_dataframe(path, filename,treename):
    rootfile = rt.TFile.Open(path+filename)
    tree = rootfile.Get(treename)
    np =convert(tree)
    dataframe = pd.DataFrame.from_records(np)
    return dataframe, tree

    ###
def main():
    #path='/eos/cms/store/user/nlu/Hmm/CMSDAS122019/ntuple/vbfcategory/'
    path=''
    sig_FILE='/publicfs/cms/user/wangzebing/ALP/Analysis_out/17/ALP_M1.root'
    ggh_FILE='ggh_amcPS_nominal.root'
    ewz_FILE='ewk_lljj_mll105_160_nominal.root'
    dy_FILE='/publicfs/cms/user/wangzebing/ALP/Analysis_code/MVA/DY.root'

    global variables
    variables = ['pho1IetaIeta55','pho2IetaIeta55','pho1PIso_noCorr','pho2PIso_noCorr','ALP_calculatedPhotonIso']
    global id_variables
    id_variables = ['Run','LumiSect','Event']
    global wt_variables
    wt_variables = ['event_weight']

    dfs = []
    df_sig, sigtree_vbf = convert_ntuple_dataframe(path,sig_FILE,"passedEvents")
    df_bkg_dy, bkgtree_dy = convert_ntuple_dataframe(path,dy_FILE,"passedEvents")
    #df_bkg_ewz, bkgtree_ewz = convert_ntuple_dataframe(path,ewz_FILE,"tree")
    #df_sig_ggh, sigtree_ggh = convert_ntuple_dataframe(path,ggh_FILE,"tree")


    dfs.append(df_sig)
    dfs.append(df_bkg_dy)
    #dfs.append(df_bkg_ewz)
    #dfs.append(df_sig_ggh)

    ###

    xlabel= ['leading photon SigmaIEtaIEta 5 by 5','sub-leading SigmaIEtaIEta Isolation 5 by 5','leading photon Photon Isolation','sub-leading photon Photon Isolation', 'ALP Photon Isolation']

    for hlf,xlabel_hlf in zip(variables,xlabel):
        plt.figure()
        plt.hist(dfs[0][hlf], bins=40, normed=True, histtype='step', label='signal')
        #plt.hist(dfs[3][hlf], bins=40, normed=True, histtype='step', label='ggH signal')
        plt.hist(dfs[1][hlf], bins=40, normed=True, histtype='step', label='DY bkg')
        #plt.hist(dfs[2][hlf], bins=40, normed=True, histtype='step', label='EW-Z bkg')
        plt.xlabel(xlabel_hlf)
        plt.ylabel('Events (normalized to unit area)')
        plt.legend(loc='best')

        plt.show()

    ###
    var_indices = [dfs[0].columns.get_loc(v) for v in variables] # get positions of all the variables set above
    id_var_indices = [dfs[0].columns.get_loc(v) for v in id_variables]
    wt_var_indices = [dfs[0].columns.get_loc(v) for v in wt_variables]

    signal = dfs[0].values
    background_dy = dfs[1].values

    print "Number of VBF signal MC events:",len(signal)
    print "Number of background DY MC events:",len(background_dy)

    nsigw = np.sum(signal[:,wt_var_indices])
    nbkgw_dy = np.sum(background_dy[:,wt_var_indices])

    print "expected number of events for signal: "
    print nsigw
    print "expected number of events for dy bkg: "
    print nbkgw_dy

    ###
    #signal label as 1, bkg label as 0 (ground truth)
    sig_label = np.ones(len(signal))
    bkg_label_dy = np.zeros(len(background_dy))

    sig_proc = np.ones(len(signal))
    bkg_proc_dy = np.zeros(len(background_dy))

    x = np.concatenate((signal,background_dy))
    y = np.concatenate((sig_label,bkg_label_dy))
    z = np.concatenate((sig_proc,bkg_proc_dy))

    ###
    # split data into train and test sets
    seed = 7
    test_size = 0.4
    x_train, x_test, y_train, y_test, z_train, z_test = train_test_split(x, y, z, test_size=test_size, random_state=seed)

    # For training we ignore the columns with the event ID information
    x_train_reduced = x_train[:,var_indices]
    x_test_reduced = x_test[:,var_indices]
    x_test_index = x_test[:,id_var_indices]
    x_test_w = x_test[:,wt_var_indices]

    model_file = 'model_ALP.pkl'

    #XGBClassifier/BDT model parameters
    #https://xgboost.readthedocs.io/en/latest/python/python_api.html

    depth=2
    learning_rate=0.5
    n_estimators=300


    # fit model no training sample
    model = XGBClassifier(depth,learning_rate,n_estimators)
    print(model)

    #early_stopping_rounds (int): Activates early stopping. Validation metric needs to improve at least once in every early_stopping_rounds round(s) to continue training.
    eval_set = [(x_train_reduced, y_train), (x_test_reduced, y_test)]
    model.fit(x_train_reduced, y_train,early_stopping_rounds=10,eval_metric=["logloss","error"],eval_set=eval_set,verbose=False)

    print("save model file ",model_file)
    output = open(model_file, 'wb')
    pickle.dump(model, output)
    output.close()

    # Read in model saved from previous running of BDT
    filename="model_ALP.pkl"
    # load the model from disk
    model = pickle.load(open(filename, 'rb'))

    # retrieve performance metrics
    results = model.evals_result()
    epochs = len(results['validation_0']['error'])
    x_axis = range(0, epochs)
    # plot log loss
    fig, ax = plt.subplots()
    ax.plot(x_axis, results['validation_0']['logloss'], label='Train')
    ax.plot(x_axis, results['validation_1']['logloss'], label='Test')
    ax.legend()
    plt.ylabel('Log Loss')
    plt.title('XGBoost Log Loss')
    plt.show()

    # plot classification error
    fig, ax = plt.subplots()
    ax.plot(x_axis, results['validation_0']['error'], label='Train')
    ax.plot(x_axis, results['validation_1']['error'], label='Test')
    ax.legend()
    plt.ylabel('Classification Error')
    plt.title('XGBoost Classification Error')
    plt.show()

    #make predictions for test sample
    y_pred = model.predict_proba(x_test_reduced)[:, 1]

    ##########################################################
    # make histogram of discriminator value for signal and bkg
    ##########################################################
    print(len(y_test))

    y_frame = pd.DataFrame({'truth':z_test, 'disc':y_pred, 'label':y_test})
    disc_bkg_dy    = y_frame[y_frame['truth'] == 0]['disc'].values
    disc_signal = y_frame[y_frame['truth'] == 1]['disc'].values
    plt.figure()
    plt.hist(disc_bkg_dy, normed=True, bins=50, alpha=0.3)
    plt.hist(disc_signal, normed=True, bins=50, alpha=0.3)
    plt.show()





if __name__ == "__main__":
    main()
