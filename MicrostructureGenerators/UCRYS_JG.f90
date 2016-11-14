!      Crystal Plasticity Input File Generator for Abaqus Standard
!      
!      5/7/00 - 	Only valid for FCC structure
!               	Only Asaro hardening model implemented
!               	Only valid for isotropic elastic properties
!               	Latent hardening parameters (Q1, Q2) set to (1, 0)
!	   30/08/11 - 	Modified by JGROGAN. Removed some seldom used choices
!					and added new random generator due to potential
!					problems with previous 'RANDU' type generator.(igen)
!					Added gen plane strain option (igps)
!					
!      Use odd number as seed for random number generator
!
!      NLGEOM flag automatically assumed
!      Newton-raphson iteration scheme and default parameters inputted
!
! ******************************************************************
	program matgen
        integer ncrys,iseed
		character(1) filename
		character(len=256)input2(2)
		integer seed(1)		
        real*8 E,mu,g0,ginf,h0,adot,n,thick
! ******************************************************************
		ncrys=2000
		nfiles=5
        thick=0.1  
		E=193000.
		mu=0.3
		g0=140.
		ginf=800.
		h0=150.
        adot=0.0106
		n=50.
!        iseed=22828385 !ori1
!		iseed=5835828  !ori2
!		iseed=369256 !ori3
!		iseed=39935222  !ori4
!		iseed=787678764 !ori5
!		iseed=987565  !ori6
		iseed=75336563  !ori7
!		iseed=367222567  !ori8
!		iseed=682268  !ori9
!		iseed=68768553  !ori10
		seed=iseed
		call random_seed(put=seed)
		igen=2
		istan=0
		igps=0
		do i=1,nfiles
			write(filename,'(i1)')i
			open(unit=11,status='unknown',file='Tens500_100.inp')
			open(unit=10,status='unknown',file='Tens500_100_'//trim(filename)//'.inp')
			input2(1)='**'
			do while (index(input2(1),'*End Assembly')==0)
				read(11,'(a)')input2(2)
				write(10,'(a)')input2(1)
				input2(1)=input2(2)
			enddo
			write(10,'(a)')'*End Assembly' 
! ******************************************************************
			do icrys=1,ncrys
				write(10,'(a)') '**'
				write(10,'(a,i5)')'*MATERIAL, NAME=MAT',icrys
				write(10,'(a)')'**'
				write(10,'(a)')'*USER MATERIAL, CONSTANTS=160, UNSYMM'
				write(10,'(f16.4,a,f6.4,a)')E,',',mu,','
				write(10,'(f6.4,a)')0.,','
				write(10,'(f6.4,a)')0.,','
				write(10,'(f6.4,a)')1.,','
				write(10,'(6(f6.4,a))')1.,',',1.,',',1.,',',1.,',',1.,',',0.,','
				write(10,'(f6.4,a)')0.,','
				write(10,'(f6.4,a)')0.,','
				call random_number(rand1)
				rand1=(rand1-0.5)*2.
				call random_number(rand2)
				rand2=(rand2-0.5)*2.
				call random_number(rand3)
				rand3=(rand3-0.5)*2.
				call random_number(rand4)
				rand4=(rand4-0.5)*2.
				call random_number(rand5)
				rand5=(rand5-0.5)*2.				
				write(10,'(3(f12.6,a),3(f6.4,a))')rand1,',',rand2,',',rand3,',',1.,',',0.,',',0.			
				rand6 = (rand1*rand4+rand2*rand5)/(-rand3)
				write(10,'(3(f12.6,a),3(f6.4,a))')rand4,',',rand5,',',rand6,',',0.,',',0.,',',1.	
				write(10,'(2(f12.4,a))') n,',',adot,','
				write(10,'(f6.4,a)') 0.,','
				write(10,'(f6.4,a)') 0.,','
				write(10,'(3(f12.4,a))') h0,',',ginf,',',g0,','
				write(10,'(2(f6.4,a))') 1.,',',0.,','
				write(10,'(f6.4,a)') 0.,','
				write(10,'(f6.4,a)') 0.,','
				write(10,'(f6.4,a)') 0.,','
				write(10,'(f6.4,a)') 0.,','
				write(10,'(2(f6.4,a))') 0.5,',',1.,','
				write(10,'(2(f12.4,a))') 1.,',',10.,',1.e-5,'
				write(10,'(a)') '*Depvar'
				write(10,'(a)') '113'
				write(10,'(a)') '**'
			enddo
			ierr=0
			do while (ierr==0)
				read(11,'(a)',iostat=ierr)input2(1)
				if(ierr==0)write(10,'(a)')input2(1)          
			enddo
			close(unit=10)
			close(unit=11)
		enddo
	end program matgen
