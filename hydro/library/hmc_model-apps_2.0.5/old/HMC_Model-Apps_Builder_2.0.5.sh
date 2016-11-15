#!/bin/bash

#-----------------------------------------------------------------------------------------
# Declare script name and version
NameTar='hmc_model-apps_codes_2.0.5.tar.gz'

NameExe='HMC_Model_V2_$RUN.x'
Script='HMC Model-Apps Builder'
Version='2.0.5'

NameProf='gprof2dot.py'

# Profiling flag
FProf=0

# Pass netCDF main path
#NETCDF_DIR=/usr/local/netcdf-4.1.2 #LOCAL
NETCDF_DIR=/home/dpc-marche/library/netcdf-4.1.2 #SERVER

# Compiler options
op_object='-c -g -O2'
op_exec='-march=native -ffast-math -funroll-loops -O2 -finline-limit=600 -fwhole-program -flto'

if (( $FProf == 1 )); then
    op_prof='-pg'
else
    op_prof=''
fi
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Start - Script
echo "-----------------------------------------------------"
echo " $Script - Version $Version "
echo "-----------------------------------------------------"
echo ""
echo " Start script ... "
echo ""

# Define library path
NETCDF_INC=$NETCDF_DIR/include \
NETCDF_LIB=$NETCDF_DIR/lib \
LIBS="-lnetcdff -lnetcdf"

# Get current folder
CURRENT_DIR=${PWD}
UNZIP_DIR=$CURRENT_DIR/temp

if [ -d "$UNZIP_DIR" ]; then
  rm -R $UNZIP_DIR
fi

# Set stack size (kbytes, -s) unlimited
echo " Step 0 - Set stack size to unlimited ... "
ulimit -s unlimited
ulimit -a
echo " Step 0 - Set stack size to unlimited ... OK"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Expand the tar file
echo " Step 1 - Expand tar file ... "
mkdir $UNZIP_DIR
echo tar xvfz $NameTar -C $UNZIP_DIR
tar xvfz $NameTar -C $UNZIP_DIR
echo " Step 1 - Expand tar file ... Done! "
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Compilling module(s) without creating executable(s)
cd $UNZIP_DIR
echo " Step 2 - Create object(s) of Fortran program(s) ... "
gfortran $op_object gnufor2.f90 $op_prof
gfortran $op_object HMC_Module_Tools_Debug.f90 $op_prof
gfortran $op_object HMC_Module_Namelist.f90 $op_prof
gfortran $op_object HMC_Module_Tools_Generic.f90 $op_prof
gfortran $op_object HMC_Module_Tools_IO.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS} 
gfortran $op_object HMC_Module_Tools_Time.f90 $op_prof
gfortran $op_object HMC_Module_Vars_Loader.f90 $op_prof
gfortran $op_object HMC_Module_Vars_Manager.f90 $op_prof
gfortran $op_object HMC_Module_Phys_Convolution_Apps.f90 $op_prof
gfortran $op_object HMC_Module_Phys_Convolution.f90 $op_prof
gfortran $op_object HMC_Module_Phys_LSM_Apps.f90 $op_prof
gfortran $op_object HMC_Module_Phys_LSM.f90 $op_prof
gfortran $op_object HMC_Module_Phys_Snow_Apps.f90 $op_prof
gfortran $op_object HMC_Module_Phys_Snow.f90 $op_prof
gfortran $op_object HMC_Module_Phys_ET.f90 $op_prof
gfortran $op_object HMC_Module_Phys_Retention.f90 $op_prof
gfortran $op_object HMC_Module_Phys.f90 $op_prof
gfortran $op_object HMC_Module_Data_Forcing_Gridded.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Data_Forcing_Point.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Data_Output_Gridded.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Data_Output_Point.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Data_Restart_Gridded.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Data_Restart_Point.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Data_State_Gridded.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Data_State_Point.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Data_Static_Gridded.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Data_Static_Point.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Info_Gridded.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Info_Point.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
gfortran $op_object HMC_Module_Info_Time.f90 $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
echo " Step 2 - Create object(s) of Fortran program(s) ... Done! "
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Link object(s) and create executable(s)
echo " Step 3 - Link object(s) and create executable(s) of Fortran program(s) ... "
gfortran $op_exec gnufor2.o HMC_Module_Data_Forcing_Gridded.o HMC_Module_Data_Forcing_Point.o HMC_Module_Data_Output_Gridded.o HMC_Module_Data_Output_Point.o HMC_Module_Data_Restart_Gridded.o HMC_Module_Data_Restart_Point.o HMC_Module_Data_State_Gridded.o HMC_Module_Data_State_Point.o HMC_Module_Data_Static_Gridded.o HMC_Module_Data_Static_Point.o HMC_Module_Info_Gridded.o HMC_Module_Info_Point.o HMC_Module_Info_Time.o HMC_Module_Namelist.o HMC_Module_Phys_Convolution_Apps.o HMC_Module_Phys_Convolution.o HMC_Module_Phys_ET.o HMC_Module_Phys.o HMC_Module_Phys_LSM_Apps.o HMC_Module_Phys_LSM.o HMC_Module_Phys_Snow_Apps.o HMC_Module_Phys_Snow.o HMC_Module_Phys_Retention.o HMC_Module_Tools_Debug.o HMC_Module_Tools_Generic.o HMC_Module_Tools_IO.o HMC_Module_Tools_Time.o HMC_Module_Vars_Loader.o HMC_Module_Vars_Manager.o HMC_Main.f90 -o $NameExe $op_prof -I${NETCDF_INC} -L${NETCDF_LIB} ${LIBS}
echo " Step 3 - Link object(s) and create executable(s) of Fortran program(s) ... Done!"
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Change executable(s) permission(s)
echo " Step 4 - Change options of executable(s) ... "
chmod +x $NameExe
cp $UNZIP_DIR/$NameExe $CURRENT_DIR/$NameExe 
echo " Step 4 - Change options of executable(s) ... Done!"
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Change executable(s) permission(s)
echo " Step 5 - Get profiling tools ... "
if (( $FProf == 1 )); then
    echo " Step 5 - Get profiling tools ... PROFILING ACTIVATED"
    chmod +x $NameProf
    cp $UNZIP_DIR/$NameProf $CURRENT_DIR/$NameProf
else
    echo " Step 5 - Get profiling tools ... PROFILING NOT ACTIVATED"
fi

echo " Step 5 - Get profiling tools ... Done!"
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Change executable(s) permission(s)
echo " Step 6 - Get exec test file ... "

chmod +x HMC_Main_ExecTest.sh
cp $UNZIP_DIR/HMC_Main_ExecTest.sh $CURRENT_DIR/HMC_Main_ExecTest.sh

echo " Step 6 - Get exec test file ... Done!"
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Change executable(s) permission(s)
echo " Step 7 - Get memory test file ... "

chmod +x HMC_Main_MemoryTest.sh
cp $UNZIP_DIR/HMC_Main_MemoryTest.sh $CURRENT_DIR/HMC_Main_MemoryTest.sh

echo " Step 7 - Get memory test file ... Done!"
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-----------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-----------------------------------------------------"
#-----------------------------------------------------------------------------------------


