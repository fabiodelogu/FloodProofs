function HMC_writeForcingMap_NC4MET(sFileName, sTime, ...
                    a2dData, a2dGeoX, a2dGeoY, ...
                    dCellSize, dXLLCorner, dYLLCorner, ...
                    dMissingValue, ...
                    sVarName, sVarLongName, sVarLevel, sVarUnits, ...
                    sVarCodeGrib)

% Defino los NaN como un valor dado (e.g. -9999.99)
a2dData(isnan(a2dData)) = dMissingValue;

[iNGeoY, iNGeoX] = size(a2dData);
%dGeoX_LL = nanmin(nanmin(a2dGeoX)); dGeoY_LL = nanmin(nanmin(a2dGeoY));

% Open file
iNC_ID = netcdf.create(sFileName,'NC_CLOBBER');

% Write global attributes
netcdf.putAtt(iNC_ID,netcdf.getConstant('NC_GLOBAL'),'MET_version','V5.0');
netcdf.putAtt(iNC_ID,netcdf.getConstant('NC_GLOBAL'),'Projection','LatLon');
netcdf.putAtt(iNC_ID,netcdf.getConstant('NC_GLOBAL'),'lat_ll', num2str(dXLLCorner));
netcdf.putAtt(iNC_ID,netcdf.getConstant('NC_GLOBAL'),'lon_ll', num2str(dYLLCorner));
netcdf.putAtt(iNC_ID,netcdf.getConstant('NC_GLOBAL'),'delta_lat',[num2str(dCellSize),' degrees']); %%%%
netcdf.putAtt(iNC_ID,netcdf.getConstant('NC_GLOBAL'),'delta_lon',[num2str(dCellSize),' degrees']); %%%
netcdf.putAtt(iNC_ID,netcdf.getConstant('NC_GLOBAL'),'Nlat',[num2str(iNGeoY),' grid_points']);
netcdf.putAtt(iNC_ID,netcdf.getConstant('NC_GLOBAL'),'Nlon',[num2str(iNGeoX),' grid_points']);

% set dimension(s)
iSNDim = netcdf.defDim(iNC_ID,'lat',iNGeoY);
iWEDim = netcdf.defDim(iNC_ID,'lon',iNGeoX);

netcdf.endDef(iNC_ID);

% Latitude
a2dGeoY = transpose(flipud(a2dGeoY));
netcdf.reDef(iNC_ID);
iGeoY_ID = netcdf.defVar(iNC_ID,'latitude','float',[iWEDim iSNDim]);
netcdf.putAtt(iNC_ID,iGeoY_ID,'long_name','latitude coordinate');
netcdf.putAtt(iNC_ID,iGeoY_ID,'units','degrees_north');
netcdf.putAtt(iNC_ID,iGeoY_ID,'standard_name','latitude');
netcdf.endDef(iNC_ID);
netcdf.putVar(iNC_ID,iGeoY_ID, a2dGeoY);

% Longitude
a2dGeoX = transpose(flipud(a2dGeoX));
netcdf.reDef(iNC_ID);
iGeoX_ID = netcdf.defVar(iNC_ID,'longitude','float',[iWEDim iSNDim]);
netcdf.putAtt(iNC_ID, iGeoX_ID,'long_name','longitude coordinate');
netcdf.putAtt(iNC_ID, iGeoX_ID,'units','degrees_east');
netcdf.putAtt(iNC_ID, iGeoX_ID,'standard_name','longitude');
netcdf.endDef(iNC_ID);
netcdf.putVar(iNC_ID, iGeoX_ID, a2dGeoX);

% Variable:
a2dData = transpose(flipud(a2dData));
netcdf.reDef(iNC_ID);
iVar_ID = netcdf.defVar(iNC_ID,'precip','float',[iWEDim iSNDim]);
netcdf.putAtt(iNC_ID, iVar_ID, 'name', sVarName);
netcdf.putAtt(iNC_ID, iVar_ID,'long_name', sVarLongName);
netcdf.putAtt(iNC_ID, iVar_ID,'level', sVarLevel);
netcdf.putAtt(iNC_ID, iVar_ID,'units', sVarUnits);
netcdf.putAtt(iNC_ID, iVar_ID,'grib_code', sVarCodeGrib);
netcdf.putAtt(iNC_ID, iVar_ID,'_FillValue',single(dMissingValue));
netcdf.putAtt(iNC_ID, iVar_ID,'init_time',sTime);
netcdf.putAtt(iNC_ID, iVar_ID,'init_time_ut',int32(str2double(sTime)));
netcdf.putAtt(iNC_ID, iVar_ID,'valid_time',sTime);
netcdf.putAtt(iNC_ID, iVar_ID,'valid_time_ut',int32(str2double(sTime)));
netcdf.putAtt(iNC_ID, iVar_ID,'accum_time','86400');
netcdf.putAtt(iNC_ID, iVar_ID,'accum_time_sec',int32(86400));
netcdf.putAtt(iNC_ID, iVar_ID,'coordinates','longitude latitude');
netcdf.endDef(iNC_ID);

netcdf.putVar(iNC_ID,iVar_ID, a2dData);
netcdf.close(iNC_ID);










