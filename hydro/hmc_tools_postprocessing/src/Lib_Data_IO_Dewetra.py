"""
Library Features:

Name:          Lib_Data_IO_Dewetra
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151110'
Version:       '1.0.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Global libraries
import os, collections
import numpy as np

from os.path import join
from os.path import isfile
from os.path import split

from GetException import GetException

# Debug
import matplotlib.pylab as plt
#################################################################################

#-------------------------------------------------------------------------------------
# Method to get file 2D in ASCII format
def getData2D(sFileName, iSkipRows=0, sSplitRow='\t'):
    
    # Initialize variable
    oTableData = np.array([]);
    
    # Check file availability
    if os.path.exists(sFileName):
    
        # Open ascii file
        oFile = open(os.path.join(sFileName), 'r')
        # Read data
        oTableData = [sRow.strip().split(sSplitRow) for sRow in oFile]
        
        oTableData = oTableData[iSkipRows : ]
        
    else:
        GetException(' -----> WARNING: file 2D does not exist! Check your filesystem!',2,1)
        oTableData = np.array([]);

    # Return variable
    return oTableData
        
#-------------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------------
# Method to get file 1D in ASCII format
def getData1D(sFileName, iSkipRows=0):
    
    # Initialize variable
    oVarData = np.array([]); 
    
    # Check file availability
    if os.path.exists(sFileName):
    
        # Open ascii file
        oFile = open(sFileName, 'r')
        # Read data
        try:
            oVarData = np.loadtxt(oFile, skiprows=iSkipRows)
        except:
            
            # Open the file using universal line ending support:
            oFile_UnivMode = open(sFileName, 'rU')
            oVarData = np.genfromtxt(oFile_UnivMode, skiprows=iSkipRows)
            GetException(' -----> WARNING: in file ' + sFileName + ' found undefined value(s)! Check your data! ',2,1)
            oVarData[np.isnan(oVarData)] = -9999.0
    else:
        GetException(' -----> WARNING: file 1D does not exist! Check your filesystem!',2,1)
        oVarData = np.array([]);

    # Return variable
    return oVarData

#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Method to parse data section info
def parseDataSection(oData):
    
    # Parse file
    a1oDataInfo = []
    for oSection in oData:
        
        oDataInfo = []
        [sX, sY, sBasinName, sSectionName, sSectionCode, sSectionDrainArea, sSectionQAlarm, sSectionQAlert] = oSection[0].split()
        
        #sBasinName = sBasinName.lower(); sBasinName = sBasinName.replace(' ','')
        #sSectionName = sSectionName.lower(); sSectionName = sSectionName.replace(' ','')
        
        oDataInfo = [sX, sY, sBasinName, sSectionName, sSectionCode, sSectionDrainArea, sSectionQAlarm, sSectionQAlert];
        a1oDataInfo.append(oDataInfo)
    
    return a1oDataInfo
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Method to parse data dam info
def parseDataDam(oData):
    
    oDataParse = {}; sLine_STR = ''
    iLineCounter = 0; oXParse = []; oYParse = []; oComplexParse = []; oNameParse = []
    for oLine in oData:
        
        sLineRaw = oLine[0]
        
        iLineCounter = iLineCounter + 1
        if not sLineRaw.startswith('##') and iLineCounter <= 3:
            
            sLineSplit = sLineRaw.split('#')[0]
            
            if sLineSplit.replace(' ','').replace('-','').isdigit():
                
                sLineSplit = sLineSplit.rstrip()
                a1sLineSplit_NUM = sLineSplit.split(' ')
                oLine_NUM = map(float, a1sLineSplit_NUM)
                
                if iLineCounter == 2:
                    iX = int(oLine_NUM[0])
                    iY = int(oLine_NUM[1])
                    oXParse.append(str(iX))
                    oYParse.append(str(iY))
                    
                elif iLineCounter == 3:
                    iDamComplex = int(oLine_NUM[0])
                    oComplexParse.append(str(iDamComplex))
                else:
                    pass
   
            else:
                sLine_STR = sLineSplit.rstrip()
                #sLine_STR = sLine_STR.lower(); sLine_STR = sLine_STR.replace(' ','');
                oNameParse.append(str(sLine_STR))
                
        else:
            
            if sLineRaw.startswith('##'):
                iLineCounter = 0;
            else:
                pass
    
    a1oWorkspace = zip(oXParse, oYParse, oNameParse, oComplexParse)
        
    a1oName = []; sDigit = '%03d'; 
    
    a1oDataInfo = []
    for oLine in a1oWorkspace:
        
        oDataInfo = []
        sX = oLine[0]; sY = oLine[1]; sName = oLine[2]; iComplexMax = int(oLine[3]);
        
        oDataInfo = [sX, sY, sName, sName];
        a1oDataInfo.append(oDataInfo)
        
#         if iComplexMax == 1:
#             
#             oDataInfo = [sX, sY, sName, sName];
#             a1oDataInfo.append(oDataInfo)
#             
#         else:
#             for iComplex in range(1, iComplexMax + 1):
#                 sNameC = sName + str(sDigit%(iComplex))
#                 oDataInfo = [sX, sY, sName, sName];
#                 a1oDataInfo.append(oDataInfo)
          
    return a1oDataInfo
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Method to save file 1D in ASCII format with a specified header
def saveTimeSeries(sFileName, 
               a2dDataModel=None, a1dDataObs=None, 
               sTimeFrom=None, sTimeNow=None,
               sRunType=None, 
               iTimeRes=0, iEnsN=0):
    
    # Convert array from float to string
    a1sDataObs = [a1dDataObs.tolist()]
    
    # Save update information
    oModelData = {}
    
    # Flag information
    oModelData['Line_01'] = 'Procedure='+ str(sRunType) + ' \n'
    oModelData['Line_02'] = 'DateMeteoModel='+ str(sTimeNow) + ' \n'
    oModelData['Line_03'] = 'DateStart='+ str(sTimeFrom) + ' \n'
    oModelData['Line_04'] = 'Temp.Resolution='+ str(iTimeRes) + ' \n'
    oModelData['Line_05'] = 'SscenariosNumber='+ str(int(iEnsN)) + ' \n'
    oModelData['Line_06'] = (' '.join(map(str, a1sDataObs[0]))) + ' \n'
    
    # Cycle(s) on data dimension(s)
    sDigit = '%02d';
    for iEns in range(0, iEnsN):
        
        sLineName = 'Line_'+ str(sDigit%(iEns+7)) 
        
        a1dDataModel = a2dDataModel[iEns]
        a1sDataModel = [a1dDataModel.tolist()]
        
        oModelData[sLineName] = (' '.join(map(str, a1sDataModel[0]))) + ' \n'
        
    # Dictionary sorting
    oModelDataOrd = collections.OrderedDict(sorted(oModelData.items()))
    
    # Open ASCII file (to save all data)
    oFileHandler = open(sFileName,'w');
    
    # Write data in ASCII file
    oFileHandler.writelines(oModelDataOrd.values())
    # Close ASCII file
    oFileHandler.close()
    
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Method to save file warnings in ASCII format with a specified header
def saveWarnings(sFileName, 
                    sLineHeader='', oSecWarning=None, 
                    sTimeFrom='', sTimeTo='', sTimeNow='',
                    sRunType='', iEnsN=0):
    
    # Open ASCII file (to save all data)
    oFileHandler = open(sFileName,'w');
    
    sLine1 = 'Procedure='+ str(sRunType) + ' \n'
    oFileHandler.write(sLine1)
    sLine2 = 'TimeFrom='+ str(sTimeFrom) + ' \n'
    oFileHandler.write(sLine2)
    sLine3 = 'TimeTo='+ str(sTimeTo) + ' \n'
    oFileHandler.write(sLine3)
    sLine4 = 'sTimeNow='+ str(sTimeNow) + ' \n'
    oFileHandler.write(sLine4)
    sLine5='SscenariosNumber='+ str(int(iEnsN)) + ' \n'
    oFileHandler.write(sLine5)
    
    oFileHandler.write(sLineHeader + ' \n')
    
    # Cycle(s) on warning(s)
    for sWarning in oSecWarning:
        # Compose warning line
        sLine = sWarning + ' \n' 
        # Write data in ASCII file
        oFileHandler.write(sLine)
        
    # Close ASCII file
    oFileHandler.close()
    
#-------------------------------------------------------------------------------------
    
    
