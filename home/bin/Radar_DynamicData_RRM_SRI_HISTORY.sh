#!/bin/bash

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/netcdf-4.1.2/lib/
export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/

python /hydro/hmc_tools_datacreator/radar_rrm/Radar_DynamicData_RRM_SRI.py -settingfile /hydro/hmc_tools_datacreator/radar_rrm/config_algorithms/radar_dynamicdata_rrm-sri_algorithm_server_history.config -logfile /hydro/hmc_tools_datacreator/radar_rrm/config_logs/radar_dynamicdata_rrm-sri_logging_server_history.config
