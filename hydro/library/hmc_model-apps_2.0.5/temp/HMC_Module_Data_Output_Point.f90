!------------------------------------------------------------------------------------------    
! File:   HMC_Module_Data_Output_Point.f90
! Author(s): Fabio Delogu, Francesco Silvestro, Simone Gabellani
!
! Created on May 7, 2015, 4:37 PM
!------------------------------------------------------------------------------------------

!------------------------------------------------------------------------------------------
! Module Header
module HMC_Module_Data_Output_Point
    
    !------------------------------------------------------------------------------------------
    ! External module(s) for all subroutine in this module
    use netcdf
    
    use HMC_Module_Namelist,        only:   oHMC_Namelist
    use HMC_Module_Vars_Loader,     only:   oHMC_Vars
    
    
    use HMC_Module_Tools_Debug
    use HMC_Module_Tools_IO,        only:   HMC_Tools_IO_Put1d_NC, &
                                            HMC_Tools_IO_Put1d_ASCII, &
                                            check
    
    use HMC_Module_Tools_Generic,   only:   HMC_Tools_Generic_ReplaceText, & 
                                            HMC_Tools_Generic_CreateFolder, &
                                            HMC_Tools_Generic_ZipFile, &
                                            HMC_Tools_Generic_RemoveFile, &
                                            mean2Dvar
    
    ! Implicit none for all subroutines in this module
    implicit none
    !------------------------------------------------------------------------------------------
    
contains
    
    !------------------------------------------------------------------------------------------
    ! Subroutine to manage output gridded data
    subroutine HMC_Data_Output_Point_Cpl( iID, sTime, &
                                          iRowsStart, iRowsEnd, iColsStart, iColsEnd, &
                                          iNSection, iNData, &
                                          iNLake, iNDam, iNPlant, iNJoint, iNCatch, iNRelease)
        
    !------------------------------------------------------------------------------------------
                                          
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4), parameter    :: iNVar = 20
                                          
        integer(kind = 4)               :: iID
        integer(kind = 4)               :: iRows, iCols
        integer(kind = 4)               :: iRowsStart, iRowsEnd, iColsStart, iColsEnd
        integer(kind = 4)               :: iNSection, iNData
        integer(kind = 4)               :: iNLake, iNDam, iNPlant, iNJoint, iNCatch, iNRelease
        
        integer(kind = 4)               :: iFlagTypeData_Output
        integer(kind = 4)               :: iScaleFactor
        
        character(len = 19)             :: sTime
        character(len = 700)            :: sPathData_Output
        character(len = 700)            :: sCommandCreateFolder
        
        real(kind = 4), dimension(iNSection)    :: a1dVarQoutSection
        
        real(kind = 4), dimension(iNDam)        :: a1dVarVDam, a1dVarLDam
        
        real(kind = 4), dimension(iNVar)        :: a1dVarMeanValue
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Initialize variable(s)
        a1dVarVDam = -9999.0; a1dVarLDam= -9999.0; 
        a1dVarMeanValue = -9999.0; a1dVarQoutSection = -9999.0
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Defining iRows and iCols (output data)
        iRows = iRowsEnd - iRowsStart + 1
        iCols = iColsEnd - iColsStart + 1
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Get global information
        sPathData_Output = oHMC_Namelist(iID)%sPathData_Output_Point
        iFlagTypeData_Output = oHMC_Namelist(iID)%iFlagTypeData_Output_Point
        sCommandCreateFolder = oHMC_Namelist(iID)%sCommandCreateFolder
        ! Info start
        call mprintf(.true., iINFO_Extra, ' Data :: Output point ... ' )
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Replace general path with specific time feature(s)
        call HMC_Tools_Generic_ReplaceText(sPathData_Output, '$yyyy', sTime(1:4))
        call HMC_Tools_Generic_ReplaceText(sPathData_Output, '$mm', sTime(6:7))
        call HMC_Tools_Generic_ReplaceText(sPathData_Output, '$dd', sTime(9:10))
        call HMC_Tools_Generic_ReplaceText(sPathData_Output, '$HH', sTime(12:13))
        call HMC_Tools_Generic_ReplaceText(sPathData_Output, '$MM', sTime(15:16))
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Create output folder
        call HMC_Tools_Generic_CreateFolder(sCommandCreateFolder, sPathData_Output, .true.)
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Get variable(s) from global workspace
        
        ! Get Forcing variable(s)
        a1dVarMeanValue(1) = mean2Dvar(oHMC_Vars(iID)%a2dRain,          oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(2) = mean2Dvar(oHMC_Vars(iID)%a2dTa,            oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(3) = mean2Dvar(oHMC_Vars(iID)%a2dK,             oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(4) = mean2Dvar(oHMC_Vars(iID)%a2dW,             oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(5) = mean2Dvar(oHMC_Vars(iID)%a2dRHum,          oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(6) = mean2Dvar(oHMC_Vars(iID)%a2dPres,          oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(7) = mean2Dvar(oHMC_Vars(iID)%a2dLAI,           oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(8) = mean2Dvar(oHMC_Vars(iID)%a2dAlbedo,        oHMC_Vars(iID)%a2iMask) 
        ! Get Outcome variable(s)
        a1dVarMeanValue(9) = mean2Dvar(oHMC_Vars(iID)%a2dLST,           oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(10) = mean2Dvar(oHMC_Vars(iID)%a2dH,            oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(11) = mean2Dvar(oHMC_Vars(iID)%a2dLE,           oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(12) = mean2Dvar(oHMC_Vars(iID)%a2dET,           oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(13) = mean2Dvar(oHMC_Vars(iID)%a2dIntensity,    oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(14) = mean2Dvar(oHMC_Vars(iID)%a2dVTot,         oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(15) = mean2Dvar(oHMC_Vars(iID)%a2dVRet,         oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(16) = mean2Dvar(oHMC_Vars(iID)%a2dVSub,         oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(17) = mean2Dvar(oHMC_Vars(iID)%a2dVLoss,        oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(18) = mean2Dvar(oHMC_Vars(iID)%a2dVExf,         oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(19) = mean2Dvar(oHMC_Vars(iID)%a2dFlowDeep,     oHMC_Vars(iID)%a2iMask) 
        a1dVarMeanValue(20) = mean2Dvar(oHMC_Vars(iID)%a2dWTable,       oHMC_Vars(iID)%a2iMask)
 
        ! Get discharge in outlet section(s)
        a1dVarQoutSection = oHMC_Vars(iID)%a1dQoutSection
        ! Get volume, level amd discharge in dam section(s)
        a1dVarVDam = oHMC_Vars(iID)%a1dVDam 
        a1dVarLDam = oHMC_Vars(iID)%a1dLDam 
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Subroutine for writing sequential netCDF output data 
        if (iFlagTypeData_Output == 2) then
                        
            !------------------------------------------------------------------------------------------
            ! Call subroutine to write point data
            call HMC_Data_Output_Point_NC(iID, &
                                          sPathData_Output, &
                                          iNSection, iNData, iNVar, &
                                          iNLake, iNDam, iNPlant, iNJoint, iNCatch, iNRelease, &
                                          sTime, &
                                          a1dVarQoutSection, a1dVarVDam, a1dVarLDam, &
                                          a1dVarMeanValue)
            !------------------------------------------------------------------------------------------
            
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Subroutine for writing sequential binary output data 
        if (iFlagTypeData_Output == 1) then
                        
            !------------------------------------------------------------------------------------------
            ! Call subroutine to write point data
            call HMC_Data_Output_Point_ASCII(iID, &
                                           sPathData_Output, &
                                           iNSection, iNData, iNVar, &
                                           iNLake, iNDam, iNPlant, iNJoint, iNCatch, iNRelease, &
                                           sTime, &
                                           a1dVarQoutSection, a1dVarVDam, a1dVarLDam, &
                                           a1dVarMeanValue)
            !------------------------------------------------------------------------------------------
        
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Info end
        call mprintf(.true., iINFO_Extra, ' Data :: Output point ... OK ' )
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Data_Output_Point_Cpl
    !------------------------------------------------------------------------------------------
    
    !------------------------------------------------------------------------------------------
    ! Subroutine to write netCDF point data output
    subroutine HMC_Data_Output_Point_NC(iID, &
                                          sPathData_Output, &
                                          iNSection, iDataN, iNVar, &
                                          iNLake, iNDam, iNPlant, iNJoint, iNCatch, iNRelease, &
                                          sTime, &
                                          a1dVarQoutSection, a1dVarVDam, a1dVarLDam, &
                                          a1dVarMeanValue)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4)                       :: iID                  
                                  
        character(len = 256), intent(in)        :: sPathData_Output 
        character(len = 700)                    :: sFileNameData_Output
        character(len = 256)                    :: sVarName, sVarNameLong
        character(len = 256)                    :: sVarGridMap, sVarDescription, sVarCoords
        integer(kind = 4), intent(in)           :: iNSection, iDataN, iNVar
        integer(kind = 4), intent(in)           :: iNLake, iNDam, iNPlant, iNJoint, iNCatch, iNRelease

        character(len = 19)                     :: sTime, sTimeSave

        real(kind = 4)                          :: dVarMissingValue
        
        character(len = 700)                    :: sCommandZipFile

        real(kind = 4), dimension(iNVar), intent(in)        :: a1dVarMeanValue
        real(kind = 4), dimension(iNSection), intent(in)    :: a1dVarQoutSection
        real(kind = 4), dimension(iNDam), intent(in)        :: a1dVarVDam, a1dVarLDam
        
        character(len = 256)    :: sVarUnits
        integer(kind = 4)       :: iErr
        
        integer(kind = 4)       :: iFileID
        integer(kind = 4)       :: iID_Dim_Section, iID_Dim_Var, iID_Dim_Time, iID_Dim_Dam
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Get from global workspace
        sCommandZipFile = oHMC_Namelist(iID)%sCommandZipFile
        ! Info start
        call mprintf(.true., iINFO_Extra, ' Data :: Output point :: NetCDF ... ' )
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Filename output
        sFileNameData_Output = trim(sPathData_Output)//"hmc.output-point."// &
        sTime(1:4)//sTime(6:7)//sTime(9:10)// & 
        sTime(12:13)//sTime(15:16)// &
        ".nc"
            
        ! Info netCDF filename
        call mprintf(.true., iINFO_Verbose, ' Save filename (result point): '//trim(sFileNameData_Output)//' ... ')
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Create netcdf file
        call check( nf90_create(trim(sFileNameData_Output), 0, iFileID) )
	
        ! Dimension(s)
        call check( nf90_def_dim(iFileID, "time", NF90_UNLIMITED, iID_Dim_Time) )
        call check( nf90_def_dim(iFileID, "section", iNSection, iID_Dim_Section) )
        call check( nf90_def_dim(iFileID, "average_var", iNVar, iID_Dim_Var) )
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Global attribute(s)
        sTimeSave(1:len_trim(sTime)) = sTime
        call check( nf90_put_att(iFileID, NF90_GLOBAL, "time_coverage_end", sTimeSave) )
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Definition mode OFF - Data mode ON
        call check( nf90_enddef(iFileID))
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Writing dynamic point variable(s) in netCDF output file
        ! Section discharge
        sVarName = 'Discharge'; sVarNameLong = 'section_discharge'; sVarDescription = 'outlet section discharge';
        sVarUnits = 'm^3/s'; sVarCoords = 'x y'; sVarGridMap = 'epsg:4326'; dVarMissingValue = -9E15;
        call HMC_Tools_IO_Put1d_NC(iFileID, iID_Dim_Section, & 
                             sVarName, sVarNameLong, sVarDescription, &
                             sVarUnits, sVarCoords, sVarGridMap, dVarMissingValue, &
                             iNSection, a1dVarQoutSection)
        ! Mean point variable(s)
        sVarName = 'MeanVar'; sVarNameLong = 'mean_variable'; sVarDescription = 'avarage variable(s) at each timestep';
        sVarUnits = ''; sVarCoords = 'x y'; sVarGridMap = 'epsg:4326'; dVarMissingValue = -9E15;
        call HMC_Tools_IO_Put1d_NC(iFileID, iID_Dim_Var, & 
                             sVarName, sVarNameLong, sVarDescription, &
                             sVarUnits, sVarCoords, sVarGridMap, dVarMissingValue, &
                             iNVar, a1dVarMeanValue)
        ! Dam volume
        sVarName = 'VDam'; sVarNameLong = 'dam_volume'; sVarDescription = 'dam volume';
        sVarUnits = 'm^3'; sVarCoords = 'x y'; sVarGridMap = 'epsg:4326'; dVarMissingValue = -9E15;
        call HMC_Tools_IO_Put1d_NC(iFileID, iID_Dim_Dam, & 
                             sVarName, sVarNameLong, sVarDescription, &
                             sVarUnits, sVarCoords, sVarGridMap, dVarMissingValue, &
                             iNDam, a1dVarVDam)
        ! Dam level
        sVarName = 'LDam'; sVarNameLong = 'dam_level'; sVarDescription = 'dam level';
        sVarUnits = 'm'; sVarCoords = 'x y'; sVarGridMap = 'epsg:4326'; dVarMissingValue = -9E15;
        call HMC_Tools_IO_Put1d_NC(iFileID, iID_Dim_Dam, & 
                             sVarName, sVarNameLong, sVarDescription, &
                             sVarUnits, sVarCoords, sVarGridMap, dVarMissingValue, &
                             iNDam, a1dVarLDam)                                   
        !------------------------------------------------------------------------------------------
                             
        !------------------------------------------------------------------------------------------
        ! Close
        call check( nf90_close(iFileID) )
        ! Info netCDF filename
        call mprintf(.true., iINFO_Verbose, ' Save filename (result point): '//trim(sFileNameData_Output)//' ... OK ')
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Zip file
        !call HMC_Tools_Generic_ZipFile(sCommandZipFile, &
        !                               sFileNameData_Output//'.gz', sFileNameData_Output, .false.)
        ! Remove un-zipped file
        !call HMC_Tools_Generic_RemoveFile(oHMC_Namelist(iID)%sCommandRemoveFile, sFileNameData_Output, .false.)
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Info end
        call mprintf(.true., iINFO_Extra, ' Data :: Output point :: NetCDF ... OK ' )
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Data_Output_Point_NC
    !------------------------------------------------------------------------------------------
    
    !------------------------------------------------------------------------------------------
    ! Subroutine to write point ASCII data output
    subroutine HMC_Data_Output_Point_ASCII(iID, &
                                           sPathData_Output, &
                                           iNSection, iNData, iNVar, &
                                           iNLake, iNDam, iNPlant, iNJoint, iNCatch, iNRelease, &
                                           sTime, &
                                           a1dVarQoutSection, a1dVarVDam, a1dVarLDam, &
                                           a1dVarMeanValue)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4)                       :: iID                  
                                  
        character(len = 700), intent(in)        :: sPathData_Output
        character(len = 700)                    :: sFileNameData_Output
        character(len = 256)                    :: sVarName
        integer(kind = 4)                       :: iNSection, iNData, iNVar
        integer(kind = 4)                       :: iNLake, iNDam, iNPlant, iNJoint, iNCatch, iNRelease

        character(len = 19), intent(in)         :: sTime

        real(kind = 4), dimension(iNVar), intent(in)        :: a1dVarMeanValue
        real(kind = 4), dimension(iNSection), intent(in)    :: a1dVarQoutSection
        real(kind = 4), dimension(iNDam), intent(in)        :: a1dVarVDam, a1dVarLDam
       
        character(len = 256)    :: sVarUnits
        integer(kind = 4)       :: iErr
        
        character(len = 20), parameter :: sFMTDischarge = "(F14.2)"
        character(len = 20), parameter :: sFMTVarMean = "(F20.5)"
        character(len = 20), parameter :: sFMTVarVDam = "(F20.5)"
        character(len = 20), parameter :: sFMTVarLDam = "(F20.5)"
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Info start
        call mprintf(.true., iINFO_Extra, ' Data :: Output point :: ASCII ... ' )
        ! Info filename(s) at each time step
        call mprintf(.true., iINFO_Verbose, ' Save (result point) at time: '//trim(sTime)//' ... ')
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Writing dynamic point variable(s) in ASCII output file
        ! Section discharge
        sFileNameData_Output = trim(sPathData_Output)//"hmc.discharge."// &
                           sTime(1:4)//sTime(6:7)//sTime(9:10)//sTime(12:13)//sTime(15:16)// &
                           ".txt"    
        call mprintf(.true., iINFO_Extra, ' Save filename: '//trim(sFileNameData_Output) )
        call HMC_Tools_IO_Put1d_ASCII(sFileNameData_Output, a1dVarQoutSection, iNSection, .true., iErr, sFMTDischarge)
        !call HMC_Tools_Generic_ZipFile(oHMC_Namelist(iID)%sCommandZipFile, &
        !                               sFileNameData_Output//'.gz', sFileNameData_Output, .false.)
        !call HMC_Tools_Generic_RemoveFile(oHMC_Namelist(iID)%sCommandRemoveFile, sFileNameData_Output, .false.)
    
        ! Mean variable(s)
        sFileNameData_Output = trim(sPathData_Output)//"hmc.varmean."// &
                           sTime(1:4)//sTime(6:7)//sTime(9:10)//sTime(12:13)//sTime(15:16)// &
                           ".txt"            
        call mprintf(.true., iINFO_Extra, ' Save filename: '//trim(sFileNameData_Output) )
        call HMC_Tools_IO_Put1d_ASCII(sFileNameData_Output, a1dVarMeanValue, iNVar, .true., iErr, sFMTVarMean)
        !call HMC_Tools_Generic_ZipFile(oHMC_Namelist(iID)%sCommandZipFile, &
        !                               sFileNameData_Output//'.gz', sFileNameData_Output, .false.)
        !call HMC_Tools_Generic_RemoveFile(oHMC_Namelist(iID)%sCommandRemoveFile, sFileNameData_Output, .false.)
        
        ! Dam volume
        sFileNameData_Output = trim(sPathData_Output)//"hmc.vdam."// &
                           sTime(1:4)//sTime(6:7)//sTime(9:10)//sTime(12:13)//sTime(15:16)// &
                           ".txt"            
        call mprintf(.true., iINFO_Extra, ' Save filename: '//trim(sFileNameData_Output) )
        call HMC_Tools_IO_Put1d_ASCII(sFileNameData_Output, a1dVarVDam, iNDam, .true., iErr, sFMTVarVDam)
        !call HMC_Tools_Generic_ZipFile(oHMC_Namelist(iID)%sCommandZipFile, &
        !                               sFileNameData_Output//'.gz', sFileNameData_Output, .false.)
        !call HMC_Tools_Generic_RemoveFile(oHMC_Namelist(iID)%sCommandRemoveFile, sFileNameData_Output, .false.)
        
        ! Dam level
        sFileNameData_Output = trim(sPathData_Output)//"hmc.ldam."// &
                           sTime(1:4)//sTime(6:7)//sTime(9:10)//sTime(12:13)//sTime(15:16)// &
                           ".txt"            
        call mprintf(.true., iINFO_Extra, ' Save filename: '//trim(sFileNameData_Output) )
        call HMC_Tools_IO_Put1d_ASCII(sFileNameData_Output, a1dVarLDam, iNDam, .true., iErr, sFMTVarLDam)
        !call HMC_Tools_Generic_ZipFile(oHMC_Namelist(iID)%sCommandZipFile, &
        !                               sFileNameData_Output//'.gz', sFileNameData_Output, .false.)
        !call HMC_Tools_Generic_RemoveFile(oHMC_Namelist(iID)%sCommandRemoveFile, sFileNameData_Output, .false.)
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Print filename(s) info
        call mprintf(.true., iINFO_Verbose, ' Save (result point) at time: '//trim(sTime)//' ... OK')
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Info end
        call mprintf(.true., iINFO_Extra, ' Data :: Output point :: ASCII ... OK' )
        !------------------------------------------------------------------------------------------
    
    end subroutine HMC_Data_Output_Point_ASCII
    !------------------------------------------------------------------------------------------   
    
end module HMC_Module_Data_Output_Point
!------------------------------------------------------------------------------------------