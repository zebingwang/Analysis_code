#!/bin/bash

years=( 16 16APV 17 18 )
massList=( 1 2 3 4 5 6 7 8 9 10 15 20 25 30 )
#massList=( 11 12 13 14 16 17 18 19 21 22 23 24 26 27 28 29 )

nMass=${#massList[@]}
nYear=${#years[@]}

for ((iBin=0; iBin<$nMass; iBin++))
    do
    for ((jBin=0; jBin<$nYear; jBin++))
        do
        hep_sub runjob.sh -g cms -o job${massList[$iBin]}_${years[$jBin]}.out -e job${massList[$iBin]}_${years[$jBin]}.err -argu ${years[$jBin]} ${massList[$iBin]}
    done
done