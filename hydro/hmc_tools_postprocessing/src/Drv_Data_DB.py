"""
Class Features

Name:          Drv_Data_DB
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20150806'
Version:       '1.0.1'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Libraries
import os
import datetime
import numpy as np

from Drv_Data_IO import Drv_Data_IO

from GetException import GetException
######################################################################################

#-------------------------------------------------------------------------------------
# Class GetMeteoData
class Drv_Data_DB:
    
    #-------------------------------------------------------------------------------------
    # Initializing class
    def __init__(self, sTime = None, sFileName = None, oVarInfo = None, oParamsInfo = None):
        
        # Check Database name
        if oParamsInfo['DB']['ID'] == 'DB_UNKNOWN':
            
            # DB UNKNOWN
            GetException(' -----> WARNING: Database set DB_UNKNOWN: Nothing to do!', 2, 1)
            oLogStream.info( ' ------> SELECTED DATABASE: ' + str(oParamsInfo['DB']['ID']) )
            
        elif oParamsInfo['DB']['ID'] == 'DB_RegMarche':
            
            # DB RegMarche
            oLogStream.info( ' ------> SELECTED DATABASE: ' + str(oParamsInfo['DB']['ID']) )
            DB_RegMarche(sTime, sFileName, oVarInfo, oParamsInfo['DB'])
            
        else:
            # Error message
            GetException(' -----> ERROR: DB name not correctly set! Please check your settings file!',1,1)
    #--------------------------------------------------------------------------------
        
#-------------------------------------------------------------------------------------
    
#--------------------------------------------------------------------------------
# Class to use DB_RegMarche
class DB_RegMarche:

    #--------------------------------------------------------------------------------
    # Class init
    def __init__(self, sTimeStep, sFileName, oVarInfo, oDBInfo):
        
        self.sTimeStep = sTimeStep
        self.sFileName = sFileName
        self.oVarInfo = oVarInfo
        self.oDBInfo = oDBInfo
        
        self.iTimeStep = self.oVarInfo['VarTimeStep']
        self.sVarName = self.oVarInfo['VarOp']['Op_GetEx']['Name']

        # Get time
        self.getTime(); 
        
        # Get data
        self.getData();
        
        # Save data
        self.saveData();

    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to get time info
    def getTime(self):
        
        # Time step info
        sTimeStep = self.sTimeStep
        iTimeStep = self.iTimeStep
        
        # Time definition
        oTimeStep = datetime.datetime.strptime(sTimeStep,'%Y%m%d%H%M%S')

        oTimeStepTo = oTimeStep; sTimeStepTo = oTimeStepTo.strftime('%Y-%m-%dT%H:%M:%S.%f'); 
        sTimeStepTo = sTimeStepTo[:-3]; #sTimeSaveTo = oTimeStepTo.strftime('%Y%m%d%H%M')
        oTimeStepFrom = oTimeStep - datetime.timedelta(seconds = iTimeStep); sTimeStepFrom = oTimeStepFrom.strftime('%Y-%m-%dT%H:%M:%S.%f'); 
        sTimeStepFrom = sTimeStepFrom[:-3]; #sTimeSaveFrom = oTimeStepFrom.strftime('%Y%m%d%H%M')
        
        # Save time in global declaration
        self.sTimeStepFrom = sTimeStepFrom
        self.sTimeStepTo = sTimeStepTo
        
    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to save data info
    def saveData(self):
        
        # Get information
        sFileName = self.sFileName
        a1oDBData = self.a1oDBData
        
        # Save data
        oFileDrv = Drv_Data_IO(sFileName, 'w')
        oFileDrv.oFileWorkspace.writeFileData(a1oDBData)
     
    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to get data info
    def getData(self):
        
        # SQL library
        import pymssql
        
        # Define DB query
        sDBQuery = self.defineQuery(self.sVarName, self.sTimeStepFrom, self.sTimeStepTo)
        
        # Define DB info
        sDBID = self.oDBInfo['ID']
        sDBUser = self.oDBInfo['User']
        sDBName = self.oDBInfo['Name']
        sDBPassword = self.oDBInfo['Password']
        sDBServer = self.oDBInfo['Server']

        # Open DB connection
        oDBConnection = pymssql.connect(sDBServer, sDBUser, sDBPassword, sDBName)
        oDBCursor = oDBConnection.cursor()
        # Execute DB query
        oDBCursor.execute(sDBQuery)
        # Get all data
        self.a1oDBData = oDBCursor.fetchall(); #iDBLen = len(a1oDBData)
        # Close DB connection
        oDBConnection.commit()
        
    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to define query db
    def defineQuery(self, sVarName, sTimeStepFrom, sTimeStepTo):
        
        sDBQuery  = "DECLARE @DataInizio DATETIME, @DataFine DATETIME "
        sDBQuery += "SET @DataInizio = '" + sTimeStepFrom + "' "
        sDBQuery += "SET @DataFine = '" + sTimeStepTo + "' "
        sDBQuery += "SELECT s.CodiceUnico AS CodiceSensore, st.CodiceUnico AS CodiceStazione, st.NomeAnnale AS NomeStazione, ds.DatoOrigine AS Pioggia_mm, "
        sDBQuery += "geo.LongCentesimale AS Lon, geo.LatCentesimale AS Lat, geo.Quota AS Zm, sito.Regione, sito.Provincia, sito.Comune, s.BacinoAnnale, "
        sDBQuery += "CONVERT(CHAR(19), @DataInizio, 126 ) AS DataInizio, "
        sDBQuery += "CONVERT(CHAR(19), @DataFine,   126 ) AS DataFine "
        sDBQuery += "FROM DatoSensore AS ds INNER JOIN Sensore AS s ON ds.Sensore = s.CodiceUnico "
        sDBQuery += "    INNER JOIN Stazione AS st ON s.Stazione = st.CodiceUnico "
        sDBQuery += "    INNER JOIN Georeferenza AS geo ON st.Posizione = geo.IDGeo "
        sDBQuery += "    INNER JOIN Sito ON st.SitoCollocazione = sito.IDSito "
        sDBQuery += "WHERE "
        sDBQuery += "    ( ( ds.Data BETWEEN @DataInizio AND @DataFine ) AND NOT( ds.Data=@DataInizio ) ) "
        sDBQuery += "    AND ( s.NomeRete='RMIPR' AND s.TipoSensore='" + sVarName + "' ) "
        sDBQuery += "    AND NOT( ds.DatoOrigine IS NULL ) "
        sDBQuery += "    AND NOT( geo.GaussBoagaEst IS NULL ) "
        sDBQuery += "    AND NOT( geo.GaussBoagaNord IS NULL ) "
        sDBQuery += "    AND NOT( geo.Quota IS NULL ) "
        sDBQuery += "ORDER BY st.CodiceUnico, ds.Data ASC "
        
        return sDBQuery
        
    #--------------------------------------------------------------------------------
        
        
        
        
        
        
    
