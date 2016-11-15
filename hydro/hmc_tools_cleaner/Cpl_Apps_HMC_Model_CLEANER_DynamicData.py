"""
Class Features

Name:          Cpl_Apps_HMC_Model_CLEANER_DynamicData
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151205'
Version:       '1.0.0'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os, datetime, time, re, shutil
import subprocess
from os import listdir
from os.path import isfile, join, split

import src.Lib_Data_IO_Utils as Lib_Data_IO_Utils
from src.GetException import GetException

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Cpl_Apps_HMC_Model_CLEANER_DynamicData:

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataTime=None, oDataInfo=None):
        
        # Data settings and data reference 
        self.oDataTime = oDataTime
        self.oDataInfo = oDataInfo
        
    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------  
    # Method to synchronize files between two folders
    def syncDynamicData(self,sTime):
        
        #------------------------------------------------------------------------------------- 
        # Get variable information
        oVarsInfoSYNC = self.oDataInfo.oInfoVarDynamic.oDataSyncDynamic
        
        # Get time information
        oTimeNow = datetime.datetime.strptime(sTime,'%Y%m%d%H%M')
        oTimeNow = oTimeNow.replace(minute = 0, second = 0, microsecond = 0)
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> SYNC DATA AT TIME: ' + sTime + ' ... ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Cycling on variable type
        for sVarType in oVarsInfoSYNC:
            
            #-------------------------------------------------------------------------------------
            # Variable information
            oVarInfoIN = oVarsInfoSYNC[sVarType]
            sVarType = oVarInfoIN['DataType']
            sVarName = oVarInfoIN['DataName']
            sVarPathSource = oVarInfoIN['DataPathSource']
            sVarPathDest = oVarInfoIN['DataPathDest']
            oVarHour = oVarInfoIN['DataHour']
            iVarArchive = int(oVarInfoIN['DataArchive'])
            sSyncCommand = oVarInfoIN['SyncCommand']
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Define path destination main
            sVarPathDestMain = sVarPathDest.replace('$YYYY','')
            sVarPathDestMain = sVarPathDestMain.replace('//','/')
            sVarPathDestMain = sVarPathDestMain.replace('$MM','')
            sVarPathDestMain = sVarPathDestMain.replace('//','/')
            sVarPathDestMain = sVarPathDestMain.replace('$DD','')
            sVarPathDestMain = sVarPathDestMain.replace('//','/')
            sVarPathDestMain = sVarPathDestMain.replace('$TYPE','')
            sVarPathDestMain = sVarPathDestMain.replace('//','/')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Create sync folder 
            if not os.path.exists(sVarPathDestMain): os.makedirs(sVarPathDestMain)
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Define sync command
            sSyncCommand = sSyncCommand.replace('$SOURCE', sVarPathSource)
            sSyncCommand = sSyncCommand.replace('$DEST', sVarPathDestMain)
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Execute command
            oProcess = subprocess.Popen(sSyncCommand, shell=True,  stdout=subprocess.PIPE)            
            # Collect stdout and stderr and exitcode
            sStdOut, sStdErr = oProcess.communicate(); sCodeExit = oProcess.poll()
            # Information about synchronizing
            oLogStream.info( ' =====> SYNC DATA INFO: ' + sStdOut)
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # List folder(s) and file(s)
            oVarFiles = [oF for oF in listdir(sVarPathDestMain) if isfile(join(sVarPathDestMain, oF))]

            # Cycle(s) on file(s)
            for sVarFile in oVarFiles:
                
                #-------------------------------------------------------------------------------------
                # Define filename adding absolute path
                sVarFile = os.path.join(sVarPathDestMain, sVarFile)
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Check file availability
                if os.path.isfile(sVarFile):
                    
                    #-------------------------------------------------------------------------------------
                    # Get path and file
                    sFilePath = split(sVarFile)[0]
                    sFileName = split(sVarFile)[1]
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Check extension of file(s)
                    if sVarFile.endswith(sVarType) or sVarType == '':
                
                        #-------------------------------------------------------------------------------------
                        # Get file time
                        oMatch = re.search(r'\d{4}\d{2}\d{2}\d{2}\d{2}', sFileName)
                        sTime = oMatch.group();
                        oTime = datetime.datetime.strptime(oMatch.group(), '%Y%m%d%H%M')
                        
                        iFileYear = oTime.year; sFileYear = str(iFileYear).zfill(4);
                        iFileMonth = oTime.month; sFileMonth = str(iFileMonth).zfill(2);
                        iFileDay = oTime.day; sFileDay = str(iFileDay).zfill(2);
                        iFileHour = oTime.hour; sFileHour = str(iFileHour).zfill(2)
                        iFileMin = oTime.minute; sFileMin = str(iFileMin).zfill(2)
                        
                        sFileHHMM = sFileHour + sFileMin
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Check var type in filename
                        if sVarType in sFileName:
                            
                            #-------------------------------------------------------------------------------------
                            # Check if HH is selected or not in file settings
                            if not sFileHHMM in oVarHour.values():
                                # HH not selected file removing activated
                                os.remove(join(sFilePath,sFileName))
                            else:
                                # Define path destination subfolder(s)
                                sVarPathDestSub = sVarPathDest.replace('$YYYY', sFileYear)
                                sVarPathDestSub = sVarPathDestSub.replace('$MM', sFileMonth)
                                sVarPathDestSub = sVarPathDestSub.replace('$DD', sFileDay)
                                
                                # Check folder availability
                                if not os.path.exists(sVarPathDestSub): os.makedirs(sVarPathDestSub)
                                
                                # Move to final destination
                                shutil.move(os.path.join(sVarPathDestMain,sFileName), 
                                            os.path.join(sVarPathDestSub, sFileName))
                            #-------------------------------------------------------------------------------------
                            
                        else:
                            #-------------------------------------------------------------------------------------
                            # Remove if var type is not selected
                            os.remove(join(sFilePath,sFileName))
                            #-------------------------------------------------------------------------------------
                    else:
                        #-------------------------------------------------------------------------------------
                        # Removing file if extension not selected
                        os.remove(join(sFilePath,sFileName))
                        #-------------------------------------------------------------------------------------
                        
                    #-------------------------------------------------------------------------------------
                    
                #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> SYNC DATA AT TIME: ' + sTime + ' ... OK')
        #------------------------------------------------------------------------------------- 

    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Method to compute data
    def cleanDynamicData(self, sTime):
        
        #------------------------------------------------------------------------------------- 
        # Get variable(s) information
        oVarsInfoIN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        oVarsInfoOUT = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic
        
        # Get settings information
        sPathDataSource = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        sPathTemp = self.oDataInfo.oInfoSettings.oPathInfo['DataTemp']
        
        # Get time information
        oTimeNow = datetime.datetime.strptime(sTime,'%Y%m%d%H%M')
        oTimeNow = oTimeNow.replace(minute = 0, second = 0, microsecond = 0)
        #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> CLEAN DATA AT TIME: ' + sTime + ' ... ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Cycling on variable type definition (input)
        oLogStream.info( ' =====> CLEAN INPUT DATA ... ')
        for sVarType in oVarsInfoIN:
            
            #-------------------------------------------------------------------------------------
            # Variable information
            oVarInfoIN = oVarsInfoIN[sVarType]
            sVarType = oVarInfoIN['DataType']
            sVarName = oVarInfoIN['DataName']
            sVarPath = oVarInfoIN['DataPath']
            oVarHour = oVarInfoIN['DataHour']
            iVarArchive = int(oVarInfoIN['DataArchive'])
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Compute time information
            oTimeDelta = datetime.timedelta(days = iVarArchive)
            
            oTimeArchive = oTimeNow - oTimeDelta
            oTimeArchive = oTimeArchive.replace(minute = 0, second = 0, microsecond = 0)
            sTimeArchive = oTimeArchive.strftime('%Y%m%d%H%M')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # List folder(s) and file(s)
            oVarFolders, oVarFiles = Lib_Data_IO_Utils.listObject(sVarPath)
            
            # Cycle(s) on file(s)
            for sVarFile in oVarFiles:
                
                #-------------------------------------------------------------------------------------
                # Info file
                #oLogStream.info( ' -----> File: ' + sVarFile)
                #-------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------
                # Check file availability
                if os.path.isfile(sVarFile):
                    
                    #-------------------------------------------------------------------------------------
                    # Check extension of file(s)
                    if sVarFile.endswith(sVarType) or sVarType == '':
                
                        #-------------------------------------------------------------------------------------
                        # Get file information
                        (mode, ino, dev, 
                         nlink, uid, gid, size, 
                         oTimeA, oTimeM, oTimeC) = os.stat(sVarFile)
                         
                        # Get file time information
                        oTimeFileM = datetime.datetime.fromtimestamp(oTimeM)
                        oTimeFileC = datetime.datetime.fromtimestamp(oTimeC)
                        oTimeFileA = datetime.datetime.fromtimestamp(oTimeA)
                         
                        sTimeFileM = oTimeFileM.strftime('%Y%m%d%H%M')
                        sTimeFileC = oTimeFileC.strftime('%Y%m%d%H%M')
                        sTimeFileA = oTimeFileA.strftime('%Y%m%d%H%M')
                        
                        oTimeFile = max(oTimeFileM, oTimeFileC)
                        oTimeFile = oTimeFile.replace(minute = 0, second = 0, microsecond = 0)
                        sTimeFile = oTimeFile.strftime('%Y%m%d%H%M')

                        # Get path and file
                        sFilePath = split(sVarFile)[0]
                        sFileName = split(sVarFile)[1]
                        
                        oMatch = re.search(r'\d{4}\d{2}\d{2}\d{2}\d{2}', sFileName)
                        
                        sTime = oMatch.group();
                        try:
                            if len(sTime) == 12:
                                try:
                                    oTime = datetime.datetime.strptime(sTime, '%Y%m%d%H%M%S') # day format
                                except:
                                    oTime = datetime.datetime.strptime(sTime, '%Y%j%H%M%S') # julian format
     
                            elif len(sTime) == 10:
                                oTime = datetime.datetime.strptime(sTime, '%Y%m%d%H%M')
                        except:
                            GetException(' ERROR: file IN time ' +sTime+' has unknown format! Cleaning STOPPED' ,1,1)
                        
                        iFileHour = oTime.hour; iFileMin = oTime.minute; 
                        sFileHHMM = str(iFileHour).zfill(2) + str(iFileMin).zfill(2)
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Check file hour to avoid deleting
                        bStopDelete = False
                        if sFileHHMM in oVarHour.values():
                            bStopDelete = True
                        else:
                            bStopDelete = False
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Info
                        oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... ')
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Check stop deleting condition
                        if bStopDelete is False:
                            
                            #-------------------------------------------------------------------------------------
                            # Delete old files and save archive file(s)
                            if oTimeFile < oTimeArchive:
                                
                                # Info
                                oLogStream.info( ' -----> File Time: ' + sTimeFile + ' File Created: ' + str(sTimeFileC) + ' Last Modified: ' + str(sTimeFileM) )
                                # Delete for old file
                                oLogStream.info( ' -----> FileTime ('+sTimeFile+') < ArchiveTime ('+sTimeArchive+')')
                                os.remove(sVarFile)
                                oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... OK')
                                
                            else: 
                                # Exit for archive file
                                #oLogStream.info( ' -----> FileTime ('+sTimeFile+') >= ArchiveTime ('+sTimeArchive+')')
                                oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... SKIPPED (DATEFILE SAVE')
                        
                        else:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit for archive file
                            #oLogStream.info( ' -----> FileTimeHH ('+sFileHHMM+') == FileSaveHH ('+str(oVarHour.values())+')')
                            oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... SKIPPED (ARCHIVEHH SAVE)')
                            #-------------------------------------------------------------------------------------
                            
                        #-------------------------------------------------------------------------------------
                    
                    else: pass
                        #-------------------------------------------------------------------------------------
                        # Exit due to unselected file extension
                        # oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... SKIPPED --- TYPE FILE SELECTED FOR DELETING ('+sVarType+') DOES NOT MATCH')
                        #-------------------------------------------------------------------------------------
                    
                else:
                    #-------------------------------------------------------------------------------------
                    # Exit file not available on disk
                    GetException(' WARNING: ' +sVarFile+' does not exist! Cleaning SKIPPED' ,2,1)
                    #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Cycle(s) on folder(s) --> from subfolders to root folder
            for sVarFolder in sorted(oVarFolders,reverse=True):
                
                #-------------------------------------------------------------------------------------
                # Check empty or not empty folder
                if not os.listdir(sVarFolder):
                    # Info
                    oLogStream.info( ' -----> Folder: ' + sVarFolder)
                    oLogStream.info( ' -----> Deleting Folder: ' + sVarFolder + ' ... ')
                    
                    # Delete for empty folder
                    os.rmdir(sVarFolder)
                    oLogStream.info( ' -----> Deleting Folder: ' + sVarFolder + ' ... OK')
                else: pass
                    # Exit for folder not empty
                    #oLogStream.info( ' -----> Deleting Folder: ' + sVarFolder + ' ... SKIPPED! Folder is not empty!')
                #-------------------------------------------------------------------------------------
        
        # Info end
        oLogStream.info( ' =====> CLEAN INPUT DATA ... OK')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Cycling on variable type definition (output)
        oLogStream.info( ' =====> CLEAN OUTPUT DATA ... ')
        for sVarType in oVarsInfoOUT:
            
            #-------------------------------------------------------------------------------------
            # Variable information
            oVarInfoOUT = oVarsInfoOUT[sVarType]
            sVarType = oVarInfoOUT['DataType']
            sVarName = oVarInfoOUT['DataName']
            sVarPath = oVarInfoOUT['DataPath']
            oVarHour = oVarInfoOUT['DataHour']
            iVarArchive = int(oVarInfoOUT['DataArchive'])
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Compute time information
            oTimeDelta = datetime.timedelta(days = iVarArchive)
            
            oTimeArchive = oTimeNow - oTimeDelta
            oTimeArchive = oTimeArchive.replace(minute = 0, second = 0, microsecond = 0)
            sTimeArchive = oTimeArchive.strftime('%Y%m%d%H%M')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # List folder(s) and file(s)
            oVarFolders, oVarFiles = Lib_Data_IO_Utils.listObject(sVarPath)
            
            # Cycle(s) on file(s)
            for sVarFile in oVarFiles:
                
                #-------------------------------------------------------------------------------------
                # Info file
                #oLogStream.info( ' -----> File: ' + sVarFile)
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Check file availability
                if os.path.isfile(sVarFile):
                    
                    #-------------------------------------------------------------------------------------
                    # Check extension of file(s)
                    if sVarFile.endswith(sVarType) or sVarType == '':
                    
                        #-------------------------------------------------------------------------------------
                        # Get file information
                        (mode, ino, dev, 
                         nlink, uid, gid, size, 
                         oTimeA, oTimeM, oTimeC) = os.stat(sVarFile)

                        # Get file time information
                        oTimeFileM = datetime.datetime.fromtimestamp(oTimeM)
                        oTimeFileC = datetime.datetime.fromtimestamp(oTimeC)
                        oTimeFileA = datetime.datetime.fromtimestamp(oTimeA)
                         
                        sTimeFileM = oTimeFileM.strftime('%Y%m%d%H%M')
                        sTimeFileC = oTimeFileC.strftime('%Y%m%d%H%M')
                        sTimeFileA = oTimeFileA.strftime('%Y%m%d%H%M')
                        
                        oTimeFile = max(oTimeFileM, oTimeFileC)
                        oTimeFile = oTimeFile.replace(minute = 0, second = 0, microsecond = 0)
                        sTimeFile = oTimeFile.strftime('%Y%m%d%H%M')
                        
                        # Get path and file
                        sFilePath = split(sVarFile)[0]
                        sFileName = split(sVarFile)[1]
                        
                        oMatch = re.search(r'\d{4}\d{2}\d{2}\d{2}\d{2}', sFileName)
                        sTime = oMatch.group();
                        
                        try:
                            if len(sTime) == 12:
                                try:
                                    oTime = datetime.datetime.strptime(sTime, '%Y%m%d%H%M%S') # day format
                                except:
                                    oTime = datetime.datetime.strptime(sTime, '%Y%j%H%M%S') # julian format
     
                            elif len(sTime) == 10:
                                oTime = datetime.datetime.strptime(sTime, '%Y%m%d%H%M')
                        except:
                            GetException(' ERROR: file IN time ' +sTime+' has unknown format! Cleaning STOPPED' ,1,1)
                        
                        iFileHour = oTime.hour; iFileMin = oTime.minute; 
                        sFileHHMM = str(iFileHour).zfill(2) + str(iFileMin).zfill(2)
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Check file hour to avoid deleting
                        bStopDelete = False
                        if sFileHHMM in oVarHour.values():
                            bStopDelete = True
                        else:
                            bStopDelete = False
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Info
                        oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... ')
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Check stop deleting condition
                        if bStopDelete is False:
                            
                            #-------------------------------------------------------------------------------------
                            # Delete old files and save archive file(s)
                            if oTimeFile < oTimeArchive:
                                
                                # Info
                                oLogStream.info( ' -----> File Time: ' + sTimeFile + ' File Created: ' + str(sTimeFileC) + ' Last Modified: ' + str(sTimeFileM) )
                                # Delete for old file
                                oLogStream.info( ' -----> FileTime ('+sTimeFile+') < ArchiveTime ('+sTimeArchive+')')
                                os.remove(sVarFile)
                                oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... OK')
                                
                            else: 
                                # Exit for archive file
                                #oLogStream.info( ' -----> FileTime ('+sTimeFile+') >= ArchiveTime ('+sTimeArchive+')')
                                oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... SKIPPED (DATEFILE SAVE)')
                                
                            #-------------------------------------------------------------------------------------
                    
                        else: 
                            
                            #-------------------------------------------------------------------------------------
                            # Exit for archive file
                            #oLogStream.info( ' -----> FileTimeHH ('+sFileHHMM+') == FileSaveHH ('+str(oVarHour.values())+')')
                            oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... SKIPPED (ARCHIVEHH SAVE)')
                            #-------------------------------------------------------------------------------------
                            
                        #-------------------------------------------------------------------------------------
                    
                    else: pass
                        #-------------------------------------------------------------------------------------
                        # Exit due to unselected file extension
                        # oLogStream.info( ' -----> Deleting File: ' + sVarFile + ' ... SKIPPED --- TYPE FILE SELECTED FOR DELETING ('+sVarType+') DOES NOT MATCH')
                        #-------------------------------------------------------------------------------------
                    
                else:
                    #-------------------------------------------------------------------------------------
                    # Exit file not available on disk
                    GetException(' WARNING: ' +sVarFile+' does not exist! Cleaning SKIPPED' ,2,1)
                    #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Cycle(s) on folder(s) --> from subfolders to root folder
            for sVarFolder in sorted(oVarFolders,reverse=True):
                
                #-------------------------------------------------------------------------------------
                # Check empty or not empty folder
                if not os.listdir(sVarFolder):
                    
                    # Info
                    oLogStream.info( ' -----> Folder: ' + sVarFolder)
                    oLogStream.info( ' -----> Deleting Folder: ' + sVarFolder + ' ... ')
                
                    # Delete for empty folder
                    os.rmdir(sVarFolder)
                    oLogStream.info( ' -----> Deleting Folder: ' + sVarFolder + ' ... OK')
                else: pass
                    # Exit for folder not empty
                    #oLogStream.info( ' -----> Deleting Folder: ' + sVarFolder + ' ... SKIPPED! Folder is not empty!')
                #-------------------------------------------------------------------------------------
        
        # Info end
        oLogStream.info( ' =====> CLEAN OUTPUT DATA ... OK')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> CLEAN DATA AT TIME: ' + sTime + ' ... OK')
        #------------------------------------------------------------------------------------- 
        
        # End cycle(s) on variable type(s)
        #-------------------------------------------------------------------------------------
        
    # End method
    #-------------------------------------------------------------------------------------
    
# End class
#-------------------------------------------------------------------------------------
            







 
