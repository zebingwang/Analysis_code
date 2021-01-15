#!/bin/bash
/bin/hostname
gcc -v
pwd
export PATH=$PATH:/afs/ihep.ac.cn/soft/common/sysgroup/hep_job/bin/
source /cvmfs/cms.cern.ch/cmsset_default.sh

python /publicfs/cms/user/wangzebing/ALP/Analysis_code/Reduced-tree/runCondor/condorFile/codeFile/makePlots_LLA.py -i /scratchfs/cms/wangzebing/ntuple_DoubleEG_Run2017B.root -o /publicfs/cms/user/wangzebing/ALP/Analysis_out/17/data/ALP_DoubleEG.root
