#!/bin/bash

if [ "$1" == "clean" ]
    then
    rm ./smackConfig/*.bc
    rm ./smackConfig/__pycache__ -rf
    rm ./smackConfig/benchmarks/*.bc ./smackConfig/benchmarks/*.bpl
    exit
fi


cd smackConfig
ruby ../paramils2.3.7-source/param_ils_2_3_run.rb -numRun 0 -userunlog 1 -scenariofile scenarioSmack.txt -validN 1000 
#ruby ../paramils2.3.7-source/param_ils_2_3_run.rb -numRun 1 -userunlog 1 -scenariofile scenario-smack.txt -validN 1000 &
cd ..
