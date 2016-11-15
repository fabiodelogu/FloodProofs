#!/bin/bash

# Test to profile hmc model

name_comp='HMC_Model_V2_$RUN.x'
name_exec='HMC_Model_V2_Prof.x'
name_prof='gprof2dot.py'

# Settings
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/netcdf-4.1.2/lib/
ulimit -s unlimited

# Exec
cp $name_comp $name_exec
./$name_exec 30 3 0.6 0.015 marche 0.3 500 1 70 

# Profiling
gprof $name_exec gmon.out > hmc_model_analysis.txt
gprof $name_exec | ./$name_prof | dot -Tpng -o hmc_model_analysis.png
