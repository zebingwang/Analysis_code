#!/bin/bash
/bin/hostname
gcc -v
pwd
export PATH=$PATH:/afs/ihep.ac.cn/soft/common/sysgroup/hep_job/bin/
source /cvmfs/cms.cern.ch/cmsset_default.sh

python $1 -i $2 -o $3 -xs $4 -L $5 -N $6 -y $7
