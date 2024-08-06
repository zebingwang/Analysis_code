#!/bin/bash
/bin/hostname
gcc -v
pwd
export PATH=$PATH:/afs/ihep.ac.cn/soft/common/sysgroup/hep_job/bin/
source /cvmfs/cms.cern.ch/cmsset_default.sh


#### job

##########hep_sub runjob.sh -g cms -mem 8000 -wt mid -o job.out -e job.err
#python ALP_plot_param.py -m -y 2016 

#python ALP_Optimization.py -y run2 -o ./optimize_run2 --doOpt -c 5
#python ALP_plot_param.py -y run2 -m --ln

#python ALP_plot_param.py -y run2 -m -S #--ln #--cut --mA M30
python makeWorkspace_sig_scalesmear.py -m 30




sysType = ['photon', 'lepton']
            
for scsm in param_float:
    line = "photonCat" + scsm +"="
    for p in sysType:
        line = line + p + '_' + scsm + '_M' + str(a_mass)+'_'+year + ','
    line.rstrip(',')
    file.write(line + '\n')

L = ['diphotonCat=0', 'proc=ggh']
for line in L:
    file.write(line + '\n')

mean_change = 0.0
sigma_change = 0.0
rate_change = 0.0

for scsm in param_float:
    for p in sysType:
        line = p + '_' + scsm + '_' + str(a_mass)+'_'+year +'\t'

        par_val_norm = -99.9
        par_val_change = -99.9

        for par in param_float[scsm]:

            for sys in sysList:

                if sys == 'normal':
                    if scsm == 'Scale':
                        par_val = fitResult['phoScale_up'].floatParsInit().find(par).getVal()
                    else:
                        par_val = fitResult['phoScale_up'].constPars().find(par).getVal()
                    par_val_norm = par_val
                else:
                    if scsm in sys:
                        par_val = fitResult[sys].floatParsFinal().find(par).getVal()
                    else:
                        par_val = fitResult[sys].constPars().find(par).getVal()

                if scsm == 'Scale':
                    if abs(par_val_norm - par_val)/(125.0+par_val_norm) > par_val_change:
                        par_val_change = abs(par_val_norm - par_val)/(125.0+par_val_norm)
                else:
                    if abs(par_val_norm - par_val) > par_val_change:
                        par_val_change = abs(par_val_norm - par_val)
        
        
        if scsm == 'Scale':
            line = line + str(par_val_change) + '\t0.0\t0.0'
        else:
            line = line + '0.0\t' + str(par_val_change) + '\t0.0'

        file.write(line + '\n')