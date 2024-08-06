#!/bin/bash
massList=( 1 2 3 4 5 6 7 8 9 10 15 20 25 30 )

years=( 16 16APV 17 18 )

nMass=${#massList[@]}
nyear=${#years[@]}

for ((iBin=0; iBin<$nMass; iBin++))
    do
    for ((jBin=0; jBin<$nyear; jBin++))
        do
        sshpass -p WZB0@9.qq scp zewang@lxplus7.cern.ch:/afs/cern.ch/work/z/zewang/private/flashggfit/CMSSW_10_2_13/src/flashggFinalFit/Signal/ALP_SigModel_param_UL/fit_results_run2_ele/M${massList[$iBin]}/${years[$jBin]}/plots_ALP/paramDump_ggh_cat0txt paramDump_ggh_cat0_M${massList[$iBin]}_${years[$jBin]}.txt
        #spawn scp zewang@lxplus7.cern.ch:/afs/cern.ch/work/z/zewang/private/flashggfit/CMSSW_10_2_13/src/flashggFinalFit/Signal/ALP_SigModel_param_UL/fit_results_run2_ele/M${massList[$iBin]}/${years[$jBin]}/plots_ALP/paramDump_ggh_cat0txt paramDump_ggh_cat0_${massList[$iBin]}_${years[$jBin]}.txt
        #expect "Password:"
        #send "WZB0@9.qq"

    done
done