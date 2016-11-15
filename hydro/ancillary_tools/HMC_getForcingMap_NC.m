%--------------------------------------------------------------------------
% Funzione per l'estrazione dei valori delle mappe di input di Continuum
% Versione 0.0.1 (20151003)
%--------------------------------------------------------------------------

function [a2dDataMap, a2dDataGeoX, a2dDataGeoY] = HMC_getForcingMap_NC(sFileName, sVarName)

try
    a2dDataMap = flipud(transpose(double(ncread(sFileName,sVarName))));
catch
    a2dDataMap = [];
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


