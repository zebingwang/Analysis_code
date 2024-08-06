-xs#!/bin/bash
/bin/hostname
gcc -v
pwd

export PATH=/cvmfs/common.ihep.ac.cn/software/hepjob/bin:$PATH
source /cvmfs/cms.cern.ch/cmsset_default.sh

python $1 -i $2 -o $3 -xs $4 -L $5 -N $6 -y $7
