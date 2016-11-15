"""
Class Features

Name:          Cpl_Apps_HMC_Model_DataLand
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20150823'
Version:       '1.0.5'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
from os.path import join

import src.Lib_Data_IO_Utils as Lib_Data_IO_Utils

from src.GetGeoData import GetGeoData
from src.GetException import GetException
from src.Drv_Data_IO import Drv_Data_IO
from src.Drv_Data_Land import Drv_Data_Land

# Debug
#import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Cpl_Apps_HMC_Model_DataLand:

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataTerrain=None, oDataVegType=None, oDataMask=None, oDataWaterMark=None, 
                 oDataNature=None, oDataAA=None, oDataInfo=None):
        
        # Data settings and data reference 
        self.oDataInfo = oDataInfo
        self.oDataTerrain = oDataTerrain
        self.oDataVegType = oDataVegType
        self.oDataMask = oDataMask
        self.oDataWaterMark = oDataWaterMark
        self.oDataNature = oDataNature
        self.oDataAA = oDataAA

    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------  
    # Run land data application(s)
    def maskStaticData(self):
        
        #-------------------------------------------------------------------------------------
        # Land data application(s)
        oApps = Drv_Data_Land(self.oDataInfo)
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Info
        oLogStream.info( ' ------> MASK AND REWRITE FILE OUTPUT ASCII ... ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get data path
        sPathDataStaticOutcome = self.oDataInfo.oInfoSettings.oPathInfo['DataStaticOutcome']
        # Get domain name
        sDomainName = self.oDataInfo.oInfoSettings.oParamsInfo['DomainName']

        # Get mask information
        oMaskData = GetGeoData(join(self.oDataInfo.oInfoSettings.oPathInfo['DataStaticOutcome'], 
                                    self.oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Mask']['VarSource']))
        
        # Get variable(s) data
        a1oVarData = self.oDataInfo.oInfoVarStatic.oDataOutputStatic['ASCII']
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cycle(s) on output variable(s)
        for sVarName in a1oVarData:
            
            #-------------------------------------------------------------------------------------
            # Info
            oLogStream.info( ' --------> MASK AND REWRITE Variable ' + sVarName + ' ... ')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Define variable filename 
            sVarFileName = Lib_Data_IO_Utils.defineFileName(join(sPathDataStaticOutcome, a1oVarData[sVarName]['VarSource']), 
                                                      {'domain' : sDomainName})
            
            # Get variable data
            oVarData = a1oVarData[sVarName]
            
            # Rewrite data using data mask 
            oApps.rewriteArcGrid(sVarFileName, oVarData , oMaskData)
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Info
            oLogStream.info( ' --------> MASK AND REWRITE Variable ' + sVarName + ' ... OK')
            #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Info
        oLogStream.info( ' ------> MASK AND REWRITE FILE OUTPUT ASCII ... OK')
        #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    
    #-------------------------------------------------------------------------------------  
    # Run land data application(s)
    def computeStaticData(self):
    
        # Land data application(s)
        oApps = Drv_Data_Land(self.oDataInfo)
        
        # Model parameters
        [sSdOutMP, oSdErrMP] = oApps.computeModelParameters(self.oDataTerrain, self.oDataWaterMark)
        Lib_Data_IO_Utils.checkProcess(sSdOutMP, oSdErrMP)
        
        # Digital Elevation Model
        [sSdOutT, oSdErrT] = oApps.computeTerrain(self.oDataTerrain)
        Lib_Data_IO_Utils.checkProcess(sSdOutT, oSdErrT)
        
        # Vegetation Type
        [sSdOutVT, oSdErrVT] = oApps.computeVegetationType(self.oDataVegType, self.oDataTerrain)
        Lib_Data_IO_Utils.checkProcess(sSdOutVT, oSdErrVT)
        # Vegetation Ia
        [sSdOutVT, oSdErrVT, self.iDimVarIa] = oApps.computeVegetationIA()
        Lib_Data_IO_Utils.checkProcess(sSdOutVT, oSdErrVT)
        
        # Mask
        [sSdOutM, oSdErrM] = oApps.computeMask(self.oDataTerrain, self.oDataVegType, self.oDataMask)
        Lib_Data_IO_Utils.checkProcess(sSdOutM, oSdErrM)
        
        # Nature
        [sSdOutNT, oSdErrNT] = oApps.computeNatureType(self.oDataTerrain, self.oDataVegType, self.oDataNature)
        Lib_Data_IO_Utils.checkProcess(sSdOutNT, oSdErrNT)
        
        # AlertArea
        [sSdOutAA, oSdErrAA] = oApps.computeAlertArea(self.oDataTerrain, self.oDataVegType, self.oDataAA)
        Lib_Data_IO_Utils.checkProcess(sSdOutAA, oSdErrAA)
        
        # Flow Directions
        [sSdOutFD, oSdErrFD] = oApps.computeFlowDirections(self.oDataTerrain)
        Lib_Data_IO_Utils.checkProcess(sSdOutFD, oSdErrFD)
        # Cell Area
        [sSdOutCA, oSdErrCA] = oApps.computeCellArea(self.oDataTerrain)
        Lib_Data_IO_Utils.checkProcess(sSdOutCA, oSdErrCA)
        # Drainage Area
        [sSdOutDA, oSdErrDA] = oApps.computeDrainageArea(self.oDataTerrain)
        Lib_Data_IO_Utils.checkProcess(sSdOutDA, oSdErrDA)
        # Channels Distinction
        [sSdOutCD, oSdErrCD] = oApps.computeChannelsDistinction(self.oDataTerrain)
        Lib_Data_IO_Utils.checkProcess(sSdOutCD, oSdErrCD)
        # Water Table Slopes
        [sSdOutWS, oSdErrWS] = oApps.computeWatertableSlopes(self.oDataTerrain)
        Lib_Data_IO_Utils.checkProcess(sSdOutWS, oSdErrWS)
        # Coefficient Resolution Map
        [sSdOutCR, oSdErrCR] = oApps.computeCoeffResMap(self.oDataTerrain)
        Lib_Data_IO_Utils.checkProcess(sSdOutCR, oSdErrCR)
        
    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------
    # Write land data file(s) in NetCDF format
    def saveStaticData(self):
        
        #-------------------------------------------------------------------------------------
        # Check method
        try:
        
            #-------------------------------------------------------------------------------------
            # Info
            oLogStream.info( ' ------> SAVING FILE OUTPUT NETCDF ... ')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Get structured information
            oVarsOUT = self.oDataInfo.oInfoVarStatic.oDataOutputStatic
            oPathInfo = self.oDataInfo.oInfoSettings.oPathInfo
            
            oGeneralInfo = self.oDataInfo.oInfoSettings.oGeneralInfo
            oPathInfo = self.oDataInfo.oInfoSettings.oPathInfo
            oParamsInfo = self.oDataInfo.oInfoSettings.oParamsInfo
            oGeoSystemInfo = self.oDataInfo.oInfoSettings.oGeoSystemInfo
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Define NetCDF filename
            sVarSource_NC = Lib_Data_IO_Utils.defineUniqueValue(oVarsOUT['NetCDF'], 1, 'VarSource')
            sFileName_NC = Lib_Data_IO_Utils.defineFileName(join(oPathInfo['DataStaticOutcome'], sVarSource_NC), 
                                                           {'domain' : oParamsInfo['DomainName']})
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Initialize and open NetCDF file
            oFileDriver_NC = Drv_Data_IO(join(sFileName_NC),'w')
    
            # Write global attributes (common and extra)
            oFileDriver_NC.oFileWorkspace.writeFileAttrsCommon(oGeneralInfo)
            oFileDriver_NC.oFileWorkspace.writeFileAttrsExtra(oParamsInfo, self.oDataTerrain.a1oGeoInfo)
    
            # Write geographical information
            oFileDriver_NC.oFileWorkspace.writeGeoSystem(oGeoSystemInfo, self.oDataTerrain.oGeoData.a1dGeoBox)
            
            # Declare variable(s) dimension(s)
            sDimVarX = oVarsOUT['NetCDF']['Terrain']['VarDims']['X']
            oFileDriver_NC.oFileWorkspace.writeDims(sDimVarX, self.oDataTerrain.oGeoData.iCols)
            sDimVarY = oVarsOUT['NetCDF']['Terrain']['VarDims']['Y']
            oFileDriver_NC.oFileWorkspace.writeDims(sDimVarY, self.oDataTerrain.oGeoData.iRows)
            sDimVarT = 'time'; 
            oFileDriver_NC.oFileWorkspace.writeDims(sDimVarT, 1)
            sDimVarIa = oVarsOUT['NetCDF']['VegetationIA']['VarDims']['Y'] 
            #oFileDriver_NC.oFileWorkspace.writeDims(sDimVarIa, self.iDimVarIa[0])
            oFileDriver_NC.oFileWorkspace.writeDims(sDimVarIa, 100)
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Cycling on variable name(s)
            for sVarName in oVarsOUT['NetCDF']:
                
                #-------------------------------------------------------------------------------------
                # Info
                oLogStream.info( ' --------> SAVING Variable ' + sVarName + ' ... ')
                #-------------------------------------------------------------------------------------
                
                try:
                
                    #-------------------------------------------------------------------------------------
                    # Get data (model, land and geo)
                    # Latitude case
                    if sVarName == 'Latitude':
                        # Get data
                        oData = [];
                        oData = self.oDataTerrain.oGeoData.a2dGeoY
                    # Longitude case
                    elif sVarName == 'Longitude':
                        # Get data
                        oData = [];
                        oData = self.oDataTerrain.oGeoData.a2dGeoX 
                    # Other variable(s)
                    else:
        
                        # Get ascii filename and read function
                        sFileName_ASCII = Lib_Data_IO_Utils.defineFileName(join(oPathInfo['DataStaticOutcome'], oVarsOUT['ASCII'][sVarName]['VarSource']), 
                                                                          {'domain' : oParamsInfo['DomainName']})
                        sFileFuncType_ASCII = oVarsOUT['ASCII'][sVarName]['VarOp']['Op_Load']['Func']
                    
                        # Get ascii file values and info
                        oFileDriver_ASCII = Drv_Data_IO(join(oPathInfo['DataStaticOutcome'], sFileName_ASCII),'r')
                        oFileDriver_ASCII_ReadMethod = getattr(oFileDriver_ASCII.oFileWorkspace, sFileFuncType_ASCII)
                        oFileDriver_ASCII.oFileWorkspace.openFile()
                        oFile_ASCII_Object = oFileDriver_ASCII_ReadMethod()
                        oFileDriver_ASCII.oFileWorkspace.closeFile()
                        
                        # Get data
                        oData = [];
                        oData = oFile_ASCII_Object['Data']
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Prepare NetCDF write method
                    oFileDrv_NC_WriteMethod = getattr(oFileDriver_NC.oFileWorkspace, 
                                   oVarsOUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Func'])
                    # Save data in NetCDF file
                    oFileDrv_NC_WriteMethod(  sVarName, oData, 
                                           oVarsOUT['NetCDF'][sVarName]['VarAttributes'], 
                                           oVarsOUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Format'], 
                                           oVarsOUT['NetCDF'][sVarName]['VarDims']['Y'], 
                                           oVarsOUT['NetCDF'][sVarName]['VarDims']['X'])
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Info
                    oLogStream.info( ' --------> SAVING Variable ' + sVarName + ' ... OK')
                    #-------------------------------------------------------------------------------------
                
                except:

                    #----------------------------------------------------------------------------
                    # Algorithm exception(s)
                    GetException(' -----> WARNING: SAVING Variable ' + sVarName + ' ... FAILED', 2, 1)
                    #----------------------------------------------------------------------------
                
            #-------------------------------------------------------------------------------------
            # Close NetCDF file
            oFileDriver_NC.oFileWorkspace.closeFile()
            # Info
            oLogStream.info( ' ------> SAVING FILE OUTPUT NETCDF ... OK')
            #-------------------------------------------------------------------------------------
        
        except:

            #----------------------------------------------------------------------------
            # Algorithm exception(s)
            GetException(' -----> ERROR: SAVING FILE OUTPUT NETCDF ... FAILED', 1, 1)
            #----------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
    