#!/bin/bash

if [ $1 == "clean" ]
    then
    rm ./smackConfig/*.bc
    rm ./smackConfig/smack-benchmarks/*.bc ./smackConfig/smack-benchmarks/*.bpl
    exit
fi


cd smackConfig
ruby ../paramils2.3.7-source/param_ils_2_3_run.rb -numRun 0 -userunlog 1 -scenariofile scenario-smack.txt -validN 1000 
#ruby ../paramils2.3.7-source/param_ils_2_3_run.rb -numRun 1 -userunlog 1 -scenariofile scenario-smack.txt -validN 1000 &
cd ..
