#!/bin/bash

export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/

python /hydro/hmc_tools_datacreator/ws_db/WS_DynamicData_DB_Network.py -settingfile /hydro/hmc_tools_datacreator/ws_db/config_algorithms/ws_dynamicdata_db-network_algorithm_server_history.config -logfile /hydro/hmc_tools_datacreator/ws_db/config_logs/ws_dynamicdata_db-network_logging_server_history.config
