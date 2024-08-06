#!/bin/bash
/bin/hostname
gcc -v
pwd
export PATH=$PATH:/afs/ihep.ac.cn/soft/common/sysgroup/hep_job/bin/
source /cvmfs/cms.cern.ch/cmsset_default.sh

python /publicfs/cms/user/wangzebing/ALP/Analysis_code/Reduced-tree/runCondor/condorFile/codeFile/makePlots_LLA_GEN_tree.py -i /publicfs/cms/user/wangzebing/ALP/NTuples/UL/$1/sig/ntuple_M$2.root -o /publicfs/cms/user/wangzebing/ALP/Analysis_code/TheoryUnc/output/$2_$1.root -xs 0.1