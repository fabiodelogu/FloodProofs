program coeff_resolution_map
    
    !----------------------------------------------------------------------------------------------
    ! Implicit none
    implicit none
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Variable(s) declaration
    integer iRows,iCols
    integer i,j,k
    integer ios
    
    integer*4 incols, inrows
    
    character*700 filenameIN_1, filenameIN_2, filenameIN_3, filenameIN_4
    character*700 filenameOUT
    character*30 tmp
    
    character(len = 12) ncols, nrows, xllcorner, yllcorner, cellsize, nodata
    real(kind = 8) dxllcorner, dyllcorner, dcellsize, dnodata
    
    integer(kind = 4), allocatable,  dimension(:, :)    :: a2iMask, a2iChoice
    real(kind = 8), allocatable,  dimension(:, :)    :: a2dDem, a2dArea, a2dAreaCell
    real(kind = 8), allocatable,  dimension(:, :)    :: a2dSecWidth, a2dCoeffResol
    
    real(kind = 8)  :: dNCellMin, dACellMin, dCoffMean, dMaxW, dMinW, dRateResol
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Initialize variable(s)
    dNCellMin = -9999.0; dACellMin = -9999.0; dCoffMean= -9999.0; 
    dMaxW = -9999.0; dMinW = -9999.0; dRateResol = -9999.0;
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Get program input
    CALL GETARG(1,filenameIN_1)     ! dem
    CALL GETARG(2,filenameIN_2)     ! area
    CALL GETARG(3,filenameIN_3)     ! choice
    CALL GETARG(4,filenameIN_4)     ! areacell
    CALL GETARG(5,filenameOUT)      ! coeff_map
    CALL GETARG(6,tmp)
    read(tmp,*) dRateResol
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Parameter(s)
    !dRateResol = 0.5 
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Load DEM
    goto 11
10  write(6,*)'I/O ERROR OCCOURS N = ',ios
    write(6,*)'Control ESRI file to be in working directory (basin_name.dem.txt)'
    read(5,*)

11  open(unit=2,file=trim(filenameIN_1),iostat=ios,access='sequential', &
    err=10,status='old')
    read(2,*) ncols,incols
    read(2,*) nrows,inrows
    read(2,*) xllcorner,dxllcorner
    read(2,*) yllcorner,dyllcorner
    read(2,*) cellsize,dcellsize
    read(2,*) nodata,dnodata
    
    ! Dims definition
    iRows=inrows; iCols=incols
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Load area
    goto 21
20  write(6,*)'I/O ERROR OCCOURS N = ',ios
    write(6,*)'Control ESRI file to be in working directory (basin_name.area.txt)'
    read(5,*)

21  open(unit=3,file=trim(filenameIN_2),iostat=ios,access='sequential', &
    err=20,status='old')
    read(3,*)
    read(3,*)
    read(3,*)
    read(3,*)
    read(3,*)
    read(3,*)
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Load choice
    goto 31
30  write(6,*)'I/O ERROR OCCOURS N = ',ios
    write(6,*)'Control ESRI file to be in working directory (basin_name.choice.txt)'
    read(5,*)
    
31  open(unit=4,file=trim(filenameIN_3),iostat=ios,access='sequential', &
    err=30,status='old')
    read(4,*)
    read(4,*)
    read(4,*)
    read(4,*)
    read(4,*)
    read(4,*)
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Load areacell
    goto 41
40  write(6,*)'I/O ERROR OCCOURS N = ',ios
    write(6,*)'Control ESRI file to be in working directory (basin_name.areacell.txt)'
    read(5,*)

41  open(unit=20,file=trim(filenameIN_4),iostat=ios,access='sequential', &
    err=40,status='old')
    read(20,*)
    read(20,*)
    read(20,*)
    read(20,*)
    read(20,*)
    read(20,*)
    !----------------------------------------------------------------------------------------------

    !----------------------------------------------------------------------------------------------
    ! Allocate variable(s)
    allocate( a2dDem			(iRows,iCols))
    allocate( a2dArea           (iRows,iCols))
    allocate( a2dAreaCell		(iRows,iCols))
    allocate( a2iMask		    (iRows,iCols))
    allocate( a2iChoice		    (iRows,iCols))
    
    allocate( a2dSecWidth		(iRows,iCols))
    allocate( a2dCoeffResol	    (iRows,iCols))
    
    ! Initialize variable(s)
    a2iMask = 0; a2iChoice = 0;
    a2dDem = 0.0; a2dAreaCell = 0.0; a2dArea = 0.0

    a2dSecWidth = -9999; a2dCoeffResol = 1.0
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Read dem, area and areacell
    do i=1,iRows
		read(2,*)(a2dDem(iRows + 1 - i, k), k=1, iCols)
	end do
    do i=1,iRows
		read(3,*)(a2dArea(iRows + 1 - i, k), k=1, iCols)
	end do
	do i=1,iRows
		read(20,*)(a2dAreaCell(iRows + 1 - i, k), k=1, iCols)
	end do
	! Compute mask
	where(a2dDem.ge.0.0)
	    a2iMask = 1
    endwhere
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Coeff to regulate subsurface and deep flow
    dNCellMin = MINVAL(MINVAL(a2dArea,dim=1,mask=a2iMask.gt.0.0.and.a2dArea.gt.0.0))
    dACellMin = MINVAL(MINVAL(a2dAreaCell,dim=1,mask=a2iMask.gt.0.0.and.a2dAreaCell.gt.0.0))
    write(*,*) 'Min CellNumber: ',dNCellMin, ' - Min CellArea: ',dACellMin       
    
    IF(dNCellMin.gt.1)THEN !Area matrix and not cells number matrix
	    write(*,*)'Conversion from area to cell number'
	    WHERE(a2dDem.gt.0.and.a2iChoice.gt.0)
		    a2dArea = a2dArea/a2dAreaCell*1000000 !Approximate formula
	    ENDWHERE
    ENDIF
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Section width
    !WHERE(a2dDem.gt.0.and.a2iChoice.gt.0)
	!    a2dSecWidth = 0.01*(a2dArea*a2dAreaCell/1000000)**0.4*1000 !width in m
    !ENDWHERE
    !
    !dMaxW = MAXVAL(MAXVAL(a2dSecWidth,dim=1, mask=a2iChoice.gt.0.0))
    !dMinW = MINVAL(MINVAL(a2dSecWidth,dim=1, mask=a2iChoice.eq.1.and.a2dDem.gt.0))
    !
    !write(*,*),'Section Max and Min Width: ',dMaxW, dMinW
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Compute coeff map
    WHERE(a2dDem.gt.0.and.a2iChoice.ge.0)
	    a2dCoeffResol = dexp(-dsqrt(a2dAreaCell)*0.0007)
    ENDWHERE    
    WHERE(a2dCoeffResol.lt.0)
	    a2dCoeffResol=0.0
    ENDWHERE

    write(*,*),'Coeff Res Mean: ',a2dCoeffResol((iRows/2),(iCols/2))
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Save output
701 FORMAT (1000(f12.6,1x))
    
    ! Save coeffres
    goto 76
70  write(6,*)'I/O ERROR OCCOURS N = ',ios
    write(6,*)'Control ASCII coeffres file to be in working directory (basin_name.coeffres.txt)'
    read(5,*)
76  open(unit=3,file=trim(filenameOUT),iostat=ios,err=70)
    write(3,*) ncols,incols
    write(3,*) nrows,inrows
    write(3,*) xllcorner,dxllcorner
    write(3,*) yllcorner,dyllcorner
    write(3,'(A10,x,f9.7)') cellsize,dcellsize
    write(3,*)nodata, int(dnodata)
    do i = 1, iRows
        write(3,701) (a2dCoeffResol(iRows+1-i,k),k=1,iCols) 
    end do
    close(3)
    !----------------------------------------------------------------------------------------------

end program coeff_resolution_map
