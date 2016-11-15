"""
Class Features

Name:          GetPointData
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20160211'
Version:       '1.0.1'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Libraries
import os
import numpy as np

from os.path import isfile
from os.path import split
from os.path import join
    
from GetException import GetException
from Drv_Data_IO import Drv_Data_IO, FileAscii

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class GetGeoData
class GetPointData:
    
    #-------------------------------------------------------------------------------------
    # Initializing class
    def __init__(self, sFileName = None):
        
        # Check if filename is defined
        if (sFileName is not None):
        
            # Check file availability
            if isfile(sFileName):
            
                # Passing information to a global allocation
                self.sFileName = sFileName

                # Checking data availability
                if self.sFileName:
                    # Reading ascii-grid file
                    self.readPoint()
                else:
                    # Otherwise exiting with error
                    GetException(' -----> ERROR: Getting geodata failed! Check file settings!', 1, 1)
                    
            else:
                # Otherwise exiting with warning
                GetException(' -----> WARNING: File does not exist! Check your source folder! ('+sFileName+')', 2, 1)
                self.oGeoData = None
        else:
            # Otherwise exiting with warning
            GetException(' -----> WARNING: both filename and geobox are undefined! ('+sFileName+')', 2, 1)
            self.oGeoData = None
                
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Getting section point 
    def readPoint(self):
        
        #-------------------------------------------------------------------------------------
        # Read ascii grid file
        oFileDriver = Drv_Data_IO(self.sFileName,'r')
        oFileObject = oFileDriver.oFileWorkspace.read2DVar(iSkipRows=0, sSplitRow='\t')
        oFileDriver.oFileWorkspace.closeFile()
        # Load data 
        oTableData = oFileObject['Data']; 
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Read and parser data
        oSecGeoX = []; oSecGeoY = []; oSecDomain = []; oSecName = []; 
        oSecCode = []; oSecArea = []; oSecQAlarm = []; oSecQAlert = [];
        for oLineData in oTableData:
            
            a1sLineData = oLineData[0].split()
            
            oSecGeoX.append(a1sLineData[0])
            oSecGeoY.append(a1sLineData[1])
            oSecDomain.append(a1sLineData[2])
            oSecName.append(a1sLineData[3])
            oSecCode.append(a1sLineData[4])
            oSecArea.append(a1sLineData[5])
            oSecQAlarm.append(a1sLineData[6])
            oSecQAlert.append(a1sLineData[7])
        
        self.a1oSecGeoX = map(int, oSecGeoX)
        self.a1oSecGeoY = map(int, oSecGeoY)
        self.a1oSecDomain = map(str, oSecDomain)
        self.a1oSecName = map(str, oSecName)
        self.a1oSecCode = map(int, oSecCode)
        self.a1oSecArea = map(float, oSecArea)
        self.a1oSecQAlarm = map(float, oSecQAlarm)
        self.a1oSecQAlert = map(float, oSecQAlert)
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------

    








