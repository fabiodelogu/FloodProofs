#!/bin/bash

export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/

python /hydro/hmc_tools_datacreator/kf_expertforecast/KF_DynamicData_EF_AirTemperature.py -settingfile /hydro/hmc_tools_datacreator/kf_expertforecast/config_algorithms/kf_dynamicdata_ef-airtemperature_algorithm_server_history.config -logfile /hydro/hmc_tools_datacreator/kf_expertforecast/config_logs/kf_dynamicdata_ef-airtemperature_logging_server_history.config
