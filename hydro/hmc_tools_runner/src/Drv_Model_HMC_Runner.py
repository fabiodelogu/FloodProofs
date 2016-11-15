"""
Class Features

Name:          Drv_Model_HMC_Runner
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151022'
Version:       '1.6.2'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os
import numpy as np
import subprocess, shlex

import Lib_Data_IO_Utils as Lib_Data_IO_Utils

from GetException import GetException

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Drv_Model_HMC_Runner:
    
    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, sDomainName, sRunName, oDataInfo, oDrvBuilder, sEnsembleName):
        
        # Global variable(s)
        self.sDomainName = sDomainName
        self.sRunName = sRunName
        self.oDataInfo = oDataInfo
        self.oDrvBuilder = oDrvBuilder
        
        self.sEnsembleName = sEnsembleName

    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to check run settings
    def checkRunData(self):
        
        #-------------------------------------------------------------------------------------
        # Info
        oLogStream.info(' ====> RUN DATA CHECKER ... ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get status information
        [a1oTime_STEP, a1oVar_TYPE, a1oVar_STATUS] = zip(*self.oDrvBuilder.oDataStatus)
        #-------------------------------------------------------------------------------------
        
        # Check variable status
        if np.all(a1oVar_STATUS) == True:
            
            # Info
            oLogStream.info(' -----> All data are available for selected run')
            oLogStream.info(' ====> RUN DATA CHECKER ... OK')
            
        elif np.any(a1oVar_STATUS) == True:
            
            # Info
            GetException(' -----> WARNING: some data are unavailable for selected run! Model Run could be affected by errors', 2, 1)
            
            # Get step status
            a1bVar_STATUS = np.asarray(a1oVar_STATUS)
            a1iVar_INDEX = np.where(a1bVar_STATUS == False)
            
            # Cycle(s) on data N/A
            for iVar_INDEX in a1iVar_INDEX[0]:
                sTime_STEP = str(a1oTime_STEP[iVar_INDEX])
                sVar_TYPE = str(a1oVar_TYPE[iVar_INDEX])
                sVar_STATUS = str(a1oVar_STATUS[iVar_INDEX])
                
                # Write information about data N/A
                GetException(' -----> WARNING: Data N/A --- Step: '+ sTime_STEP +
                             ' Type: '+ sVar_TYPE +' Status: ' + sVar_STATUS , 2, 1)
                
            # Info
            oLogStream.info(' ====> RUN DATA CHECKER ... OK --- SOME DATA ARE MISSED!')
            
        elif np.all(a1oVar_STATUS) == False:  
            
            # Info
            oLogStream.info(' ====> RUN DATA CHECKER ... FAILED')
            GetException(' -----> ERROR: all data are unavailable for selected run!', 1, 1)
        
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to compose command line
    def composeCLine(self):
        
        #-------------------------------------------------------------------------------------
        # Example:     Continuum.x --> parameters uc=20 uh= 1.5 ct=0.5 cf=0.02 domain=marche cpi=0.3 Rf=1 Vmax=500 slopemax=70
        #              Continuum.x 20 1.5 0.5 0.02 marche 0.3 500 1 70
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Info start
        oLogStream.info(' ====> COMMAND LINE COMPOSER ... ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get information
        sPathRun = self.oDrvBuilder.oDataInfo.oInfoSettings.oPathInfo['Run']
        sCommandRun = self.oDrvBuilder.oDataInfo.oInfoSettings.oParamsInfo['RunCommand']
        sFileNameExec = self.oDrvBuilder.oDataInfo.oInfoSettings.oParamsInfo['FileExecName']
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Check file availability
        if os.path.exists(os.path.join(sPathRun, sFileNameExec)):
            
            #-------------------------------------------------------------------------------------
            # Change permission(s) ---> chmod +x (permissions problem)
            #os.chmod(os.path.join(sPathRun, sFileNameExec), stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Add executable character
            sCommandLine = './' + sCommandRun
            #-------------------------------------------------------------------------------------
        
            #-------------------------------------------------------------------------------------
            # Set command line in global variable(s)
            self.sCommandPath = sPathRun
            self.sCommandLine = sCommandLine
            self.sCommandFile = sFileNameExec
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Info start
            oLogStream.info(' ====> COMMAND LINE COMPOSER ... OK')
            #-------------------------------------------------------------------------------------
            
        else:
            
            #-------------------------------------------------------------------------------------
            # Exit message
            GetException(' -----> ERROR: command line composer failed! Check your setting(s)!', 1, 1)
            #-------------------------------------------------------------------------------------
            
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to run command line
    def runCLine(self):
        
        #-------------------------------------------------------------------------------------
        # Get information
        sCommandPath = self.sCommandPath
        sCommandLine = self.sCommandLine
        sEnsembleName = self.sEnsembleName
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Info start
        oLogStream.info(' ====> COMMAND LINE RUNNER ... ')
        #-------------------------------------------------------------------------------------
    
        #-------------------------------------------------------------------------------------
        # Check executable and command line
        try:
            
            #-------------------------------------------------------------------------------------
            # Info command line
            oLogStream.info(' -----> Run Name: ' + sEnsembleName)
            oLogStream.info(' -----> Command Line: ' + sCommandLine)
            
            # Execute command line
            os.chdir(sCommandPath)
            #oProcess = subprocess.Popen(shlex.split(sCommandLine), shell=True,  stdout=subprocess.PIPE)
            oProcess = subprocess.Popen(sCommandLine, shell=True,  stdout=subprocess.PIPE)
            while True:
                sOut = oProcess.stdout.readline()
                if sOut == '' and oProcess.poll() is not None:
                    
                    if oProcess.poll() == 0:
                        GetException(' -----> WARNING: Process POOL = ' + str(oProcess.poll()) , 2, 1)
                        sOut = 'Process POOL Killed!'
                        break
                    else:
                        GetException(' -----> ERROR: run failed! Check your settings!', 1, 1)
                if sOut:
                    oLogStream.info(str(sOut.strip()))
            
            # Collect stdout and stderr and exitcode
            sStdOut, sStdErr = oProcess.communicate(); sCodeExit = oProcess.poll()
            
            # Check process execution
            Lib_Data_IO_Utils.checkProcess(sStdOut, sStdErr)
            # Info end
            oLogStream.info(' ====> COMMAND LINE RUNNER ... OK')
            #-------------------------------------------------------------------------------------
            
        except subprocess.CalledProcessError:
        
            #-------------------------------------------------------------------------------------
            # Exit code for process error
            GetException(' -----> ERROR: command line runner failed! Errors in the called executable!', 1, 1)
            #-------------------------------------------------------------------------------------
            
        except OSError:
            
            #-------------------------------------------------------------------------------------
            # Exit code for os error
            GetException(' -----> ERROR: command line runner failed! Executable not found!', 1, 2)
            #-------------------------------------------------------------------------------------
            
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------------
    
    
    
    
    
    
