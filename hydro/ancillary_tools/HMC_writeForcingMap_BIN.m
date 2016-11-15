%--------------------------------------------------------------------------
% Funzione per il salvataggio dei valori delle mappe di input di Continuum
% Versione 0.0.1 (20160409) format=int32 iScaleFactor= 10
%--------------------------------------------------------------------------

function HMC_writeForcingMap_BIN(sFileName, a2dDataRef, iScaleFactor, sFileFormat)

oFid = fopen(sFileName, 'w');
a2dDataRef = a2dDataRef*iScaleFactor;

fwrite(oFid, a2dDataRef, sFileFormat);
fclose(oFid);





        
        
        