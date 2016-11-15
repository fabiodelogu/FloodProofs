%--------------------------------------------------------------------------
% Funzione per l'estrazione dei valori delle mappe di input di Continuum
% Versione 0.0.1 (20151003)
%--------------------------------------------------------------------------

function [oDataMapDest, a2dDataGeoX, a2dDataGeoY] = HMC_getStateMap_NC(sFileName, sVarName)

try
    
    oDataMapSource = double(ncread(sFileName,sVarName));
    iDataDims = ndims(oDataMapSource); iDataSize = size(oDataMapSource);
    
    if iDataDims == 2;
        
        oDataMapDest = flipud(transpose(oDataMapSource));
        
    else iDataDims > 2;
        
        oDataMapDest = zeros(iDataSize(2), iDataSize(1), iDataSize(3));
        for iD = 1 : iDataDims
            oDataMapRaw = flipud(transpose(oDataMapSource(:,:,iD)));
            oDataMapDest(:,:,iD) = oDataMapRaw;
        end
        
    end
    
catch
    oDataMapDest = [];
end

try
    a2dDataGeoX = flipud(transpose(double(ncread(sFileName,'Longitude'))));
catch
    a2dDataGeoX = flipud(transpose(double(ncread(sFileName,'longitude'))));
end

try
    a2dDataGeoY = flipud(transpose(double(ncread(sFileName,'Latitude'))));
catch
    a2dDataGeoX = flipud(transpose(double(ncread(sFileName,'latitude'))));
end


