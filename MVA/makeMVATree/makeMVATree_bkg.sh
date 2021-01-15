#!/bin/bash
/bin/hostname
gcc -v
pwd
export PATH=$PATH:/afs/ihep.ac.cn/soft/common/sysgroup/hep_job/bin/
source /cvmfs/cms.cern.ch/cmsset_default.sh

python ../Reduced-tree/runCondor/condorFile/codeFile/makePlots_LLA_MVAtree.py -i ../../NTuples/17/mc/ntuple_DYJetsToLL.root -o phoMVA_bkg.root -L 40.09 -xs 5338.0
