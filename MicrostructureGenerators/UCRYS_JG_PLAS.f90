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
		ncrys=300
		nfiles=5
        thick=0.1  
		E=193000.
		mu=0.3
		g0=150.
		ginf=360.
		h0=380.
        adot=0.0106
		n=50.
        iseed=830963 !ori1
		iseed=211327  !ori2
		iseed=312099  !ori3
		iseed=98247  !ori4
		iseed=446725  !ori5
		iseed=504991  !ori6
		iseed=493487  !ori7
		iseed=902013  !ori8
		iseed=363209  !ori9
		iseed=418743  !ori10
		iseed=647832 !ori11
		iseed=921647832 !ori12
		seed=iseed
		call random_seed(put=seed)
		igen=2
		istan=0
		igps=0
		do i=1,nfiles
			write(filename,'(i1)')i
			open(unit=11,status='unknown',file='W1L80ST.inp')
			open(unit=10,status='unknown',file='W1L80STP_'//trim(filename)//'.inp')
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
				write(10,'(a)')'*elastic'
				write(10,'(f16.4,a,f6.4)')E,',',mu
				call random_number(rand1)
				rh=800.
				if (rand1<0.1)rh=500.
				write(10,'(a)')'*plastic'
				stran=0.
				do j=1,50
					stress=350.+(rh-350.)*tanh(abs(1200.*stran/(rh-350.)))
					write(10,'(f16.4,a,f6.4)')stress,',',stran
					stran=stran+0.01
				enddo
				write(10,'(a)')'**'
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
