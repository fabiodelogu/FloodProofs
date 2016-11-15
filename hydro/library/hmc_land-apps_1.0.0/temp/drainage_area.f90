!***********************************************************************
!     PROGRAMMA INTEGRALI: GENERA LA MATRICE DEGLI INTEGRALI
!     A PARTIRE DALLA MATRICE DELLE QUOTE GIA' CALCOLATA IN FORMATO
!     BINARIO UNFORMATTED (RECL=JDIM*4) E DALLA MATRICE DEI PUNTATORI
!     IN FORMATO ASCII PRODOTTA DAL PROGRAMMA PUNTATORI.
!
!     DATI E FILES DI INPUT:
!	  
!     - PATH e NOME DEL BACINO CONSIDERATO.
!	  
!	  - NOME FILE DELLA MATRICE DELLE QUOTE DEL DEM IN FORMATO BINARIO 
!	    (basin_name.dem.txt).
!	  
!	  - NOME FILE DELLA MATRICE DEI PUNTATORI IN FORMATO ASCII
!       (basin_name.pun.txt).
!
!	  FILE DI OUTPUT:
!     
!	  - NOME FILE DELLA MATRICE DEGLI INTEGRALI IN FORMATO ASCII
!	    (basin_name.area.txt).
!***********************************************************************
      
	  program drainage_area

!-----------------------------------------------------------------------
!     DICHIARAZIONE DELLE VARIABILI
!-----------------------------------------------------------------------

      common /declaration/ mat,ms,mm,zz,zq,mattmp
      
	  integer*4 ,pointer :: mat(:,:),mm(:,:),ms(:,:),zz(:,:),mattmp(:,:)
	  real      ,pointer :: zq(:,:)

	  integer*4 ,allocatable ,target:: amat(:,:),ams(:,:),amm(:,:),amattmp(:,:) &
                  ,azz(:,:)
      real      ,allocatable, target:: azq(:,:)
      
	  character*400 iname, basinname, pathdati
	  character*600 filenameIN_1, filenameIN_2, filenameOUT
      integer*4 name_lenght,calcola

	  character*12 ncols,nrows,xllcorner,yllcorner,cellsize,nodata
	  integer*4 incols,inrows,jdim,idim
	  real*8 dxllcorner,dyllcorner,dcellsize,dnodata
      common /com/ ncols,nrows,xllcorner,yllcorner,cellsize,nodata
      common /com/ incols,inrows
      common /com/ dxllcorner,dyllcorner,dcellsize,dnodata


 1    iunit=0
    
      CALL GETARG(1,filenameIN_1)
      CALL GETARG(2,filenameIN_2)
      CALL GETARG(3,filenameOUT)
      
!----------------------------------------------------------------------
!     LU 2 QUOTE IN INPUT
!     LU 3 PUNTATORI MAT E REG.TOTALI ZZ  
!----------------------------------------------------------------------


!-----------------------------------------------------------------------
!     NOME DEL BACINO DEL FIUME
!-----------------------------------------------------------------------

	  !name_lenght = lstr(basinname)
	  !write(6,*)'Insert Basin Name : ',basinname(1:name_lenght)

	  

!----------------------------------------------------------------------
!     FILES DI INPUT
!----------------------------------------------------------------------
      
      goto 11
 10   write(6,*)'I/O ERROR OCCOURS N = ',ios
      write(6,*)'Control ESRI DEM file to be in working directory (basin_name.dem.txt)'
      read(5,*)

!-------------------------------------------------------------------
!     PER LA LETTURA DI UN FILE IN FORMATO BINARIO 
!     AD ACCESSO DIRETTO CON ELEMENTI REALI (4 BYTES)
!-------------------------------------------------------------------

 11   open(unit=2,file=trim(filenameIN_1),iostat=ios,access='sequential', &
           err=10,status='old')
      read(2,*)ncols,incols
      read(2,*)nrows,inrows
      read(2,*)xllcorner,dxllcorner
      read(2,*)yllcorner,dyllcorner
      read(2,*)cellsize,dcellsize
      read(2,*)nodata,dnodata
      jdim=inrows
	  idim=incols
      idcb=2
   
   !--------------------------------------------------------------------------------
!     ALLOCAZIONE DI MEMORIA PER LE MATRICI USATE
!--------------------------------------------------------------------------------

	  allocate(amat(jdim,idim));
	  allocate(ams (jdim,idim));
	  allocate(amm (jdim,idim));
	  allocate(azq (jdim,idim));
	  allocate(azz (jdim,idim));
	  allocate(amattmp(jdim,idim))

	  mat  => amat
	  ms   => ams
	  mm   => amm
	  zz   => azz
	  zq   => azq 
	  mattmp => amattmp

	  mat=0
	  ms=0
	  mm =0
	  zz =0
	  zq=0
	  mattmp=0

	  do  i=1,jdim
		read(2,*)(zq(jdim+1-i,k),k=1,idim)
	  end do
      close(2)

   
      goto 22
 20   write(6,*)'I/O ERROR OCCOURS N = ',ios
      write(6,*)'Control ASCII Pointers file to be in working directory (basin_name.pun.txt)'
      read(5,*)
 22   open(unit=3,file=trim(filenameIN_2),iostat=ios,status='old')
      if (ios.ne.0) go to 20
      jdcb=3
	  read(3,*) 
      read(3,*)
      read(3,*)
      read(3,*)
      read(3,*)
	  read(3,*)
      do  i=1,jdim
	   read(3,*)(mat(jdim+1-i,k),k=1,idim)
	  end do
      close(3)

!Controllo se la notazione è quella ESRI, potenze di 2 e converto
	 IF((maxval(maxval(mat,DIM = 1),DIM = 1)).gt.10)THEN
		mattmp=mat

		WHERE(mattmp.eq.32)
			mat=7 !Ok
		ENDWHERE
		WHERE(mattmp.eq.64)
			mat=8 !Ok
		ENDWHERE
		WHERE(mattmp.eq.128)
			mat=9 !Ok
		ENDWHERE
		WHERE(mattmp.eq.1)
			mat=6 !Ok
		ENDWHERE
		WHERE(mattmp.eq.2)
			mat=3	!Ok
		ENDWHERE
		WHERE(mattmp.eq.4)
			mat=2	!Ok
		ENDWHERE
		WHERE(mattmp.eq.8)
			mat=1 !Ok
		ENDWHERE
		WHERE(mattmp.eq.16)
			mat=4
		ENDWHERE

		
	ENDIF
 
    
!Converto nella convenzione generata da Fortran
	  where(mat.le.0)
			mat=0
      endwhere
      mattmp=mat
	  if(1.eq.1)then
		 where(mattmp.eq.7)
			mat=3
         endwhere
		 where(mattmp.eq.8)
			mat=6
         endwhere
		 where(mattmp.eq.6)
			mat=8
         endwhere
		 where(mattmp.eq.3)
			mat=7
         endwhere
		 where(mattmp.eq.2)
			mat=4
         endwhere
		 where(mattmp.eq.4)
			mat=2
         endwhere
         
      endif

	 
!--------------------------------------------------------------------
!     CHIAMA LA SUBROUTINE INTE
!     (CALCOLA LA MATRICE ZZ INTEGRALE) 
!--------------------------------------------------------------------
      call inte(idim,jdim,idcb,jdcb,6)
!---------------------------------------------------------------------
!     FILE DI OUTPUT
!---------------------------------------------------------------------
	  WHERE(zq.lt.-200)
		zz=dnodata
	  ENDWHERE
        
      goto 66
 60   write(6,*)'I/O ERROR OCCOURS N = ',ios
      write(6,*)'Control ASCII area file to be in working directory (basin_name.area.txt)'
      read(5,*)
 66   open(unit=3,file=trim(filenameOUT),iostat=ios,err=60)
      write(3,*)ncols,incols
	  write(3,*)nrows,inrows
      write(3,*)xllcorner,dxllcorner
      write(3,*)yllcorner,dyllcorner
      write(3,'(A10,x,f9.7)')cellsize,dcellsize
      write(3,*)nodata,int(dnodata)
	  do  i=1,jdim
	   write(3,'(100000(I12,x))')(zz(jdim+1-i,k),k=1,idim) !Non moltiplico per demstep perchè pdistance è dimensionale
	  end do
      close(3)

	  write(*,*)'Area Max (number of cells): ',maxval(maxval(zz,DIM = 1),DIM = 1)
      write(*,*)'Approssimative Area Max (Km^2): ',maxval(maxval(zz,DIM = 1),DIM = 1)*(dcellsize*100)**2

!--------------------------------------------------------------------
!     DEALLOCAZIONE DI MEMORIA PER LE MATRICI UTILIZZATE
!--------------------------------------------------------------------

	  deallocate(amat);
	  deallocate(ams );
	  deallocate(amm );
	  deallocate(azq );
	  deallocate(azz );
	  deallocate(amattmp)

!-------------------------------------------------------------------
!     END MAIN 
!-------------------------------------------------------------------
      
	  end program drainage_area

!-------------------------------------------------------------------
!     SUBROUTINES 
!-------------------------------------------------------------------



!-------------------------------------------------------------------
!     IND. MAT. DOVE VA I,J            
!                                    
!                                        1 3---------6--------9
!                                          !         !        !
!     0 NON SCOLA   1....9 SI              !         !        !
!     I0=(MAT-1)/3-1              ASSE J 0 2---------0--------8
!                                          !         !        !
!     J0=MAT-5-3*I0                        !         !        !
!                                       -1 1---------4--------7
!                                         -1         0        1
!                                                  ASSE I
!-------------------------------------------------------------------      
	

!-------------------------------------------------------------------
!     SUBROUTINE INTE
!-------------------------------------------------------------------

      subroutine inte(idim,jdim,idcb,jdcb,ilu)
      common /declaration/ mat,ms,mm,zz,zq,mattmp

      integer*4 ,pointer :: mat(:,:),mm(:,:),ms(:,:),zz(:,:),mattmp(:,:)
	  real      ,pointer :: zq(:,:)

!-------------------------------------------------------------------
!     CALCOLA AREE SCOLANTI 
!     IDCB=MS SERVIZIO; JDCB=ZZ INTEGRALE
!-------------------------------------------------------------------

      do 1001 i=1,idim
          do 1002 j=1,jdim
              zz(j,i)=1
              ms(j,i)=1
 1002     continue
 1001 continue

      kkk=0
 1000 kk=0
      do 2 i=1,idim
      do 3 j=1,jdim
      if(ms(j,i).eq.0) go to 3
      if(mat(j,i).eq.0) go to 3
      i0=(mat(j,i)-1)/3-1
      j0=mat(j,i)-5-3*i0
      i0=i0+i
      j0=j0+j
!     write(*,*)j0,i0
      ms(j0,i0)=ms(j0,i0)+ms(j,i)
      zz(j0,i0)=zz(j0,i0)+ms(j,i)
      ms(j,i)=0
      kkk=kkk+1
      kk=1
 3    continue
 2    continue
      !write(ilu,*)'* ',kkk
      if(kk.eq.1) go to 1000
!     write(ilu,*)'End subroutine INTE'

      return
      end

!----------------------------------------------------------------
!     CALCOLA LA LUNGHEZZA DEL NOME
!----------------------------------------------------------------      
	  
	  integer function lstr(a)
      character*40 a
      last=1
      do while (a(last:last).ne.' ')
         last=last+1
      enddo
      lstr=last-1
      end

