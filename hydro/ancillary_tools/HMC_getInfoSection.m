%--------------------------------------------------------------------------
% Funzione per l'estrazione dei valori del file info section di HMC
% Versione 0.0.1 (20160118)
%--------------------------------------------------------------------------

function [a2oInfoTable] = HMC_getInfoSection(sFileName)

oInfoTable = importdata(sFileName);

a2dInfoTable = oInfoTable.data;
a1oInfoTable = oInfoTable.textdata;

iSecN = size(a1oInfoTable,1);

a2oInfoTable = cell(iSecN, 7);
for iS = 1:iSecN
    
    a1oInfoSection = a1oInfoTable(iS,:);
    %sInfoSection = strsplit(sInfoSection, ' ');
    a1oInfoSection = a1oInfoSection(~cellfun('isempty',a1oInfoSection));

    a2oInfoTable(iS,1) = {num2str(iS)};
    try
        oInfoSection = a1oInfoSection(1,1);
        oInfoSection = oInfoSection(~cellfun('isempty',oInfoSection));
        a2oInfoTable(iS,4) = oInfoSection;
    catch
        a2oInfoTable(iS,4) = {NaN};
    end
    
    try
        oInfoSection = a1oInfoSection(1,2);
        oInfoSection = oInfoSection(~cellfun('isempty',oInfoSection));
        a2oInfoTable(iS,5) = oInfoSection;
    catch
        a2oInfoTable(iS,5) = {NaN};
    end
    
    try
        oInfoSection = a1oInfoSection(1,3);
        oInfoSection = oInfoSection(~cellfun('isempty',oInfoSection));
        a2oInfoTable(iS,2) = oInfoSection;
    catch
        a2oInfoTable(iS,2) = {NaN};
    end
    
    try
        oInfoSection = a1oInfoSection(1,4);
        oInfoSection = oInfoSection(~cellfun('isempty',oInfoSection));
        a2oInfoTable(iS,3) = oInfoSection;
    catch
        a2oInfoTable(iS,3) = {NaN};
    end
    
    try
        a2oInfoTable(iS,6) = {num2str(a2dInfoTable(iS,1))};
    catch
        a2oInfoTable(iS,6) = {NaN};
    end
    
    try
        a2oInfoTable(iS,7) = {num2str(a2dInfoTable(iS,2))};
    catch
        a2oInfoTable(iS,7) = {NaN};
    end
    
end
