#!/bin/bash

# GDAL Library
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/gdal-2.0.0/lib/
# NetCDF Library
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/netcdf-4.1.2/lib/
# HDF5 Library
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/hdf5-1.8.7/lib/
# ZLIB Library
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/zlib-1.2.5/lib/
# HDF4 Library
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/hdf4-4.2.10/lib/

# GDAL Path executable(s)
export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/

# MODIS Reprojection Tool
MRT_HOME="/home/dpc-marche/library/MODIS_Reprojection_Tool/"
PATH="$PATH:/home/dpc-marche/library/MODIS_Reprojection_Tool/bin"
MRT_DATA_DIR="/home/dpc-marche/library/MODIS_Reprojection_Tool/data"
export MRT_HOME PATH MRT_DATA_DIR

# COMMAND LINE
python /hydro/hmc_tools_datacreator/satellite_modis/Satellite_DynamicData_MODIS_Snow.py -settingfile /hydro/hmc_tools_datacreator/satellite_modis/config_algorithms/satellite_dynamicdata_modis-snow_algorithm_server_history.config -logfile /hydro/hmc_tools_datacreator/satellite_modis/config_logs/satellite_dynamicdata_modis-snow_logging_server_history.config
