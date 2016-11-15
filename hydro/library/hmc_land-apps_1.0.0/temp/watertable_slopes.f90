program watertable_slopes
    
    !----------------------------------------------------------------------------------------------
    ! Variable(s) declaration 
    
    implicit none

    integer iRows, iCols
    integer i, ii, iii, j, jj, jjj, k, kk, kkk, ttt
    integer a, b, perc_tot
    integer ios
    
    integer*4 name_lenght

    character*400 iname, basinname, pathdati
    character*30 tmp
    
    character*700 filenameIN_1, filenameIN_2, filenameIN_3, filenameIN_4
    character*700 filenameOUT_1, filenameOUT_2
    
    real*8 pi, DD, diff, fn, fMean, fNumPen
    real*8 dBmin, dBmax, dem_max
    real*8 dDistanceT, dDxM, dDyM
    
    integer(kind = 4), allocatable,  dimension(:, :) :: a2iPun, a2iChoice
    real(kind = 8), allocatable,  dimension(:, :)    :: a2dDem, a2dAreaCell
    
    real(kind = 8), allocatable,  dimension(:, :)    :: pdistance, LDD, mask_perc_tot
    real(kind = 8), allocatable,  dimension(:, :)    :: diff_DD, pend, pend2, pend3
    
    real(kind = 8), allocatable,  dimension(:, :)    :: a2dAlpha, a2dBeta
    
    character*12 ncols, nrows, xllcorner, yllcorner, cellsize, nodata
    integer*4 incols, inrows
    real*8 dxllcorner, dyllcorner, dcellsize, dnodata
    
    integer lstr
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Get program input
    
    CALL GETARG(1,filenameIN_1)
    CALL GETARG(2,filenameIN_2)
    CALL GETARG(3,filenameIN_3)
    CALL GETARG(4,filenameIN_4)
    
    CALL GETARG(5,filenameOUT_1)
    CALL GETARG(6,filenameOUT_2)
    
    CALL GETARG(7,tmp)
    read(tmp,*) DD
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Basin name lenght
    !name_lenght = lstr(basinname)
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

    ! Load pointers
    goto 21
20  write(6,*)'I/O ERROR OCCOURS N = ',ios
    write(6,*)'Control ESRI file to be in working directory (basin_name.pnt.txt)'
    read(5,*)

21  open(unit=3,file=trim(filenameIN_2),iostat=ios,access='sequential', &
    err=20,status='old')
    read(3,*)
    read(3,*)
    read(3,*)
    read(3,*)
    read(3,*)
    read(3,*)
    
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
    allocate( a2dAreaCell		(iRows,iCols))
    allocate( a2iPun            (iRows,iCols))
    allocate( a2iChoice         (iRows,iCols))
    
    allocate( pdistance			(iRows,iCols))
    allocate( LDD			    (iRows,iCols))
    allocate( mask_perc_tot		(iRows,iCols))
    allocate( diff_DD			(iRows,iCols))
    allocate( pend			    (iRows,iCols))
    allocate( pend2			    (iRows,iCols))
    allocate( pend3			    (iRows,iCols))
    
    allocate( a2dAlpha		    (iRows,iCols))
    allocate( a2dBeta		    (iRows,iCols))
    
    ! Initialize variable(s)
    a2dDem = 0.0; a2dAreaCell = 0.0; a2iPun = 0; a2iChoice = 0;
    
    LDD = 0.0
    pdistance = 0.0
    diff_DD = -9999.0
   
    mask_perc_tot = -9999.0
    pend = 0; pend2 = 0; pend3 = 0;
    
    a2dAlpha = -9999.0; a2dBeta = -9999.0
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Read land data info
    do i=1,iRows
		read(2,*)(a2dDem(iRows + 1 - i, k), k=1, iCols)
	end do
	do i=1,iRows
		read(3,*)(a2iPun(iRows + 1 - i, k), k=1, iCols)
	end do
	do i=1,iRows
		read(4,*)(a2iChoice(iRows + 1 - i, k), k=1, iCols)
	end do
	do i=1,iRows
		read(20,*)(a2dAreaCell(iRows + 1 - i, k), k=1, iCols)
	end do
    !----------------------------------------------------------------------------------------------

    !----------------------------------------------------------------------------------------------
    ! Defining cell area mean value (x and y)
    dDxM = sqrt(sum(a2dAreaCell, mask=a2dAreaCell.gt.0.0) / count(a2dAreaCell.gt.0.0))
    dDyM = sqrt(sum(a2dAreaCell, mask=a2dAreaCell.gt.0.0) / count(a2dAreaCell.gt.0.0))
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Checking distance t
    dDistanceT=500
    IF(dDxM.ge.100.and.dDxM.lt.1000)THEN
         dDistanceT = 2000
    ENDIF
    IF(dDxM.ge.5000.and.dDxM.lt.20000)THEN
         dDistanceT = 30000
    ENDIF
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! DEM Corrections
    where(a2dDem.le.0.and.a2dDem.gt.-1000)
	    a2dDem = 0.2
    endwhere
    
    ! Lakes subroutine to correct depression area
    call lakes(iRows, iCols, a2dDem)
    !----------------------------------------------------------------------------------------------

    !----------------------------------------------------------------------------------------------
    ! Define alpha matrix angle
    perc_tot=0
    DO i = 1, iRows 
        DO j = 1, iCols 
				
		a = i
		b = j
		
		IF(a2dDem(i,j).gt.0.0)THEN
		    
			perc_tot = perc_tot + 1
			fNumPen = 0
			
			DO WHILE((a2dDem(a,b).gt.0.0).and.diff_DD(a,b).eq.-9999)

				IF((a.gt.0.and.a.le.iRows).and.(b.gt.0.and.b.le.iCols))THEN

					iii = a + (INT((a2iPun(a,b)-1)/3)-1)
					jjj = b + a2iPun(a,b) - 5-3*(INT((a2iPun(a,b)-1)/3)-1)
					LDD(a,b) = SQRT(((a-iii)*dDyM)**2 + ((b-jjj)*dDxM)**2)
					
					IF(iii.lt.1.or.jjj.lt.1)THEN
						EXIT
					ENDIF
					
					pdistance(a,b) = LDD(a,b)					
					diff_DD(a,b) = a2dDem(a,b)-a2dDem(iii,jjj)
					mask_perc_tot(a,b) = perc_tot

					!Pendenza media sui canali
					if(datan2(diff_DD(a,b),LDD(a,b)).gt.0.0)then
						fNumPen=fNumPen+1
						pend(a,b)=pend(a,b)+datan2(diff_DD(a,b),LDD(a,b))
					endif
					
					DO WHILE(a2dDem(a,b)-a2dDem(iii,jjj).le.DD.AND.(iii.gt.0.and.iii.le.iRows).and.(jjj.gt.0.and.jjj.le.iCols) &
								.and.a2dDem(iii,jjj).gt.0.0.and.LDD(a,b).lt.dDistanceT)	
					
						mask_perc_tot(a,b) = perc_tot
						diff_DD(a,b) = a2dDem(a,b) - a2dDem(iii,jjj)
						ii = iii + (INT((a2iPun(iii,jjj)-1)/3)-1)
						jj = jjj + a2iPun(iii,jjj) - 5-3*(INT((a2iPun(iii,jjj)-1)/3)-1)	
										
						IF(a2dDem(a,b)-a2dDem(ii,jj).le.DD.and.(ii.gt.0.and.ii.le.iRows).and.(jj.gt.0.and.jj.le.iCols))THEN	
						
							LDD(a,b) = LDD(a,b) + SQRT(((ii-iii)*dDyM)**2+((jj-jjj)*dDxM)**2)
							
							!Pendenza media sui canali
							if(datan2(diff_DD(a,b),LDD(a,b)).gt.0.0)then
								if(a2iChoice(a,b).eq.1)then
									fNumPen = fNumPen + 1
									pend(a,b) = pend(a,b) + datan2(diff_DD(a,b),LDD(a,b))
								endif
								if(a2iChoice(a,b).eq.0.and.LDD(a,b).lt.500)then
									fNumPen = fNumPen + 1
									pend(a,b) = pend(a,b) + datan2(diff_DD(a,b),LDD(a,b))
								endif
							endif
							
						ENDIF
									
						iii=ii
						jjj=jj	
						
						IF(diff_DD(iii,jjj).ne.-9999)THEN
							DO WHILE(a2dDem(a,b)-a2dDem(iii,jjj).le.DD.AND.(iii.gt.0.and.iii.le.iRows).and. &
										(jjj.gt.0.and.jjj.le.iCols).and.a2dDem(iii,jjj).gt.0.0.and.LDD(a,b).lt.dDistanceT)	
					    
								mask_perc_tot(a,b) = perc_tot					
								diff_DD(a,b) = a2dDem(a,b) - a2dDem(iii,jjj)
								ii = iii + (INT((a2iPun(iii,jjj)-1)/3)-1)
								jj = jjj + a2iPun(iii,jjj) - 5-3*(INT((a2iPun(iii,jjj)-1)/3)-1)	
									
								IF(a2dDem(a,b) - a2dDem(ii,jj).le.DD.and.(ii.gt.0.and.ii.le.iRows).and.(jj.gt.0.and.jj.le.iCols))THEN	
									
									LDD(a,b) = LDD(a,b) + SQRT(((ii-iii)*dDyM)**2+((jj-jjj)*dDxM)**2)
									
									!Pendenza media sui canali
									if(datan2(diff_DD(a,b),LDD(a,b)).gt.0.0)then
										if(a2iChoice(a,b).eq.1)then
											fNumPen = fNumPen + 1
											pend(a,b) = pend(a,b) + datan2(diff_DD(a,b),LDD(a,b))
										endif
										if(a2iChoice(a,b).eq.0.and.LDD(a,b).lt.500)then
											fNumPen = fNumPen + 1
											pend(a,b) = pend(a,b) + datan2(diff_DD(a,b),LDD(a,b))
										endif
									endif											
								ENDIF		
								iii=ii
								jjj=jj

					        ENDDO									
					    ENDIF

					ENDDO					
					
					if(fNumPen.gt.0.0)then	
						pend(a,b)=pend(a,b)/fNumPen
					endif
										
					a2dAlpha(a,b) = datan2(DD,LDD(a,b))  !Angolo in radianti
					
					if(diff_DD(a,b).lt.0.9.or.diff_DD(a,b).gt.500)then
						diff_DD(a,b) = 0.9
					endif
					if(diff_DD(a,b).lt.1.and.LDD(a,b).lt.4*dDxM)then
						LDD(a,b) = 4*dDxM
					endif

					a2dAlpha(a,b) = datan2(diff_DD(a,b),LDD(a,b))
					    	
					ii = a + (INT((a2iPun(a,b)-1)/3)-1)
					jj = b + a2iPun(a,b) - 5-3*(INT((a2iPun(a,b)-1)/3)-1)
					IF(a2dDem(ii,jj).gt.0.0)THEN
						a=ii
						b=jj
						fNumPen=0
					ELSE
						EXIT !esce ma conserva gli indici della fine percorso svolto
					ENDIF

				ENDIF
		     
			ENDDO !FINE DI UN PERCORSO COMPLETO SEGUENDO I PUNTATORI		
		
			ii = a + (INT((a2iPun(a,b)-1)/3)-1)
			jj = b + a2iPun(a,b) - 5-3*(INT((a2iPun(a,b)-1)/3)-1)
		       
	    ENDIF
            
	    ENDDO
    ENDDO
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Define beta matrix angle
    a2dBeta = pend

    where(a2iChoice.lt.1)
	    pend = 0
    endwhere
    
    pend2 = pend
    pend = 0

    ! Smoothing della pendenza sui canali
    DO i=1,iRows 
	    DO j=1,iCols
		    if(a2iChoice(i,j).eq.1)then
			    fn=0
			    DO ii=i-1,i+1
				    DO jj=j-1,j+1
					    if(pend2(ii,jj).gt.0.0)then
						    fn=fn+1
						    pend(i,j)=pend(i,j)+pend2(ii,jj)
					    endif
				    ENDDO
			    ENDDO
			    if(fn.lt.1)fn=1
			    pend(i,j)=pend(i,j)/fn
			    if(LDD(i,j).le.4*dDxM.and.diff_DD(i,j).lt.2)then
				    pend(i,j)=a2dAlpha(i,j)
			    endif
			    if(pend(i,j).gt.0.0)then
				    a2dAlpha(i,j)=pend(i,j)
				    a2dBeta(i,j)=pend(i,j)
			    endif
		    endif
		
	    ENDDO
    ENDDO

    dBmin = minval(minval(pend,DIM = 1,MASK = pend.gt.0), DIM=1)

    where(a2dDem.gt.0.and.a2dBeta.eq.0)
	    a2dBeta = a2dAlpha
    endwhere

    where(a2dDem.gt.0.and.a2dBeta.eq.0)
	    a2dBeta = dBmin
    endwhere
    
    write(*,*) 'alpha max: ', maxval(maxval(a2dAlpha,DIM = 1),DIM = 1)
    write(*,*) 'alpha min: ', minval(minval(a2dAlpha,DIM = 1),DIM = 1)

    write(*,*) 'beta max: ', maxval(maxval(a2dBeta,DIM = 1),DIM = 1)
    write(*,*) 'beta min: ', minval(minval(a2dBeta,DIM = 1),DIM = 1)

    write(*,*) 'pend max: ', maxval(maxval(pend,DIM = 1),DIM = 1)
    write(*,*) 'pend min: ', minval(minval(pend,DIM = 1),DIM = 1)
    
    !----------------------------------------------------------------------------------------------
    
    !----------------------------------------------------------------------------------------------
    ! Save output
701 FORMAT (1000(f12.6,1x))
    
    ! Save alpha 
    goto 76
70  write(6,*)'I/O ERROR OCCOURS N = ',ios
    write(6,*)'Control ASCII alpha file to be in working directory (basin_name.alpha.txt)'
    read(5,*)
76  open(unit=3,file=trim(filenameOUT_1),iostat=ios,err=70)
    write(3,*) ncols,incols
    write(3,*) nrows,inrows
    write(3,*) xllcorner,dxllcorner
    write(3,*) yllcorner,dyllcorner
    write(3,'(A10,x,f9.7)') cellsize,dcellsize
    write(3,*)nodata, int(dnodata)
    do i = 1, iRows
        write(3,701) (a2dAlpha(iRows+1-i,k),k=1,iCols) 
    end do
    close(3)

    ! Save beta 
    goto 86
80  write(6,*)'I/O ERROR OCCOURS N = ',ios
    write(6,*)'Control ASCII beta file to be in working directory (basin_name.beta.txt)'
    read(5,*)
86  open(unit=3,file=trim(filenameOUT_2),iostat=ios,err=80)
    write(3,*) ncols,incols
    write(3,*) nrows,inrows
    write(3,*) xllcorner,dxllcorner
    write(3,*) yllcorner,dyllcorner
    write(3,'(A10,x,f9.7)') cellsize,dcellsize
    write(3,*)nodata, int(dnodata)
    do i = 1, iRows
        write(3,701) (a2dBeta(iRows+1-i,k),k=1,iCols) 
    end do
    close(3)
    !----------------------------------------------------------------------------------------------

end program watertable_slopes
!----------------------------------------------------------------------------------------------

!----------------------------------------------------------------------------------------------
! Subroutine lakes
subroutine lakes(iRows, iCols, a2dDem)
    
    implicit none
    
    integer iRows, iCols
    integer i, ii, iii, j, jj, jjj, k, kk, kkk, ttt
    integer i1, i2, j1, j2, ix, jx
    
    real*8 zmin, zx
    
    real*8 a2dDem(iRows,iCols)

    i1 = -1
    i2 = 1
    j1 = -1
    j2 = 1
    ix = 2
    jx = 2
    kkk = 0
500 kk = 0

    do 11 i = ix,iCols-1
        do 10 j = jx,iRows-1
        
        if(a2dDem(j,i).lt.0.0) go to 10
            
        zmin=1.e20
        zx=a2dDem(j,i)
            
        do 2 iii=i1,i2
            do 2 jjj=j1,j2
            
            if(iii.eq.0.and.jjj.eq.0) go to 22
            
            ii=iii+i
            jj=jjj+j
            
            if(zx.gt.a2dDem(jj,ii)) go to 10
            if(zmin.gt.a2dDem(jj,ii)) zmin=a2dDem(jj,ii)
            
22          continue
2           continue

            if(zx.le.zmin) then
                a2dDem(j,i)=zmin+.4
                kkk=kkk+1
                kk=1
                if (i.ne.2)ix=i-1
                if (j.ne.2)jx=j-1
                
                if(kkk/1000*1000.eq.kkk) then
                    write(*,'(i6,2i4,f8.2)')kkk,i,j,a2dDem(j,i)
                end if
                
                go to 500
            end if
            
10          continue
        
        jx=2
11      continue
       
        write(*,*)'* ',kkk
        if(kk.eq.1) go to 500

end subroutine lakes
!----------------------------------------------------------------------------------------------

!----------------------------------------------------------------------------------------------
! Integer funcion lstr
integer function lstr(a)
    character*40 a
    last=1
    do while (a(last:last).ne.' ')
        last=last+1
    enddo
    lstr=last-1
end
!----------------------------------------------------------------------------------------------






