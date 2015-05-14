#!/bin/bash

# Use existance of paramils install folder as evidence of prior install
#   If already installed, just refresh paramils code customizations
if [ ! -d ./paramils2.3.7-source/ ]
    then
    sudo apt-get update
    sudo apt-get install ruby-full
    wget http://www.cs.ubc.ca/labs/beta/Projects/ParamILS/paramils2.3.7-source.tgz
    tar -zvxf paramils2.3.7-source.tgz
fi


# Patch default algo_specifics with geomean10, which penalizes wrong results
#  for overall objective
cp algoPatchParamils/algo_specifics.rb ./paramils2.3.7-source/
