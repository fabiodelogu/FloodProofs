!**********************************************************************
!     PROGRAMMA DISTINCTION: CALCOLA LA MATRICE DI DISTINZIONE VERSANTE
!     CANALE PARTENDO DAL FILE DELLA MATRICE DELLE QUOTE DEL DEM IN 
!     FORMATO BINARIO (basin_name.bin), DAL FILE DELLA MATRICE DEI 
!     PUNTATORI IN FORMATO ASCII (basi_name.pun) E DAL FILE DELLA 
!     MATRICE DEGLI INTEGRALI IN FORMATO ASCII (basin_name.int) GIA'
!     CALCOLATI NEI PRECEDENTI PROGRAMMI. INOLTRE IL PROGRAMMA CALCOLA
!     LA MATRICE DELLE DISTANZE PARZIALE PARTENDO DAI MEDESIMI FILES DI
!     INPUT.
!    
!     DATI E FILES DI INPUT:
!
!     - IDIM, JDIM (I=ORDINATE, J=ASCISSE).
!
!     - INSERIRE IL PASSO DEL DEM UTILIZZATO
!
!     - NOME FILE DELLA MATRICE DEL DEM IN FORMATO ASCII
!       (basin_name.dem.txt).
!
!     - NOME FILE DELLA MATRICE DEI PUNTATORI IN FORMATO ASCII
!       (basin_name.pun.txt).
!
!     - NOME FILE DELLA MATRICE DEGLI INTEGRALI IN FORMATO ASCII
!       (basin_name.int).
!
!     - DECLARATION.F: FILE DOVE SONO DICHIARATE NUMEROSE VARIABILI CHE
!       IL PROGRAMMA UTILIZZA.
!
!     - INSERIRE IL VALORE DELLA SOGLIA CONST DA CONFRONTARE CON IL 
!       VALORE CALCOLATO DI AS^K (PER IL DEM CON PASSO 225 TALE VALORE
!       E' STATO TARATO PARI A CONST = 100000.
!
!     FILES DI OUTPUT:
!
!     - NOME FILE DELLA MATRICE CHE DISTINGUE CANALE E VERSANTE IN 
!       FORMATO BINARIO (basin_name.choice) ED IN PARTICOLARE NELLA 
!       MATRICE VENGONO ASSOCIATI I SEGUENTI VALORI: 
!        0 --> VERSANTE
!        1 --> CANALE
!       -1 --> PER LE ZONE INDEFINITE (PER ESEMPIO: IL MARE).
!
!     - NOME FILE DELLA MATRICE DELLE DISTANZE PARZIALI IN FORMATO ASCII
!       (basin_name.pdistance).
!***********************************************************************      
	  
	  program channels_distinction
      include 'channels_distinction_declaration.f90'

!-----------------------------------------------------------------------
!     DICHIARAZIONE DELLE VARIABILI
!-----------------------------------------------------------------------

	  integer*4 , allocatable, target :: aichoice(:,:), amusk(:,:)
	  integer*4 , allocatable, target :: aipun(:,:), aiarea(:,:),amattmp(:,:)
	  integer*4 name_lenght
      real		, allocatable, target :: adem(:,:),apdistance(:,:),afslope(:,:)
      character*30 idem, pun, area, choice, distance, mas,tmp

      character*400 iname, basinname, pathdati
      character*400 filenameIN_1, filenameIN_2, filenameIN_3, filenameOUT_1, filenameOUT_2

	  character*12 ncols,nrows,xllcorner,yllcorner,cellsize,nodata
	  integer*4 incols,inrows
	  real*8 dxllcorner,dyllcorner,dcellsize,dnodata
	  
      common /com/ ncols,nrows,xllcorner,yllcorner,cellsize,nodata
      common /com/ incols,inrows
      common /com/ dxllcorner,dyllcorner,dcellsize,dnodata
	  
      CALL GETARG(1,filenameIN_1)
      !write(*,*)'Path Data : ', pathdati

      CALL GETARG(2,filenameIN_2)
      !write(*,*)'Domain Name : ', basinname

      CALL GETARG(3,filenameIN_3)
      !write(*,*)'Domain Name : ', basinname

      CALL GETARG(4,filenameOUT_1)
      !write(*,*)'Domain Name : ', basinname

      CALL GETARG(5,filenameOUT_2)
      !write(*,*)'Domain Name : ', basinname
        
	  CALL GETARG(6,tmp)
	  read(tmp,*)step

	  CALL GETARG(7,tmp)
	  read(tmp,*)const

	  !name_lenght = lstr(basinname)
	  !write(6,*)'Insert Basin Name : ',basinname(1:name_lenght)

!-----------------------------------------------------------------------
!     ASSEGNAZIONE DEL VALORE DI SOGLIA CONST
!-----------------------------------------------------------------------

      write(*,*)'AS^k value: ',const


!----------------------------------------------------------------------
!     FILES DI INPUT
!----------------------------------------------------------------------
      
      goto 11
 10   write(6,*)'I/O ERROR OCCOURS N = ',ios
      write(6,*)'Control ESRI DEM file to be in working directory (basin_name.dem.txt)'
      read(5,*)

!----------------------------------------------------------------------
!     APERTURA DEL FILE DELLE QUOTE DEL DEM IN FORMATO ASCII
!----------------------------------------------------------------------
 

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
!-----------------------------------------------------------------------
!     ALLOCAZIONE DI MEMORIA PER LE MATRICI USATE
!-----------------------------------------------------------------------

	  allocate( adem			(jdim,idim))
	  allocate( aipun			(jdim,idim)) 
	  allocate( apdistance	    (jdim,idim))
	  allocate( aiarea	        (jdim,idim))
	  allocate( aichoice		(jdim,idim))

      allocate( amusk		(jdim,idim))

	  allocate( afslope (jdim,idim))
	  allocate( amattmp(jdim,idim))


	  dem		=> adem
	  ipun	    => aipun		
	  pdistance	=> apdistance	
	  iarea		=> aiarea		
	  ichoice	=> aichoice	

	  musk		=> amusk
	  fslope	=> afslope
      mattmp => amattmp

	  do  i=1,jdim
		read(2,*)(dem(jdim+1-i,k),k=1,idim)
	  end do
      close(2)

	  flsope=0.0

	  musk=dnodata
	  WHERE(dem.gt.-100)
		musk=1
	  ENDWHERE



!----------------------------------------------------------------------
!     APERTURA DEL FILE DEI PUNTATORI IN FORMATO ASCII
!----------------------------------------------------------------------

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
		read(3,*)(ipun(jdim+1-i,k),k=1,idim)
	  end do
      close(3)
!----------------------------------------------------------------------
!     APERTURA DEL FILE AREE IN FORMATO ASCII
!----------------------------------------------------------------------

      goto 33
 30   write(6,*)'I/O ERROR OCCOURS N = ',ios
      write(6,*)'Control file area.txt to be in working directory'
      read(5,*)
 33   open(unit=3,file=trim(filenameIN_3), &
                       status='old',form='formatted',access='sequential',iostat=ios,err=30)
      read(3,*) 
      read(3,*)
      read(3,*)
      read(3,*)
      read(3,*)
	  read(3,*)
	  do  i=1,jdim
	   read(3,*)(iarea(jdim+1-i,k),k=1,idim)
	  end do
	  close(3)


!Controllo se la notazione è quella ESRI, potenze di 2 e converto
	 IF((maxval(maxval(ipun,DIM = 1),DIM = 1)).gt.10)THEN
		mattmp=ipun

		WHERE(mattmp.eq.32)
			ipun=7 !Ok
		ENDWHERE
		WHERE(mattmp.eq.64)
			ipun=8 !Ok
		ENDWHERE
		WHERE(mattmp.eq.128)
			ipun=9 !Ok
		ENDWHERE
		WHERE(mattmp.eq.1)
			ipun=6 !Ok
		ENDWHERE
		WHERE(mattmp.eq.2)
			ipun=3	!Ok
		ENDWHERE
		WHERE(mattmp.eq.4)
			ipun=2	!Ok
		ENDWHERE
		WHERE(mattmp.eq.8)
			ipun=1 !Ok
		ENDWHERE
		WHERE(mattmp.eq.16)
			ipun=4
		ENDWHERE

		
	ENDIF
 
    
!Converto nella convenzione generata da Fortran
	  where(ipun.le.0)
			ipun=0
      endwhere
      mattmp=ipun
	  if(1.eq.1)then
		 where(mattmp.eq.7)
			ipun=3
         endwhere
		 where(mattmp.eq.8)
			ipun=6
         endwhere
		 where(mattmp.eq.6)
			ipun=8
         endwhere
		 where(mattmp.eq.3)
			ipun=7
         endwhere
		 where(mattmp.eq.2)
			ipun=4
         endwhere
		 where(mattmp.eq.4)
			ipun=2
         endwhere
         
      endif

	 


!---------------------------------------------------------------------
!     PREPARAZIONE DELLA MATRICE ICHOICE CONTENENTE I VALORI
!      0 PER I VERSANTI
!      1 PER I CANALI
!     -1 PER LE ZONE INDEFINITE (MARE)
!---------------------------------------------------------------------

   
      ichoice=-1


!--------------------------------------------------------------------      
!     CHIAMA LA SUBROUTINE SCAN 
!--------------------------------------------------------------------
 
      call scan(1,idim,1,jdim,1,1)
	  !where(ichoice.eq.0)
	!	fslope=0.0
	 ! endwhere
	   do j=1,jdim
         do i=1,idim
            if(ichoice(j,i).eq.0)then
				fslope(j,i)=0
			endif
         enddo
      enddo
!--------------------------------------------------------------------
!     FILES DI OUTPUT
!--------------------------------------------------------------------

!--------------------------------------------------------------------
!     SCRITTURA DELLE MATRICI IN FORMATO BINARIO E ASCII
!--------------------------------------------------------------------
 

      goto 66
 60   write(6,*)'I/O ERROR OCCOURS N = ',ios
      write(6,*)'Control ASCII choice file to be in working directory (basin_name.choice.txt)'
      read(5,*)
 66   open(unit=3,file=trim(filenameOUT_1),iostat=ios,err=60)
      write(3,*)ncols,incols
	  write(3,*)nrows,inrows
      write(3,*)xllcorner,dxllcorner
      write(3,*)yllcorner,dyllcorner
      write(3,'(A10,x,f9.7)')cellsize,dcellsize
      write(3,*)nodata,int(dnodata)
	  do  i=1,jdim
	   write(3,'(100000(I12,x))')(ichoice(jdim+1-i,k),k=1,idim) !Non moltiplico per demstep perchè pdistance è dimensionale
	  end do
      close(3)



	  goto 76
 70   write(6,*)'I/O ERROR OCCOURS N = ',ios
      write(6,*)'Control ASCII partial distance file to be in working directory (basin_name.partial_distance.txt)'
      read(5,*)
 76   open(unit=3,file=trim(filenameOUT_2),iostat=ios,err=70)
      write(3,*)ncols,incols
	  write(3,*)nrows,inrows
      write(3,*)xllcorner,dxllcorner
      write(3,*)yllcorner,dyllcorner
      write(3,'(A10,x,f9.7)')cellsize,dcellsize
      write(3,*)nodata,int(dnodata)
	  do  i=1,jdim
	   write(3,'(100000(I12,x))')(int(pdistance(jdim+1-i,k)),k=1,idim) !Non moltiplico per demstep perchè pdistance è dimensionale
	  end do
      close(3)
!---------------------------------------------------------------------
!     DEALLOCAZIONE DI MEMORIA PER LE MATRICI UTILIZZATE
!---------------------------------------------------------------------

      deallocate( adem		)
	  deallocate( aipun		) 
	  deallocate( apdistance)
	  deallocate( aiarea	)
	  deallocate( aichoice	)

	  deallocate( amusk	)
	  deallocate( amattmp)

!--------------------------------------------------------------------
!     END MAIN
!--------------------------------------------------------------------      
	  
	  end program channels_distinction

!--------------------------------------------------------------------
!     SUBROUTINES
!--------------------------------------------------------------------

!--------------------------------------------------------------------
!     SUBROUTINE READDIRECT
!--------------------------------------------------------------------

      subroutine readdirect(iunit)
      include 'channels_distinction_declaration.f90'

	  real quota
      
      do i=1,idim,1
	           read(iunit,rec=i) (dem(j,i),j=1,jdim)
      enddo



      n=0
	  do i=1,idim
	    do j=1,jdim
	    if(musk(j,i).ne.dnodata) then
		  n=n+1
		  quota=quota+dem(j,i)
         end if
		enddo
	  end do
	  quota=quota/n
	  write(*,*)'quota media',quota
	  !!pause
	  return
      end

	  

!--------------------------------------------------------------------
!     SUBROUTINE READSEQUENTIAL
!--------------------------------------------------------------------

      subroutine readsequential(iunit,ilab)
      include 'channels_distinction_declaration.f90'

      if (ilab.eq.1) then
         do i=1,idim 
            read(iunit,'(20I6)') (iarea(j,i),j=1,jdim)
         enddo
      else 
         do i=1,idim,1
            read(iunit,'(24I2)') (ipun(j,i),j=1,jdim)
         enddo
      endif
      return

      end

!-------------------------------------------------------------------
!     SUBROUTINE SCAN 
!     (ANALIZZA LA MATRICE DEL BACINO)
!-------------------------------------------------------------------

      subroutine scan(ist,ien,jst,jen,istp,jstp)
      include 'channels_distinction_declaration.f90'
      logical noexit,nopit,new
      
      do j=jst,jen,jstp
         
         do i=ist,ien,istp
            noexit=.true.
            new=.false.
            ii=i
            jj=j
            ifill=0
            
            do while (noexit)
               
               nopit=(ipun(jj,ii).ne.0)

               if (ichoice(jj,ii).eq.-1) new=.true.
               if ((ifill.eq.1).and.(ichoice(jj,ii).eq.0)) new=.true.

               if ((nopit).and.(new)) then
                  i0=(ipun(jj,ii)-1)/3-1
                  j0=(ipun(jj,ii)-5-3*i0)
                  iii=ii+i0
                  jjj=jj+j0

                  if (ifill.eq.1) then
                     ichoice(jj,ii)=1
                     pdistance(jj,ii)=distance(ii,jj)
                     new=.false.
                  endif

                  if (ifill.eq.0) then
                     call comparison(ii,jj,ihorc,iii,jjj)
					  
                     ichoice(jj,ii)=ihorc
                     ifill=ihorc
                     pdistance(jj,ii)=distance(ii,jj)
                     new=.false.
                  endif

                  ii=iii
                  jj=jjj
               else
                  noexit=.false.
               endif
            enddo

		
         enddo
      enddo

      end

!------------------------------------------------------------------
!     SUBROUTINE COMPARISON
!     (DISTINGUE LA RETE DEI CANALI DAI VERSANTI)     
!------------------------------------------------------------------

      subroutine comparison(id,jd,ihorc,iid,jjd)
      include 'channels_distinction_declaration.f90'

!------------------------------------------------------------------
!     ASSEGNAZIONE DEL VALORE DELL'ESPONENTE K PER IL CALCOLO DEL
!     VALORE DI AS^K DA CONFRONTARE POI CON IL VALORE CHE VIENE 
!     ATTRIBUITO ALLA SOGLIA CONST
!------------------------------------------------------------------
      
	  rk=1.7

!------------------------------------------------------------------      
!     CHIAMA LA SUBROUTINE SLOPE 
!
!     STEP [M] * STEP [M] RAPPRESENTA LA DIMENSIONE DEL PIXEL
!     MENTRE CON SM VIENE INDICATA LA PENDENZA MEDIA
!------------------------------------------------------------------

      call slope(id,jd,iid,jjd,sm)
	  ifT=1/10000 ! Soglia eventualmente da rivedere
	  if(sm.lt.ifT)sm=ifT
      ASK=(iarea(jd,id)*step*step)*sm**rk
	  
	 
      !fslope(jd,id)=fslope(jd,id)+sm
	  
      if (ASK.le.const) then
         ihorc=0
      else
         ihorc=1
	  endif

      end

!------------------------------------------------------------------
!     SUBROUTINE SLOPE
!     (CALCOLA LA PENDENZA MEDIA)   
!------------------------------------------------------------------

      subroutine slope(id,jd,iid,jjd,sm)
      include 'channels_distinction_declaration.f90'

      sm=(dem(jd,id)-dem(jjd,iid))/(distance(id,jd)*step)
      icount=1

      if (ipun(jd+1,id+1).eq.1) then
         sm=sm+(dem(jd+1,id+1)-dem(jd,id))/(1.41412356*step)
         icount=icount+1
      endif

      if (ipun(jd+1,id).eq.4) then
         sm=sm+(dem(jd+1,id)-dem(jd,id))/step
         icount=icount+1
      endif

      if (ipun(jd+1,id-1).eq.7) then
         sm=sm+(dem(jd+1,id-1)-dem(jd,id))/(1.41412356*step)
         icount=icount+1
      endif

      if (ipun(jd,id-1).eq.8) then
         sm=sm+(dem(jd,id-1)-dem(jd,id))/step
         icount=icount+1
      endif

      if (ipun(jd-1,id-1).eq.9) then
         sm=sm+(dem(jd-1,id-1)-dem(jd,id))/(1.41412356*step)
         icount=icount+1
      endif

      if (ipun(jd-1,id).eq.6) then
         sm=sm+(dem(jd-1,id)-dem(jd,id))/step
         icount=icount+1
      endif

      if (ipun(jd-1,id+1).eq.3) then
         sm=sm+(dem(jd-1,id+1)-dem(jd,id))/(1.41412356*step)
         icount=icount+1
      endif
      
      if (ipun(jd,id+1).eq.2) then
         sm=sm+(dem(jd,id+1)-dem(jd,id))/step
         icount=icount+1
      endif
      
	  if(sm.gt.4) then
	     sm=0
	  end if


	  sm=(sm/icount)
      
	  if(musk(jd,id).eq.1) then
	      pmedia=sm+pmedia
	      m=m+1
		  fslope(jd,id)=sm
			!write(*,*)'num,slopetot,slope',m,pmedia/float(m),sm
			if(sm.eq.0)then
			!	pause
			endif
	    end if

      end

!-----------------------------------------------------------------
!      CALCOLA LA DISTANZA DA PIXEL A PIXEL SEGUENDO IL 
!      PERCORSO DISEGNATO DAI PUNTATORI
!-----------------------------------------------------------------

      function distance (id,jd)
      include 'channels_distinction_declaration.f90'

!-----------------------------------------------------------------
!     DISTANCE E' MISURATA IN NUMERO DI PIXELS
!-----------------------------------------------------------------

      i0=(ipun(jd,id)-1)/3-1
      j0=(ipun(jd,id)-5-3*i0)
      if ((i0.eq.0).or.(j0.eq.0)) then
         distance=1
      else 
         distance=1.414
      endif
      end

!-----------------------------------------------------------------


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






































