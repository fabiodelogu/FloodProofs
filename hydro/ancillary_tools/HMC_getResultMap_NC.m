%--------------------------------------------------------------------------
% Funzione per l'estrazione dei valori delle mappe dei risultati di Continuum
% Versione 0.0.1 (20160128)
%--------------------------------------------------------------------------

function [a2dDataMap, a2dDataGeoX, a2dDataGeoY] = HMC_getResultMap_NC(sFileName, sVarName)

try
    a2dDataMap = flipud(transpose(double(ncread(sFileName,sVarName))));
catch
    a2dDataMap = [];
end

try
    a2dDataGeoX = flipud(transpose(double(ncread(sFileName,'LAT'))));
catch
    a2dDataGeoX = flipud(transpose(double(ncread(sFileName,'longitude'))));
end

try
    a2dDataGeoY = flipud(transpose(double(ncread(sFileName,'LON'))));
catch
    a2dDataGeoX = flipud(transpose(double(ncread(sFileName,'latitude'))));
end