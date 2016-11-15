"""
Class Features

Name:          GetAncillaryData
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151125'
Version:       '1.0.0'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Global libraries
import os
import numpy as np

# Debug
#import matplotlib.pylab as plt
######################################################################################

#----------------------------------------------------------------------------
# Method to read 3d slope array
def ExpertForecast_RF_VM(sFileName):
    
    import scipy.io as io
    
    # Slope array
    oVM = io.loadmat(sFileName)
    a3dVM = oVM['vm']
    
    # Fitted avg array (update 20 feb 2014, fa)
    a1dVarMean_DEF = np.array([1, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]);
    # Fitted slope X (update 20 feb 2014, fa)
    dVarSXMin = 0.5; dVarSXMax = 3.5; dVarSXRes = 0.2
    iVarSXStep = (dVarSXMax - dVarSXMin)/dVarSXRes + 1
    a1dVarSX = np.linspace(dVarSXMin, dVarSXMax, iVarSXStep, endpoint=True)
    # Fitted slope X (update 20 feb 2014, fa)
    dVarSTMin = 0.5; dVarSTMax = 3.5; dVarSTRes = 0.2
    iVarSTStep = (dVarSTMax - dVarSTMin)/dVarSTRes + 1
    a1dVarST = np.linspace(dVarSTMin, dVarSTMax, iVarSTStep, endpoint=True)
    
    ############### start test ###############
    # Test value(s)
    dVarMax = 18.0; dVarMean = 10;
    # Compute index linked with mean value
    a1dVarMean_COM = np.abs(a1dVarMean_DEF - dVarMean);
    a1iVarMinIndex = np.where(a1dVarMean_COM == np.min(a1dVarMean_COM));
    # Get S as function of VM
    a2dSVM = np.reshape( a3dVM[a1iVarMinIndex[0], :, :], [a3dVM.shape[1], a3dVM.shape[2]]);
    # Compute index linked with max value
    a2dVarMax_COM = np.abs(a2dSVM - dVarMax)
    [iVarSXIndex, iVarSTIndex] = np.where( a2dVarMax_COM == np.min(a2dVarMax_COM));
    # Get slope(s) X and T
    dSX = a1dVarSX[iVarSXIndex]; dST = a1dVarST[iVarSTIndex];
    ############### end test #################
    
    # Save data
    oDataObj = {}
    oDataObj['VM'] = a3dVM
    oDataObj['RAvg'] = a1dVarMean_DEF
    oDataObj['Sx'] = a1dVarSX
    oDataObj['Sy'] = a1dVarSX
    oDataObj['St'] = a1dVarST
    
    return oDataObj
    
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Method to read weather station registry for kf procedure
def ExpertForecast_KF_WeatherStationRegistry(sFileName):
    
    # Library
    import csv
    
    # Init variable(s)
    oWS = []; oGeoX = []; oGeoY = []; oGeoZ = [];
    if os.path.exists(sFileName):
        # Open file
        oFile = csv.reader(open(sFileName, 'r'), delimiter=',')
        
        # Get data raw from csv handle file
        for oRow in oFile:
            sWS = oRow[0].strip(); sWS = sWS.replace(' ', '_');
            sGeoX = oRow[1].strip(); sGeoY = oRow[2].strip(); sGeoZ = oRow[3].strip();
            oWS.append(sWS); oGeoX.append(sGeoX); oGeoY.append(sGeoY); oGeoZ.append(sGeoZ)

    else:
        # Exit table with no data
        oWS = None; oGeoX = None; oGeoY = None;
    
    # Save result(s)
    oTableData = {}
    oTableData['WS'] = oWS
    oTableData['GeoX'] = oGeoX
    oTableData['GeoY'] = oGeoY
    oTableData['GeoZ'] = oGeoZ
    
    # Return table
    return oTableData
#----------------------------------------------------------------------------

