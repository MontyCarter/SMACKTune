#!/bin/bash

sudo apt-get update
sudo apt-get install ruby-full

wget http://www.cs.ubc.ca/labs/beta/Projects/ParamILS/paramils2.3.7-source.tgz
tar -zvxf paramils2.3.7-source.tgz

# Patch default algo_specifics with geomean10, which penalizes wrong results
#  for overall objective
cp algoPatchParamils/algo_specifics.rb ./paramils2.3.7-source/
