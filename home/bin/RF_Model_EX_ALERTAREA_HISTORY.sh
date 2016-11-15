#!/bin/bash

export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/

python /hydro/hmc_tools_datacreator/rainfarm_expertforecast/RF_Model_EF_AlertArea.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_expertforecast/config_algorithms/rf_model_ef-alertarea_algorithm_server_history.config -logfile /hydro/hmc_tools_datacreator/rainfarm_expertforecast/config_logs/rf_model_ef-alertarea_logging_server_history.config
