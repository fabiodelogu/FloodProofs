 !------------------------------------------------------------------------------------
! File:   HMC_Module_Phys_Convolution_Apps.f90
!
! Author(s):    Fabio Delogu, Francesco Silvestro, Simone Gabellani
! Date:         20150212
!
! Convolution Apps subroutine(s) for HMC model
!------------------------------------------------------------------------------------

!------------------------------------------------------------------------------------
! Module Header
module HMC_Module_Phys_Convolution_Apps

    !------------------------------------------------------------------------------------
    ! External module(s) 
    use HMC_Module_Namelist,                only: oHMC_Namelist
    use HMC_Module_Vars_Loader,             only: oHMC_Vars
    
    use HMC_Module_Tools_Debug
    
    ! Implicit none for all subroutines in this module
    implicit none
    !------------------------------------------------------------------------------------------

contains 

    !------------------------------------------------------------------------------------------
    ! Subroutine to calculate dynamic integration step
    subroutine HMC_Phys_Convolution_Apps_IntegrationStep(iID, iRows, iCols, dDtDataForcing, dDtIntegrAct)
	
        !------------------------------------------------------------------------------------------
        ! Variable(s) declaration
        integer(kind = 4)               :: iID, iRows, iCols
        
        real(kind = 4)                  :: dDtDataForcing
        real(kind = 4)                  :: dDtIntegr, dDtIntegrPStep
        real(kind = 4), intent(out)     :: dDtIntegrAct
        
        integer(kind = 4)               :: iFlagVarDtPhysConv
        real(kind = 4)                  :: dBc
        real(kind = 4)                  :: dDtRef, dDtRefRatio, dDtIntegrMin
        real(kind = 4)                  :: dDEMStepMean, dVarRainMax, dVarUcDtMax
        real(kind = 4)                  :: dVarHydroMax
        
        real(kind = 4), dimension (iRows, iCols)            :: a2dVarUc, a2dVarUh
        
        real(kind = 4), dimension (iRows, iCols)            :: a2dVarHydro, a2dVarRain, a2dVarRouting
        
        real(kind = 4), dimension (iRows, iCols)            :: a2dVarUcDt, a2dVarUcAct
        
        character(len = 20)                                 :: sStrDtIntegrStep, sStrVarUcDtMax
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Variable(s) initialization
        dDtIntegrAct = 0.0; dDtIntegrPStep = 0.0; dDtIntegr = 0.0;
        dVarRainMax = 0.0; dDEMStepMean = 0.0;
        dDtRef = 0.0; dDtRefRatio = 0.0; dDtIntegrMin = 0.0;
       
        a2dVarHydro = 0.0; 
        
        a2dVarUcDt = 0.0; a2dVarUcAct = 0.0;
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Temporal integration at previous step
        dDtIntegr = real(oHMC_Vars(iID)%iDtIntegr)
        dDtIntegrPStep = real(oHMC_Vars(iID)%iDtIntegrPStep)
        ! Dynamic temporal integration step
        iFlagVarDtPhysConv = oHMC_Namelist(iID)%iFlagVarDtPhysConv
        ! Exponent of dUcAct formula
        dBc = oHMC_Namelist(iID)%dBc
        ! DEM mean step
        dDEMStepMean = oHMC_Vars(iID)%dDEMStepMean
        
        ! Channel and hill surface velocity
        a2dVarUc = oHMC_Vars(iID)%a2dUc
        a2dVarUh = oHMC_Vars(iID)%a2dUh
        
        ! Dynamic variable(s)
        a2dVarHydro = oHMC_Vars(iID)%a2dHydro
        a2dVarRain = oHMC_Vars(iID)%a2dRain
        a2dVarRouting = oHMC_Vars(iID)%a2dRouting
        a2dVarUcAct = oHMC_Vars(iID)%a2dUcAct
        a2dVarUcDt = oHMC_Vars(iID)%a2dUcDt
        
        ! Info start
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: IntegrationStep ... ' )
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Dynamic temporal integration step flag
        if (iFlagVarDtPhysConv.eq.1 ) then
            
            !------------------------------------------------------------------------------------------
            ! Actual temporal integration Step
            dDtIntegrAct = dDtIntegr
            ! Rain intensity max value
            dVarRainMax = maxval(maxval(a2dVarRain,DIM = 1),DIM = 1)*3600.0/dDtDataForcing
            !------------------------------------------------------------------------------------------
            
            !------------------------------------------------------------------------------------------
            ! Definition of temporal integration parameter(s)
            if ( (dDEMStepMean.ge.10) .and. (dDEMStepMean.lt.100) ) then
                dDtRef = 6.0; ! seconds
                dDtIntegrMin = 25.0; ! seconds
                dDtRefRatio = 3.0; 
            elseif ( dDEMStepMean.lt.10 ) then 
                dDtRef = 1.0; ! seconds
                dDtIntegrMin = 10.0; ! seconds
                dDtRefRatio = 3.0; 
            elseif (dDEMStepMean.gt.1000 ) then
                dDtRef = 60.0; ! seconds
                dDtIntegrMin = 600.0; ! seconds
                dDtRefRatio = 2.0; 
            else
                dDtRef = 6.0; ! seconds
                dDtIntegrMin = 25.0; ! seconds
                dDtRefRatio = 3.0;
            endif
            !------------------------------------------------------------------------------------------

            !------------------------------------------------------------------------------------------
            ! Dynamic integration step evaluation
            where( (oHMC_Vars(iID)%a2iChoice.eq.1) .and. (oHMC_Vars(iID)%a2dDem.gt.0.0) )
                a2dVarUcAct = a2dVarUc*(tan(oHMC_Vars(iID)%a2dBeta)**0.5)*a2dVarHydro**dBc
                a2dVarUcDt = a2dVarHydro*a2dVarUcAct/(1000*3600)*oHMC_Vars(iID)%a2dAreaCell !m^3/s
            endwhere

            where( (oHMC_Vars(iID)%a2iChoice.eq.0) .and. (oHMC_Vars(iID)%a2dDem.gt.0.0) ) 
                a2dVarUcDt = a2dVarHydro*a2dVarUcAct/(1000*3600)*oHMC_Vars(iID)%a2dAreaCell !m^3/s
            endwhere

            ! Checking waterlevel and updating 
            where( (a2dVarHydro.gt.0.0) .and. (oHMC_Vars(iID)%a2dDem.gt.0.0) )
                a2dVarUcDt = a2dVarUcDt/(a2dVarHydro/1000*dDEMStepMean) !m/s
            elsewhere
                a2dVarUcDt = 0.0
            endwhere
            !! al secondo giro vale 96.15 ... qua c'è un valore assurdo (al primo giro vale 0)
            dVarHydroMax = maxval(maxval(a2dVarHydro,DIM = 1),DIM = 1)
            dVarUcDtMax = maxval(maxval(a2dVarUcDt,DIM = 1),DIM = 1)
            !------------------------------------------------------------------------------------------
            
            !------------------------------------------------------------------------------------------
            if (dVarUcDtMax.le.0.1) dVarUcDtMax = 0.1

            ! First estimation of integration step
            dDtIntegrAct = dDEMStepMean/dVarUcDtMax*0.6

            ! Checking Integration step value
            if (dDtIntegrAct.gt.dDtDataForcing/dDtRefRatio) then
                dDtIntegrAct = dDtDataForcing/dDtRefRatio
            endif
            if ( (dVarRainMax.gt.1.0) .and. (dDtIntegrAct.gt.dDtIntegr) ) then
                dDtIntegrAct = dDtIntegr*exp(-dVarRainMax/3.0) + dDtIntegr
            endif
            if (dDtIntegrAct.lt.dDtIntegrMin) then
                dDtIntegrAct = dDtIntegrMin
            endif

            dDtIntegrAct = dDtDataForcing/int(dDtDataForcing/dDtIntegrAct)
            dDtIntegrAct = int(dDtIntegrAct/dDtRef)*dDtRef
            !------------------------------------------------------------------------------------------

            !------------------------------------------------------------------------------------------
            ! Checking if dt integration is too big of previous dt integration
            if(dDtIntegrAct.gt.dDtIntegrPStep + dDtRef) then
                dDtIntegrAct = dDtIntegrPStep + dDtRef
            endif
            !------------------------------------------------------------------------------------------

            !------------------------------------------------------------------------------------------
            ! Updating routing variable; intensity must be the same between steps
            a2dVarRouting = a2dVarRouting/dDtIntegrPStep*dDtIntegrAct
            !------------------------------------------------------------------------------------------

        else
            
            !------------------------------------------------------------------------------------------
            ! Actual temporal integration Step
            dDtIntegrAct = dDtIntegr
            !------------------------------------------------------------------------------------------
            
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Temporal integration step info
        write(sStrDtIntegrStep, *) dDtIntegrAct
        write(sStrVarUcDtMax, *) dVarUcDtMax
        call mprintf(.true., iINFO_Verbose, ' Phys :: Convolution :: IntegrationStep :: '// &
                                          ' Integration Step Update: '//sStrDtIntegrStep//' [s] '// &
                                          ' Uc Max: '//sStrVarUcDtMax//' [m/s]')
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Passing varible(s) to global declaration
        oHMC_Vars(iID)%iDtIntegrPStep = int(dDtIntegrAct)
        oHMC_Vars(iID)%a2dRouting = a2dVarRouting
        oHMC_Vars(iID)%a2dUcAct = a2dVarUcAct
        oHMC_Vars(iID)%a2dUcDt = a2dVarUcDt
        
        ! Info end
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: IntegrationStep ... OK' )
        endif
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Phys_Convolution_Apps_IntegrationStep
    !------------------------------------------------------------------------------------
    
    !------------------------------------------------------------------------------------------
    ! Subroutine for calculating convolution
    subroutine HMC_Phys_Convolution_Apps_DeepFlow(iID, iRows, iCols, dDtDataForcing, iNSection, iNLake)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s) declaration
        integer(kind = 4)           :: iID
        integer(kind = 4)           :: iRows, iCols
        integer(kind = 4)           :: iNSection, iNLake
        
        integer(kind = 4)           :: iI, iII, iIII, iJ, iJJ, iJJJ, iL
        integer(kind = 4)           :: iFlagFlowDeep, iVarPNT, iNgr, iT
        real(kind = 4)              :: dHt, dHm, dGamma, dKSatRatio
        real(kind = 4)              :: dDt, dDtDataForcing
        
        real(kind = 4)              :: dVarWTable, dVarFlowDeep
        
        integer(kind = 4), dimension (iRows, iCols) :: a2iVarMask, a2iVarPNT, a2iVarChoice
        real(kind = 4), dimension (iRows, iCols)    :: a2dVarDEM, a2dVarAlpha, a2dVarBeta, a2dVarS
        real(kind = 4), dimension (iRows, iCols)    :: a2dVarCostF1, a2dVarAreaCell
        
        real(kind = 4), dimension (iRows, iCols)    :: a2dVarVTot, a2dVarVLoss, a2dVarFlowDeep
        real(kind = 4), dimension (iRows, iCols)    :: a2dVarDarcy, a2dVarHydro
        
        real(kind = 4), dimension (iRows, iCols)    :: a2dVarWTable, a2dVarWTableMax, a2dVarWTableStep
        
        integer(kind = 4), dimension (iNSection, 2) :: a2iVarXYSection
        
        integer(kind = 4), dimension (iNLake, 2)    :: a2iVarXYLake
        real(kind = 4), dimension (iNLake)          :: a1dVarCodeLake, a1dVarVMinLake, a1dVarVLake, a1dVarCostLake
        real(kind = 4), dimension (iNLake)          :: a1dVarQoutLake
        
        real(kind = 4)                              :: dVarHydroMax
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Initialization variable(s)
        a2iVarPNT = 0; a2iVarChoice = 0;
        a2dVarDEM = 0.0; a2dVarS = 0.0; a2dVarAlpha = 0.0; a2dVarBeta = 0.0; 
        a2dVarCostF1 = 0.0; a2dVarAreaCell = 0.0;
        
        a2dVarVTot = 0.0; a2dVarVLoss = 0.0; a2dVarFlowDeep = 0.0;
        a2dVarDarcy = 0.0; a2dVarHydro = 0.0;
        
        a2dVarWTable = 0.0; a2dVarWTableStep = 0.0; a2dVarWTableMax = 0.0;
        
        dVarWTable = 0.0; dVarHydroMax = 0.0
        
        a2iVarXYSection = 0; a2iVarXYLake = 0;
        a1dVarCodeLake = 0.0; a1dVarVMinLake = 0.0; a1dVarVLake = 0.0; a1dVarCostLake = 0.0;
        
        oHMC_Vars(iID)%a1dQoutLake = 0.0;   ! Re-initialize outgoing lake flow
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Flow deep flag
        iFlagFlowDeep = oHMC_Namelist(iID)%iFlagFlowDeep 
                    
        ! Info start
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: DeepFlow ... ' )
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Condition for activating flow deep process
        if (iFlagFlowDeep.eq.1) then
            
            !------------------------------------------------------------------------------------------
            ! Re-initializing flow deep 
            oHMC_Vars(iID)%a2dFlowDeep = 0.0
            oHMC_Vars(iID)%a2dDarcy = 0.0
            !------------------------------------------------------------------------------------------
            
            !------------------------------------------------------------------------------------------
            ! Ratio deep flow coefficient
            dKSatRatio = oHMC_Namelist(iID)%dKSatRatio
            !------------------------------------------------------------------------------------------

            !------------------------------------------------------------------------------------------
            ! Temporal step of model and forcing data
            iT = oHMC_Vars(iID)%iTime
            dDt = real(oHMC_Namelist(iID)%iDtModel)
            !------------------------------------------------------------------------------------------

            !------------------------------------------------------------------------------------------
            ! Land data from global declaration
            a2iVarMask = oHMC_Vars(iID)%a2iMask
            a2dVarDEM = oHMC_Vars(iID)%a2dDem
            a2iVarPNT = oHMC_Vars(iID)%a2iPNT
            a2iVarChoice = oHMC_Vars(iID)%a2iChoice
            a2dVarS = oHMC_Vars(iID)%a2dS
            a2dVarAreaCell = oHMC_Vars(iID)%a2dAreaCell

            a2dVarCostF1 = oHMC_Vars(iID)%a2dCostF1

            a2dVarWTable = oHMC_Vars(iID)%a2dWTable
            a2dVarWTableMax = oHMC_Vars(iID)%a2dWTableMax
            
            a2dVarHydro = oHMC_Vars(iID)%a2dHydro
            a2dVarVTot = oHMC_Vars(iID)%a2dVTot
            a2dVarVLoss = oHMC_Vars(iID)%a2dVLoss

            a2dVarAlpha = oHMC_Vars(iID)%a2dAlpha
            a2dVarBeta = oHMC_Vars(iID)%a2dBeta

            a2iVarXYSection = oHMC_Vars(iID)%a2iXYSection

            a2iVarXYLake = oHMC_Vars(iID)%a2iXYLake
            a1dVarCodeLake = oHMC_Vars(iID)%a1dCodeLake
            a1dVarVMinLake = oHMC_Vars(iID)%a1dVMinLake
            a1dVarVLake = oHMC_Vars(iID)%a1dVLake
            a1dVarCostLake = oHMC_Vars(iID)%a1dCostLake
            
            a1dVarQoutLake = oHMC_Vars(iID)%a1dQoutLake

            dVarHydroMax = maxval(maxval(a2dVarHydro,DIM = 1),DIM = 1)
            !------------------------------------------------------------------------------------------
            
            !-----------------------------------------------------------------------------------------
            ! Debug
            if (iDEBUG.gt.0) then
                call mprintf(.true., iINFO_Extra, ' ========= DEEPFLOW START =========== ')  
                call mprintf(.true., iINFO_Extra, checkvar(a2dVarFlowDeep, a2iVarMask, 'FLOWDEEP START ') )
                call mprintf(.true., iINFO_Extra, checkvar(a2dVarVTot, a2iVarMask, 'VTOT START ') )
                call mprintf(.true., iINFO_Extra, checkvar(a2dVarWTable, a2iVarMask, 'WTABLE START ') )
                call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydro, a2iVarMask, 'HYDRO START ') )
                call mprintf(.true., iINFO_Extra, ' ') 
            endif
            !-----------------------------------------------------------------------------------------
            
            !------------------------------------------------------------------------------------------
            ! Update WTable
            where( a2dVarDEM.gt.0.0 )
                a2dVarWTableStep = a2dVarWTable + a2dVarVLoss/1000
            endwhere
            !------------------------------------------------------------------------------------------

            !------------------------------------------------------------------------------------------
            ! Compute deep flow
            do iJ = 3, iCols - 1
                do iI = 3, iRows - 1
                    
                    ! Initialization cycle variable(s)
                    iNgr = 0
                    dHt = 0.0
                    dHm = 0.0
                    
                    ! Rate and pointers definition
                    iVarPNT = 0
                    iVarPNT = int(a2iVarPNT(iI,iJ))
                    
                    ! Defining flow directions
                    iII = int((iVarPNT  - 1)/3) - 1
                    iJJ = iVarPNT - 5 - 3*iII
                    iIII = iI + iII
                    iJJJ = iJ + iJJ
                    
                    !write(*,*) 'PNT: ',iVarPNT   
                    !write(*,*) 'iJ: ',iJ, ' iI: ',iI, ' iJJ: ',iJJ, ' iII: ',iII , ' iJJJ: ',iJJJ, ' iIII: ',iIII
                    !------------------------------------------------------------------------------------------

                    !------------------------------------------------------------------------------------------
                    ! Terrain condition for i,j and iii,jjj 
                    if ( (a2dVarDEM(iI,iJ).gt.0.0 ) .and. (a2dVarDEM(iIII,iJJJ).gt.0.0) ) then

                        !------------------------------------------------------------------------------------------
                        ! Cycle(s) on buffer area
                        do iII = iI - 1, iI + 1
                            do iJJ = iJ - 1, iJ + 1

                                if ( (a2dVarDEM(iII,iJJ).gt.0.0 ) .and. ((iII.ne.iI).and.(iJJ.ne.iJ)) ) then

                                    if ( (a2dVarWTable(iI, iJ) - a2dVarWTable(iII,iJJ)).gt.0.0 ) then

                                        dHt = dHt + (a2dVarWTable(iI, iJ) - a2dVarWTable(iII, iJJ))
                                        iNgr = iNgr + 1

                                    endif

                                endif

                            enddo
                        enddo
                        !------------------------------------------------------------------------------------------
                        
                        !------------------------------------------------------------------------------------------
                        if (iNgr.gt.0) then

                            !------------------------------------------------------------------------------------------
                            dHm = dHt/iNgr
                            
                            a2dVarDarcy(iI,iJ) = dHm/sqrt(a2dVarAreaCell(iI,iJ)) * &
                                                 a2dVarCostF1(iI,iJ) * dDtDataForcing/3600*dKSatRatio
                                               
                            if ( a2dVarDarcy(iI,iJ) .gt. ( a2dVarWTable(iI,iJ) - a2dVarWTableMax(iI,iJ))*1000 ) then
                                a2dVarDarcy(iI,iJ) = (a2dVarWTable(iI,iJ) - a2dVarWTableMax(iI,iJ))*1000
                            endif
                            !------------------------------------------------------------------------------------------
                            
                            !------------------------------------------------------------------------------------------
                            do iII = iI - 1, iI + 1
                                do iJJ = iJ - 1, iJ + 1

                                    if ( (a2dVarDEM(iII, iJJ).gt.0.0) .and. ((iII.ne.iI).and.(iJJ.ne.iJ)) ) then
                                        if ( (a2dVarWTable(iI,iJ) - a2dVarWTable(iII,iJJ)).gt.0.0 ) then

                                            a2dVarWTableStep(iII, iJJ) = a2dVarWTableStep(iII, iJJ) + & 
                                                                         a2dVarDarcy(iI,iJ)*(a2dVarWTable(iI, iJ) - &
                                                                         a2dVarWTable(iII,iJJ))/(dHt*1000)
                                            dHm = dHm

                                        endif
                                    endif
                                    
                                enddo
                            enddo
                            !------------------------------------------------------------------------------------------
                            
                        endif
                        !------------------------------------------------------------------------------------------

                    endif
                    !------------------------------------------------------------------------------------------
                    
                    !------------------------------------------------------------------------------------------
                    ! Outlet cell
                    if ( (a2dVarDEM(iI,iJ).gt.0.0) .and. (a2dVarDEM(iIII, iJJJ).lt.0.0) ) then
                        
                        a2dVarDarcy(iI, iJ) = a2dVarAlpha(iI,iJ)*a2dVarCostF1(iI,iJ)*dDtDataForcing/(3600*1000)*dKSatRatio

                        if ( a2dVarDarcy(iI,iJ) .gt. (a2dVarWTable(iI,iJ) - a2dVarWTableMax(iI,iJ)) ) then
                            a2dVarDarcy(iI,iJ) = (a2dVarWTable(iI,iJ) - a2dVarWTableMax(iI,iJ))
                        endif

                    endif
                    !------------------------------------------------------------------------------------------

                enddo
            enddo
            !------------------------------------------------------------------------------------------

            !------------------------------------------------------------------------------------------
            where( a2dVarDEM.GT.0.0 )
                a2dVarWTableStep = a2dVarWTableStep - a2dVarDarcy/1000
            endwhere

            dVarWTable = a2dVarDarcy(a2iVarXYSection(1,2),a2iVarXYSection(1,1)) !!! CONTROLLARE CON MODIFICA INDEX SEZIONI
            !------------------------------------------------------------------------------------------
            
            !------------------------------------------------------------------------------------------
            ! Flow deep - Interaction between watertable and surface
            where( (a2dVarDEM.gt.0.0) .and. (a2dVarWTableStep.gt.a2dVarDEM) )
                a2dVarFlowDeep = (a2dVarWTableStep - a2dVarDEM)*dDtDataForcing/3600*1000
                a2dVarWTableStep = a2dVarDEM
            endwhere

            ! Updating watertable
            where( a2dVarDEM.gt.0.0 )
                a2dVarWTable = a2dVarWTableStep
            endwhere

            ! Updating VTot
            where( a2dVarDEM.gt.0.0 )
                a2dVarVTot = a2dVarVTot + a2dVarFlowDeep
            endwhere
            
            ! Updating flow deep and vtot where vtot >= vmax
            a2dVarFlowDeep = 0.0
            where( (a2dVarDEM.gt.0.0) .and. (a2dVarVTot.gt.a2dVarS) )
                a2dVarFlowDeep = a2dVarVTot - a2dVarS
                a2dVarVTot = a2dVarS
            endwhere
            
            ! Total flow deep
            dVarFlowDeep = sum(sum( (a2dVarWTable - a2dVarWTableMax)*1000, DIM=1, mask=a2dVarDEM.gt.0.0))
            !------------------------------------------------------------------------------------------
            
            !------------------------------------------------------------------------------------------
            ! Check lake availability
            if (iNLake .gt. 0) then
                ! Cycle on lake
                iL = 0
                do iL = 1, iNLake
                    ! Check lake volume 
                    if ( a1dVarVLake(iL) .gt. a1dVarVMinLake(iL) ) then
                        iI = 0; iJ = 0;
                        iI = a2iVarXYLake(iL,2); iJ = a2iVarXYLake(iL,1);
                        
                        ! Output lake discharge [mm/h] 
                        a1dVarQoutLake(iL) = (a1dVarVLake(iL) - a1dVarVMinLake(iL))* &
                                             (a1dVarCostLake(iL)/3600)/(a2dVarAreaCell(iI,iJ))*3600*1000
                        ! Lake outgoing flow
                        a1dVarVLake(iL) = a1dVarVLake(iL) - &
                                          (a1dVarVLake(iL) - a1dVarVMinLake(iL))*(a1dVarCostLake(iL)/3600)*dDtDataForcing
                        
                        ! Flow direction
                        iVarPNT = 0; iVarPNT = int(a2iVarPNT(iI,iJ))
                        ! Defining flow directions
                        iII = int((iVarPNT  - 1)/3) - 1; iJJ = iVarPNT - 5 - 3*iII
                        iIII = iI + iII; iJJJ = iJ + iJJ
                        
                        ! Lake equation to fill lake [mm]
                        if (a1dVarCodeLake(iL).gt.0) then
                            where (a2iVarChoice.eq.a1dVarCodeLake(iL) .and. a2dVarDem.gt.0.0)
                                ! Lake volume to lake mean level
                                a2dVarHydro = a1dVarVLake(iL)/(a1dVarCodeLake(iL)*a2dVarAreaCell(iI,iJ))*1000
                            endwhere
                        endif

                        ! Add lake flow to deep flow (summed to intensity in Horton subroutine) [mm/dt]
                        a2dVarFlowDeep(iIII, iJJJ) = a2dVarFlowDeep(iIII, iJJJ) + a1dVarQoutLake(iL)*dDtDataForcing/3600
		                
                    endif        
                enddo
            endif
            !------------------------------------------------------------------------------------------
            
            !-----------------------------------------------------------------------------------------
            ! Debug
            if (iDEBUG.gt.0) then
                call mprintf(.true., iINFO_Extra, ' ') 
                call mprintf(.true., iINFO_Extra, checkvar(a2dVarFlowDeep, a2iVarMask, 'FLOWDEEP END ') )
                call mprintf(.true., iINFO_Extra, checkvar(a2dVarVTot, a2iVarMask, 'VTOT END ') )
                call mprintf(.true., iINFO_Extra, checkvar(a2dVarWTable, a2iVarMask, 'WTABLE END ') )
                call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydro, a2iVarMask, 'HYDRO END ') )
                call mprintf(.true., iINFO_Extra, ' ========= DEEPFLOW END =========== ') 
            endif
            !-----------------------------------------------------------------------------------------
            
        else
            
            !-----------------------------------------------------------------------------------------
            ! Deep flow process not activated
            if (iDEBUG.gt.0) then
                call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: DeepFlow ... Skipped!' )
            endif
            a2dVarVTot = oHMC_Vars(iID)%a2dVTot
            a2dVarFlowDeep = 0.0
            dVarFlowDeep = 0.0
            !-----------------------------------------------------------------------------------------
            
        endif
        !-----------------------------------------------------------------------------------------
        
        !-----------------------------------------------------------------------------------------
        ! Debug
        dVarHydroMax = maxval(maxval(a2dVarHydro,DIM = 1),DIM = 1)
        !-----------------------------------------------------------------------------------------
                
        !-----------------------------------------------------------------------------------------
        ! Updating model global variable(s)
        oHMC_Vars(iID)%a2dFlowDeep = a2dVarFlowDeep
        oHMC_Vars(iID)%a2dVTot = a2dVarVTot
        oHMC_Vars(iID)%a2dWTable = a2dVarWTable
        
        oHMC_Vars(iID)%a2dHydro = a2dVarHydro
        
        oHMC_Vars(iID)%a1dVLake = a1dVarVLake
        oHMC_Vars(iID)%a1dQoutLake = a1dVarQoutLake
        
        ! Info end
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: DeepFlow ... OK' )
        endif
        !-----------------------------------------------------------------------------------------

    end subroutine HMC_Phys_Convolution_Apps_DeepFlow
    !------------------------------------------------------------------------------------------

    !------------------------------------------------------------------------------------
    ! Subroutine for calculating discharge
    subroutine HMC_Phys_Convolution_Apps_Discharge(iID, iRows, iCols, iNSection, &
                                                   dDtDataForcing, dDtAct, iNTime, iTq, dDtMax)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s) declaration
        integer(kind = 4)   :: iID, iRows, iCols, iTAct
        real(kind = 4)      :: dDtDataForcing, dDtMax, dDtAct, dDtDischarge
        
        integer(kind = 4), intent(inout)    :: iNTime, iTq  
        integer(kind = 4)                   :: iI, iJ, iT, iS, iD
        integer(kind = 4)                   :: iNSection
        
        integer(kind = 4)   :: iFlagVarUc
        real(kind = 4)      :: dRate
        
        !real(kind = 4), dimension (iRows, iCols)          :: a2dVarHydroPrev, a2dVarHydro, a2dVarIntensity
        real(kind = 4), dimension (iRows, iCols)          :: a2dVarQDisOut, a2dVarQVolOut, a2dVarQTot, a2dVarQout

        real(kind = 4), dimension (iNSection)             :: a1dVarQoutSection
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Variable(s) initialization 
        a2dVarQDisOut = 0.0; a2dVarQVolOut = 0.0; a2dVarQTot = 0.0; a2dVarQout = 0.0; 
        !a2dVarHydroPrev = 0.0; a2dVarHydro = 0.0; a2dVarIntensity = 0.0; 
        
        a1dVarQoutSection = 0.0; 
        
        ! Re-initializing Q distributed discharge matrix (in global memory)
        oHMC_Vars(iID)%a2dQout = 0.0;           ! Distributed discharge
        oHMC_Vars(iID)%a1dQoutSection = 0.0;    ! Section discharge OUT
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Flags
        iFlagVarUc = oHMC_Namelist(iID)%iFlagVarUc

        ! Temporal model step
        iT = int(oHMC_Vars(iID)%iTime)
        
        ! Variable(s) time dependent from global declaration
        a2dVarQDisOut = oHMC_Vars(iID)%a2dQDisOut ! Qout
        a2dVarQVolOut = oHMC_Vars(iID)%a2dQVolOut ! Qtmp
        a2dVarQTot = oHMC_Vars(iID)%a2dQTot
        a2dVarQout = oHMC_Vars(iID)%a2dQout

        !a2dVarHydro = oHMC_Vars(iID)%a2dHydro
        !a2dVarHydroPrev = oHMC_Vars(iID)%a2dHydroPrev
        !a2dVarIntensity = oHMC_Vars(iID)%a2dIntensity
        
        a1dVarQoutSection = oHMC_Vars(iID)%a1dQoutSection
        
        ! Info start
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: Discharge ... ' )
        endif
        !------------------------------------------------------------------------------------------
       
        !------------------------------------------------------------------------------------------
        ! Debug
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' ========= DISCHARGE START =========== ') 
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQDisOut, oHMC_Vars(iID)%a2iMask, 'QDIS OUT START (Qout)') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQVolOut, oHMC_Vars(iID)%a2iMask, 'QVOL OUT START (Qtmp)') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQTot, oHMC_Vars(iID)%a2iMask, 'QTOT START (Q)') ) 
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQout, oHMC_Vars(iID)%a2iMask, 'QOUT START (Qmap)') )  

            !call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydro, oHMC_Vars(iID)%a2iMask, 'HYDRO UPD START') )
            !call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydroPrev, oHMC_Vars(iID)%a2iMask, 'HYDRO PREV START') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dUc, oHMC_Vars(iID)%a2iMask, 'UC ') )
            call mprintf(.true., iINFO_Extra, ' ') 
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Integrating step (SurfaceFlow)
        dDtDischarge = dDtAct
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Discharge in channel cells [mm/s]
        where( (oHMC_Vars(iID)%a2iChoice.eq.1) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) )
            a2dVarQTot = a2dVarQTot + a2dVarQVolOut
        endwhere

        ! Discharge in hills cells [mm/s]
        where( (oHMC_Vars(iID)%a2iChoice.eq.0) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) )
            a2dVarQTot = a2dVarQTot + a2dVarQVolOut
        endwhere
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Compute discharge from mm/s to m^3/s (constant is in 1/h)
        if( (real(iTq)*dDtDischarge) .ge. (dDtDataForcing - dDtMax*1.001) ) then ! 1.001 for numerical approx
            
            ! Compute distributed discharge (total and for each step)
            where( oHMC_Vars(iID)%a2dDEM.gt.0.0 )
                a2dVarQTot = a2dVarQTot/(real(iTq)*1000)*oHMC_Vars(iID)%a2dAreaCell
                a2dVarQout = a2dVarQTot                                
            endwhere
            
            ! Calculating discharge in selected outlet(s).
            a1dVarQoutSection = 0.0
            do iS = 1, iNSection
                
                ! Extracting outlet(s) indexes
                iI = 0; iJ = 0;
                iI = oHMC_Vars(iID)%a2iXYSection(iS, 2); iJ = oHMC_Vars(iID)%a2iXYSection(iS, 1)
                
                ! Get section discharge
                a1dVarQoutSection(iS) =  a2dVarQTot(iI, iJ)
               
                ! Subsurface flux
                dRate = sin(oHMC_Vars(iID)%a2dBeta(iI, iJ))
                
                if (dRate.gt.1) dRate = 0.99
                if (dRate.lt.0) dRate = 0.1
                
                if (oHMC_Vars(iID)%a2dWTableMax(iI,iJ).eq.0.0) dRate = 1.0 !Celle dove non ho falda
        
            enddo
                        
            ! Re-initialize qtot array and q counter
            !write(*,*) a1dVarQoutSection; write(*,*) a1dVarQinDam
            a2dVarQTot = 0.0 
            iTq = 0
            
        endif
        !------------------------------------------------------------------------------------------
               
        !------------------------------------------------------------------------------------------
        ! Debug
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' ') 
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQDisOut, oHMC_Vars(iID)%a2iMask, 'QDIS OUT END (Qout)') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQVolOut, oHMC_Vars(iID)%a2iMask, 'QVOL OUT END (Qtmp)') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQTot, oHMC_Vars(iID)%a2iMask, 'QTOT END (Q)') )  
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQout, oHMC_Vars(iID)%a2iMask, 'QOUT END (Qmap)') )  
            !call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydro, oHMC_Vars(iID)%a2iMask, 'HYDRO UPD END') )
            !call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydroPrev, oHMC_Vars(iID)%a2iMask, 'HYDRO PREV END') )
            call mprintf(.true., iINFO_Extra, ' ========= DISCHARGE END =========== ') 
        endif
        !------------------------------------------------------------------------------------------
     
        !------------------------------------------------------------------------------------------
        ! Updating model global variable(s)
        oHMC_Vars(iID)%a2dQTot = a2dVarQTot    
        oHMC_Vars(iID)%a2dQout = a2dVarQout   ! Distributed discharge
        oHMC_Vars(iID)%a1dQoutSection = a1dVarQoutSection   ! Section discharge OUT
        
        ! Info end
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: Discharge ... OK' )
        endif
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Phys_Convolution_Apps_Discharge
    !------------------------------------------------------------------------------------------
        
    !------------------------------------------------------------------------------------------
    ! Subroutine for calculating surface flow
    subroutine HMC_Phys_Convolution_Apps_SurfaceFlow(iID, iRows, iCols, &
                                                     dDtDataForcing, dDtAct, iTAct, iTq, iDtMax, &
                                                     iNData, iNDam, iNLake, & 
                                                     iNPlant, iNCatch, iNRelease, iNJoint, &
                                                     iTime, iNTime, iETime)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s) declaration
        integer(kind = 4)   :: iID, iRows, iCols, iTAct, iTq, iDtMax
        integer(kind = 4)   :: iNData, iNDam, iNLake, iNPlant, iNCatch, iNRelease, iNJoint
        real(kind = 4)      :: dDtDataForcing, dDtAct
        
        integer(kind = 4)   :: iTTemp
        integer(kind = 4)   :: iI, iII, iIII, iJ, iJJ, iJJJ, iP, iR, iD, iL, iC
        integer(kind = 4)   :: iIm, iJm, iIin, iJin, iIout, iJout
        real(kind = 4)      :: dHm, dHin
        real(kind = 4)      :: dDtSurfaceFlow
        
        integer(kind = 4)   :: iFlagVarUc, iVarPNT
        real(kind = 4)      :: dUMax
        real(kind = 4)      :: dRm, dBc
        real(kind = 4)      :: dVLake, dDh
        real(kind = 4)      :: dQt, dHinFD
        
        real(kind = 4), dimension (iRows, iCols)        :: a2dVarIntensityPrev, a2dVarIntensityUpd
        real(kind = 4), dimension (iRows, iCols)        :: a2dVarHydroPrev, a2dVarHydroUpd
        
        real(kind = 4), dimension (iRows, iCols)        :: a2dVarFlowExf
        real(kind = 4), dimension (iRows, iCols)        :: a2dVarUcAct, a2dVarUhAct
        real(kind = 4), dimension (iRows, iCols)        :: a2dVarQDisOut, a2dVarQVolOut
        real(kind = 4), dimension (iRows, iCols)        :: a2dVarRouting
        
        real(kind = 4), dimension (iNDam)               :: a1dVarVDam, a1dVarHDam, a1dVarLDam, a1dVarCoeffDam, a1dVarQoutDam
      
        real(kind = 4), dimension (iNLake)              :: a1dVarVLake

        real(kind = 4), dimension (iNPlant)             :: a1dVarQPlant
        
        real(kind = 4), dimension (iNPlant, iETime)     :: a2dVarHydroPlant
        real(kind = 4), dimension (iNCatch, iETime)     :: a2dVarHydroCatch
        real(kind = 4), dimension (iNRelease, iETime)   :: a2dVarHydroRelease
        
        integer(kind=4) :: iStep, iTime, iNTime, iETime
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Variable(s) initialization 
        a2dVarIntensityPrev = 0.0; a2dVarIntensityUpd = 0.0;
        
        a2dVarHydroPrev = 0.0; a2dVarHydroUpd = 0.0;

        a2dVarUcAct = 0.0; a2dVarUhAct = 0.0; 
        a2dVarFlowExf = 0.0; a2dVarRouting = 0.0;
        
        a2dVarQDisOut = 0.0 ! Outgoing discharge in m^3/s from each cell
        a2dVarQVolOut = 0.0 ! Outgoing discharge in volume from each cell
        
        a1dVarVDam = 0.0; a1dVarHDam = 0.0; a1dVarLDam = 0.0; a1dVarCoeffDam = 0.0; a1dVarQoutDam = 0.0
        
        a1dVarVLake = 0.0;
        
        a1dVarQPlant = 0.0; 
        
        a2dVarHydroPlant = 0.0;
        a2dVarHydroCatch = 0.0;
        a2dVarHydroRelease = 0.0;

        ! Null global variable(s)
        oHMC_Vars(iID)%a2dQVolOut = 0.0 ! Initialize each step (Portata in volume in uscita da una cella == Qtmp)
        oHMC_Vars(iID)%a2dQDisOut = 0.0 ! Initialize each step (Portata in uscita da una cella == Qout)
        
        oHMC_Vars(iID)%a1dQoutDam = 0.0
        
        !oHMC_Vars(iID)%a2dHydroPrev = 0.0 ! Initialize each step
        
        dDh = 0.0
        
        iStep = 1
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Temporal step 
        iTTemp = int(iTAct)
        
        ! Integrating step (SurfaceFlow)
        dDtSurfaceflow = dDtAct
        
        ! Variable(s) time dependent from global declaration
        a2dVarFlowExf = oHMC_Vars(iID)%a2dFlowExf        
        a2dVarHydroPrev = oHMC_Vars(iID)%a2dHydro
        a2dVarIntensityPrev = oHMC_Vars(iID)%a2dIntensity
        a2dVarRouting = oHMC_Vars(iID)%a2dRouting

        ! Dam variable(s)
        a1dVarVDam = oHMC_Vars(iID)%a1dVDam
        a1dVarHDam = oHMC_Vars(iID)%a1dHDam
        a1dVarLDam = oHMC_Vars(iID)%a1dLDam
        a1dVarCoeffDam = oHMC_Vars(iID)%a1dCoeffDam

        ! Lake variable(s)
        a1dVarVLake = oHMC_Vars(iID)%a1dVLake
        
        ! Plant variable(s)
        a2dVarHydroPlant = oHMC_Vars(iID)%a2dHydroPlant
        ! Release variable(s)
        a2dVarHydroCatch = oHMC_Vars(iID)%a2dHydroCatch
        ! Release variable(s)
        a2dVarHydroRelease = oHMC_Vars(iID)%a2dHydroRelease
        
        ! Exponent of dUcAct formula
        dBc = oHMC_Namelist(iID)%dBc
        
        ! Dynamic channel velocity
        iFlagVarUc = oHMC_Namelist(iID)%iFlagVarUc
        
        ! Info start
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: SurfaceFlow ... ' )
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Debug
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' ========= SURFACE FLOW START ========= ') 
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dAreaCell, oHMC_Vars(iID)%a2iMask, 'AREACELL') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydroUpd, oHMC_Vars(iID)%a2iMask, 'HYDRO UPD START') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydroPrev, oHMC_Vars(iID)%a2iMask, 'HYDRO PREV START') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQDisOut, oHMC_Vars(iID)%a2iMask, 'QDIS OUT START (Qout)') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQVolOut, oHMC_Vars(iID)%a2iMask, 'QVOL OUT START (Qtmp)') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarRouting, oHMC_Vars(iID)%a2iMask, 'ROUTING START') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarIntensityPrev, oHMC_Vars(iID)%a2iMask, 'INTENSITY START') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarFlowExf, oHMC_Vars(iID)%a2iMask, 'EXFILTRATION START') )
            call mprintf(.true., iINFO_Extra, checkarray(a2dVarHydroPlant(:,2), 'HYDRO PLANT START') )
            call mprintf(.true., iINFO_Extra, checkarray(a2dVarHydroCatch(:,2), 'HYDRO CATCH START') )
            call mprintf(.true., iINFO_Extra, checkarray(a2dVarHydroRelease(:,2), 'HYDRO RELEASE START') )
            call mprintf(.true., iINFO_Extra, ' ') 
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Channel max surface velocity (UcMax)
        dUMax = 3600.0/dDtSurfaceflow*0.5
        
        ! Hill overland equation 
        a2dVarUhAct = oHMC_Vars(iID)%a2dUh
        where ( (oHMC_Vars(iID)%a2iChoice.eq.0) .and. (a2dVarUhact.gt.dUMax))  ! numerical check
            a2dVarUhAct = dUMax
        endwhere
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Hydro variable (previous and update array)
        where (a2dVarHydroPrev .lt. 0.0)
            a2dVarHydroPrev = 0.0000001
        endwhere
        where(a2dVarHydroPrev.lt.0.0000001)
            a2dVarHydroPrev = 0.0000001
        endwhere
        
        where (a2dVarHydroPrev .gt. 100000.0)
            a2dVarHydroPrev = 0.0000001
        endwhere
        
        ! Updating hydro variable (using previous step and checking values under zero) --> WaterLevel (tirante)
        a2dVarHydroUpd = a2dVarHydroPrev
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Intensity variable (previous and update) 
        where(a2dVarIntensityPrev.lt.0.0)
            a2dVarIntensityPrev = 0.0
        endwhere
        !Updating variables surface cell input (exfiltration + runoff [mm/h]) --> CHECKING CONVERSION
        where(oHMC_Vars(iID)%a2dDEM.gt.0.0)
            a2dVarIntensityUpd = a2dVarIntensityPrev + a2dVarFlowExf*1000.0*3600.0 + &
                                 (1 - oHMC_Vars(iID)%a2dCoeffResol)*a2dVarRouting/dDtSurfaceflow*3600.0
        endwhere
        !------------------------------------------------------------------------------------------
         
        !------------------------------------------------------------------------------------------
        ! Check plant(s) availability
        if (iNPlant .gt. 0) then
            ! Cycle on plant(s)
            iP = 0;
            do iP = 1, iNPlant
                iI = 0; iJ = 0;
                iI = oHMC_Vars(iID)%a2iXYPlant(iP, 2); iJ = oHMC_Vars(iID)%a2iXYPlant(iP, 1);
                
                if (a2dVarHydroPlant(iP, iTTemp + 1) .ge. 0) then
                    a2dVarIntensityUpd(iI, iJ) = a2dVarIntensityUpd(iI, iJ) + a2dVarHydroPlant(iP, iTTemp + 1)

                    ! Update dam volume
                    a1dVarVDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)) = a1dVarVDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)) - &
                        a2dVarHydroPlant(iP, iTTemp + 1)*(oHMC_Vars(iID)%a2dAreaCell(iI, iJ))/(1000*3600)*dDtSurfaceflow !m^3
                        
                else
                    a1dVarQPlant(iP) = oHMC_Vars(iID)%a1dQMaxPlant(iP)

                    if ( a1dVarVDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)) .lt. &
                         oHMC_Vars(iID)%a1dVMaxDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)) )then
                         
                        a1dVarQPlant(iP) = oHMC_Vars(iID)%a1dQMaxPlant(iP)* &
                        (a1dVarVDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP))/ &
                        oHMC_Vars(iID)%a1dVMaxDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)))**6
                        
                    endif

                    ! Check plant discharge
                    if (a1dVarQPlant(iP) .lt. 0.0) a1dVarQPlant(iP) = 0.0

                    a2dVarIntensityUpd(iI, iJ) = a2dVarIntensityUpd(iI, iJ) + &
                                                 a1dVarQPlant(iP)*1000*3600/(oHMC_Vars(iID)%a2dAreaCell(iI, iJ))

                    ! Update dam volume
                    a1dVarVDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)) = a1dVarVDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)) - &
                                                                     a1dVarQPlant(iP)*dDtSurfaceflow
                    
                    !write(*,*) a1dVarVDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)), a1dVarQPlant(iP)
                endif
                
                ! Check dam volume
                if(a1dVarVDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)) .lt. 0.0) a1dVarVDam(oHMC_Vars(iID)%a1iFlagDamPlant(iP)) = 0.0

            enddo 
        
        endif
        !------------------------------------------------------------------------------------------ 

        !------------------------------------------------------------------------------------------ 
        ! Check release(s) availability
        if (iNRelease .gt. 0) then
            ! Cycle on release(s)
            iR = 0;
            do iR = 1, iNRelease
                iI = 0; iJ = 0;
                iI = oHMC_Vars(iID)%a2iXYRelease(iR, 2); iJ = oHMC_Vars(iID)%a2iXYRelease(iR, 1);
                
                if (a2dVarHydroRelease(iR,iTTemp + 1) .lt. 0.0) a2dVarHydroRelease(iR,iTTemp + 1) = 0.0
                a2dVarIntensityUpd(iI, iJ) = a2dVarIntensityUpd(iI, iJ) + a2dVarHydroRelease(iR,iTTemp + 1)

            enddo
            
        endif
        !------------------------------------------------------------------------------------------ 
        
        !------------------------------------------------------------------------------------------
        ! Surface Routing
        
        ! HILLS
        ! Surface equation for hills (direct euler's method)
        where ( (oHMC_Vars(iID)%a2iChoice.eq.0.0) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) ) 
            a2dVarHydroUpd = a2dVarHydroUpd + a2dVarIntensityUpd*dDtSurfaceflow/3600 - &
                             a2dVarHydroUpd*a2dVarUhAct*dDtSurfaceflow/3600.0
            a2dVarQDisOut = a2dVarHydroPrev*a2dVarUhAct*dDtSurfaceflow/3600.0
        endwhere
        
        ! CHANNELS
        ! Surface equation for channels (direct euler's method)
        where ( (oHMC_Vars(iID)%a2iChoice.eq.1.0) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) ) 

            a2dVarUcAct = 0.1 + oHMC_Vars(iID)%a2dUc*(tan(oHMC_Vars(iID)%a2dBeta)**0.5)*a2dVarHydroUpd**dBc

            where (a2dVarUcAct.gt.dUMax)
                a2dVarUcAct = dUMax
            endwhere

            a2dVarQDisOut = a2dVarHydroUpd*a2dVarUcAct*dDtSurfaceflow/3600.0

            ! Surface tank equation (runoff with routing + exfiltration) 
            a2dVarHydroUpd = a2dVarHydroUpd + a2dVarIntensityUpd*dDtSurfaceflow/3600 - &
                          a2dVarHydroUpd*a2dVarUcAct*dDtSurfaceflow/3600.0

        endwhere
        
        where ( (oHMC_Vars(iID)%a2iChoice.eq.1.0) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) ) 

            a2dVarQDisOut = oHMC_Vars(iID)%a2dUc*(tan(oHMC_Vars(iID)%a2dBeta)**0.5)*(0.5*a2dVarHydroPrev**(1 + dBc) + &
                            0.5*a2dVarHydroUpd**(1 + dBc))*dDtSurfaceflow/3600
                          
            where (a2dVarQDisOut .gt. (a2dVarHydroPrev + a2dVarIntensityUpd*dDtSurfaceflow/3600)*0.7)
                a2dVarQDisOut = (a2dVarHydroPrev + a2dVarIntensityUpd*dDtSurfaceflow/3600)*0.7
            endwhere

            a2dVarHydroUpd = a2dVarHydroPrev + a2dVarIntensityUpd*dDtSurfaceflow/3600 - a2dVarQDisOut
           
        endwhere
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Check dam availability
        if (iNDam .gt. 0) then
            ! Cycle on dam
            iD = 0;
            do iD = 1, iNDam
                iI = 0; iJ = 0;
                iI = oHMC_Vars(iID)%a2iXYDam(iD, 2); iJ = oHMC_Vars(iID)%a2iXYDam(iD, 1);
                
                if (oHMC_Vars(iID)%a1dCodeDam(iD) .gt. 0.0) then
                    ! Distributed lake
                    dVLake = 0.0;
                    dVLake = sum(sum(a2dVarIntensityUpd, dim=1, mask=oHMC_Vars(iID)%a2iChoice.eq.oHMC_Vars(iID)%a1dCodeDam(iD)))
                    a1dVarVDam(iD) = a1dVarVDam(iD) + dVLake*dDtSurfaceflow/(3600*1000)*(oHMC_Vars(iID)%a2dAreaCell(iI, iJ)) ! in m^3
                else
                    ! Punctual lake
                    a1dVarVDam(iD) = a1dVarVDam(iD) + a2dVarQDisOut(iI, iJ)/1000*(oHMC_Vars(iID)%a2dAreaCell(iI, iJ))
                endif
                a2dVarQDisOut(iI, iJ) = 0.0
                
            enddo
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Check lake availability
        if (iNLake .gt. 0) then
            ! Cycle on lake
            iL = 0;
            do iL = 1, iNLake
                iI = 0; iJ = 0;
                iI = oHMC_Vars(iID)%a2iXYLake(iL, 2); iJ = oHMC_Vars(iID)%a2iXYLake(iL, 1);
                
                if (oHMC_Vars(iID)%a1dCodeLake(iL) .gt. 0) then
                    ! Distributed lake
                    dVLake = 0.0;
                    dVLake = sum(sum(a2dVarIntensityUpd, dim=1, mask=oHMC_Vars(iID)%a2iChoice.eq.oHMC_Vars(iID)%a1dCodeLake(iL)))
                    a1dVarVLake(iL) = a1dVarVLake(iL) + dVLake*dDtSurfaceflow/(3600*1000)*(oHMC_Vars(iID)%a2dAreaCell(iI, iJ)) ! in m^3
                else
                    ! Punctual lake
                    a1dVarVLake(iL) = a1dVarVLake(iL) + a2dVarQDisOut(iI, iJ)/1000*(oHMC_Vars(iID)%a2dAreaCell(iI, iJ))
                endif
                
            enddo
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Flow part for following cell 
        ! In Horton this flow will add at rain rate in the following step

        ! Checking hydro variable
        where(a2dVarHydroUpd.lt.0.0)
            a2dVarHydroUpd = 0.0000001
        endwhere
        where(a2dVarHydroUpd.lt.0.0000001)
            a2dVarHydroUpd = 0.0000001
        endwhere
        
        ! Calculating flow 
        ! Calcolo la porzione di acqua che va nella cella successiva
        ! Essa verr� sommata alla pioggia nella subroutine di Horton
        ! l'istante successivo
        a2dVarRouting = 0.0
        do iI = 1, iRows
            do iJ = 1, iCols 
                
                ! DEM condition
                if (oHMC_Vars(iID)%a2dDEM(iI,iJ).gt.0.0) then
                    
                    ! Rate and pointers definition
                    !iVarPNT = 0
                    !iVarPNT = int(oHMC_Vars(iID)%a2iPNT(iI,iJ))
                    
                    ! Defining flow directions
                    iII = int((int(oHMC_Vars(iID)%a2iPNT(iI,iJ))  - 1)/3) - 1
                    iJJ = int(oHMC_Vars(iID)%a2iPNT(iI,iJ)) - 5 - 3*iII
                    iIII = iI + iII
                    iJJJ = iJ + iJJ
                    
                    ! Debug
                    !write(*,*) iCols, iJ, iRows, iI, iVarPNT, iJJ, iII, iJJJ, iIII
        
                    if ( (iJJJ.ge.1).and.(iIII.ge.1) ) then
                        
                        ! Integrazione del routing in mm/passo_integrazione_del_routing
                        ! L'acqua viene mandata nella cella successiva e utilizzata nella Subrotine
                        ! Horton
                        dRm = 0.0;
                        dRm = a2dVarQDisOut(iI, iJ) ! Trapezi
                        

                        a2dVarRouting(iIII, iJJJ) = a2dVarRouting(iIII, iJJJ) + dRm  ![mm]
                        a2dVarQVolOut(iI, iJ) = dRm/dDtSurfaceflow	
                        
                    endif 
                endif   
            enddo
        enddo				
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Check catch availability
        if (iNCatch .gt. 0) then
            ! Cycle on catch(es) ---> subtract turbinate(s) from routing
            iC = 0;
            do iC = 1, iNCatch
                
                iI = 0; iJ = 0; dDh = 0.0
                iI = oHMC_Vars(iID)%a2iXYCatch(iC, 2); iJ = oHMC_Vars(iID)%a2iXYCatch(iC, 1);
                
                ! Compute h
                dDh = a2dVarHydroCatch(iC, iTTemp + 1)/(oHMC_Vars(iID)%a2dAreaCell(iI,iJ))*dDtSurfaceflow*1000 ! in [mm]

                ! Pointers definition
                !iVarPNT = 0
                !iVarPNT = int(oHMC_Vars(iID)%a2iPNT(iI,iJ))

                ! Defining flow directions
                iII = int((int(oHMC_Vars(iID)%a2iPNT(iI,iJ))  - 1)/3) - 1
                iJJ = int(oHMC_Vars(iID)%a2iPNT(iI,iJ)) - 5 - 3*iII
                iIII = iI + iII
                iJJJ = iJ + iJJ
                
                ! Index(es) not allowed
                if( (iIII.ge.1) .and. (iJJJ.ge.1) ) then
                    
                    a2dVarRouting(iIII, iJJJ) = a2dVarRouting(iIII, iJJJ) - dDh
                    
                    if(a2dVarRouting(iIII, iJJJ).lt.0.0) a2dVarRouting(iIII, iJJJ) = 0.0
                endif

            enddo
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Check joint availability
        if (iNJoint .gt. 0) then
            ! Cycle on joint(s) 
            iJ = 0;
            do iJ = 1, iNJoint
                iIm = 0; iJm = 0; iIin = 0; iJin = 0;
                iIm = oHMC_Vars(iID)%a2iXYJoint(iJ,2); iJm = oHMC_Vars(iID)%a2iXYJoint(iJ,1);
                iIin = oHMC_Vars(iID)%a2iXYInJoint(iJ,2); iJin = oHMC_Vars(iID)%a2iXYInJoint(iJ,1);
                
                dHm = 0.0; dHin = 0.0;
                dHm = a2dVarHydroUpd(iIm, iJm) !dH2
                dHin = a2dVarHydroUpd(iIin,iJin) !dH1
                
                if ( (dHin.lt.dHm) .and. (dHm.gt.0.0) ) then
                    dQt = 0.0; dHinFD = 0.0;
                    dQt = a2dVarQVolOut(iIin, iJin)/1000 + oHMC_Vars(iID)%a2dAreaCell(iIm, iJm) ! in [m^3/s]
                    dHinFD = sqrt(dHin**2 + 1000*1000*2*(dQt**2)/(oHMC_Vars(iID)%a2dAreaCell(iIm, iJm)*9.8*dHin/1000)) ! derivata eq delle spinte
                    
                    if (dHinFD/dHm .lt. oHMC_Vars(iID)%a1dThrLevelJoint(iJ)) then
                        
                        iIout = 0; iJout = 0;
                        iIout = oHMC_Vars(iID)%a2iXYOutJoint(iJ,2); iJout = oHMC_Vars(iID)%a2iXYOutJoint(iJ,1);
                        
                        ! Main channel
                        a2dVarRouting(iIout,iJout) = a2dVarRouting(iIout,iJout) + a2dVarRouting(iIm,iJm)*(1 - dHinFD/dHm) ! Routing dove immetto la derivazione del Master 
                        a2dVarRouting(iIm,iJm) = a2dVarRouting(iIm,iJm)*dHinFD/dHm ! Routing in main channel
                        
                        ! Tributary channel
			a2dVarRouting(iIout,iJout) = a2dVarRouting(iIout,iJout) + a2dVarRouting(iIin,iJin)*(1 - dHinFD/dHm) ! Routing dove immetto la derivazione dell'immissario
			a2dVarRouting(iIin,iJin) = a2dVarRouting(iIin,iJin)*dHinFD/dHm ! Routing in main channel
                        
                    endif
                endif
            enddo    
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Compute discharge output of the dam
        call HMC_Phys_Convolution_Apps_Discharge_Dam(iID, iNDam, dDtSurfaceflow, &
                                                     a1dVarVDam, a1dVarHDam, a1dVarLDam, a1dVarCoeffDam, &
                                                     a1dVarQoutDam, &
                                                     iTq, iDtMax)
        !------------------------------------------------------------------------------------------
                                     
        !------------------------------------------------------------------------------------------
        ! Check dam availability
        if (iNDam .gt. 0) then
            ! Cycle on dam
            iD = 0
            do iD = 1, iNDam
            
                iI = 0; iJ = 0;
                iI = oHMC_Vars(iID)%a2iXYDam(iD, 2); iJ = oHMC_Vars(iID)%a2iXYDam(iD, 1);
                
                ! Pointers definition
                !iVarPNT = 0
                !iVarPNT = int(oHMC_Vars(iID)%a2iPNT(iI,iJ))
                
                ! Defining flow directions
                iII = int((int(oHMC_Vars(iID)%a2iPNT(iI,iJ))  - 1)/3) - 1
                iJJ = int(oHMC_Vars(iID)%a2iPNT(iI,iJ)) - 5 - 3*iII
                iIII = iI + iII
                iJJJ = iJ + iJJ
                
                ! Update routing 
                a2dVarRouting(iIII, iJJJ) = a2dVarRouting(iIII, iJJJ) + a1dVarQoutDam(iD)
                
                ! Volume to mean dam level [mm]
                where( oHMC_Vars(iID)%a2iChoice.eq.oHMC_Vars(iID)%a1dCodeDam(iD) .and. (oHMC_Vars(iID)%a2dDem.gt.0.0) ) 
                    a2dVarHydroUpd = a1dVarVDam(iD)/(oHMC_Vars(iID)%a1iNCellDam(iD)*oHMC_Vars(iID)%a2dAreaCell(iI,iJ))*1000
                endwhere
                    
            enddo
            
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Debug
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' ') 
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydroUpd, oHMC_Vars(iID)%a2iMask, 'HYDRO UPD END') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarHydroPrev, oHMC_Vars(iID)%a2iMask, 'HYDRO PREV END') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQDisOut, oHMC_Vars(iID)%a2iMask, 'QDIS OUT END (Qout)') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarQVolOut, oHMC_Vars(iID)%a2iMask, 'QVOL OUT END (Qtmp)') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarRouting, oHMC_Vars(iID)%a2iMask, 'ROUTING END') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarIntensityUpd, oHMC_Vars(iID)%a2iMask, 'INTENSITY END') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarFlowExf, oHMC_Vars(iID)%a2iMask, 'EXFILTRATION END') )     
            call mprintf(.true., iINFO_Extra, checkarray(a2dVarHydroPlant(:,2), 'HYDRO PLANT END') )
            call mprintf(.true., iINFO_Extra, checkarray(a2dVarHydroCatch(:,2), 'HYDRO CATCH END') )
            call mprintf(.true., iINFO_Extra, checkarray(a2dVarHydroRelease(:,2), 'HYDRO RELEASE END') )
            call mprintf(.true., iINFO_Extra, ' ========= SURFACE FLOW END =========== ') 
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Updating model global variable(s)
	oHMC_Vars(iID)%a2dQVolOut = a2dVarQVolOut
        oHMC_Vars(iID)%a2dQDisOut = a2dVarQDisOut
        
        oHMC_Vars(iID)%a2dHydro = a2dVarHydroUpd
        oHMC_Vars(iID)%a2dHydroPrev = a2dVarHydroPrev
        oHMC_Vars(iID)%a2dIntensity = a2dVarIntensityUpd
        
        oHMC_Vars(iID)%a2dRouting = a2dVarRouting   ! Compute to use in horton and after set to zero
        
        oHMC_Vars(iID)%a1dVDam = a1dVarVDam
        oHMC_Vars(iID)%a1dHDam = a1dVarHDam 
        oHMC_Vars(iID)%a1dLDam = a1dVarLDam
        oHMC_Vars(iID)%a1dCoeffDam = a1dVarCoeffDam 
        oHMC_Vars(iID)%a1dQoutDam = a1dVarQoutDam
        
        oHMC_Vars(iID)%a1dVLake = a1dVarVLake
        
        oHMC_Vars(iID)%a2dHydroPlant = a2dVarHydroPlant
        oHMC_Vars(iID)%a2dHydroCatch = a2dVarHydroCatch
        oHMC_Vars(iID)%a2dHydroRelease = a2dVarHydroRelease
        
        ! Info end
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: SurfaceFlow ... OK' )
        endif
        !------------------------------------------------------------------------------------------
           
    end subroutine HMC_Phys_Convolution_Apps_SurfaceFlow
    !------------------------------------------------------------------------------------------

    !------------------------------------------------------------------------------------------
    ! Subroutine for calculating hypodermic flow
    subroutine HMC_Phys_Convolution_Apps_SubFlow(iID, iRows, iCols, dDtDataForcing, dDtAct, iNDam)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s) declaration
        integer(kind = 4)   :: iID, iRows, iCols
        integer(kind = 4)   :: iNDam
        real(kind = 4)      :: dDtDataForcing, dDtAct 
        
        integer(kind = 4)   :: iI, iII, iIII, iJ, iJJ, iJJJ, iD
        !integer(kind = 4)   :: iVarPNT
        
        integer(kind = 4)   :: iFlagFlowDeep
        real(kind = 4)      :: dDtSubflow
        real(kind = 4)      :: dRate, dRateMin
        
        real(kind = 4), dimension (iRows, iCols)            :: a2dVarVTot, a2dVarVTotStep, a2dVarVLoss

        real(kind = 4), dimension (iRows, iCols)            :: a2dVarFlowExf
        !real(kind = 4), dimension (iRows, iCols)            :: a2dVarVSub

        real(kind = 4), dimension (iNDam)                   :: a1dVarVDam
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Initialize variable(s)
        dDtSubflow = 0.0; dRate = 0.0;  dRateMin = 0.0; iFlagFlowDeep = 0;
        
        a2dVarVTot = 0.0; a2dVarVTotStep = 0.0;  a2dVarVLoss = 0.0; 
        a2dVarFlowExf = 0.0
        
        a1dVarVDam = 0.0
        
        oHMC_Vars(iID)%a2dFlowExf = 0.0
        
        !iVarPNT = 0; a2dVarVSub = 0.0;
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Integrating step (Subflow)
        dDtSubflow = dDtAct
        
        ! Hypodermic flow minimum rate
        dRateMin = oHMC_Namelist(iID)%dRateMin
        iFlagFlowDeep = oHMC_Namelist(iID)%iFlagFlowDeep

        ! Dam(s) data from global declaration
        a1dVarVDam = oHMC_Vars(iID)%a1dVDam
 
        ! Variable(s) from global declaration
        a2dVarVTot = oHMC_Vars(iID)%a2dVTot
        !a2dVarVSub = oHMC_Vars(iID)%a2dVSub
        a2dVarVLoss = oHMC_Vars(iID)%a2dVLoss
        
        a2dVarFlowExf = oHMC_Vars(iID)%a2dFlowExf
        
        ! Info start
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: SubFlow ... ' )
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Debug
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' ========= SUBFLOW START ========= ') 
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarVTot, oHMC_Vars(iID)%a2iMask, 'VTOT START ') )
            !call mprintf(.true., iINFO_Extra, checkvar(a2dVarVSub, oHMC_Vars(iID)%a2iMask, 'VSUB START ') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarVLoss, oHMC_Vars(iID)%a2iMask, 'VLOSS START ') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarFlowExf, oHMC_Vars(iID)%a2iMask, 'FLOWEXF START ') )        
            call mprintf(.true., iINFO_Extra, '')
        endif
        !------------------------------------------------------------------------------------------
         
        !------------------------------------------------------------------------------------------
        ! Conditions on total and loss volume
        where( (oHMC_Vars(iID)%a2dDEM.gt.0.0).and.(a2dVarVTot.lt.0.0) ) a2dVarVTot = 0.0
        where( (oHMC_Vars(iID)%a2dDEM.gt.0.0).and.(a2dVarVLoss.lt.0.0) ) a2dVarVLoss = 0.0
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Check dam availability
        if (iNDam .gt. 0) then
            ! Set VTot equal zero into Dam(s) cell(s)
            do iD = 1,iNDam
                iI = 0; iJ = 0;
                iI = oHMC_Vars(iID)%a2iXYDam(iD, 2); iJ = oHMC_Vars(iID)%a2iXYDam(iD, 1)
                a2dVarVTot(iI,iJ) = 0.0
            enddo
        endif
        !------------------------------------------------------------------------------------------
            
        !------------------------------------------------------------------------------------------
        ! Cycling on each pixels
        ! Calcola il volume di uscita dalla cella nei due casi: a2dV > o < di a2dS;
        ! Qsup � la portata che esce dalla parte superiore della cella e si aggiunge al deflusso superficiale               
        ! il contatore punta alla cella successiva(controllare se vale per l'ultima cella)
        iI = 0; iJ = 0;
        do iJ = 1, iCols
            do iI = 1, iRows
                
                ! DEM condition
                if (oHMC_Vars(iID)%a2dDEM(iI,iJ).gt.0.0) then
                    
                    ! Rate and pointers definition
                    dRate = 0.0; 
                    dRate = sin(oHMC_Vars(iID)%a2dBeta(iI,iJ))
                    !iVarPNT = 0
                    !iVarPNT = int(oHMC_Vars(iID)%a2iPNT(iI,iJ))
                    
                    ! Defining flow directions
                    iII = int((int(oHMC_Vars(iID)%a2iPNT(iI,iJ))  - 1)/3) - 1
                    iJJ = int(oHMC_Vars(iID)%a2iPNT(iI,iJ)) - 5 - 3*iII
                    iIII = iI + iII
                    iJJJ = iJ + iJJ
                    
                    ! Debugging ndexes
                    !write(*,*) 'Rate: ',dRate,' iPNT: ',iVarPNT
                    !write(*,*) 'iJ: ',iJ, ' iI: ',iI, ' iJJ: ',iJJ, ' iII: ',iII , ' iJJJ: ',iJJJ, ' iIII: ',iIII
                    
                    ! Calculating VTot and VLoss using flowdeep condition
                    if (iFlagFlowDeep.eq.0) then
                        
                        ! VTot (Vloss == 0)
                        if(iIII.ge.1.and.iJJJ.ge.1) then
                            a2dVarVTotStep(iIII,iJJJ) = a2dVarVTotStep(iIII,iJJJ) + oHMC_Vars(iID)%a2dVSub(iI, iJ)
                        endif
                        
                    else
                        
                        ! Checking rate value
                        if(dRate.gt.1.0)        dRate = 0.99
                        if(dRate.lt.dRateMin)   dRate = dRateMin

                        ! VTot
                        if(iIII.ge.1.and.iJJJ.ge.1) then
                            a2dVarVTotStep(iIII,iJJJ) = a2dVarVTotStep(iIII,iJJJ) + oHMC_Vars(iID)%a2dVSub(iI, iJ)*dRate
                        endif
                        ! Vloss
                        if(iIII.ge.1.and.iJJJ.ge.1) then 
                            a2dVarVLoss(iIII,iJJJ) = a2dVarVLoss(iIII,iJJJ) + oHMC_Vars(iID)%a2dVSub(iI, iJ)*(1 - dRate)
                        endif
                    
                    endif
                    
                endif
              
            enddo
        enddo
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Updating total volume 
        a2dVarVTot = a2dVarVTot + a2dVarVTotStep
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Checking total volume and calculating exfiltration volume
	where ( (oHMC_Vars(iID)%a2dDEM.gt.0.0) .and. (a2dVarVTot.gt.oHMC_Vars(iID)%a2dS) )
            ! Calculating esfiltration flow [m/seconds]
            a2dVarFlowExf = (a2dVarVTot - oHMC_Vars(iID)%a2dS)/(1000.0*dDtSubflow) !in m/sec
            ! Updating total volume information
            a2dVarVTot = 1.0*oHMC_Vars(iID)%a2dS 
        endwhere
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Hypodermic flow to fill cell(s)-lake of the dam
        if (iNDam .gt. 0) then
            do iD = 1,iNdam
                iI = 0; iJ = 0;
                iI = oHMC_Vars(iID)%a2iXYDam(iD,2); iJ = oHMC_Vars(iID)%a2iXYDam(iD,1)
                ! Amount of upstream volume at dam section. V set zero at the subroutine begin
                a1dVarVDam(iD) = a1dVarVDam(iD) + a2dVarVTot(iI,iJ)*(oHMC_Vars(iID)%a2dAreaCell(iI,iJ))/1000
            enddo
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Debug
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, '')
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarVTot, oHMC_Vars(iID)%a2iMask, 'VTOT END ') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarVTotStep, oHMC_Vars(iID)%a2iMask, 'VTOTSTEP START ') )
            !call mprintf(.true., iINFO_Extra, checkvar(a2dVarVSub, oHMC_Vars(iID)%a2iMask, 'VSUB END ') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarVLoss, oHMC_Vars(iID)%a2iMask, 'VLOSS END ') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarFlowExf, oHMC_Vars(iID)%a2iMask, 'FLOWEXF END ') ) 
            call mprintf(.true., iINFO_Extra, ' ========= SUBFLOW END ========= ') 
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Updating variable(s)
        oHMC_Vars(iID)%a2dVTot = a2dVarVTot
        oHMC_Vars(iID)%a2dVLoss = a2dVarVLoss
        
        oHMC_Vars(iID)%a2dFlowExf = a2dVarFlowExf
        
        oHMC_Vars(iID)%a1dVDam = a1dVarVDam
        
        ! Info end
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: SubFlow ... OK' )
        endif
        !------------------------------------------------------------------------------------------

    end subroutine HMC_Phys_Convolution_Apps_SubFlow
    !------------------------------------------------------------------------------------------

    !------------------------------------------------------------------------------------------
    ! Subroutine for calculating infiltration/runoff (using horton modified method)
    subroutine HMC_Phys_Convolution_Apps_Horton(iID, iRows, iCols, dDtDataForcing, dDtAct, iTq, iTime, iNTime)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s) declaration
        integer(kind = 4) :: iID, iRows, iCols
        real(kind = 4) :: dDtDataForcing, dDtAct
        
        real(kind = 4) :: dVarVErr
        real(kind = 4) :: dDtHorton
        real(kind = 4) :: dDomainArea

        real(kind = 4), dimension (iRows, iCols)         :: a2dVarVTot, a2dVarVTotPStep
        real(kind = 4), dimension (iRows, iCols)         :: a2dVarVSub
        real(kind = 4), dimension (iRows, iCols)         :: a2dVarRain, a2dVarIntensity
        
        !real(kind = 4), dimension (iRows, iCols)         :: a2dVarB, a2dVarCh, a2dVarVErr
        real(kind = 4), dimension (iRows, iCols)         :: a2dVarG
        
        real(kind = 4), dimension (iRows, iCols)         :: a2dVarRouting, a2dVarFlowDeep
        
        integer(kind = 4) :: iTq, iTime, iNTime
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Variable(s) initialization
        a2dVarVTot = 0.0; a2dVarVTotPStep = 0.0; a2dVarVSub = 0.0
        a2dVarRain = 0.0; a2dVarIntensity = 0.0;
        
        a2dVarRouting = 0.0; a2dVarFlowDeep = 0.0;
        
        !a2dVarG = 0.0; a2dVarCh = 0.0; a2dVarVErr = 0.0; dVarVErr = 0.0;
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Integrating step (horton)
        dDtHorton = dDtAct
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------ 
        ! Domain Area
        dDomainArea =  oHMC_Vars(iID)%dDomainArea
        
        ! Variable(s) from global declaration
        a2dVarVTot = oHMC_Vars(iID)%a2dVTot
        a2dVarVSub = oHMC_Vars(iID)%a2dVSub
        a2dVarRouting = oHMC_Vars(iID)%a2dRouting
        a2dVarFlowDeep = oHMC_Vars(iID)%a2dFlowDeep
        
        !a2dVarB = oHMC_Vars(iID)%a2dCf
        !a2dVarCh = oHMC_Vars(iID)%a2dCostChFix
        !dVarVErr = oHMC_Vars(iID)%dVErr
        
        ! Extracting dynamic forcing variable(s)
        a2dVarRain = oHMC_Vars(iID)%a2dRain
        where (a2dVarRain.lt.0.0.or.a2dVarRain.gt.845.0) a2dVarRain = 0.0
            
        ! Info start
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: Horton ... ' )
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Total volume previous step
        a2dVarVTotPStep = a2dVarVTot
        !------------------------------------------------------------------------------------------
         
        !------------------------------------------------------------------------------------------
        ! Horton filter equation
        where (oHMC_Vars(iID)%a2dS.gt.0.0)
            a2dVarG = oHMC_Vars(iID)%a2dCostF - &
                     (oHMC_Vars(iID)%a2dCostF - oHMC_Vars(iID)%a2dCostF1)/oHMC_Vars(iID)%a2dS*a2dVarVTot
        elsewhere
            a2dVarG = 0.0
        endwhere
        !------------------------------------------------------------------------------------------
                
        !------------------------------------------------------------------------------------------
        ! Debug
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' ========= HORTON START =========== ') 
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarRouting, oHMC_Vars(iID)%a2iMask, 'ROUTING START') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarIntensity, oHMC_Vars(iID)%a2iMask, 'INTENSITY START') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarVTot, oHMC_Vars(iID)%a2iMask, 'VTOT START') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarVSub, oHMC_Vars(iID)%a2iMask, 'VSUB START') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarFlowDeep, oHMC_Vars(iID)%a2iMask, 'FLOWDEEP START') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dHydro, oHMC_Vars(iID)%a2iMask, 'HYDRO UPD START') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dHydroPrev, oHMC_Vars(iID)%a2iMask, 'HYDRO PREV START') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dQDisOut, oHMC_Vars(iID)%a2iMask, 'QOUT START (Qtot)') )
            call mprintf(.true., iINFO_Extra, ' ') 
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dCostChFix, oHMC_Vars(iID)%a2iMask, 'CHFIX ') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dCostF, oHMC_Vars(iID)%a2iMask, 'COSTF ') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dCostF1, oHMC_Vars(iID)%a2iMask, 'COSTF1 ') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarG, oHMC_Vars(iID)%a2iMask, 'G ') )
            !call mprintf(.true., iINFO_Extra, checkvar(a2dVarB, oHMC_Vars(iID)%a2iMask, 'B ') )
            !call mprintf(.true., iINFO_Extra, checkvar(a2dVarCh, oHMC_Vars(iID)%a2iMask, 'CH ') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dS, oHMC_Vars(iID)%a2iMask, 'S ') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dCoeffResol, oHMC_Vars(iID)%a2iMask, 'COEFF RESOL') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarRain, oHMC_Vars(iID)%a2iMask, 'RAIN ') )
            call mprintf(.true., iINFO_Extra, ' ') 
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Defining subterranean volume 
        where ( (a2dVarVTot.lt.oHMC_Vars(iID)%a2dCt*oHMC_Vars(iID)%a2dS) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) )
            a2dVarVSub = 0.0
        elsewhere(oHMC_Vars(iID)%a2dDEM.gt.0.0)
            ! *dDth/3600 perch� a2dCostF1 � in mm/h ma lavoro in mm/dDth
            a2dVarVSub = oHMC_Vars(iID)%a2dF2*(a2dVarVTot - oHMC_Vars(iID)%a2dCt*oHMC_Vars(iID)%a2dS)/ &
                         oHMC_Vars(iID)%a2dS*dDtHorton/3600  
        endwhere   
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Evaluating intensity --> horton initialization = rain + routing drained cells
        a2dVarIntensity = a2dVarRain*3600.0/dDtDataForcing + &
                          oHMC_Vars(iID)%a2dCoeffResol*a2dVarRouting/dDtHorton*3600.0 + &
                          a2dVarFlowDeep*3600.0/dDtDataForcing
        !-------------------------------------------------------------------------------
                       
        !------------------------------------------------------------------------------------------
        ! Intensity Evaluation
        ! Condition ----> Intensity == 0
        where ( (a2dVarIntensity.eq.0.0) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) .and. &
                (a2dVarVTot.ge.oHMC_Vars(iID)%a2dCt*oHMC_Vars(iID)%a2dS) )     
                
            a2dVarVTot = a2dVarVTot - oHMC_Vars(iID)%a2dF2*(a2dVarVTot - oHMC_Vars(iID)%a2dCt*oHMC_Vars(iID)%a2dS)/ &
                         oHMC_Vars(iID)%a2dS*dDtHorton/3600.0	
            
        endwhere
        	
        ! Condition ----> 0 < Intensity <= G					
        where ( (a2dVarIntensity.gt.0.0) .and. (a2dVarIntensity.le.a2dVarG) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) ) 

                where ( (a2dVarVTot.lt.oHMC_Vars(iID)%a2dCt*oHMC_Vars(iID)%a2dS) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) )
                        a2dVarVTot = a2dVarVTot + a2dVarRain/dDtDataForcing*dDtHorton + &
                                     oHMC_Vars(iID)%a2dCoeffResol*a2dVarRouting + &
                                     a2dVarFlowDeep/dDtDataForcing*dDtHorton
                        a2dVarIntensity = 0.0
                elsewhere(oHMC_Vars(iID)%a2dDEM.gt.0.0)
                        a2dVarVTot = a2dVarVTot + a2dVarIntensity*dDtHorton/3600.0 - a2dVarVSub
                        a2dVarIntensity = 0.0
                endwhere
                
        endwhere

        ! Condition ----> Intensity > G	
        where ( (a2dVarIntensity.gt.a2dVarG) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) ) 						

                where ( (a2dVarVTot.lt.oHMC_Vars(iID)%a2dCt*oHMC_Vars(iID)%a2dS) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) )
                        a2dVarVTot = a2dVarVTot + a2dVarG*dDtHorton/3600.0              
                elsewhere (oHMC_Vars(iID)%a2dDEM.gt.0.0)
                        a2dVarVTot = a2dVarVTot + a2dVarG*dDtHorton/3600.0 - a2dVarVSub           
                endwhere
                
                a2dVarIntensity = a2dVarIntensity - a2dVarG

        endwhere			
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Updating intensity variable
        where ( (a2dVarVTot.gt.oHMC_Vars(iID)%a2dS) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) )
                a2dVarIntensity =  a2dVarIntensity + (a2dVarVTot - oHMC_Vars(iID)%a2dS)/dDtHorton*3600.0
                a2dVarVTot = oHMC_Vars(iID)%a2dS
        endwhere
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Calculating mass balance errors
        where ( (a2dVarRain.lt.0.0) .and. (oHMC_Vars(iID)%a2dDEM.gt.0.0) ) a2dVarRain = 0.0 ! Checking rain
        
        ! Calculating Volume error
        where ( oHMC_Vars(iID)%a2dDEM.gt.0.0 )
            
                !a2dVarVErr = a2dVarFlowDeep/dDtDataForcing*dDtHorton + &
                !             a2dVarRain/dDtDataForcing*dDtHorton + oHMC_Vars(iID)%a2dCoeffResol*a2dVarRouting - &
                !             a2dVarIntensity*dDtHorton/3600.0 - &
                !             (a2dVarVTot - a2dVarVTotPStep + a2dVarVSub)

                where (a2dVarVTot.lt.0.0)
                        a2dVarVTot = 0.0
                endwhere

        endwhere
        
        ! Cumulative mean error
        !dVarVErr = dVarVErr + SUM(SUM(a2dVarVErr, DIM=1, mask=oHMC_Vars(iID)%a2dDEM.gt.0.0))/dDomainArea !DIM=1 columns
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Debug
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, '')
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarRouting, oHMC_Vars(iID)%a2iMask, 'ROUTING END') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarIntensity, oHMC_Vars(iID)%a2iMask, 'INTENSITY END') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarVTot, oHMC_Vars(iID)%a2iMask, 'VTOT END') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarVSub, oHMC_Vars(iID)%a2iMask, 'VSUB END') )
            call mprintf(.true., iINFO_Extra, checkvar(a2dVarFlowDeep, oHMC_Vars(iID)%a2iMask, 'FLOWDEEP END') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dHydro, oHMC_Vars(iID)%a2iMask, 'HYDRO UPD END') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dHydroPrev, oHMC_Vars(iID)%a2iMask, 'HYDRO PREV END') )
            call mprintf(.true., iINFO_Extra, checkvar(oHMC_Vars(iID)%a2dQDisOut, oHMC_Vars(iID)%a2iMask, 'QOUT END (Qtot)') )
            call mprintf(.true., iINFO_Extra, ' ========= HORTON END =========== ') 
        endif
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Updating field(s) in global declaration
        oHMC_Vars(iID)%a2dVTot = a2dVarVTot
        oHMC_Vars(iID)%a2dVSub = a2dVarVSub
       
        oHMC_Vars(iID)%a2dIntensity = a2dVarIntensity
        oHMC_Vars(iID)%a2dFlowDeep = a2dVarFlowDeep
        
        oHMC_Vars(iID)%a2dRain = a2dVarRain
        
        !oHMC_Vars(iID)%a2dVErr = a2dVarVErr
        !oHMC_Vars(iID)%dVErr = dVarVErr
        
        ! Info end
        if (iDEBUG.gt.0) then
            call mprintf(.true., iINFO_Extra, ' Phys :: Convolution :: Horton ... OK' )
        endif
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Phys_Convolution_Apps_Horton
    !------------------------------------------------------------------------------------
    
    !------------------------------------------------------------------------------------------
    ! Subroutine to compute out dam discharge
    subroutine HMC_Phys_Convolution_Apps_Discharge_Dam(iID, iNDam, dDt, &
                                                       a1dVarVDam, a1dVarHDam, a1dVarLDam, a1dVarCoeffDam,  &
                                                       a1dVarQoutDam, iTq, iDtMax)
                                                    
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4)           :: iID
        integer(kind = 4)           :: iI, iJ, iD, iK, iRank, iTq, iDtMax
        integer(kind = 4)           :: iNDam
        real(kind = 4)              :: dDt, dTV, dQtmp, dDamSpillH
        
        character(len = 256)                        :: sQtmp, sD, sCoeffDam, sHDam, sHMaxDam
        
        integer(kind = 4)                           :: iFlagD
        
        integer(kind = 4), dimension (iNDam, 2)     :: a2iVarXYDam
        real(kind = 4), dimension (iNDam)           :: a1dVarQcSLDam, a1dVarHMaxDam, a1dVarVMaxDam
        
        real(kind = 4), dimension (iNDam)           :: a1dVarVDam, a1dVarHDam, a1dVarLDam, a1dVarCoeffDam
        
        real(kind = 4), dimension (iNDam)           :: a1dVarQoutDam
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Initialize variable(s)
        a2iVarXYDam = 0;
        a1dVarVMaxDam = 0.0; a1dVarQcSLDam = 0.0; a1dVarHMaxDam = 0.0;
        a1dVarQoutDam = 0.0
        
        iFlagD = 0; dTV = 0
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Get global information
        dTV = oHMC_Namelist(iID)%dTV    ! Volume percentage to start with outgoing dam flow
        dDamSpillH = oHMC_Namelist(iID)%dDamSpillH ! Difference between dam and spill 
        
        a2iVarXYDam = oHMC_Vars(iID)%a2iXYDam
        a1dVarQcSLDam = oHMC_Vars(iID)%a1dQcSLDam
        a1dVarHMaxDam = oHMC_Vars(iID)%a1dHMaxDam
        a1dVarVMaxDam = oHMC_Vars(iID)%a1dVMaxDam
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Check dam availability
        if (iNDam .gt. 0) then

            !------------------------------------------------------------------------------------------
            ! Cycle on dam
            do iD = 1, iNDam
                
                !------------------------------------------------------------------------------------------
                ! Check limit(s)
                if ( (a1dVarCoeffDam(iD) .gt. 0.0) .and. (a1dVarVDam(iD) .gt. dTV*a1dVarVMaxDam(iD)) ) then  
                   
                    !------------------------------------------------------------------------------------------
                    ! Get dam indexes
                    iI = 0; iJ = 0;
                    iI = a2iVarXYDam(iD,2); iJ = a2iVarXYDam(iD,1)
		    !------------------------------------------------------------------------------------------
                    
                    !write(*,*) iI, iJ, a1dVarVDam(iD), a1dVarVMaxDam(iD), a1dVarCoeffDam(iD), a1dVarQoutDam(iD)
                    
                    !------------------------------------------------------------------------------------------
                    ! Discharge in [m^3/s]
                    a1dVarQoutDam(iD) = (a1dVarVDam(iD) - dTV*a1dVarVMaxDam(iD))*a1dVarCoeffDam(iD) 
                    
                    if ( a1dVarQoutDam(iD).gt.a1dVarQcSLDam(iD) ) a1dVarQoutDam(iD) = a1dVarQcSLDam(iD)

                    ! Update dam volume
                    a1dVarVDam(iD) = a1dVarVDam(iD) - a1dVarQoutDam(iD)*dDt
                    ! Discharge in [mm]
                    a1dVarQoutDam(iD) = a1dVarQoutDam(iD)*1000*dDt/(oHMC_Vars(iID)%a2dAreaCell(iI,iJ))
                    
                    if (a1dVarVDam(iD) .lt. 0.0) then
                        a1dVarVDam(iD) = 0.0
                        a1dVarQoutDam(iD) = 0.0
                    endif
                    !------------------------------------------------------------------------------------------
                    
                endif
                !------------------------------------------------------------------------------------------

                !------------------------------------------------------------------------------------------
                ! Update dam outflow coefficient at the integration last step
                if (iTq .eq. iDtMax) then
                    
                    !------------------------------------------------------------------------------------------
                    ! Re-initialize dam height
                    a1dVarHDam(iD) = 0.0
                    !------------------------------------------------------------------------------------------
                    
                    !------------------------------------------------------------------------------------------
                    ! Check considering 0.95 total volume
                    if ( a1dVarVDam(iD) .gt. dTV*a1dVarVMaxDam(iD) ) then

                        !------------------------------------------------------------------------------------------
                        ! Check dam length
                        if (a1dVarLDam(iD) .le. 0) then
                            a1dVarLDam(iD) = 40; ! [m]
                        endif
                        !------------------------------------------------------------------------------------------
                        
                        !------------------------------------------------------------------------------------------
                        ! Compute H dam
                        ! Linear interpolation
                        iFlagD = 0
                        iRank = size(oHMC_Vars(iID)%a2dVDam, dim=2)
                        ! Cycle on array dimension
                        do iK = iRank, 1, -2
                            
                            ! Check TV curve availability
                            if ( (oHMC_Vars(iID)%a2dVDam(iNDam, iK) .gt. a1dVarVDam(iD)) .and. &
                                 (oHMC_Vars(iID)%a2dVDam(iNDam, iK-1) .lt. a1dVarVDam(iD))  ) then 
                                ! TV curve defined 
                                iFlagD = 1
                                a1dVarHDam(iD) = oHMC_Vars(iID)%a2dLDam(iD,iK-1) + &
                                                 (oHMC_Vars(iID)%a2dLDam(iD,iK) - oHMC_Vars(iID)%a2dLDam(iD,iK-1))* &
                                                 (a1dVarVDam(iD) - oHMC_Vars(iID)%a2dVDam(iD,iK-1))/ &
                                                 (oHMC_Vars(iID)%a2dVDam(iD,iK) - oHMC_Vars(iID)%a2dVDam(iD,iK-1))

                            elseif (oHMC_Vars(iID)%a2dVDam(iNDam, iK) .lt. 0.0) then
                                ! TV curve undefined
                                iFlagD = 2  
                            else
                                iFlagD = 0
                            endif

                        enddo

                        if (iFlagD .eq. 0) then !Sono fuori dalla curva invaso volume
                            a1dVarHDam(iD) = oHMC_Vars(iID)%a2dLDam(iD,iRank) + &       
                                             (oHMC_Vars(iID)%a2dLDam(iD,iRank) - oHMC_Vars(iID)%a2dLDam(iD,iRank-1))* &                                        
                                             (a1dVarVDam(iD) - oHMC_Vars(iID)%a2dVDam(iD,iRank))/ &                                       
                                             (oHMC_Vars(iID)%a2dVDam(iD,iRank) - oHMC_Vars(iID)%a2dVDam(iD,iRank-1))
                        endif
                        
                        if (iFlagD .eq. 2) then !Non ho la curva invaso volume uso relazione lineare
                            a1dVarHDam(iD) = a1dVarHMaxDam(iD)*a1dVarVDam(iD)/a1dVarVMaxDam(iD)
                        endif    
                        !------------------------------------------------------------------------------------------
                            
                        !------------------------------------------------------------------------------------------
                        ! Check Hdam > Hdammax-3 (if true starting with dam outgoing flow)
                        if ( a1dVarHDam(iD) .gt. (a1dVarHMaxDam(iD) - dDamSpillH) ) then

                            ! Outgoing dam discharge [m^3/s]
                            dQtmp = 0.0;
                            dQtmp = 0.385*a1dVarLDam(iD)*( (2*9.81)**0.5)*(a1dVarHDam(iD) - (a1dVarHMaxDam(iD) - 3) )**1.5

                            ! Check Hdam > Hdammax
                            if ( a1dVarHDam(iD) .gt. a1dVarHMaxDam(iD) ) then
                                ! Exceeded volume used for outgoing dam discharge [m^3/s]
                                dQtmp = (a1dVarVDam(iD) - a1dVarVMaxDam(iD))/3600

                                ! Check Qdam <= Qdamoutmax 
                                if (dQtmp .gt. a1dVarQcSLDam(iD)) then
                                    dQtmp = a1dVarQcSLDam(iD)
                                endif

                            endif

                        else
                            dQtmp = 0.0;
                        endif
                        !------------------------------------------------------------------------------------------

                        !------------------------------------------------------------------------------------------
                        ! Compute dam outgoing flow coefficient [1/s]
                        if (dQtmp .gt. 0.0) then
                            a1dVarCoeffDam(iD) = dQtmp/(a1dVarVDam(iD) - dTV*a1dVarVMaxDam(iD))
                        else
                            a1dVarCoeffDam(iD) = 0.000
                        endif
                        !------------------------------------------------------------------------------------------
                        
                    endif
                    !------------------------------------------------------------------------------------------
                    
                    !------------------------------------------------------------------------------------------
                    ! Info dam coefficient updating
                    write(sQtmp, *) dQtmp; write(sD, *) iD; write(sCoeffDam, *) a1dVarCoeffDam(iD); 
                    write(sHDam, *) a1dVarHDam(iD); write(sHMaxDam, *) a1dVarHMaxDam(iD)
                    call mprintf(.true., iINFO_Verbose, &
                                ' Phys :: Convolution :: Discharge Dam :: NDam: '//trim(sD)//' [-]'// &
                                ' QDam: '//trim(sQtmp)//' [m^3/s]'// &
                                ' CoeffDam: '//trim(sCoeffDam)//' [-]'// &
                                ' HDam: '//trim(sHDam)//' [m]'// &
                                ' HMaxDam: '//trim(sHMaxDam)//' [m]')
                    !------------------------------------------------------------------------------------------
                    
                endif
                !------------------------------------------------------------------------------------------

            enddo
            !------------------------------------------------------------------------------------------

        endif
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Phys_Convolution_Apps_Discharge_Dam
    !------------------------------------------------------------------------------------------
    
end module HMC_Module_Phys_Convolution_Apps
!------------------------------------------------------------------------------------------