#!/bin/bash

#-----------------------------------------------------------------------------------------
# Declare script name and version
NameTar='hmc_land-apps_codes_1.0.0.tar.gz'

Script='HMC Land-Apps Builder'
Version='1.0.0'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Start - Script
echo "-----------------------------------------------------"
echo " $Script - Version $Version "
echo "-----------------------------------------------------"
echo ""
echo " Start script ... "
echo ""

# Get current folder
CURRENT_DIR=${PWD}
UNZIP_DIR=$CURRENT_DIR/temp

if [ -d "$UNZIP_DIR" ]; then
  rm -R $UNZIP_DIR
fi
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Expand the tar file
echo " Step 1 - Expand tar file ... "
mkdir $UNZIP_DIR
echo tar xvfz $NameTar -C $UNZIP_DIR
tar xvfz $NameTar -C $UNZIP_DIR
echo " Step 1 - Expand tar file ... Done!"
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Compilling module(s) without creating executable(s)
echo " Step 2 - Create object(s) of Fortran program(s) ... "
cd $UNZIP_DIR
gfortran -c flow_directions.f90
gfortran -c channels_distinction.f90
gfortran -c drainage_area.f90
gfortran -c watertable_slopes.f90
gfortran -c coeff_resolution_map.f90
echo " Step 2 - Create object(s) of Fortran program(s) ... Done! "
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Link object(s) and create executable(s)
echo " Step 3 - Link object(s) and create executable(s) of Fortran program(s) ... "
gfortran flow_directions.o -o flow_directions.x
gfortran channels_distinction.o -o channels_distinction.x
gfortran drainage_area.o -o drainage_area.x
gfortran watertable_slopes.o -o watertable_slopes.x
gfortran coeff_resolution_map.o -o coeff_resolution_map.x
echo " Step 3 - Link object(s) and create executable(s) of Fortran program(s) ... Done!"
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Change executable(s) permission(s)
echo " Step 4 - Change options of executable(s) ... "
chmod +x flow_directions.x
chmod +x channels_distinction.x
chmod +x drainage_area.x
chmod +x watertable_slopes.x
chmod +x coeff_resolution_map.x
echo " Step 4 - Change options of executable(s) ... Done!"
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Change executable(s) permission(s)
echo " Step 4 - Change options of executable(s) ... "
chmod +x flow_directions.x
chmod +x channels_distinction.x
chmod +x drainage_area.x
chmod +x watertable_slopes.x
chmod +x coeff_resolution_map.x
cp $UNZIP_DIR/flow_directions.x $CURRENT_DIR/flow_directions.x
cp $UNZIP_DIR/channels_distinction.x $CURRENT_DIR/channels_distinction.x
cp $UNZIP_DIR/drainage_area.x $CURRENT_DIR/drainage_area.x
cp $UNZIP_DIR/watertable_slopes.x $CURRENT_DIR/watertable_slopes.x
cp $UNZIP_DIR/coeff_resolution_map.x $CURRENT_DIR/coeff_resolution_map.x
echo " Step 4 - Change options of executable(s) ... Done!"
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-----------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-----------------------------------------------------"
#-----------------------------------------------------------------------------------------





