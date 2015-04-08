#!/bin/bash

cd smackConfig
ruby ../paramils2.3.7-source/param_ils_2_3_run.rb -numRun 0 -scenariofile scenario-smack.txt -validN 100
cd ..
