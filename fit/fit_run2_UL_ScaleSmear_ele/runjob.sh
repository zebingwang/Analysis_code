#!/bin/bash
/bin/hostname
gcc -v
pwd
export PATH=$PATH:/afs/ihep.ac.cn/soft/common/sysgroup/hep_job/bin/
source /cvmfs/cms.cern.ch/cmsset_default.sh

#python makeWorkspace_sig_scalesmear.py -m $1 --ele
python makeWorkspace_sig_scalesmear_v2.py -m $1 --ele