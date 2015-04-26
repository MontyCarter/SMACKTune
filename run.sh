#!/bin/bash

#Clean before each run, to ensure *.bpl's and *.bc's are fresh
rm ./smackConfig/*.bc
rm ./smackConfig/__pycache__ -rf
rm ./smackConfig/benchmarks/*.bc ./smackConfig/benchmarks/*.bpl

if [ "$1" == "clean" ]
    then
    exit
fi

cd smackConfig

#Generate instance file reference times for this hardware
if [ ! -f instanceSmack.txt ]
    then
    echo "============================"
    echo "| Generating Instance File |"
    echo "============================"
    echo
    ./generateInstanceFile.py benchmarks
    echo
    echo
    #Clean after generating instance reference timings,
    #  to ensure *.bpl's and *.bc's are fresh
    rm ./*.bc
    rm ./__pycache__ -rf
    rm ./benchmarks/*.bc ./smackConfig/benchmarks/*.bpl
fi


echo "============================"
echo "| Running ParamILS         |"
echo "============================"
echo
ruby ../paramils2.3.7-source/param_ils_2_3_run.rb -numRun 0 -userunlog 1 -scenariofile scenarioSmack.txt -validN 1000 &
ruby ../paramils2.3.7-source/param_ils_2_3_run.rb -numRun 1 -userunlog 1 -scenariofile scenarioSmack.txt -validN 1000 &
ruby ../paramils2.3.7-source/param_ils_2_3_run.rb -numRun 2 -userunlog 1 -scenariofile scenarioSmack.txt -validN 1000 &
ruby ../paramils2.3.7-source/param_ils_2_3_run.rb -numRun 3 -userunlog 1 -scenariofile scenarioSmack.txt -validN 1000 &

cd ..
