%--------------------------------------------------------------------------
% Funzione per il salvataggio dei valori delle mappe di stato di Continuum
% Versione 0.0.1 (20160409) format=int32 iScaleFactor= 10
%--------------------------------------------------------------------------

function HMC_writeStateMap_BIN(sFileName, oDataRef, iScaleFactor, sFileFormat)

iDataDims = ndims(oDataRef);

if iDataDims == 2
    oFid = fopen(sFileName, 'w');
    oDataRefRaw = oDataRef*iScaleFactor;
    
    fwrite(oFid, oDataRefRaw, sFileFormat);
    fclose(oFid);
end

if iDataDims > 2
    
    oFid = fopen(sFileName, 'w');
    for iD = 1 : iDataDims
        
        oDataRefRaw = oDataRef(:,:,iD)*iScaleFactor;
        fwrite(oFid, oDataRefRaw, sFileFormat);
        
    end
    fclose(oFid);
end




        
        
        