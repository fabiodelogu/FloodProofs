#!/bin/bash

export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/

python /hydro/hmc_tools_datacreator/rs_db/RS_DynamicData_DB_Network.py -settingfile /hydro/hmc_tools_datacreator/rs_db/config_algorithms/rs_dynamicdata_db-network_algorithm_server_history.config -logfile /hydro/hmc_tools_datacreator/rs_db/config_logs/rs_dynamicdata_db-network_logging_server_history.config
