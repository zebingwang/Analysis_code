#!/bin/bash
/bin/hostname
gcc -v
pwd
export PATH=$PATH:/afs/ihep.ac.cn/soft/common/sysgroup/hep_job/bin/
source /cvmfs/cms.cern.ch/cmsset_default.sh

python /publicfs/cms/user/wangzebing/ALP/Analysis_code/Reduced-tree/runCondor/condorFile/codeFile/makePlots_LLA.py -i /publicfs/cms/user/wangzebing/ALP/NTuples/17/data/ntuple_DoubleMuon_Run2017B.root /publicfs/cms/user/wangzebing/ALP/NTuples/17/data/ntuple_DoubleMuon_Run2017C.root /publicfs/cms/user/wangzebing/ALP/NTuples/17/data/ntuple_DoubleMuon_Run2017D.root /publicfs/cms/user/wangzebing/ALP/NTuples/17/data/ntuple_DoubleMuon_Run2017E.root /publicfs/cms/user/wangzebing/ALP/NTuples/17/data/ntuple_DoubleMuon_Run2017F.root -o /publicfs/cms/user/wangzebing/ALP/Analysis_out/17/data/ALP_DoubleMuon.root
