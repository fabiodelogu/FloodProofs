#!/bin/bash

export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/

python /hydro/hmc_tools_datacreator/rainfarm_lami/RF_Model_LAMI_I7.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_algorithms/rf_model_lami-i7_algorithm_server_history.config -logfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_logs/rf_model_lami-i7_logging_server_history.config
