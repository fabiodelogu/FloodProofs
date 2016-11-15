#!/bin/bash

export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/

python /hydro/hmc_tools_datacreator/nwp_ecmwf/NWP_DynamicData_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/nwp_ecmwf/config_algorithms/nwp_dynamicdata_ecmwf-0125_algorithm_server_history.config -logfile /hydro/hmc_tools_datacreator/nwp_ecmwf/config_logs/nwp_dynamicdata_ecmwf-0125_logging_server_history.config

python /hydro/hmc_tools_datacreator/astrorad_ecmwf/ARad_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/astrorad_ecmwf/config_algorithms/arad_model_ecmwf-0125_algorithm_server_history.config -logfile /hydro/hmc_tools_datacreator/astrorad_ecmwf/config_logs/arad_model_ecmwf-0125_logging_server_history.config

