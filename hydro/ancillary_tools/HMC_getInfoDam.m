%--------------------------------------------------------------------------
% Funzione per l'estrazione dei valori del file info dam di HMC
% Versione 0.0.1 (20160118)
%--------------------------------------------------------------------------

function [a2oInfoDamMain, a2oInfoDamSub] = HMC_getInfoDam(sFileName)

a1oInfoTable = importdata(sFileName);
iLineN = size(a1oInfoTable);

a1oInfoData = cell(iLineN,1); iDamMain = 0; iDamDer = 0;
for iL = 1 : iLineN
    
    sText = char(a1oInfoTable(iL));
    bCommentCheck = strncmpi(sText,'####',4);
    
    if bCommentCheck == 0
        
        a1oText = strsplit(sText,'#');
        sDataString = strtrim(char(a1oText(1)));

        if iL == 1
            iDamMain = str2double(sDataString);
        elseif iL == 2
            iDamDer = str2double(sDataString);
        end
        
        
        if isempty(sDataString)
            sDataStringFinal = 'NaN';
        else
            
            sDataStringFinal = sDataString;
            
        end
    else
        sDataStringFinal = '#';
    end
    
    a1oInfoData(iL,1) = {sDataStringFinal};
    
end

iDamMax = nanmax(iDamMain, iDamDer);

bDam = 0; iDam = 0; a2oInfoData = cell(100,iDamMain);
for iL = 1 : iLineN
    
    sInfoData = char(a1oInfoData(iL,1));
    if bDam == 1 && all(char(sInfoData) ~= '#');
        a2oInfoData(iC, iDam) = {sInfoData};
        iC = iC + 1;
    else
        bDam = 0;
    end
    
    if char(sInfoData) == '#'
        bDam = 1; 
        iDam = iDam + 1;
        iC = 1;
    end
end

iLineDamMain = 11; iLineDamDer = 5; a2oDamTotal = cell(iDamMain, 13);
for iD = 1 : iDamMain
    a1oInfoDam = a2oInfoData(:, iD);
    a1oDamSingle = {num2str(iD)};
    for iDL = 1 : iLineDamMain
        a1sInfoDam = strsplit(char(a1oInfoDam(iDL,1)));
        for iF = 1:size(a1sInfoDam,2)
            a1oDamSingle = strcat(a1oDamSingle, {a1sInfoDam(1,iF)});
        end
    end
    a1oDamSingle = a1oDamSingle{1,1};
    a2oDamTotal(iD,:) = a1oDamSingle;
end

iKK = 0;  a2oDamSubTotal = cell(iDamDer, 7);
for iD = 1 : iDamMain
    
    iDamDerN = str2double(char(a2oDamTotal(iD, 5)));
    iLineSlave = iLineDamMain;
    
    for iDD = 1 : iDamDerN
        
        a1oDamSubSingle = {num2str(iD)};
        
        iKK = iKK + 1;
       
        iLineStart = iLineSlave + 1;
        iLineEnd = iLineStart + iLineDamDer - 1;
        
        a1oInfoDamSub = a2oInfoData(iLineStart:iLineEnd,iD);
        
        for iL = 1 : iLineDamDer
            
            a1sInfoDamSub = strsplit(char(a1oInfoDamSub(iL,1)));
            for iF = 1:size(a1sInfoDamSub,2)
                a1oDamSubSingle = strcat(a1oDamSubSingle, {a1sInfoDamSub(1,iF)});
            end
            
        end
        
        a1oDamSubSingle = a1oDamSubSingle{1,1};
        a2oDamSubTotal(iKK,:) = a1oDamSubSingle;

        iLineSlave = iLineEnd;
        
    end
    
end


a2oInfoDamMain = a2oDamTotal; a2oInfoDamSub = a2oDamSubTotal;


































