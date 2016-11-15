%--------------------------------------------------------------------------
% Funzione per l'estrazione dei valori delle mappe statiche di HMC
% Versione 0.0.1 (20151013)
%--------------------------------------------------------------------------

function [a2dMapData, a2dMapGeoX, a2dMapGeoY, a2dMapGeo] = HMC_getRasterMap(sFileName)


% [a2dDataMap, a2dDataCoord] = arcgridread(sFileName);
% a1iIndexDataMapFinite = find(a2dDataMap>0);
% 
% iDataRows = size(a2dDataMap,1); iDataCols = size(a2dDataMap,2);
% 
% dDataGeoXMin = a2dDataCoord(3,1);
% dDataGeoYMax = a2dDataCoord(3,2);
% dDataGeoXStep = abs(a2dDataCoord(2,1));
% dDataGeoYStep = abs(a2dDataCoord(1,2));
% 
% a2dDataGeoX = zeros(size(a2dDataMap,1), size(a2dDataMap,2));
% a2dDataGeoY = zeros(size(a2dDataMap,1), size(a2dDataMap,2));
% [a2dDataGeoX, a2dDataGeoY] = ...
%     meshgrid(dDataGeoXMin:dDataGeoXStep:dDataGeoXMin+(iDataCols-1)*dDataGeoXStep, ...
%     dDataGeoYMax:-dDataGeoYStep:dDataGeoYMax-(iDataRows-1)*dDataGeoYStep);


% Get geographical information
[a2dMapData,a2dMapGeo] = arcgridread(sFileName);
[iMapRows, iMapCols] = size(a2dMapData);
[a2iMapRows, a2iMapCols] = ndgrid(1:iMapRows, 1:iMapCols);
[a2dMapGeoY, a2dMapGeoX] = pix2latlon(a2dMapGeo, a2iMapRows, a2iMapCols);
dMapGeoXMin = nanmin(nanmin(a2dMapGeoX)); dMapGeoXMax = nanmax(nanmax(a2dMapGeoX));
dMapGeoYMin = nanmin(nanmin(a2dMapGeoY)); dMapGeoYMax = nanmax(nanmax(a2dMapGeoY));









