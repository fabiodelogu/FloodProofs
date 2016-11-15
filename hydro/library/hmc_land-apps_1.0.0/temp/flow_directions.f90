!********************************************************************
!     PROGRAMMA PUNTATORI: IL PROGRAMMA CALCOLA E CREA LA MATRICE DEI
!     PUNTATORI PARTENDO DAI DATI ALTIMETRICI 
!     (FILE DEM ELABORATO basin_name.bin) AD ACCESSO DIRETTO 
!     RECL=DIM ORIZ*4). 
!     
!     DATI E FILES DI INPUT:
!    
!    
!     - NOME FILE DELLA MATRICE DELLE QUOTE DEL DEM IN FORMATO 
!       ESRI-ASCII (basin_name.dem.txt.
!
!     DATI DI OUTPUT:
!
!     - NOME FILE DelLA MATRICE DEI PUNTATORI (I PUNTATORI SONO 
!       SCRITTI SU RIGHE DI 24 ELEMENTI DOVE OGNI ELEMENTO E`IN 
!       FORMATO ASCII I2) (basin_name.pnt.txt).
!  
!********************************************************************
      
	  program flow_directions

!--------------------------------------------------------------------
!     DICHIARAZIONE DELLE VARIABILI
!--------------------------------------------------------------------	  

	  common /com/ mat,zz,mm
      
	  integer*2 , pointer :: mat(:,:),mm(:,:)
	  real      , pointer :: zz(:,:)

 	  real      , allocatable ,target:: azz(:,:)
      integer*2 , allocatable ,target:: amat(:,:),amm(:,:)
      
	  character*400 iname, basinname
	  character*600 filenameIN, filenameOUT
	  
      integer*4 name_lenght
      character*12 ncols,nrows,xllcorner,yllcorner,cellsize,nodata
	  integer*4 incols,inrows
	  real*8 dxllcorner,dyllcorner,dcellsize,dnodata
      common /com/ ncols,nrows,xllcorner,yllcorner,cellsize,nodata
      common /com/ incols,inrows
      common /com/ dxllcorner,dyllcorner,dcellsize,dnodata

	  !CALL GETARG(1,basinname)
	  
  	  CALL GETARG(1,filenameIN)
	  !write(*,*)'Path Data : ', pathdati
	  
	  CALL GETARG(2,filenameOUT)
	  !write(*,*)'Domain Name : ', basinname
	  
	  
!--------------------------------------------------------------------
!     LU 2 QUOTE IN INPUT
!     LU 3 PUNTATORI MAT IN OUTPUT 
!--------------------------------------------------------------------


	  !name_lenght = lstr(basinname)

!--------------------------------------------------------------------
!     FILES DI INPUT E DI OUTPUT 
!--------------------------------------------------------------------
     
!	  go to 122
      goto 11
 10   write(6,*)'I/O ERROR OCCOURS N = ',ios
      write(6,*)'Control ESRI DEM file to be in working directory (basin_name.dem.txt)'
      read(5,*)

!-------------------------------------------------------------------
!     PER LA LETTURA DI UN FILE IN FORMATO BINARIO 
!     AD ACCESSO DIRETTO CON ELEMENTI REALI (4 BYTES)
!-------------------------------------------------------------------

 11   open(unit=2,file=trim(filenameIN),iostat=ios,access='sequential', &
           err=10,status='old')
      read(2,*)ncols,incols
      read(2,*)nrows,inrows
      read(2,*)xllcorner,dxllcorner
      read(2,*)yllcorner,dyllcorner
      read(2,*)cellsize,dcellsize
      read(2,*)nodata,dnodata
      idim=inrows
	  jdim=incols
!-------------------------------------------------------------------
!     PER LA LETTURA DI UN FILE IN FORMATO ASCII
!-------------------------------------------------------------------




      goto 23
 20   write(6,*)'I/O ERROR OCCOURS N = ',ios
      write(6,*)'Control ASCII Pointers file to be in working directory (basin_name.pun)'
      read(5,*)
!22   write(*,*)'Output Pointers file name (ASCII) ? (basin_name.pun)'
!     read(*,'(a100)')iname 
 23   open(unit=3,file=trim(filenameOUT),iostat=ios,err=20)
! 23   open(unit=3,file=basinname(1:name_lenght-8) //'.pnt2.txt',iostat=ios,err=20)






  
!-------------------------------------------------------------------
!     DET.MATRICE PUNTATORI 1...9 
!-------------------------------------------------------------------

!-------------------------------------------------------------------
!     ALLOCAZIONE DI MEMORIA PER LE MATRICI USATE
!-------------------------------------------------------------------

	  !allocate(azz(jdim,idim))
      !allocate(amm(jdim,idim))
	  !allocate(amat(jdim,idim))

      allocate(azz(idim,jdim))
      allocate(amm(idim,jdim))
	  allocate(amat(idim,jdim))

	  zz  => azz
	  mm  => amm
	  mat => amat

!-------------------------------------------------------------------
!     CHIAMA LA SUBROUTINE PUNT
!     (CALCOLA LA MATRICE DEI PUNTATORI)
!-------------------------------------------------------------------

      call punt(idim,jdim,2,3)

!-------------------------------------------------------------------
!     DEALLOCAZIONE DI MEMORIA PER LE MATRICI UTILIZZATE
!-------------------------------------------------------------------

	  deallocate(azz)
	  deallocate(amm)
	  deallocate(amat)

      close(2)
      close(3)

!-------------------------------------------------------------------      
!     END MAIN 
!-------------------------------------------------------------------
	  
	  end program flow_directions

!-------------------------------------------------------------------
!     SUBROUTINES
!-------------------------------------------------------------------

!-------------------------------------------------------------------
!     SUBROUTINE PUNTATORI
!-------------------------------------------------------------------

      subroutine punt(idim,jdim,idcb,jdcb)
      common /com/ mat,zz,mm
      integer*2,pointer :: mat(:,:),mm(:,:)
      integer*2 mattmp(idim,jdim);
	  real,pointer :: zz(:,:)
      character*100 nome
	  character*12 ncols,nrows,xllcorner,yllcorner,cellsize,nodata
	  integer*4 incols,inrows
	  real*8 dxllcorner,dyllcorner,dcellsize,dnodata,dem_min
      common /com/ ncols,nrows,xllcorner,yllcorner,cellsize,nodata
      common /com/ incols,inrows
      common /com/ dxllcorner,dyllcorner,dcellsize,dnodata


!-------------------------------------------------------------------
!     I0,J0  IN CUI VA I,J 
!     QUOTE IN ZZ(J,I) ANALIZZO VET. COLONNA I-1,I,I+1 
!     DIM MATRICE IDIM,JDIM 
!     JDCB REGISTRA DOVE VA I,J (I0,J0 CON KK IN MAT(J))
!     IDCB QUOTE ZZ 
!-------------------------------------------------------------------

      do  1001 i=1,idim

!-------------------------------------------------------------------
!     PER LA LETTURA DI UN FILE IN FORMATO BINARIO  
!     AD ACCESSO DIRETTO CON ELEMENTI REALI (4 BYTES) 
!-------------------------------------------------------------------

!      read(idcb,rec=i)(zz(k,i),k=1,jdim)
!       read(idcb,*)(zz(k,i),k=1,jdim)
	   read(idcb,*)(zz(idim+1-i,k),k=1,jdim)

!-------------------------------------------------------------------
!     PER LA LETTURA DI UN FILE IN FORMATO ASCII, FREE FORMAT 
!-------------------------------------------------------------------

!     read(idcb,*)(zz(k,i),k=1,jdim)


 1001 continue

!-------------------------------------------------------------------
!     PREPROCESSING 
!-------------------------------------------------------------------

!     do 50 i=1,idim
!       iii=idim-i+1
!       do 50 j=1,jdim
!         if(mm(j,i).le.0) then
!            zz(j,i)=-1.
!         else
!            zz(j,i)=mm(j,i)
!         end if
!50   continue

!Controllo che il dem non sia <= 0 ed eventualmente lo alzo
dem_min=minval(minval(zz,DIM = 1,MASK=zz.ne.dnodata),DIM=1)
write(*,*)'Dem lower value: ',dem_min
IF(dem_min<0)THEN 
	dem_min=abs(dem_min)+0.1
	WHERE(zz.ne.dnodata)
		zz=zz+dem_min
	ENDWHERE
ENDIF


!------------------------------------------------------------------
!     CHIAMA LA SUBROUTINE LAGO
!     (ALZA LE ZONE DEPRESSE)
!------------------------------------------------------------------

      call lago(idim,jdim,1)

      do 51 i=1,idim

 51   continue
      
      close(9)


      !do 1 i=1,idim
	  do 1 i=1,jdim
         i1=-1
         i2=1
         if(i.eq.1)i1=0
         if(i.eq.jdim)i2=0
         !do 2 j=1,jdim
         do 2 j=1,idim
            mat(j,i)=0
			
            if(zz(j,i).lt.0) go to 2
            j1=-1
            j2=1
            if(j.eq.1)j1=0
            if(j.eq.idim)j2=0
            z=zz(j,i)
            pen=-1.e20
            do 3 ii=i1,i2
               do 3 jj=j1,j2
                  p=zz(j+jj,ii+i)-z
                  p=-p
                  if(p.le.0) go to 3
                  if(ii*jj.eq.0)go to 4
                  if(zz(j+jj,ii+i).ge.zz(j+jj,i)) go to 3
                  if(zz(j+jj,ii+i).ge.zz(j,ii+i)) go to 3
                  zi=.25*(z+zz(j+jj,ii+i)+zz(j+jj,i)+zz(j,ii+i))
                  p=(zi-z)*sqrt(2.)
                  p=-p
 4                if(p.le.pen) go to 3
                  pen=p
                  mat(j,i)=3*ii+jj+5
 3             continue
 2          continue
 1       continue
!Check Zeros		 
		 do i=3,jdim-2
			 do j=3,idim-2
				!Controlla la quota 
				if(mat(j,i).eq.0.and.zz(j,i).ne.dnodata)then
					
				endif
			 enddo
		 enddo
!Converto nella convenzione generata dalla dll in C
	     mattmp=mat
		 where(mattmp.eq.3)
			mat=7
         endwhere
		 where(mattmp.eq.6)
			mat=8
         endwhere
		 where(mattmp.eq.8)
			mat=6
         endwhere
		 where(mattmp.eq.7)
			mat=3
         endwhere
		 where(mattmp.eq.4)
			mat=2
         endwhere
		 where(mattmp.eq.2)
			mat=4
         endwhere
         where(mattmp.le.0)
			mat=int(dnodata)
         endwhere
		 write(jdcb,*)ncols,incols
		 write(jdcb,*)nrows,inrows
         write(jdcb,*)xllcorner,dxllcorner
         write(jdcb,*)yllcorner,dyllcorner
         write(jdcb,'(A10,x,f9.7)')cellsize,dcellsize
         write(jdcb,*)nodata,int(dnodata)
         do 1002 i=1,idim
            write(jdcb,'(10000(i5,x))')(mat(idim+1-i,k),k=1,jdim)
 1002    continue

!-----------------------------------------------------------------
!     IND.MAT.DOVE VA I,J  
!      
!                                        1 3---------6--------9
!                                          !         !        !
!     0 NON SCOLA   1....9 SI              !         !        !
!     I0=(MAT-1)/3-1              Asse J 0 2---------0--------8
!                                          !         !        !
!     J0=MAT-5-3*I0                        !         !        !
!                                       -1 1---------4--------7
!                                         -1         0        1
!                                                  Asse I
!-----------------------------------------------------------------
        
!	  write(*,*)'End subroutine PUNT'
	  return
      end

!-----------------------------------------------------------------
!     SUBROUTINE LAGO
!-----------------------------------------------------------------

      subroutine lago(idim,jdim,ilu)
      common /com/ mat,zz,mm
      integer*2,pointer :: mat(:,:),mm(:,:)
	  real,pointer :: zz(:,:)

!-----------------------------------------------------------------
!     CALCOLA ZONE DEPRESSE E LE ALZA 
!     PUNTATORE MM(J,I)
!
!     - 0= VA BENE
!     - 1= INNALZATO
!-----------------------------------------------------------------

 !     do 1001 i=1,idim
 !        do 1002 j=1,jdim
      do 1001 i=1,jdim
         do 1002 j=1,idim
            mm(j,i)=0
 1002    continue
 1001 continue
      i1=-1
      i2=1
      j1=-1
      j2=1
      ix=2
      jx=2
      kkk=0
 1000 kk=0
      !do 11 j=jx,idim-1
       !  do 10 i=ix,jdim-1
      do 11 i=ix,jdim-1
        do 10 j=jx,idim-1
            if(zz(j,i).lt.0) go to 10
            zmin=1.e20
            zx=zz(j,i)
            
            do 2 iii=i1,i2
               do 2 jjj=j1,j2
                  if(iii.eq.0.and.jjj.eq.0) go to 22
                  ii=iii+i
                  jj=jjj+j
                  if(zx.gt.zz(jj,ii)) go to 10
                  if(zmin.gt.zz(jj,ii)) zmin=zz(jj,ii)
 22               continue
 2          continue
			
            if(zx.le.zmin) then !Versione vecchio
               zz(j,i)=zmin+.01 !!!Controllo quanto corregge
               mm(j,i)=1
               kkk=kkk+1
               kk=1
               if (i.ne.2)ix=i-1
               if (j.ne.2)jx=j-1
               if(kkk/1000*1000.eq.kkk) then
                  write(*,'(i6,2i4,f8.2)')kkk,i,j,zz(j,i)
               end if
               go to 1000
            end if
 10      continue
         jx=2
 11    continue
       
       !write(*,*)'* ',kkk
       if(kk.eq.1) go to 1000
!      write(*,*)'End subroutine LAGO'
       return
       end

!----------------------------------------------------------------
!     CALCOLA LA LUNGHEZZA DEL NOME
!----------------------------------------------------------------      
	  
	  integer function lstr(a)
      character*400 a
      last=1
      do while (a(last:last).ne.' ')
         last=last+1
      enddo
      lstr=last-1
      end

!----------------------------------------------------------------















