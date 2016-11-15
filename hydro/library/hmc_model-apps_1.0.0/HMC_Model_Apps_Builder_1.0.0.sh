#!/bin/bash

#-----------------------------------------------------------------------------------------
# Declare script name and version
NameTar='hmc_model-apps_codes_1.0.0.tar.gz'

NameExe='HMC_Model_V1.x'
Script='HMC Model-Apps Builder'
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
echo " Step 1 - Expand tar file ... Done! "
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Compilling module(s) without creating executable(s)
cd $UNZIP_DIR
echo " Step 2 - Create object(s) of Fortran program(s) ... "
gfortran -fno-align-commons -c ContinuumDamLaghi.f90 CoeffDamEquiv.f90 ContaCelleLaghi.f90 convolutionHyperCdrift.f90 convolutionHyperCdriftDamLaghi.f90 Create_Meteo_GRID.f90 dCappaCfunction.f90 DeterminaData_stepParam.f90   DeterminaData_stepParamHour.f90 evapotranspiration_FR_matrix.f90 evapotranspiration_Lake.f90 ForceRestoreEq_matrix.f90 Geoloc_meteo_file_GRID.f90 HortonMatrixHcdrift.f90 IDW.f90 iLstr.f90 indexx.f90 initialisation.f90 Laghi.f90 LinRegr.f90 MetoDataInterp.f90 QDeepFlow_al2.f90 Read3DMapBinary.f90 ReadCurveInvasoVolumiDam.f90 ReadHydrograph.f90 ReadInfoData.f90 ReadInfoDataDam.f90 ReadInfoDigheLaghi.f90 ReadInfoJoin.f90 ReadInfoLaghi.f90 ReadInfoPrese.f90 ReadInfoS3M.f90 ReadLandData.f90 ReadMapBinary.f90 ReadMeteoData.f90 ReadMeteoMapBinary.f90 ReadMeteoMapBinaryGeoloc.f90 ReadPreseRilasciDam.f90 ReadSections.f90 ReadSectionsDam.f90 ReadSnowStateMatrixBinary.f90 ReadStateDigheLaghi.f90 ReadStateMatrixBinary.f90 ReadTurbinatiDam.f90 read_f_k.f90 RetentionHcdrift.f90 richardson_matrix.f90 rk4_matrix.f90 SaltaMeteoData.f90 SaveStateDigheLaghi.f90 SelectIDWCase.f90 SmoothSerie.f90 Snow.f90 Snow_melting_ibrido.f90 sort.f90 SRaM.f90 storage.f90 SubFlowHcdrift.f90 SubFlowHcdriftDamLaghi.f90 SurfaceRouting.f90 SurfaceRoutingDamLaghi.f90 SvasoDamVolume.f90 TankLaghi.f90 thermal_inertia_matrix.f90 Write3DMapBinary.f90 WriteEsriFile.f90 WriteMeteoMapBinary.f90 WriteSnowStateMatrixBinary.f90 WriteStateMatrix.f90 WriteStateMatrixBinary.f90 wt_alpha.f90 wt_bedrock.f90 ini.f90 ReadInfoDataDamIni.f90 DeleteMeteoMapBinary.f90 CheckMeteoMapBinary.f90  CoeffResolutionMap.f90 
echo " Step 2 - Create object(s) of Fortran program(s) ... Done! "
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Link object(s) and create executable(s)
echo " Step 3 - Link object(s) and create executable(s) of Fortran program(s) ... "
gfortran -fno-align-commons -Ofast -o2 $NameExe ContinuumDamLaghi.o CoeffDamEquiv.o ContaCelleLaghi.o convolutionHyperCdrift.o convolutionHyperCdriftDamLaghi.o Create_Meteo_GRID.o dCappaCfunction.o DeterminaData_stepParam.o   DeterminaData_stepParamHour.o evapotranspiration_FR_matrix.o evapotranspiration_Lake.o ForceRestoreEq_matrix.o Geoloc_meteo_file_GRID.o HortonMatrixHcdrift.o IDW.o iLstr.o indexx.o initialisation.o Laghi.o LinRegr.o MetoDataInterp.o QDeepFlow_al2.o Read3DMapBinary.o ReadCurveInvasoVolumiDam.o ReadHydrograph.o ReadInfoData.o ReadInfoDataDam.o ReadInfoDigheLaghi.o ReadInfoJoin.o ReadInfoLaghi.o ReadInfoPrese.o ReadInfoS3M.o ReadLandData.o ReadMapBinary.o ReadMeteoData.o ReadMeteoMapBinary.o ReadMeteoMapBinaryGeoloc.o ReadPreseRilasciDam.o ReadSections.o ReadSectionsDam.o ReadSnowStateMatrixBinary.o ReadStateDigheLaghi.o ReadStateMatrixBinary.o ReadTurbinatiDam.o read_f_k.o RetentionHcdrift.o richardson_matrix.o rk4_matrix.o SaltaMeteoData.o SaveStateDigheLaghi.o SelectIDWCase.o SmoothSerie.o Snow.o Snow_melting_ibrido.o sort.o SRaM.o storage.o SubFlowHcdrift.o SubFlowHcdriftDamLaghi.o SurfaceRouting.o SurfaceRoutingDamLaghi.o SvasoDamVolume.o TankLaghi.o thermal_inertia_matrix.o Write3DMapBinary.o WriteEsriFile.o WriteMeteoMapBinary.o WriteSnowStateMatrixBinary.o WriteStateMatrix.o WriteStateMatrixBinary.o wt_alpha.o wt_bedrock.o ini.o ReadInfoDataDamIni.o DeleteMeteoMapBinary.o CheckMeteoMapBinary.o  CoeffResolutionMap.o
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
# End - Script 
echo "-----------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-----------------------------------------------------"
#-----------------------------------------------------------------------------------------



