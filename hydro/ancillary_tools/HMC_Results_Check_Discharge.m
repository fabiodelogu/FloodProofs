%--------------------------------------------------------------------------
% Clear workspace
clear all
close all
clc
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Event Def(s)
sEventName = 'event_2013_11'; 
sTimeNow_R_OBS = '201312010000'; % RUN OBS
sTimeNow_R_NWP = '201311110600'; % RUN NWP
sTimeNow_R_RF = '201311110600'; % RUN RF

%sEventName = 'event_2011_03'; 
%sTimeNow_R = '201103152300';

% Time axis definition
iTimeStep = 3600; iTimeTickThr = 50;
% Result threshold
dTS_Thr = 2500;
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Filename(s)
sFileName_Info_Sec = 'marche.info_section.txt';
sFileName_Hydro_R_OBS = 'hydrograph_$BASIN_$SECTION_$yyyy$mm$dd$HH$MM.txt';
sFileName_Hydro_R_NWP = 'hydrograph_$BASIN_$SECTION_$yyyy$mm$dd$HH$MM.txt';
sFileName_Hydro_R_RF = 'hydrograph_$BASIN_$SECTION_$yyyy$mm$dd$HH$MM.txt';

% Pathname(s)
sPathName_Info_Sec = '/home/fabio/Desktop/Project_RegioneMarche/ancillary/data_static/';
sPathName_Hydro_R_OBS = 'x/home/fabio/Desktop/Project_RegioneMarche/ancillary/data_run/event_2013_11/results/2013/12/01/00/timeseries/section_q/';

sPathName_Hydro_R_NWP = '/home/fabio/Desktop/Project_RegioneMarche/ancillary/data_run/event_2013_11/results/2013/11/11/06/timeseries_NWP/section_q/';
sPathName_Hydro_R_RF = '/home/fabio/Desktop/Project_RegioneMarche/ancillary/data_run/event_2013_11/results/$yyyy/$mm/$dd/$HH/timeseries_RF/section_q/';

sPathName_Ref = '/home/fabio/Documents/Work/Programmazione/Eclipse_Kepler/development/Project_RegioneMarche/ancillary/data_ref/';
sPathName_Plot = '/home/fabio/Desktop/Project_RegioneMarche/ancillary/plot/';

sPathName_Script = pwd;
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Get info section file
cd(sPathName_Script)
[a2oTable_Info_Sec] = HMC_getInfoSection([sPathName_Info_Sec,sFileName_Info_Sec]);
iSecN = size(a2oTable_Info_Sec,1);
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Cycle(s) on section(s)
for iS = 1 : iSecN
    
    %--------------------------------------------------------------------------
    % Get section information
    sBasinName = char(a2oTable_Info_Sec(iS,2)); sSecName = char(a2oTable_Info_Sec(iS,3));
    % Info start
    disp(['SecID: ',num2str(iS),' BasinName: ',sBasinName,' SecName: ',sSecName,' ... ']);
    %--------------------------------------------------------------------------
    
    %--------------------------------------------------------------------------
    % Get TimeSeries (RUN ON OBSERVED DATA)
    try
        % Get data
        cd(sPathName_Script)
        [a1oTS_Header_R_OBS, ...
            a1dTS_RS_R_OBS, a2dTS_MODEL_R_OBS] = HMC_getTimeSeries([sPathName_Hydro_R_OBS, sFileName_Hydro_R_OBS], 2, sTimeNow_R_OBS, ...
            iS, sBasinName, sSecName);
        % Get time
        iTimeLen_R_OBS = cell2mat(a1oTS_Header_R_OBS(6,1));
        sTimeFrom_R_OBS = char(a1oTS_Header_R_OBS(3,1)); dTimeFrom_R_OBS = datenum(sTimeFrom_R_OBS,'yyyymmddHHMM');
        dTimeTo_R_OBS = addtodate(dTimeFrom_R_OBS, iTimeLen_R_OBS, 'hour'); sTimeTo_R_OBS = datestr(dTimeTo_R_OBS, 'yyyymmddHHMM');
        cd(sPathName_Script)
        [a1oTime_R_OBS, a1oTimeLabel_R_OBS, a1iTimeTick_R_OBS] = HMC_getTimeRef(sTimeFrom_R_OBS,sTimeTo_R_OBS, ...
            iTimeStep, iTimeTickThr, sPathName_Ref);
        % Exit code
        iR_OBS = 1;
    catch
        % Exit code
        iR_OBS = 0;
    end
    
    % Get TimeSeries (RUN ON OBSERVED + NWP DATA)
    try
        
        % Get data
        cd(sPathName_Script)
        [a1oTS_Header_R_NWP, ...      
            a1dTS_RS_NWP, a2dTS_MODEL_R_NWP] = HMC_getTimeSeries([sPathName_Hydro_R_NWP, sFileName_Hydro_R_NWP], 2, sTimeNow_R_NWP, ...
            iS, sBasinName, sSecName);
        % Get time
        iTimeLen_R_NWP = cell2mat(a1oTS_Header_R_NWP(6,1));
        sTimeFrom_R_NWP = char(a1oTS_Header_R_NWP(3,1)); dTimeFrom_R_NWP = datenum(sTimeFrom_R_NWP,'yyyymmddHHMM');
        dTimeTo_R_NWP = addtodate(dTimeFrom_R_NWP, iTimeLen_R_NWP, 'hour'); sTimeTo_R_NWP = datestr(dTimeTo_R_NWP, 'yyyymmddHHMM');
        cd(sPathName_Script)
        [a1oTime_R_NWP, a1oTimeLabel_R_NWP, a1iTimeTick_R_NWP] = HMC_getTimeRef(sTimeFrom_R_NWP,sTimeTo_R_NWP, ...
            iTimeStep, iTimeTickThr, sPathName_Ref);
        % Exit code
        iR_NWP = 1;
    catch
        % Exit code
        iR_NWP = 0;
    end
    
    % Get TimeSeries (RUN ON OBSERVED + RF DATA)
    try
         % Get data
        cd(sPathName_Script)
        [a1oTS_Header_R_RF, ...
            a1dTS_RS_R_RF, a2dTS_MODEL_R_RF] = HMC_getTimeSeries([sPathName_Hydro_R_RF, sFileName_Hydro_R_RF], 2, sTimeNow_R_RF, ...
            iS, sBasinName, sSecName);
        % Get time
        iTimeLen_R_RF = cell2mat(a1oTS_Header_R_RF(6,1));
        sTimeFrom_R_RF = char(a1oTS_Header_R_RF(3,1)); dTimeFrom_R_RF = datenum(sTimeFrom_R_RF,'yyyymmddHHMM');
        dTimeTo_R_RF = addtodate(dTimeFrom_R_RF, iTimeLen_R_RF, 'hour'); sTimeTo_R_RF = datestr(dTimeTo_R_RF, 'yyyymmddHHMM');
        [a1oTime_R_RF, a1oTimeLabel_R_RF, a1iTimeTick_R_RF] = HMC_getTimeRef(sTimeFrom_R_RF,sTimeTo_R_RF, ...
            iTimeStep, iTimeTickThr, sPathName_Ref);
        % Exit code
        iR_RF = 1;
    catch
        % Exit code
        iR_RF = 0;
    end
    %--------------------------------------------------------------------------
    
    %--------------------------------------------------------------------------
    % Check case
    if (iR_OBS == 1 && iR_NWP == 1 && iR_RF == 1) 
    
        %--------------------------------------------------------------------------
        % Find common time steps period 
        dTimeFrom_R_OBS = datenum(char(a1oTime_R_OBS(1,1)),'yyyymmddHHMM');
        dTimeFrom_R_NWP = datenum(char(a1oTime_R_NWP(1,1)),'yyyymmddHHMM');
        dTimeFrom_R_RF = datenum(char(a1oTime_R_RF(1,1)),'yyyymmddHHMM');

        dTimeTo_R_OBS = datenum(char(a1oTime_R_OBS(end,1)),'yyyymmddHHMM');
        dTimeTo_R_NWP = datenum(char(a1oTime_R_NWP(end,1)),'yyyymmddHHMM');
        dTimeTo_R_RF = datenum(char(a1oTime_R_RF(end,1)),'yyyymmddHHMM');

        [dTimeFrom_R_Ref iIndexFrom_R_Ref] = nanmax([dTimeFrom_R_OBS, dTimeFrom_R_NWP, dTimeFrom_R_RF]);
        [dTimeTo_R_Ref iIndexTo_R_Ref] = nanmin([dTimeTo_R_OBS, dTimeTo_R_NWP, dTimeTo_R_RF]);

        sTimeFrom_R_Ref = datestr(dTimeFrom_R_Ref, 'yyyymmddHHMM');
        sTimeTo_R_Ref = datestr(dTimeTo_R_Ref, 'yyyymmddHHMM');

        % Find OBS index steps 
        iIndexFrom_R_OBS = find(strcmp(a1oTime_R_OBS, sTimeFrom_R_Ref));
        iIndexTo_R_OBS = find(strcmp(a1oTime_R_OBS, sTimeTo_R_Ref));

        % Find NWP index steps
        iIndexFrom_R_NWP = find(strcmp(a1oTime_R_NWP, sTimeFrom_R_Ref));
        iIndexTo_R_NWP = find(strcmp(a1oTime_R_NWP, sTimeTo_R_Ref));

        % Find RF index steps
        iIndexFrom_R_RF = find(strcmp(a1oTime_R_RF, sTimeFrom_R_Ref));
        iIndexTo_R_RF = find(strcmp(a1oTime_R_RF, sTimeTo_R_Ref));
        %--------------------------------------------------------------------------

        %--------------------------------------------------------------------------
        % Select data and time period
        a1oTime_R_OBS_SEL = a1oTime_R_OBS(iIndexFrom_R_OBS : iIndexTo_R_OBS, 1);
        a1dTS_RS_R_OBS_SEL = a1dTS_RS_R_OBS(iIndexFrom_R_OBS : iIndexTo_R_OBS, 1);
        a2dTS_MODEL_R_OBS_SEL = a2dTS_MODEL_R_OBS(iIndexFrom_R_OBS : iIndexTo_R_OBS, :);

        a1oTime_R_NWP_SEL = a1oTime_R_NWP(iIndexFrom_R_NWP : iIndexTo_R_NWP, 1);
        a1dTS_RS_R_NWP_SEL = a1dTS_RS_NWP(iIndexFrom_R_NWP : iIndexTo_R_NWP, 1);
        a2dTS_MODEL_R_NWP_SEL = a2dTS_MODEL_R_NWP(iIndexFrom_R_NWP : iIndexTo_R_NWP, :);

        a1oTime_R_RF_SEL = a1oTime_R_RF(iIndexFrom_R_RF : iIndexTo_R_RF, 1);
        a1dTS_RS_R_RF_SEL = a1dTS_RS_R_RF(iIndexFrom_R_RF : iIndexTo_R_RF, 1);
        a2dTS_MODEL_R_RF_SEL = a2dTS_MODEL_R_RF(iIndexFrom_R_RF : iIndexTo_R_RF, :);
        %--------------------------------------------------------------------------
        
        %--------------------------------------------------------------------------
        % Result threshold
        a2dTS_MODEL_R_OBS_SEL(a2dTS_MODEL_R_OBS_SEL>dTS_Thr) = NaN;
        a2dTS_MODEL_R_NWP_SEL(a2dTS_MODEL_R_NWP_SEL>dTS_Thr) = NaN;
        a2dTS_MODEL_R_RF_SEL(a2dTS_MODEL_R_RF_SEL>dTS_Thr) = NaN;
        %--------------------------------------------------------------------------
        
    elseif (iR_OBS == 0 && iR_NWP == 1 && iR_RF == 1) 
        
        %--------------------------------------------------------------------------
        % Find common time steps period 
        dTimeFrom_R_NWP = datenum(char(a1oTime_R_NWP(1,1)),'yyyymmddHHMM');
        dTimeFrom_R_RF = datenum(char(a1oTime_R_RF(1,1)),'yyyymmddHHMM');

        dTimeTo_R_NWP = datenum(char(a1oTime_R_NWP(end,1)),'yyyymmddHHMM');
        dTimeTo_R_RF = datenum(char(a1oTime_R_RF(end,1)),'yyyymmddHHMM');

        [dTimeFrom_R_Ref iIndexFrom_R_Ref] = nanmax([dTimeFrom_R_NWP, dTimeFrom_R_RF]);
        [dTimeTo_R_Ref iIndexTo_R_Ref] = nanmin([dTimeTo_R_NWP, dTimeTo_R_RF]);

        sTimeFrom_R_Ref = datestr(dTimeFrom_R_Ref, 'yyyymmddHHMM');
        sTimeTo_R_Ref = datestr(dTimeTo_R_Ref, 'yyyymmddHHMM');

        % Find NWP index steps
        iIndexFrom_R_NWP = find(strcmp(a1oTime_R_NWP, sTimeFrom_R_Ref));
        iIndexTo_R_NWP = find(strcmp(a1oTime_R_NWP, sTimeTo_R_Ref));

        % Find RF index steps
        iIndexFrom_R_RF = find(strcmp(a1oTime_R_RF, sTimeFrom_R_Ref));
        iIndexTo_R_RF = find(strcmp(a1oTime_R_RF, sTimeTo_R_Ref));
        %--------------------------------------------------------------------------

        %--------------------------------------------------------------------------
        % Select data and time period
        a1oTime_R_NWP_SEL = a1oTime_R_NWP(iIndexFrom_R_NWP : iIndexTo_R_NWP, 1);
        a1dTS_RS_R_NWP_SEL = a1dTS_RS_NWP(iIndexFrom_R_NWP : iIndexTo_R_NWP, 1);
        a2dTS_MODEL_R_NWP_SEL = a2dTS_MODEL_R_NWP(iIndexFrom_R_NWP : iIndexTo_R_NWP, :);

        a1oTime_R_RF_SEL = a1oTime_R_RF(iIndexFrom_R_RF : iIndexTo_R_RF, 1);
        a1dTS_RS_R_RF_SEL = a1dTS_RS_R_RF(iIndexFrom_R_RF : iIndexTo_R_RF, 1);
        a2dTS_MODEL_R_RF_SEL = a2dTS_MODEL_R_RF(iIndexFrom_R_RF : iIndexTo_R_RF, :);
        %--------------------------------------------------------------------------
        
        %--------------------------------------------------------------------------
        % Result threshold
        a2dTS_MODEL_R_NWP_SEL(a2dTS_MODEL_R_NWP_SEL>dTS_Thr) = NaN;
        a2dTS_MODEL_R_RF_SEL(a2dTS_MODEL_R_RF_SEL>dTS_Thr) = NaN;
        %--------------------------------------------------------------------------

    elseif (iR_OBS == 1 && iR_NWP == 0 && iR_RF == 0)
        
        %--------------------------------------------------------------------------
        % Only run obs available
        a1oTime_R_OBS_SEL = a1oTime_R_OBS;
        a1dTS_RS_R_OBS_SEL = a1dTS_RS_R_OBS;
        a2dTS_MODEL_R_OBS_SEL = a2dTS_MODEL_R_OBS;
        %--------------------------------------------------------------------------
        
        %--------------------------------------------------------------------------
        % Result(s) threshold
        a2dTS_MODEL_R_OBS_SEL(a2dTS_MODEL_R_OBS_SEL>dTS_Thr) = NaN;
        %--------------------------------------------------------------------------
        
    end
    %--------------------------------------------------------------------------
    
    %--------------------------------------------------------------------------
    % Plot section discharge
    sEventName4Graph = strrep(sEventName,'_', ' ');
    
    oFig = figure(iS); hold on

    
    if (iR_OBS == 1 && iR_NWP == 1 && iR_RF == 1) 
        
        iPlotH1 = plot(a1dTS_RS_R_OBS_SEL,'*k'); 
        iPlotH2 = plot(a2dTS_MODEL_R_OBS_SEL, '-or', 'LineWidth', 2);
        iPlotH3 = plot(a2dTS_MODEL_R_RF_SEL, 'b');
        iPlotH4 = plot(a2dTS_MODEL_R_NWP_SEL, '-xg','LineWidth', 4);
        
        set(gca,'XLim',[min(a1iTimeTick_R_NWP) max(a1iTimeTick_R_NWP)])
        set(gca,'XTick', a1iTimeTick_R_NWP)
        set(gca,'XTickLabel', a1oTimeLabel_R_NWP, 'fontsize',10, 'fontweight', 'bold')
        
        legend([iPlotH1 iPlotH2 iPlotH4 iPlotH3(1)],{'Observed','HMC-OBS','HMC-NWP', 'HMC-RF'});
    
    elseif (iR_OBS == 0 && iR_NWP == 1 && iR_RF == 1) 
        
        iPlotH1 = plot(a1dTS_RS_R_NWP_SEL,'*k'); 
        iPlotH3 = plot(a2dTS_MODEL_R_RF_SEL, 'b');
        iPlotH4 = plot(a2dTS_MODEL_R_NWP_SEL, '-xg','LineWidth', 4);
        
        set(gca,'XLim',[min(a1iTimeTick_R_NWP) max(a1iTimeTick_R_NWP)])
        set(gca,'XTick', a1iTimeTick_R_NWP)
        set(gca,'XTickLabel', a1oTimeLabel_R_NWP, 'fontsize',10, 'fontweight', 'bold')
        
        legend([iPlotH1 iPlotH4 iPlotH3(1)],{'Observed','HMC-NWP', 'HMC-RF'});
        
    elseif (iR_OBS == 1 && iR_NWP == 0 && iR_RF == 0) 
        
        iPlotH1 = plot(a1dTS_RS_R_OBS_SEL,'*k'); 
        iPlotH2 = plot(a2dTS_MODEL_R_OBS_SEL, '-or', 'LineWidth', 2);
        
        set(gca,'XTick', a1iTimeTick_R_OBS)
        set(gca,'XTickLabel', a1oTimeLabel_R_OBS, 'fontsize',10, 'fontweight', 'bold')

        legend([iPlotH1 iPlotH2],{'Observed','HMC-OBS'});
    end
    
    grid on
    
    xlabel('Time [hour]','fontsize',12, 'fontweight', 'bold')
    ylabel('Discharge [m^3/s]','fontsize',12, 'fontweight', 'bold')
    
    title(['Event: ',sEventName4Graph,' - BasinName: ',sBasinName,' - SectionName: ', sSecName], ...
        'fontsize', 14, 'fontweight', 'bold');
    
    % Save plot
    saveas(oFig,[sPathName_Plot, 'Discharge_OBSvsMODEL_',sEventName,'_',sBasinName,'_',sSecName,'.jpg'],'jpg')
    saveas(oFig,[sPathName_Plot, 'Discharge_OBSvsMODEL_',sEventName,'_',sBasinName,'_',sSecName,'.fig'],'fig')
    
    % Close plot
    close(iS)
    %--------------------------------------------------------------------------
    
    %--------------------------------------------------------------------------
    % Info end
    disp(['SecID: ',num2str(iS),' BasinName: ',sBasinName,' SecName: ',sSecName,' ... OK']);
    %--------------------------------------------------------------------------
    
    
end
%--------------------------------------------------------------------------



