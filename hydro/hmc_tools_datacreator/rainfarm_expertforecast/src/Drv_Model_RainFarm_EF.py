"""
Class Features:

Name:          Drv_Model_RainFarm
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org); Mirko D'Andrea (mirko.dandrea@cimafoundation.org)
Date:          '20150823'
Version:       '3.0.0'
"""

#################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

import sys
import os
import numpy as np
import multiprocessing as mp

from scipy.interpolate import griddata

import Lib_Model_RainFarm_Utils as RFUtils
import Lib_Model_RainFarm_Apps  as RFApps
import Lib_Model_RainFarm_Regrid as RFRegrid

from Lib_Model_RainFarm_Utils import printMessage
from GetException import GetException

# Debug
import matplotlib.pylab as plt
#################################################################################



#--------------------------------------------------------------------------------
# Class to manage RainFarm model
class Drv_Model_RainFarm_EF(object):
    
    #--------------------------------------------------------------------------------
    # Class init
    def __init__(self, a3dDataXYT_IN, 
                       sTimeFrom_IN, sTimeTo_IN, 
                       a2dGeoX_IN, a2dGeoY_IN,
                       a2dGeoX_REF, a2dGeoY_REF, dGeoXStep_REF, dGeoYStep_REF, 
                       a2iAlertArea_REF,
                       dGeoKm_EXT=0,
                       oNEnsemble={'EnsMin': 1, 'EnsMax': 1},
                       iCSsf=1, iCTsf=1,
                       iRatioS=None, iRatioT=None,
                       oDataSlope=None, 
                       bMultiCore=False,
                       sPathCache=None):
        
        # Save in global workspaceoLogStream
        self.a3dDataXYT_IN = a3dDataXYT_IN
        
        self.sTimeFrom_IN = sTimeFrom_IN
        self.sTimeTo_IN = sTimeTo_IN
        
        self.a2dGeoX_IN = a2dGeoX_IN
        self.a2dGeoY_IN = a2dGeoY_IN
        
        self.a2dGeoX_REF = a2dGeoX_REF
        self.a2dGeoY_REF = a2dGeoY_REF
        self.dGeoXStep_REF = dGeoXStep_REF
        self.dGeoYStep_REF = dGeoYStep_REF
        self.dGeoKm_EXT = dGeoKm_EXT
        
        self.a2iAlertArea_REF = a2iAlertArea_REF
        
        self.oNEnsemble = oNEnsemble
        
        self.iCSsf = iCSsf
        self.iCTsf = iCTsf
        self.iRatioS = iRatioS
        self.iRatioT = iRatioT
        
        self.oDataSlope = oDataSlope

        self.a2dMetagauss_RF = None
        
        self.bMultiCore = bMultiCore
        
        self.sPathCache = sPathCache
        
    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to initialize RF model
    @staticmethod
    def initializer(a3dDataXYT_IN,
                    sTimeFrom_IN, sTimeTo_IN,
                    a2dGeoX_IN, a2dGeoY_IN,
                    a2dGeoX_REF, a2dGeoY_REF, a2iAlertArea_REF,
                    dGeoXStep_REF, dGeoYStep_REF, 
                    dGeoKm_EXT,
                    iRatioS, iRatioT,
                    oDataSlope, 
                    sPathCache):
        
        #--------------------------------------------------------------------------------
        # Info start
        printMessage( ' ----->  Initialize RF model  ... ')
        oVol_CVOL = None; oVol_RF = None;
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Extend REF grid
        printMessage( ' ------>  Extend RF spatial domain  ... ')
        [a2dGeoX_REF, a2dGeoY_REF] = RFUtils.extendGrid(a2dGeoX_IN, a2dGeoY_IN, 
                                                        a2dGeoX_REF, a2dGeoY_REF, dGeoXStep_REF, dGeoYStep_REF, 
                                                        dGeoKm_EXT)
        printMessage( ' ------>  Extend RF spatial domain  ... OK')
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Compute RF grid
        printMessage( ' ------>  Compute RF grid  ... ')
        
        [a2dGeoX_RF, a2dGeoY_RF, a2iIndex_RF, 
         dGeoXLL_RF, dGeoYLL_RF, iIMin_RF, iIMax_RF, iJMin_RF, iJMax_RF,
         iRatioS, iResolution_RF, iNPixels_RF] = RFUtils.computeGrid(a2dGeoX_IN, a2dGeoY_IN, 
                                                                   a2dGeoX_REF, a2dGeoY_REF, 
                                                                   dGeoXStep_REF, dGeoYStep_REF, 
                                                                   iRatioS)
         
         
        a2iAlertArea_RF = griddata((a2dGeoX_REF.ravel(), a2dGeoY_REF.ravel()), a2iAlertArea_REF.ravel(),
                                              (a2dGeoX_RF, a2dGeoY_RF), method='nearest', fill_value = -9999.0)

        printMessage( ' ------>  Compute RF grid  ... OK')
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Compute RF volume (to control values on grid boundaries)
        #printMessage( ' ------>  Compute RF volume  ... ')
        #[oVol_CVOL, oVol_RF] = RFUtils.computeVolume(a2dGeoX_IN, a2dGeoY_IN, 
        #                                                 a2dGeoX_REF, a2dGeoY_REF, 
        #                                                 a2dGeoX_RF, a2dGeoY_RF,
        #                                                 iIMin_RF, iIMax_RF, iJMin_RF, iJMax_RF,
        #                                                 sPathCache)
        #printMessage( ' ------>  Compute RF volume  ... OK')
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Compute RF time steps
        printMessage( ' ------>  Compute RF time steps ... ')
        [a1oDataTime_RF, iDataStep_RF, iDataDelta_RF] = RFUtils.computeTimeSteps(sTimeFrom_IN, sTimeTo_IN, a3dDataXYT_IN.shape[2], iRatioT)
        printMessage( ' ------>  Compute RF time steps ... OK')
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Other RF variable(s)
        iNs = iResolution_RF
        iNsl = iNPixels_RF
        iNr = 1
        iNas = iNPixels_RF
        iNt = iDataStep_RF #iNt = a3dDataXYT_RF.shape[2]*iRatioT
        iNtl = a3dDataXYT_IN.shape[2]
        iNat = a3dDataXYT_IN.shape[2]
        iNDelta = iDataDelta_RF
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Info end
        printMessage( ' ----->  Initialize RF model  ... OK')
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Return variable(s)
        return (a2iAlertArea_RF, a1oDataTime_RF,
                a2dGeoX_RF, a2dGeoY_RF, a2iIndex_RF, oVol_CVOL, oVol_RF, 
                a2dGeoX_REF, a2dGeoY_REF, 
                iNs, iNsl, iNr, iNas, iNt, iNtl, iNat, iNDelta)
        #--------------------------------------------------------------------------------
        
    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to get process id
    def getProcessInfo(self, sTitle):
        
        # Info
        printMessage( ' ------> Info: ' + str(sTitle) + ' ModuleName: ' + str(__name__))
        
        if hasattr(os, 'getppid'):  # only available on Unix
            printMessage( ' -------> Parent process id: ' + str(os.getppid()))
    
        printMessage( ' -------> Process id: ' + str(os.getppid()))
    
    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to get process signal start
    def getProcessSignalStart(self):
        
        # Info
        printMessage( ' ------> Process: ' + str(mp.current_process().name) + ' ... START')

    #--------------------------------------------------------------------------------

    #--------------------------------------------------------------------------------
    # Method to get process signal end
    def getProcessSignalEnd(self, oP):
        
        # Info
        printMessage( ' ------> Process: ' + str(oP.name) + ' ExitCode: ' + str(oP.exitcode) + ' ... CLOSED')

    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to manage RF model
    def main(self):
        
        #--------------------------------------------------------------------------------
        # Initialize RF workspace
        oWorkspace_RF = {}
        oWorkspace_RF['static'] = {}
        oWorkspace_RF['dynamic'] = {}
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Info start
        printMessage(' ====> RUN RAINFARM DRV ... ')
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Initialize RF model
        [self.a2iAlertArea_RF, self.a1oDataTime_RF,
         self.a2dGeoX_RF, self.a2dGeoY_RF, self.a2iIndex_RF, self.oVol_CVOL, self.oVol_RF,
         self.a2dGeoX_REF, self.a2dGeoY_REF,
         self.iNs, self.iNsl, self.iNr, self.iNas, 
         self.iNt, self.iNtl, self.iNat, 
         self.iNDelta] = self.initializer(self.a3dDataXYT_IN,
                                          self.sTimeFrom_IN, self.sTimeTo_IN,
                                          self.a2dGeoX_IN, self.a2dGeoY_IN,
                                          self.a2dGeoX_REF, self.a2dGeoY_REF, self.a2iAlertArea_REF,
                                          self.dGeoXStep_REF, self.dGeoYStep_REF, 
                                          self.dGeoKm_EXT,
                                          self.iRatioS, self.iRatioT,
                                          self.oDataSlope, 
                                          self.sPathCache)
        # Save static data in RF workspace
        oWorkspace_RF['static'] = vars(self)
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Info about process
        self.getProcessInfo((str(sys._getframe().f_code.co_name)))
        #--------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------
        # Run RF using single core method
        oResults_RF = self.builder_expertforecast()
        #--------------------------------------------------------------------------------
            
        # Save dynamic data in output workspace
        oWorkspace_RF['dynamic'] = oResults_RF
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Info end
        printMessage(' ====> RUN RAINFARM DRV ... OK')
        # Return variable(s)
        return oWorkspace_RF
        #--------------------------------------------------------------------------------
            
    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to execute RF using expert forecast
    def builder_expertforecast(self):
        
        #--------------------------------------------------------------------------------
        # Info start
        printMessage( ' -----> Build RF model (EXPERT FORECAST MODE) ... ')
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Info about process
        self.getProcessInfo((str(sys._getframe().f_code.co_name)))
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Get data from global workspace
        a2iAAData = self.a2iAlertArea_RF
        oDataSlope = self.oDataSlope
        
        # Get ensemble information
        iEnsembleMin = int(self.oNEnsemble['EnsMin'])
        iEnsembleMax = int(self.oNEnsemble['EnsMax'])
        iEnsembleTot = iEnsembleMax - iEnsembleMin + 1
        
        if iEnsembleMin > iEnsembleMax:
            printMessage( ' --------> WARNING: ensemble min tag > ensemble max tag! Set to 1 default run!')
            iEnsembleMin = 1; iEnsembleMax = 1; iEnsembleTot = 1;
        else:pass
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Cycle(s) on ensemble(s)
        oResults_RF = {}
        a1iNEnsemble = np.linspace(iEnsembleMin, iEnsembleMax, iEnsembleTot, endpoint=True)
        for iE, iNEn in enumerate(a1iNEnsemble):
            
            #--------------------------------------------------------------------------------
            # Info ensemble
            sNEn = str(int(iNEn)).zfill(3)
            printMessage( ' ------> Ensemble: ' + str(sNEn) + ' ... ')
            #--------------------------------------------------------------------------------
            
            #--------------------------------------------------------------------------------
            # Cycling on time steps
            a3dModelXYT_RF = np.zeros([self.iNs, self.iNs, (self.iRatioT*self.iNat)])
            a3dModelIT_RF = np.zeros([self.iNs*self.iNs, (self.iRatioT*self.iNat)])
            for iTimeStep in range(0, self.iNat):
                
                #--------------------------------------------------------------------------------
                # Get time index
                iTimeIndexStart = iTimeStep*self.iRatioT
                iTimeIndexEnd = iTimeStep*self.iRatioT + self.iRatioT
                #--------------------------------------------------------------------------------
                
                #--------------------------------------------------------------------------------
                # Cycling on each domain
                for iArea in sorted(oDataSlope):
                    
                    #--------------------------------------------------------------------------------
                    # Info domain
                    printMessage( ' ------> Area: ' + str(iArea) + ' ... ')
                    #--------------------------------------------------------------------------------
                    
                    #--------------------------------------------------------------------------------
                    # Get alert area index
                    a1iAAData = a2iAAData.ravel(); a1iAAIndex = np.where(a1iAAData == iArea)[0]
                    #--------------------------------------------------------------------------------
                    
                    #--------------------------------------------------------------------------------
                    # Get slopes
                    a1dDataSlope = oDataSlope[iArea][iTimeStep]
                    dRainAvg = a1dDataSlope[0];
                    dSlopeS = a1dDataSlope[2]; dSlopeT = a1dDataSlope[4]

                    # Run RF model
                    [a3dModelXYT_RF, a2dMetagauss_RF] = self.runner(None, 
                                                                    self.iRatioS, 
                                                                    self.iRatioT/self.iNat,
                                                                    cssf = self.iCSsf, ctsf = self.iCTsf, 
                                                                    f = self.a2dMetagauss_RF,
                                                                    celle3_rainfarm=None,
                                                                    sx=dSlopeS, st=dSlopeT, 
                                                                    nx=self.iNs, ny=self.iNs, nt=self.iNat)
                    # Post-process result(s)
                    a3dModelIJT_RF = np.reshape(a3dModelXYT_RF, [self.iNs*self.iNs, self.iRatioT])
                    
                    # Compute mean and weight(s)
                    dModelMean_RF = np.nanmean(a3dModelIJT_RF[a1iAAIndex, :])
                    if dModelMean_RF > 0.0: 
                        dModelWG_RF = dRainAvg/self.iRatioT/dModelMean_RF
                    else:
                        dModelWG_RF = 0.0
                    
                    # Normalized result(s) using weight(s)
                    a3dModelIT_RF[a1iAAIndex, iTimeIndexStart:iTimeIndexEnd] = a3dModelIJT_RF[a1iAAIndex, :]*dModelWG_RF;

                    # Info domain
                    printMessage( ' ------> Area: ' + str(iArea) + ' ... OK')
                    #--------------------------------------------------------------------------------
                    
                #--------------------------------------------------------------------------------
                
            #--------------------------------------------------------------------------------
            # Reshape results in XYT format
            a3dModelXYT_RF = np.reshape(a3dModelIT_RF, [ self.iNs, self.iNs, (self.iRatioT*self.iNat) ]); 
            
            # Debug
            #plt.figure(1)
            #plt.imshow(a3dModelXYT_RF[:,:,0]); plt.colorbar()
            #plt.show()  
            #--------------------------------------------------------------------------------   
                    

            #--------------------------------------------------------------------------------
            # Finalize RF model
            a1oDataXYT_OUT = self.finalizer(None, a3dModelXYT_RF, self.a1oDataTime_RF,
                                              self.a2dGeoX_REF, self.a2dGeoY_REF, 
                                              self.a2dGeoX_RF, self.a2dGeoY_RF, self.a2iIndex_RF, 
                                              self.iNt, self.iNat, 
                                              self.iCSsf, self.iCTsf)
            #--------------------------------------------------------------------------------
            
            #--------------------------------------------------------------------------------
            # Save dynamic data in RF workspace
            oResults_RF[str(int(iNEn))] = {}
            oResults_RF[str(int(iNEn))] = a1oDataXYT_OUT

            # Info ensemble
            printMessage( ' ------> Ensemble: ' + str(sNEn) + ' ... OK')
            #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Info end
        printMessage( ' -----> Build RF model (EXPERT FORECAST MODE) ... OK')
        # Return variable(s)
        return oResults_RF
        #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to finalize RF model
    @staticmethod
    def finalizer(a3dDataXYT_RF, a3dModelXYT_RF, a1oDataTime_RF,
                  a2dGeoX_REF, a2dGeoY_REF, 
                  a2dGeoX_RF, a2dGeoY_RF, a2iIndex_RF, 
                  iNt, iNat, 
                  iCSsf, iCTsf):
        
        #--------------------------------------------------------------------------------
        # Info start
        printMessage( ' ------> Finalize RF model ... ')
        #--------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------
        # Cycling on data
        printMessage( ' --------> Compute output fields ... ' )
        sVarName = 'Rain' 
        a1oDataXYT_OUT = {}; 
        a1oDataXYT_OUT[sVarName] = {}
        for iStep in range(0, a3dModelXYT_RF.shape[2]):
        
            # Get time sinformation
            sDataTime = str(a1oDataTime_RF[iStep])
            
            # Info
            printMessage( ' --------> TIME: ' + str(sDataTime) +' STEP_OUT: ' + str(iStep) + ' ... ')
            
            # Grid data
            a2dModelXY_RF = a3dModelXYT_RF[:,:, iStep]
            #a2dDataXY_REF = RFRegrid.gridData(a2dModelXY_RF, a2dGeoX_RF, a2dGeoY_RF, a2dGeoX_REF, a2dGeoY_REF)
            a1dDataXY_REF = a2dModelXY_RF.ravel()[a2iIndex_RF.ravel()]
            a2dDataXY_REF = np.reshape(a1dDataXY_REF, [a2dGeoX_REF.shape[0], a2dGeoY_REF.shape[1]])
            
            # Debug
            #plt.figure(1)
            #plt.imshow(a2dModelXY_RF); plt.colorbar()
            #plt.figure(2)
            #plt.imshow(a2dDataXY_REF); plt.colorbar()
            #plt.show()
            
            # Save data and time
            a1oDataXYT_OUT[sVarName][sDataTime] = a2dDataXY_REF
            
            # Info
            printMessage( ' --------> TIME: ' + str(sDataTime) +' STEP_OUT: ' + str(iStep) + ' ... OK')
        
        # Info
        printMessage( ' --------> Compute output fields ... OK ')
        #--------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------
        # Info end
        printMessage( ' ------> Finalize RF model ... OK')

        # Return variable(s)
        return a1oDataXYT_OUT
        #--------------------------------------------------------------------------------
        
    #--------------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------------
    # Method to run RF model
    @staticmethod
    def runner(X, xscale, tscale, cssf, ctsf, 
             f=None, celle3_rainfarm=None, sx=None, st=None, nx=None, ny=None, nt=None):
        
        '''
        x=rainfarm(X,sx,st,xscale,cssf,csst)
        INPUT
            X = matrice 3D di dimensioni nx * nx * nt, nx
            xscale = fattore di scala spaziale (numero intero)
            tscale = fattore di scala temporale (numero intero)
            cssf = scala spaziale affidabile 
                    (numero intero, 1 = risoluzione nativa)
            ctsf = scala temporale affidabile 
                    (numero intero, 1 = risoluzione nativa)
            f = ampiezze per il campo metagaussiano,  OPZIONALE
            celle3_rainfarm = matrice per l'interpolazione,   OPZIONALE
            sx = penza spettrale spaziale,    OPZIONALE
            st = penza spettrale temporale,    OPZIONALE 
             
        OUTPUT
            x = matrice 3D con il campo disaggregato di dimensioni (nx*xscale) * 
                (nx*xscale) * (nt*tscale)
            f = ampiezze per il campo metagaussiano calcolate
        '''
        
        # Info start
        printMessage( ' ------> Run RF model ... ')
        
        # Nx and NY 
        if X != None:
            if X.ndim == 2:
                nx, ny = X.shape
                nt = nt
            elif X.ndim == 3:
                nx, ny, nt = X.shape
        elif X == None:
            X = np.float64(1.0)
            nx=nx; ny=ny; nt=nt
            cssf = nx; ctsf = nt
            
        # Alpha
        alfa = 1
        
        if cssf == 1 and ctsf == 1:
            pa = X
        else:
            if X.ndim == 0:
                pa = X
            elif X.ndim == 3:
                pa = RFApps.agg_xyt(X[:, :, 0:nt], nx/cssf, ny/cssf, nt/ctsf)

        # ====> START DEBUG DATA
        #import scipy.io as sio
        #data = {}
        #data['rain'] = X
        #sio.savemat('rain_debug.mat',data)
         
        #plt.figure(1)
        #plt.imshow(X[:,:,0], interpolation='none'); plt.colorbar()
        #plt.show()
        # ====> END DEBUG DATA
         
        # Find spectral slopes
        if sx is None and st is None:
             
            fxp,fyp,ftp = RFApps.fft3d(X)
             
            kmin = 3
            kmax = min(15, len(fxp)-1)
            wmin = 3
            wmax = min(9, len(ftp)-1)
     
            sx,sy,st = RFApps.fitallslopes(fxp, fyp, ftp, 
                                           np.arange(kmin, kmax+1),
                                           np.arange(wmin, wmax+1)) 
             
            # INIT: prepare f field for metagauss
            #np.random.rand('state',sum(100*clock))  ##ok<RAND> # 
            #seme random differente per ogni run del modello
        else:
            sx = sx; sy = sx; st = st;
        
        # Info slope(s)
        printMessage(' -------> Slopes: sx=%f sy=%f st=%f'%(sx, sy, st))
        
        if f is None:
            f = RFApps.initmetagauss(sx, st, ny*xscale, nt*tscale)
            
        # Generate metagaussian field
        g = RFApps.metagauss(f)
        
        # Nonlinear transform
        g = np.exp(alfa * g[0:ny*xscale, 0:ny*xscale, 0:nt*tscale]) 
        
        # We want the aggregated field to be the same as pa
        ga = RFApps.agg_xyt(g, nx/cssf, ny/cssf, nt/ctsf)
        
        ca = pa/ga
        
        if ca.ndim == 0:
            
            x = ca*g
            
            x[np.where(x <= 0.25*X)] = 0.0
            
        elif ca.ndim == 3:
        
            if  celle3_rainfarm is None:
                cai = RFApps.interpola_xyt(ca, nx*xscale, ny*xscale, nt*tscale)
            else:
                cai = np.reshape(ca[celle3_rainfarm], (nx*xscale, ny*xscale, nt*tscale),
                                 order='F')
            x = cai*g
            
        # Info end
        printMessage( ' ------> Run RF model ... OK')
        # Return variable(s)
        return x, f
    #--------------------------------------------------------------------------------
    
#--------------------------------------------------------------------------------


