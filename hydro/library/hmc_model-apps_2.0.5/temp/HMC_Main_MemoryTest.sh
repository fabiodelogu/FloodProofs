#!/bin/bash

# tool: sudo apt-get install valgrind; sudo apt-get install tee

name_exec=HMC_Model_V2_local.x
name_prof=gprof2dot.py

# Settings
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/netcdf-4.1.2/lib/
ulimit -s unlimited

# Executing (for output : 2>&1 | tee memory_check.txt
valgrind --track-origins=yes ./$name_exec 30 3 0.6 0.015 marche 0.3 500 1 70 

