#!/bin/bash

years=( 16 16APV 17 18 )
massList=( 1 2 3 4 5 6 7 8 9 10 15 20 25 30 )
#massList=( 11 12 13 14 16 17 18 19 21 22 23 24 26 27 28 29 )

nMass=${#massList[@]}
nYear=${#years[@]}

cd output

for ((iBin=0; iBin<$nMass; iBin++))
    do
    hadd -f ${massList[$iBin]}.root ${massList[$iBin]}_16.root ${massList[$iBin]}_16APV.root ${massList[$iBin]}_17.root ${massList[$iBin]}_18.root
done