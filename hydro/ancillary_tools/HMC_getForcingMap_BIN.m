%--------------------------------------------------------------------------
% Funzione per l'estrazione dei valori delle mappe di input di Continuum
% Versione 0.0.1 (20151003) format=int32 iScaleFactor= 10
%--------------------------------------------------------------------------

function [a2dDataMap] = HMC_getForcingMap_BIN(sFileName, a2dDataRef, iScaleFactor, sFileFormat)

oFid =fopen(sFileName,'r');
oData = fread(oFid,'int32');
fclose(oFid);

a2dDataMap = double(reshape(oData,size(a2dDataRef,1),size(a2dDataRef,2)));
a2dDataMap = a2dDataMap./iScaleFactor; 


%gunzip([sPathFile,fileName,'.gz'])

%delete([sPathFile,fileName]);



