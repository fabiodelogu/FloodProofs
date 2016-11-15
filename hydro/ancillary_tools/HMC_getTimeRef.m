%--------------------------------------------------------------------------
% Funzione per la definizione dei vettori del tempo
% Versione 0.0.1 (20131002)
%--------------------------------------------------------------------------

function [a1oTime, a1oTimeLabel, a1iTimeTick] = HMC_getTimeRef(sDateFrom,sDateTo, ...
    iStepBase, iTimeTickThr, ...
    sPathData)

%--------------------------------------------------------------------------
% CALCOLO DELLE INFORMAZIONI SUL TIME

% Definizione del numero degli steps da considerare
iStepN = (3600/iStepBase)*24;

% Nome del file della variabile tempo
sDateFormat = 'yyyymmddHHMM';
sFileNameDate = ['a1oTime_',sDateFrom,'_',sDateTo,'.mat'];

% Creazione del vettore del tempo
cd(sPathData)
bFileStatus = exist(sFileNameDate,'file');
if(bFileStatus == 0)
    
    a1iDate = datenum({sDateFrom;sDateTo},sDateFormat);
    a2iDate = datevec(a1iDate(1):1/iStepN:a1iDate(2));
    
    iTimeLength = size(a2iDate,1);
    for iS = 1 : iTimeLength
        a1iDate = a2iDate(iS,:);
        sDate = [num2str(a1iDate(1,1),'%04.0f'),num2str(a1iDate(1,2),'%02.0f'),num2str(a1iDate(1,3),'%02.0f'), ....
            num2str(a1iDate(1,4),'%02.0f'),num2str(a1iDate(1,5),'%02.0f')];
        a1oTime(iS,1) = {sDate};
    end
    save(sFileNameDate,'a1oTime');
else
    load([sPathData,sFileNameDate]);
end

% Creazione dei tick della variabile tempo
iTimeLength = size(a1oTime,1);
a1iTimeIndex = [1:1:iTimeLength];
iTimeTickStep = iTimeLength; iDiv = 1;
while(iTimeTickStep > iTimeTickThr)
    iTimeTickStep = ceil(iTimeLength/iDiv);
    iDiv = iDiv + 1;
end
a1iTimeTick = unique([1:iTimeTickStep:iTimeLength]);
a1iTimeTick = unique([a1iTimeTick iTimeLength]);

% Creazione dei label della variabile tempo
a1oTimeLabel = a1oTime(a1iTimeTick,1);
iTimeDim = size(a1oTimeLabel,1);

for iTL = 1 : iTimeDim
    sTimeLabel = char(a1oTimeLabel(iTL,1));
    sTimeLabel = sTimeLabel(1,1:10);
    a1oTimeLabel(iTL,1) = {sTimeLabel};
end

a1iTimeTick = a1iTimeTick';
%--------------------------------------------------------------------------


