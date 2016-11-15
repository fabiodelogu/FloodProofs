%--------------------------------------------------------------------------
% Funzione per l'estrazione dei valori del file info section di HMC
% Versione 0.0.1 (20160118)
%--------------------------------------------------------------------------

function [a1oTS_Header, a1dTS_OBS, a2dTS_MODEL] = HMC_getTimeSeries(sFileName, iFileVersion, varargin)

% Only want 3 optional inputs at most
iVarArgsN = length(varargin);
if iVarArgsN > 4
    error('HMC_getTimeSeries:TooManyInputs', 'requires at most 3 optional inputs');
end
% Set defaults for optional inputs
a1oOptArgs = {1 '' '' ''};

% now put these defaults into the valuesToUse cell array, 
% and overwrite the ones specified in varargin.
a1oOptArgs(1:iVarArgsN) = varargin;
% Place optional args in memorable variable names
[sTimeRef, iSectionID, sBasinName, sSectionName] = a1oOptArgs{:};

if ~isempty(sTimeRef)
    sYearRef = sTimeRef(1:4); sMonthRef = sTimeRef(5:6); sDayRef = sTimeRef(7:8);
    sHourRef = sTimeRef(9:10); sMinsRef = sTimeRef(11:12);
end
if (strfind(sFileName, '$BASIN'))
    if (~isempty(sBasinName))
        sFileName = strrep(sFileName, '$BASIN', sBasinName);
    end
end
if (strfind(sFileName, '$SECTION'))
    if (~isempty(sSectionName))
        sFileName = strrep(sFileName, '$SECTION', sSectionName);
    end
end
if (strfind(sFileName, '$yyyy'))
    if (~isempty(sTimeRef))
        sFileName = strrep(sFileName, '$yyyy', sYearRef);
    end
end
if (strfind(sFileName, '$mm'))
    if (~isempty(sTimeRef))
        sFileName = strrep(sFileName, '$mm', sMonthRef);
    end
end
if (strfind(sFileName, '$dd'))
    if (~isempty(sTimeRef))
        sFileName = strrep(sFileName, '$dd', sDayRef);
    end
end
if (strfind(sFileName, '$HH'))
    if (~isempty(sTimeRef))
        sFileName = strrep(sFileName, '$HH', sHourRef);
    end% Get TimeSeries for Calibration Mode
end
if (strfind(sFileName, '$MM'))
    if (~isempty(sTimeRef))
        sFileName = strrep(sFileName, '$MM', sMinsRef);
    end
end

if iFileVersion == 2
    
    % Get file data
    oFileTable = importdata(sFileName);
    oFileHeader = oFileTable.textdata;
    oFileData = oFileTable.data;
    
    % Parse file data
    a1dTS_OBS = oFileData(1,:)'; a1dTS_OBS(find(a1dTS_OBS <= -9990)) = NaN;
    a2dTS_MODEL = oFileData(2:end,:)'; a2dTS_MODEL(find(a2dTS_MODEL <= -9990)) = NaN;
    
    iTS_Len = length(a1dTS_OBS) - 1;
    
    % Parse file header
    a1oTS_Header = cell(6,1);
    [a1oFileHeader] = strsplit(char(oFileHeader(1,1)), '=');
    a1oTS_Header(1,1) = {strtrim(char(a1oFileHeader(2)))}; 
    [a1oFileHeader] = strsplit(char(oFileHeader(2,1)), '=');
    a1oTS_Header(2,1) = {strtrim(char(a1oFileHeader(2)))};
    [a1oFileHeader] = strsplit(char(oFileHeader(3,1)), '=');
    a1oTS_Header(3,1) = {strtrim(char(a1oFileHeader(2)))}; 
    [a1oFileHeader] = strsplit(char(oFileHeader(4,1)), '=');
    a1oTS_Header(4,1) = {str2num(strtrim(char(a1oFileHeader(2))))*60};
    [a1oFileHeader] = strsplit(char(oFileHeader(5,1)), '=');
    a1oTS_Header(5,1) = {str2num(strtrim(char(a1oFileHeader(2))))};
    
    a1oTS_Header(6,1) = {iTS_Len}; % add metadata

elseif iFileVersion == 1
    
    % Get file data
    oFileTable = importdata(sFileName);
    
    % Parse file header
    a1oTS_Header = cell(5,1);
    
    % Parse file data
    a2dTS_MODEL = oFileTable(:,iSectionID+1);
    a1dTS_OBS = cell(size(a2dTS_MODEL,1),1);
     
end


















