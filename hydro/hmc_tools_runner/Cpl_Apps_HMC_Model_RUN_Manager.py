"""
Class Features

Name:          Cpl_Apps_HMC_Model_RUN_Manager
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151022'
Version:       '1.6.2'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
from src.Drv_Model_HMC_Builder import Drv_Model_HMC_Builder
from src.Drv_Model_HMC_Runner import Drv_Model_HMC_Runner
from src.Drv_Model_HMC_Finalizer import Drv_Model_HMC_Finalizer

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Cpl_Apps_HMC_Model_RUN_Manager:
    
    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataInfo=None, oDataTime=None):
        
        #-------------------------------------------------------------------------------------
        # Get information
        self.oDataInfo = oDataInfo
        self.oDataTime = oDataTime
        # Get domain and run name
        self.sDomainName = self.oDataInfo.oInfoSettings.oParamsInfo['DomainName'].lower()
        self.sRunName = self.oDataInfo.oInfoSettings.oParamsInfo['RunName'].lower()
        
        # Select type run
        self.TypeRun()
        #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to select run type (ensemble or single run)
    def TypeRun(self):
        
        #-------------------------------------------------------------------------------------
        # initialize ensemble dictionary
        oEnsembleList = {}
        oLogStream.info( ' ======= MODEL RUN TYPE START ========== ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Check if ensemble dictionary exists in settings
        if self.oDataInfo.oInfoSettings.oParamsInfo['RunEnsemble']:
            
            #-------------------------------------------------------------------------------------
            # Get ensemble dictionary
            oParamsRunEns = self.oDataInfo.oInfoSettings.oParamsInfo['RunEnsemble']
            
            # Get ensemble information
            bEnsRun = oParamsRunEns['EnsRun']
            iEnsMax = int(oParamsRunEns['EnsMax']); iEnsMin = int(oParamsRunEns['EnsMin'])
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Check ensemble run type
            if bEnsRun:
                
                #-------------------------------------------------------------------------------------
                # Compute ensemble element(s)
                iEnsN = iEnsMax - iEnsMin + 1
                sEnsDigit = '%03d'; #sEnsDigit = '%0' + str(len(str(iEnsMax))) + 'd'; 
                
                # Cycle(s) on ensemble element(s)
                iID = 1
                for iEnsN in range(iEnsMin, iEnsMax + 1):
                    
                    # Ensemble ID
                    sEns = str(sEnsDigit%(iEnsN));
                    # Ensemble dictionary
                    oEnsembleList['Run_ENSEMBLE_' + str(sEnsDigit%(iID))] = sEns
                    # Counter ensemble
                    iID = iID + 1
                    
                #-------------------------------------------------------------------------------------
                                    
            else:  
                
                #-------------------------------------------------------------------------------------
                # Single run
                oEnsembleList['Run_Deterministic'] = ''
                #-------------------------------------------------------------------------------------
                
            #-------------------------------------------------------------------------------------
            
        else:
            
            #-------------------------------------------------------------------------------------
            # Single run
            oEnsembleList['Run_Deterministic'] = ''
            #-------------------------------------------------------------------------------------
            
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Return ensemble list
        self.oDataEnsemble = oEnsembleList
        oLogStream.info( ' ======= MODEL RUN TYPE END ============ ')
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Method to execute run model
    def Runner(self, sEnsembleName):
        
        #-------------------------------------------------------------------------------------
        # Info start
        oLogStream.info( ' ======= MODEL RUNNER START ============ ')
        #-------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------
        # Check run availability
        if self.oDrvBuilder.oFileHistory:
            
            #-------------------------------------------------------------------------------------
            # Initialize Runner
            oDrvRunner = Drv_Model_HMC_Runner(self.sDomainName, self.sRunName, self.oDataInfo, self.oDrvBuilder, 
                                              sEnsembleName)
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Check data run
            oDrvRunner.checkRunData()
            
            # Create command line 
            oDrvRunner.composeCLine()
            
            # Run command line
            oDrvRunner.runCLine()
            
            # Store DrvRunner in global variable(s)
            self.oDrvRunner = oDrvRunner
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Info end
            oLogStream.info( ' ======= MODEL RUNNER END  ============= ')
            #-------------------------------------------------------------------------------------
        else:
            
            #-------------------------------------------------------------------------------------
            # Info end
            oLogStream.info( ' ======= MODEL RUNNER FAILED =========== ')
            #-------------------------------------------------------------------------------------
            
        #-------------------------------------------------------------------------------------
        
    #------------------------------------------------------------------------------------- 
    
    #------------------------------------------------------------------------------------- 
    # Method to execute run model
    def Finalizer(self, sEnsembleName):
        
        #-------------------------------------------------------------------------------------
        # Info start
        oLogStream.info( ' ======= MODEL FINALIZER START ========= ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Check run availability
        if self.oDrvBuilder.oFileHistory:
            
            #-------------------------------------------------------------------------------------
            # Initialize finalizer
            oDrvFinalizer = Drv_Model_HMC_Finalizer(self.sDomainName, self.sRunName, self.oDataInfo, self.oDrvBuilder, 
                                                    sEnsembleName)
            
            # Collect data output and save in archive folder
            oDrvFinalizer.collectDataOutput()
    
            # Store DrvFinalizer in global variable(s)
            self.oDrvFinalizer = oDrvFinalizer
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Info end
            oLogStream.info( ' ======= MODEL FINALIZER END =========== ')
            #-------------------------------------------------------------------------------------
            
        else:
            #-------------------------------------------------------------------------------------
            # Info end
            oLogStream.info( ' ======= MODEL FINALIZER FAILED ======== ')
            #-------------------------------------------------------------------------------------
            
        #-------------------------------------------------------------------------------------
        
    #------------------------------------------------------------------------------------- 
    
    #-------------------------------------------------------------------------------------
    # Method to select reference path(s)
    def Builder(self, sEnsembleName):
        
        #-------------------------------------------------------------------------------------
        # Info start
        oLogStream.info( ' ======= MODEL BUILDER START ========== ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # INITIALIZE BUILDER
        oDrvBuilder = Drv_Model_HMC_Builder(self.sDomainName, self.sRunName, self.oDataInfo, self.oDataTime, 
                                            sEnsembleName)
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # RUN DEFINITION
        # Define run tags
        oDrvBuilder.defineRunTags()
        # Define run type
        oDrvBuilder.defineRunName()
        
        # Define run time
        oDrvBuilder.defineRunTimeNow()
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # CLEAR RUN WORKSPACE
        # Clear run folder(s) 
        #oDrvBuilder.clearRunWorkspace()
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # STATIC INPUT DATA
        # Get static data from source(s) in gridded format (ASCII or NetCDF format)
        oDrvBuilder.getFileStaticGridded()
        # Get static data from source(s) in point format (ASCII)
        oDrvBuilder.getFileStaticPoint()
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # STATIC INFO DATA
        # Get concentration time using terrain information
        oDrvBuilder.computeTc()
        # Select restart time
        oDrvBuilder.selectTimeRestart()
        #-------------------------------------------------------------------------------------
                
        #-------------------------------------------------------------------------------------
        # DYNAMIC INPUT DATA
        # Get dynamic time and define data input format
        oDrvBuilder.selectTimeDynamicGridded()
        # Define run mode and updating steps
        oDrvBuilder.selectUpdDynamicGridded()
        # Get dynamic data from source(s) in gridded format (Binary or NetCDF format)
        oDrvBuilder.getFileDynamicGridded()
        # Get dynamic data from source(s) in point format (Binary or NetCDF format)
        oDrvBuilder.getFileDynamicPoint()
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # INFO FILE
        oDrvBuilder.defineFileStaticInfo()
        # Get info file and update run tags
        oDrvBuilder.getFileStaticInfo()
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get executable file in library folder
        oDrvBuilder.defineFileExec()
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Store DrvBuilder in global variable(s)
        self.oDrvBuilder = oDrvBuilder
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Info end
        oLogStream.info( ' ======= MODEL BUILDER END ============= ')
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------------
    
    
     
     
     
    
    
    
