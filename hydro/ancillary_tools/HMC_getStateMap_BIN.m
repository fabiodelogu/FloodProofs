%--------------------------------------------------------------------------
% Funzione per l'estrazione dei valori delle mappe di stato di Continuum
% Versione 0.0.1 (20151003) format=int32 iScaleFactor= 10
%--------------------------------------------------------------------------

function [oDataMap] = HMC_getStateMap_BIN(sFileName, a2dDataRef, iScaleFactor, sFileFormat)

oFid =fopen(sFileName,'r');
oData = fread(oFid,'int32');
fclose(oFid);

iDataLen = length(oData);
iDataDims = iDataLen/(size(a2dDataRef,1)*size(a2dDataRef,2));

if iDataDims == 1;
    oDataMap = double(reshape(oData,size(a2dDataRef,1),size(a2dDataRef,2)));
    oDataMap = oDataMap./iScaleFactor; 
end

if iDataDims > 1;
    oDataMap = double(reshape(oData,size(a2dDataRef,1),size(a2dDataRef,2),iDataDims));
    oDataMap = oDataMap./iScaleFactor; 
end





