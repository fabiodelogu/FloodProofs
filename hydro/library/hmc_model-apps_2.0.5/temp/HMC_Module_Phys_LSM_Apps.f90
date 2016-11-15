 !------------------------------------------------------------------------------------
! File:   HMC_Module_Phys_LSM_Apps.f90
!
! Author:   Fabio Delogu
! Date:     20150210
!
! Force-Restore applications module
!------------------------------------------------------------------------------------

!------------------------------------------------------------------------------------
! Module Header
module HMC_Module_Phys_LSM_Apps

    !------------------------------------------------------------------------------------
    ! External module(s) 
    use HMC_Module_Namelist,           only:    oHMC_Namelist
    use HMC_Module_Vars_Loader,        only:    oHMC_Vars
   
    use HMC_Module_Tools_Debug
    
    use HMC_Module_Tools_Time,          only:   HMC_Tools_Time_MonthVal
    
    ! Implicit none for all subroutines in this module
    implicit none
    !------------------------------------------------------------------------------------------

contains

    !------------------------------------------------------------------------------------------
    ! Subroutine for calculating beta function
    subroutine HMC_Phys_LSM_Apps_BetaFunction(iID, iRows, iCols, &
                                a2dVarSM, a2dVarDEM, &
                                a2dVarBF)
                                                   
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4)       :: iID, iRows, iCols
        real(kind = 4)          :: dBFMin, dBFMax
        real(kind = 4), dimension(iRows, iCols) :: a2dVarSM, a2dVarDEM
        real(kind = 4), dimension(iRows, iCols) :: a2dVarBF 
        real(kind = 4), dimension(iRows, iCols) :: a2dVarCt
        real(kind = 4), dimension(iRows, iCols) :: a2dVarCtWP, a2dVarKb1, a2dVarKc1, a2dVarKb2, a2dVarKc2
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Constant(s)
        dBFMin = oHMC_Namelist(iID)%dBFMin
        dBFMax = oHMC_Namelist(iID)%dBFMax 
        ! Static variable(s)
        a2dVarCt = oHMC_Vars(iID)%a2dCt
        a2dVarCtWP = oHMC_Vars(iID)%a2dCtWP
        a2dVarKb1 = oHMC_Vars(iID)%a2dKb1
        a2dVarKc1 = oHMC_Vars(iID)%a2dKc1
        a2dVarKb2 = oHMC_Vars(iID)%a2dKb2 
        a2dVarKc2 = oHMC_Vars(iID)%a2dKc2 
        
        ! Info start
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: BetaFuntion ... ' )
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Calculating Beta function values
        where (a2dVarSM.lt.a2dVarCtWP.and.a2dVarDEM.gt.0.0)
                a2dVarBF = dBFMin
        elsewhere ((a2dVarSM.ge.a2dVarCtWP).and.(a2dVarSM.le.a2dVarCt).and.(a2dVarDEM.gt.0.))
                a2dVarBF = a2dVarKb1*a2dVarSM + a2dVarKc1
        elsewhere (a2dVarDEM.gt.0.0)
                a2dVarBF = a2dVarKb2*a2dVarSM + a2dVarKc2       
        endwhere
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Debug
        !call surf(a2dVarBF,pm3d='pm3d implicit map', palette='rgbformulae 31, -11, 32')
        !write(*,*) 'VAR BF' , sum(a2dVarBF)/max(1,count(a2dVarBF.gt.0.0))
        
        ! Info end
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: BetaFuntion ... OK' )
        !------------------------------------------------------------------------------------------

    end subroutine HMC_Phys_LSM_Apps_BetaFunction
    !------------------------------------------------------------------------------------------
    
    !------------------------------------------------------------------------------------------
    ! Calculating CH 
    subroutine HMC_Phys_LSM_Apps_CH(iID, iRows, iCols, sTime, &
                              a2dVarDEM, &
                              a2dVarRb, &
                              a2dVarCH)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4)       :: iID, iRows, iCols, iT, iStep    
        
        real(kind = 4)          :: dVarCH, dVarCHn, dVarPSI
        
        real(kind = 4), dimension(iRows, iCols) :: a2dVarDEM, a2dVarRb, a2dVarPSIstable
        real(kind = 4), dimension(iRows, iCols) :: a2dVarCH
        
        character(len = 19)       :: sTime
        character(len = 12)       :: sTimeMonth
        !------------------------------------------------------------------------------------------                
        
        !------------------------------------------------------------------------------------------
        ! Initialize variable(s)
        a2dVarPSIstable = 0.0
        ! Checking date
        write(sTimeMonth,'(A,A,A)') sTime(1:4), sTime(6:7), sTime(9:10)
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Constant(s)
        call HMC_Tools_Time_MonthVal(oHMC_Namelist(iID)%a1dCHMonthly, sTimeMonth, dVarCH)
        
        ! Static variable(s)
        dVarPSI = log(2.0)
        dVarCHn = exp(dVarCH)
        
        ! Info start
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: CH ... ' )
        
        ! Debug
        !call mprintf(.true., iINFO_Extra, checkvar(a2dVarCH, int(a2dVarDEM), 'CH START') )
        !call mprintf(.true., iINFO_Extra, checkvar(a2dVarRb, int(a2dVarDEM), 'RB START') )
        !call mprintf(.true., iINFO_Extra, checkvar(a2dVarPSIstable, int(a2dVarDEM), 'PSISTABLE START') )
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Calculating PSI stable values (from 1 to 3)
        where(a2dVarRb.le.0.0.and.a2dVarDEM.gt.0.0)
            a2dVarPSIstable = 1 + exp(dVarPSI)*(1 - exp(10*a2dVarRb))
        elsewhere(a2dVarDEM.gt.0.0)
            a2dVarPSIstable = 1.0
        endwhere
        
        ! Calculating CH values
        a2dVarCH = dVarCHn*a2dVarPSIstable
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Debug
        !call mprintf(.true., iINFO_Extra, checkvar(a2dVarCH, int(a2dVarDEM), 'CH END') )
        !call mprintf(.true., iINFO_Extra, checkvar(a2dVarRb, int(a2dVarDEM), 'RB END') )
        !call mprintf(.true., iINFO_Extra, checkvar(a2dVarPSIstable, int(a2dVarDEM), 'PSISTABLE END') )
        
        ! Info end
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: CH ... OK' )
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Phys_LSM_Apps_CH
    !------------------------------------------------------------------------------------------
    
    !------------------------------------------------------------------------------------------
    ! Subroutine for solving force restore equation using runge-kutta 4
    subroutine HMC_Phys_LSM_Apps_RK4(iID, iRows, iCols, & 
                            dTRef, &
                            dIntStep, iIntDelta, &
                            a2dVarTDeep, a2dVarPit, a2dVarCH, a2dVarBF, &
                            a2dVarRn, &
                            a2dVarRelHum, a2dVarWind, a2dVarTaK, a2dVarPa, & 
                            a2dVarLambda, a2dVarEA, a2dVarRhoA, &
                            a2dVarLSTPStep, a2dVarLSTUpd)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4)       :: iID, iRows, iCols
        integer(kind = 4)       :: iIntDelta
        
        real(kind = 4)          :: dTRef, dIntStep
        real(kind = 4)          :: dCp, dPiGreco, dOmega
        
        real(kind = 4), dimension(iRows, iCols) :: a2dVarDEM
        real(kind = 4), dimension(iRows, iCols) :: a2dVarTDeep, a2dVarPit, a2dVarCH, a2dVarBF
        real(kind = 4), dimension(iRows, iCols) :: a2dVarRn
        real(kind = 4), dimension(iRows, iCols) :: a2dVarRelHum, a2dVarWind, a2dVarTaK, a2dVarPa
        real(kind = 4), dimension(iRows, iCols) :: a2dVarLambda, a2dVarEA, a2dVarRhoA
        real(kind = 4), dimension(iRows, iCols) :: a2dVarLSTPStep, a2dVarLSTUpd
        real(kind = 4), dimension(iRows, iCols) :: a2dVarK1, a2dVarK2, a2dVarK3, a2dVarK4
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Constant(s)
        dCp = oHMC_Namelist(iID)%dCp        ! Specific heat (cost pressure)
        ! Static variable(s)
        dPiGreco = 3.14                     ! Pi greco
        dOmega = 1.0/(60.0*60.0*24.0)       ! Day length
        ! Extracting static variable(s)
        a2dVarDEM = oHMC_Vars(iID)%a2dDem
        ! Info start
        !call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: RK4 ... ' )
        
        ! Debug
        !call mprintf(.true., iINFO_Extra, checkvar(a2dVarLSTPStep, int(a2dVarDEM), 'LST INT START') )
        !------------------------------------------------------------------------------------------
       
        !------------------------------------------------------------------------------------------
        ! Updating land surface temperature using Runge-Kutta (fourth order)
        a2dVarLSTUpd = 0.0
        a2dVarK1 = 0.0; a2dVarK2 = 0.0; a2dVarK3 = 0.0; a2dVarK4 = 0.0
        where (a2dVarDEM.gt.0.0)
            
            ! K1
            a2dVarLSTUpd = a2dVarLSTPStep
            
            a2dVarK1 = iIntDelta *(2*sqrt(dPiGreco*dOmega)/a2dVarPit*(a2dVarRn - &
            a2dVarRhoA*dCp*a2dVarCH*a2dVarWind*(a2dVarLSTUpd - a2dVarTaK) - &
            a2dVarRhoA*a2dVarLambda*a2dVarCH*a2dVarWind*a2dVarBF*(0.611*exp(17.3*(a2dVarLSTUpd - dTRef)/ &
            (237.3 + a2dVarLSTUpd - dTRef)) - a2dVarEA)/a2dVarPa*0.622) - &
            2*dPiGreco*dOmega*(a2dVarLSTUpd - a2dVarTDeep))
        elsewhere
            ! Otherwise
            a2dVarLSTUpd = 0.0
        endwhere
        
        ! Debug
        !call mprintf(.true., iINFO_Verbose, checkvar(a2dVarK1, int(a2dVarDEM), 'K1') )
        
        where (a2dVarDEM.gt.0.0)  
            ! K2
            a2dVarLSTUpd = a2dVarLSTPStep + a2dVarK1/2.0
            
            a2dVarK2 = iIntDelta *( 2*sqrt(dPiGreco*dOmega)/a2dVarPit*(a2dVarRn - &
            a2dVarRhoA*dCp*a2dVarCH*a2dVarWind*(a2dVarLSTUpd - a2dVarTaK) - &
            a2dVarRhoA*a2dVarLambda*a2dVarCH*a2dVarWind*a2dVarBF*(0.611*exp(17.3*(a2dVarLSTUpd - dTRef)/ &
            (237.3 + a2dVarLSTUpd - dTRef)) - a2dVarEA)/a2dVarPa*0.622) - &
            2*dPiGreco*dOmega*(a2dVarLSTUpd - a2dVarTDeep))
        elsewhere
            ! Otherwise
            a2dVarLSTUpd = 0.0
        endwhere
        
        ! Debug
        !call mprintf(.true., iINFO_Verbose, checkvar(a2dVarK2, int(a2dVarDEM), 'K2') )
        
        where (a2dVarDEM.gt.0.0) 
            ! K3
            a2dVarLSTUpd = a2dVarLSTPStep + a2dVarK2/2.0
            
            a2dVarK3 = iIntDelta *( 2*sqrt(dPiGreco*dOmega)/a2dVarPit*(a2dVarRn - &
            a2dVarRhoA*dCp*a2dVarCH*a2dVarWind*(a2dVarLSTUpd - a2dVarTaK) - &
            a2dVarRhoA*a2dVarLambda*a2dVarCH*a2dVarWind*a2dVarBF*(0.611*exp(17.3*(a2dVarLSTUpd - dTRef)/ &
            (237.3 + a2dVarLSTUpd - dTRef)) - a2dVarEA)/a2dVarPa*0.622) - &
            2*dPiGreco*dOmega*(a2dVarLSTUpd - a2dVarTDeep))
        elsewhere
            ! Otherwise
            a2dVarLSTUpd = 0.0
        endwhere
        
        ! Debug
        !call mprintf(.true., iINFO_Verbose, checkvar(a2dVarK3, int(a2dVarDEM), 'K3') )
        
        where (a2dVarDEM.gt.0.0) 
            ! K4
            a2dVarLSTUpd = a2dVarLSTPStep + a2dVarK3
            
            a2dVarK4 = iIntDelta *( 2*sqrt(dPiGreco*dOmega)/a2dVarPit*(a2dVarRn - &
            a2dVarRhoA*dCp*a2dVarCH*a2dVarWind*(a2dVarLSTUpd - a2dVarTaK) - &
            a2dVarRhoA*a2dVarLambda*a2dVarCH*a2dVarWind*a2dVarBF*(0.611*exp(17.3*(a2dVarLSTUpd - dTRef)/ &
            (237.3 + a2dVarLSTUpd - dTRef)) - a2dVarEA)/a2dVarPa*0.622) - &
            2*dPiGreco*dOmega*(a2dVarLSTUpd - a2dVarTDeep))

            ! Updating LST
            a2dVarLSTUpd = a2dVarLSTPStep + (a2dVarK1 + (2.*(a2dVarK2 + a2dVarK3)) + a2dVarK4)/6.0
            
        elsewhere
            ! Otherwise
            a2dVarLSTUpd = 0.0
        endwhere
        
        ! Debug
        !call mprintf(.true., iINFO_Verbose, checkvar(a2dVarK4, int(a2dVarDEM), 'K4') )

        ! Debug
        !call mprintf(.true., iINFO_Extra, checkvar(a2dVarLSTPStep, int(a2dVarDEM), 'LST INT END') )
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Info end
        !call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: RK4 ... OK' )
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Phys_LSM_Apps_RK4
    !------------------------------------------------------------------------------------------
    
    !------------------------------------------------------------------------------------------
    ! Subroutine for calculating deep soil temperature
    subroutine HMC_Phys_LSM_Apps_TDeep(iID, iRows, iCols, iT, &
                                   a2dVarDEM, &
                                   a2dVarTaK, &
                                   a2dVarTDeep)
                        
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4)       :: iID, iRows, iCols, iT, iStep
        integer(kind = 4)       :: iDayThr, iTMarkedSteps, iDaySteps, iTdeepShift
        real(kind = 4)          :: dTRef
        
        real(kind = 4), dimension(iRows, iCols) :: a2dVarTaK, a2dVarDEM
        real(kind = 4), dimension(iRows, iCols) :: a2dVarTaK24, a2dVarTaK12
        
        real(kind = 4), dimension(iRows, iCols) :: a2dVarTDeep
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Constant(s)
        dTRef = oHMC_Namelist(iID)%dTRef
        iTdeepShift = oHMC_Namelist(iID)%iTdeepShift
        ! Static variable(s)
        iDaySteps = oHMC_Namelist(iID)%iDaySteps
        iTMarkedSteps = oHMC_Namelist(iID)%iTMarkedSteps
        
        ! Info start
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: TDeep ... ' )
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Calculating deep soil temperature
        
        ! Initializing and updating temperature 3d mean field(s)
        if (all(oHMC_Vars(iID)%a3dTaK24.le.0.0))then
            
            call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: TDeep :: '// &
                                              ' First mean temperature 3d field storing step ... ')

            do iStep=1, int(iDaySteps)
                where(a2dVarDEM.gt.0.0)
                    oHMC_Vars(iID)%a3dTaK24(:,:,int(iStep)) =  a2dVarTaK
                elsewhere
                    oHMC_Vars(iID)%a3dTaK24(:,:,int(iStep)) =  0.0
                endwhere
            enddo
            
            ! Updating with new field
            where(a2dVarDEM.gt.0.0)
                oHMC_Vars(iID)%a3dTaK24(:,:,int(iDaySteps)) =  a2dVarTaK + 10
            elsewhere
                oHMC_Vars(iID)%a3dTaK24(:,:,int(iDaySteps)) = 0.0
            endwhere
            
            call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: TDeep :: '// &
                                              ' First mean temperature 3d field storing step ... OK')
            
        else
            ! Re-initializing 
            do iStep=2, int(iDaySteps)
                oHMC_Vars(iID)%a3dTaK24(:,:,int(iStep-1)) = oHMC_Vars(iID)%a3dTaK24(:,:,int(iStep))
            enddo
            ! Updating with new field
            where(a2dVarDEM.gt.0.0)
                oHMC_Vars(iID)%a3dTaK24(:,:,int(iDaySteps)) =  a2dVarTaK
            elsewhere
                oHMC_Vars(iID)%a3dTaK24(:,:,int(iDaySteps)) = 0.0
            endwhere
            
        endif
        
        ! Calculating mean temperature last 12 and 24 hours
        where(a2dVarDEM.gt.0.0)
            a2dVarTaK24 = sum(oHMC_Vars(iID)%a3dTaK24(:,:,1:int(iDaySteps)),3)/(iDaySteps)
            a2dVarTaK12 = sum(oHMC_Vars(iID)%a3dTaK24(:,:,int(iDaySteps/2+1):int(iDaySteps)),3)/int(iDaySteps/2.) 
        elsewhere
            a2dVarTaK24 = 0.0
            a2dVarTaK12 = 0.0
        endwhere
        
        ! Initializing and updating temperature 3d mean field(s)
        if (all(oHMC_Vars(iID)%a3dTaKMarked.le.0.0))then
            
            call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: TDeep :: '// &
                                              ' First marked temperature 3d field storing step ... ')
            do iStep=1, int(iTMarkedSteps)
                where(a2dVarDEM.gt.0.0)
                    oHMC_Vars(iID)%a3dTaKMarked(:,:,iStep) = 17.3 + dTRef
                elsewhere
                    oHMC_Vars(iID)%a3dTaKMarked(:,:,iStep) =  0.0
                endwhere
            enddo
            
            call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: TDeep :: '// &
                                              ' First marked temperature 3d field storing step ... OK ')
        else
            ! Re-initializing 
            do iStep = 2, int(iTMarkedSteps)
                oHMC_Vars(iID)%a3dTaKMarked(:,:,int(iStep-1)) = oHMC_Vars(iID)%a3dTaKMarked(:,:,int(iStep))
            enddo
            
            ! Updating with new field
            where(a2dVarDEM.gt.0.0)
                oHMC_Vars(iID)%a3dTaKMarked(:,:,iTMarkedSteps) = a2dVarTaK24 + (a2dVarTaK12 - a2dVarTaK24)/exp(1.0) 
            elsewhere
                oHMC_Vars(iID)%a3dTaKMarked(:,:,iTMarkedSteps) = 0.0
            endwhere
        
        endif
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Calculating deep soil temperature [k] 
        a2dVarTDeep = oHMC_Vars(iID)%a3dTaKMarked(:,:,iTMarkedSteps - iTdeepShift*int(iDaySteps/24) )
        ! Info end
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: TDeep ... OK' )
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Phys_LSM_Apps_TDeep
    !------------------------------------------------------------------------------------------

    !------------------------------------------------------------------------------------------
    ! Subroutine for calculating thermal inertia
    subroutine HMC_Phys_LSM_Apps_ThermalInertia(iID, iRows, iCols, &
                                            a2dVarSM, a2dVarDEM, a2dVarPit)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4)       :: iID, iRows, iCols
        real(kind = 4)          :: dRhoS, dRhoW, dCpS, dCpW, dKq, dKw, dKo, dFqS, dPorS
        real(kind = 4), dimension(iRows, iCols) :: a2dVarSM, a2dVarDEM
        
        real(kind = 4) :: dRhoDa, dKDa
        real(kind = 4), dimension(iRows, iCols) :: a2dVarSMTemp, a2dVarC, a2dVarFqS, a2dVarKe
        real(kind = 4), dimension(iRows, iCols) :: a2dKsol, a2dKsolsat, a2dVarKs, a2dVarPit
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Constant(s)
        dRhoS = oHMC_Namelist(iID)%dRhoS
        dRhoW = oHMC_Namelist(iID)%dRhoW
        dCpS = oHMC_Namelist(iID)%dCpS
        dCpW = oHMC_Namelist(iID)%dCpW
        dKq = oHMC_Namelist(iID)%dKq
        dKw = oHMC_Namelist(iID)%dKw
        dKo = oHMC_Namelist(iID)%dKo
        dFqS = oHMC_Namelist(iID)%dFqS
        dPorS = oHMC_Namelist(iID)%dPorS
        ! Info start
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: ThermalInertia ... ' )
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Initialization variable(s)
        a2dVarSMTemp = 0.0;
        a2dVarC = 0.0;          ! Heat Capacity
        a2dVarFqS = 0.0;
        a2dVarKe = 0.0;
        a2dKsol = 0.0;
        a2dVarKs = 0.0;
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Quartz soil fraction [⅜]
        a2dVarFqS = dFqS
        ! Soil Moisture Temp
        a2dVarSMTemp = a2dVarSM
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Variable(s) conditions
        where( (a2dVarDEM.gt.0.0) .and. (a2dVarSM.gt.10.0) ) a2dVarSMTemp = 1.0
        where( (a2dVarDEM.gt.0.0) .and. (a2dVarSM.lt.0.0) ) a2dVarSMTemp = 0.0
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Heat Capacity [J K^-1 m^-3]
        where( a2dVarDEM.gt.0.0)
            a2dVarC = (1 - dPorS)*dRhoS*dCpS + dPorS*a2dVarSMTemp*dRhoW*dCpW
        endwhere
        
        ! Air dry density [kg m^-3]
        dRhoDa = (1 - dPorS)*dRhoS
        ! Air dry conductivity [W m^-1 K^-1]
        dKDa = (0.135*dRhoDa+64.7)/(dRhoS - 0.947*dRhoDa)
        ! Solids conductivity [W m^-1 K^-1]	
        a2dKsol = dKq**(a2dVarFqS)*dKo**(1-a2dVarFqS)
        ! Saturated soil conductivity [W m^-1 K^-1]
        a2dKsolsat = a2dKsol**(1 - dPorS)*dKw**(dPorS)
        
        ! Kersten number (funzione solo del grado di saturazione VV per terreni sottili)
        where (a2dVarDEM.gt.0.0)
            
            where(a2dVarSMTemp.ge.0.1) 
                    a2dVarKe = log10(a2dVarSMTemp) + 1
            elsewhere
                    a2dVarKe = log10(0.1) + 1
            endwhere

            ! Soil thermal conductivity [W m^-1 K^-1]
            a2dVarKs = a2dVarKe*(a2dKsolsat - dKDa) + dKDa
            ! Thermal Inertia[J m^-2 K S^-(1/2)]
            a2dVarPit = sqrt(a2dVarC*a2dVarKs)
            
        elsewhere
            a2dVarPit = 0.0
        endwhere
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Info end
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: ThermalInertia ... OK' )
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Phys_LSM_Apps_ThermalInertia
    !------------------------------------------------------------------------------------------
 
    !------------------------------------------------------------------------------------------
    ! Subroutine for calculating Richardson number
    subroutine HMC_Phys_LSM_Apps_Richardson(iID, iRows, iCols, & 
                                        a2dVarDEM, &
                                        a2dVarWind, a2dVarTaK, a2dVarPa, &
                                        a2dVarLST, & 
                                        a2dVarRb)
        
        !------------------------------------------------------------------------------------------
        ! Variable(s)
        integer(kind = 4) :: iID, iRows, iCols
        
        real(kind = 4) :: dZRef, dCp, dG, dRd
        
        real(kind = 4), dimension(iRows, iCols) :: a2dVarDEM
        real(kind = 4), dimension(iRows, iCols) :: a2dVarWind, a2dVarTaK, a2dVarPa, a2dVarLST
        real(kind = 4), dimension(iRows, iCols) :: a2dVarTp, a2dVarTp0
        real(kind = 4), dimension(iRows, iCols) :: a2dVarRb
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Constant(s)
        dZRef = oHMC_Namelist(iID)%dZRef
        dG = oHMC_Namelist(iID)%dG
        dCp = oHMC_Namelist(iID)%dCp
        dRd = oHMC_Namelist(iID)%dRd
        ! Info start
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: Richardson ... ' )
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Variable(s) initialization
        a2dVarTp = 0.0; a2dVarTp0 = 0.0; a2dVarRb = -0.9
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Calculating distributed Richardson number (Richardson from -1 to 0 values)
        where((a2dVarDEM.gt.0.0) .and. (a2dVarWind.gt.0.0))
            
            a2dVarTp = a2dVarTaK*(1000.0/a2dVarPa)**(dRd/dCp)
            a2dVarTp0 = a2dVarLST*(1000.0/a2dVarPa)**(dRd/dCp)
            a2dVarRb = (dG/a2dVarTp)*(a2dVarTp - a2dVarTp0)*dZRef/(a2dVarWind**2) 
            
        elsewhere(a2dVarDEM.gt.0.0)
            
            a2dVarTp = a2dVarTaK*(1000.0/a2dVarPa)**(dRd/dCp)
            a2dVarTp0 = a2dVarLST*(1000.0/a2dVarPa)**(dRd/dCp)
            a2dVarRb = (dG/a2dVarTp)*(a2dVarTp - a2dVarTp0)*dZRef/(0.1**2)
            
        endwhere
        !------------------------------------------------------------------------------------------
        
        !------------------------------------------------------------------------------------------
        ! Debug
        !call surf(a2dVarRb,pm3d='pm3d implicit map', palette='rgbformulae 31, -11, 32')
        !write(*,*) 'VAR Rb' , sum(a2dVarRb)/max(1,count(a2dVarRb.gt.-1.0))
        ! Info end
        call mprintf(.true., iINFO_Extra, ' Phys :: Land surface model :: Richardson ... OK' )
        !------------------------------------------------------------------------------------------
        
    end subroutine HMC_Phys_LSM_Apps_Richardson
    !------------------------------------------------------------------------------------------

end module HMC_Module_Phys_LSM_Apps
!------------------------------------------------------------------------------------
 
