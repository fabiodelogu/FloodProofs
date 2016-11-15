%--------------------------------------------------------------------------
% Clear workspace
clear all
close all
clc
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Filename(s)
sFileName_Info_Dam = 'marche.info_dam.txt';
sFileName_Info_Sec = 'marche.info_section.txt';
sFileName_Land_Choice = 'marche.choice.txt';
sFileName_Data_Sec = 'marche.data_section.txt';
%sFileName_Land_Choice = 'marche.choiceV1.txt';

% Pathname(s)
sPathName_Info_Dam = '/home/fabio/Desktop/Project_RegioneMarche/ancillary/data_static/';
sPathName_Info_Sec = '/home/fabio/Desktop/Project_RegioneMarche/ancillary/data_static/';
sPathName_Data_Sec = '/home/fabio/Desktop/Project_RegioneMarche/ancillary/data_static/';
sPathName_Land_Choice = '/home/fabio/Desktop/Project_RegioneMarche/ancillary/data_static/';
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Get info section file
[a2oTable_Info_Sec] = HMC_getInfoSection([sPathName_Info_Sec,sFileName_Info_Sec]);
iSecN = size(a2oTable_Info_Sec,1);

% Get info dam file
[a2oTable_Info_DamMain, a2oTable_Info_DamSub] = HMC_getInfoDam([sPathName_Info_Dam,sFileName_Info_Dam]);
iDamMainN = size(a2oTable_Info_DamMain,1);
iDamSubN = size(a2oTable_Info_DamSub,1);

% Get static data land
[a2dChoiceMap, a2dChoiceGeoX, a2dChoiceGeoY] = HMC_getRasterMap([sPathName_Land_Choice, sFileName_Land_Choice]);
a1iChoiceDims = size(a2dChoiceMap);
a1iChoiceIndex = find(isnan(a2dChoiceMap(:)));
%--------------------------------------------------------------------------

keyboard

%--------------------------------------------------------------------------
% Open file to save data sections
oFileID = fopen([sPathName_Data_Sec, sFileName_Data_Sec],'w');
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Plotting Sections and dams on choice map
figure(1)
imagesc(a2dChoiceMap)
hold on

% Cycle(s) on section(s)
for iS = 1 : iSecN
    
    % ID, Y and X grid
    iD = str2num(cell2mat(a2oTable_Info_Sec(iS, 1)));
    iY = str2num(cell2mat(a2oTable_Info_Sec(iS, 4)));
    iX = str2num(cell2mat(a2oTable_Info_Sec(iS, 5)));
    
    sName1 = char(a2oTable_Info_Sec(iS,2));
    sName2 = char(a2oTable_Info_Sec(iS,3));
    
    % Get choice pixel
    iChoice = a2dChoiceMap(iY,iX);
    dGeoX = a2dChoiceGeoX(iY,iX);
    dGeoY = a2dChoiceGeoY(iY,iX);
    
    % Info
    disp(['ID:',num2str(iD),' Basin: ',sName1,' Section: ', sName2,' ---> Choice: ', num2str(iChoice)])
    % Plot point 
    %text(iX,iY,['SEC_ID=',num2str(iD),' SEC_NAME=',sName1,sName2,' (',num2str(iY),',',num2str(iX),')'], ...
    %    'VerticalAlignment','bottom','fontsize',8,'fontweight', 'bold','BackgroundColor',[.7 .9 .7])
    
    text(iX,iY,['SECID=',num2str(iD),' (',num2str(iY),',',num2str(iX),')'], ...
        'VerticalAlignment','bottom','fontsize',12,'fontweight', 'bold','BackgroundColor',[.7 .9 .7])
    if iChoice == 1
        plot(iX, iY, 'ow', 'markerfacecolor', [0 0.5 0], 'MarkerSize',10)
    else 
        plot(iX, iY, 'ow', 'markerfacecolor', [0 1 0], 'MarkerSize',20)
    end
    
    fprintf(oFileID,'%3i',iS); 
    
    fprintf(oFileID,'%20s',sName1);
    fprintf(oFileID,'%20s',sName2);
    fprintf(oFileID,'%13.6f',dGeoX); fprintf(oFileID,'%13.6f',dGeoY); 
    fprintf(oFileID,'%1s \n', '');
    
end
fclose(oFileID);

% Cycle(s) on DamMain(s)
for iS = 1 : iDamMainN
    
    % ID, Y and X grid
    iD = str2num(cell2mat(a2oTable_Info_DamMain(iS, 1)));
    iY = str2num(cell2mat(a2oTable_Info_DamMain(iS, 3)));
    iX = str2num(cell2mat(a2oTable_Info_DamMain(iS, 4)));
    
    sName = a2oTable_Info_DamMain(iS,2);
    
    % Get choice pixel
    iChoice = a2dChoiceMap(iY,iX);
    
    % Info
    disp(['ID:',num2str(iD),' Dam: ',a2oTable_Info_DamMain(iS,2),' ---> Choice: ', num2str(iChoice)])
    % Plot point
    %text(iX,iY,['DAM_ID=',num2str(iD),' DAM_NAME=',sName,' (',num2str(iY),',',num2str(iX),')'], ...
    %    'VerticalAlignment','bottom','fontsize',8, 'fontweight', 'bold','BackgroundColor',[.7 .9 .7])
    
    text(iX,iY,['DAMID=',num2str(iD),' (',num2str(iY),',',num2str(iX),')'], ...
        'VerticalAlignment','bottom','fontsize',12,'fontweight', 'bold','BackgroundColor',[.7 .9 .7])
    if iChoice == 1
        plot(iX, iY, 'ow', 'markerfacecolor', [0.5 0 0], 'MarkerSize',10)
    else 
        plot(iX, iY, 'ow', 'markerfacecolor', [1 0 0], 'MarkerSize',10)
    end
end

% Cycle(s) on DamSub(s)
for iS = 1 : iDamSubN
    
    % ID, Y and X grid
    iD = str2num(cell2mat(a2oTable_Info_DamSub(iS, 1)));
    iY = str2num(cell2mat(a2oTable_Info_DamSub(iS, 3)));
    iX = str2num(cell2mat(a2oTable_Info_DamSub(iS, 4)));
    
    sName = a2oTable_Info_DamSub(iS,2);
    
    % Get choice pixel
    iChoice = a2dChoiceMap(iY,iX);
    
    % Info
    disp(['ID:',num2str(iD),' DamSub: ',a2oTable_Info_DamSub(iS,2),' ---> Choice: ', num2str(iChoice)])
    % Plot point
    %text(iX,iY,['DWR_ID=',num2str(iD),' DWR_NAME=',sName,' (',num2str(iY),',',num2str(iX),')'], ...
    %    'VerticalAlignment','bottom','fontsize',8, 'fontweight', 'bold','BackgroundColor',[.7 .9 .7])
    
    text(iX,iY,['RELID=',num2str(iD),' (',num2str(iY),',',num2str(iX),')'], ...
        'VerticalAlignment','bottom','fontsize',12,'fontweight', 'bold','BackgroundColor',[.7 .9 .7])
    if iChoice == 1
        plot(iX, iY, 'ow', 'markerfacecolor', [0 0 0.5], 'MarkerSize',10)
    else 
        plot(iX, iY, 'ow', 'markerfacecolor', [0 0 1], 'MarkerSize',20)
    end
    
end
%--------------------------------------------------------------------------

keyboard





