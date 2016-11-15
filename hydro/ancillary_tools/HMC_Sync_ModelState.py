
#------------------------------------------------------------------------------------- 
# Library
import os, datetime, time, re, shutil
import subprocess
from os import listdir
from os.path import isfile, join, split
#------------------------------------------------------------------------------------- 

#------------------------------------------------------------------------------------- 
# Script input
sVarPathSource = '/hydro/archive/history_ws-db_20160115_20160414/2016/04/14/00/state/'
sVarPathDest = '/hydro/archive/model_state/$yyyy/$mm/$dd/'

sFileLog = 'log_sync_modelstate.txt'

sSyncCommand = 'rsync -au --progress $SOURCE $DEST'

oVarsType = {'VarType_01' : 'nc.gz', 'VarType_02' : 'txt'}
oVarsHour = {'VarHour_01' : '0000', 'VarHour_02' : '1200'}
#------------------------------------------------------------------------------------- 

#------------------------------------------------------------------------------------- 
# Info
print (' ====> SYNC DATA ... ')
# Get script path
sPathScript = os.path.dirname(os.path.abspath(__file__))
#------------------------------------------------------------------------------------- 

#------------------------------------------------------------------------------------- 
# Cycling on variable type
for sVarType in oVarsType.values():
    
    #-------------------------------------------------------------------------------------
    # Define path destination main
    sVarPathDestMain = sVarPathDest.replace('$yyyy','')
    sVarPathDestMain = sVarPathDestMain.replace('//','/')
    sVarPathDestMain = sVarPathDestMain.replace('$mm','')
    sVarPathDestMain = sVarPathDestMain.replace('//','/')
    sVarPathDestMain = sVarPathDestMain.replace('$dd','')
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
    print( ' =====> SYNC DATA INFO: ' + sStdOut)
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
                    if not sFileHHMM in oVarsHour.values():
                        # HH not selected file removing activated
                        os.remove(join(sFilePath,sFileName))
                    else:
                        # Define path destination subfolder(s)
                        sVarPathDestSub = sVarPathDest.replace('$yyyy', sFileYear)
                        sVarPathDestSub = sVarPathDestSub.replace('$mm', sFileMonth)
                        sVarPathDestSub = sVarPathDestSub.replace('$dd', sFileDay)
                        
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
# Save sync data
sFileName = join(sPathScript, sFileLog)
oFile = open(sFileName, "w")
oFile.write(sStdOut)
oFile.close()
#-------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------- 
# Info end
print(' ====> SYNC DATA ... OK')
#------------------------------------------------------------------------------------- 




