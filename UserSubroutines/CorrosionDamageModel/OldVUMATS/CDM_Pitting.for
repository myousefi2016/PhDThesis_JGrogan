c	Copyright (c) 2015 James A. Grogan
c
c       Permission is hereby granted, free of charge, to any person obtaining a copy
c       of this software and associated documentation files (the "Software"), to deal
c       in the Software without restriction, including without limitation the rights
c       to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
c       copies of the Software, and to permit persons to whom the Software is
c       furnished to do so, subject to the following conditions:
c
c       The above copyright notice and this permission notice shall be included in
c       call copies or substantial portions of the Software.
c
c       THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
c       IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
c       FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
c       AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
c       LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
c       OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
c       THE SOFTWARE.
c
c       Author: J. Grogan
c       Initial Version: 2011
c	-------------------------------------------------------------------	
	  subroutine vumat ( 
c 		Read only - 
     * 	nblock,ndir,nshr,nstatev,nfieldv,nprops,lanneal,stepTime,
     * 	totalTime,dt,cmname,coordMp,charLength,props,density, 
     * 	strainInc,relSpinInc,tempOld,stretchOld,defgradOld, 
     * 	fieldOld,stressOld, stateOld, enerInternOld,enerInelasOld,   
     * 	tempNew, stretchNew, defgradNew, fieldNew, 
c 		Write only - 
     * 	stressNew, stateNew, enerInternNew, enerInelasNew ) 
c
		include 'vaba_param.inc' 
c 
		dimension coordMp(nblock,3),charLength(nblock),props(nprops),
     1 		strainInc(nblock,ndir+nshr),stressOld(nblock,ndir+nshr),  
     2 		stateOld(nblock,nstatev),stressNew(nblock,ndir+nshr), 
     3 		stateNew(nblock,nstatev),astr(nblock,ndir+nshr),
     4		rKE(3,3),enerInternNew(nblock), enerInternOld(nblock),
     5	 	density(nblock)
c
		character*80 cmname
c		
		parameter (zero = 0.d0, one = 1.d0, two = 2.d0, three = 3.d0, 
     *  	four = 4.d0,third = 1.d0 / 3.d0, half = 0.5d0, op5 = 1.5d0)
c	-------------------------------------------------------------------	
c		Common blocks store element status and random number assigment.
		common active(400000)
		common randnum(400000)
		integer active
		integer iseed(1)
		real randnum		
c
		do k=1,nblock
c	-------------------------------------------------------------------	
c			Update SDVs		
			do i=1,9
				stateNew(k,i)=stateOld(k,i)
			enddo
			do i=23,30
				stateNew(k,i)=stateOld(k,i)
			enddo						
c	-------------------------------------------------------------------	
c			Get meterial properties from INP file and form 'C' matrix
			e = props(1)
			xnu = props(2)
			syield=props(3)
			b=props(4)
			q=props(5)
			twomu = e / ( one + xnu )
			thremu = op5 * twomu
			alamda = xnu * twomu / ( one - two * xnu )							
			trace=strainInc(k,1)+strainInc(k,2)+strainInc(k,3)
c	-------------------------------------------------------------------				
c			Linear elastic material for Abq/Explicit Packager					
			if(abs(steptime)<=0.d0)then
				do i=1,3
					stressNew(k,i)=stressOld(k,i)
     * 					+twomu*strainInc(k,i)+alamda*trace
				enddo
				do i=4,6
					stressNew(k,i)=stressOld(k,i)+twomu*strainInc(k,i)
				enddo
			else
c	-------------------------------------------------------------------	
				if(totaltime==dt)then
				iseed=int(statenew(k,8)*5.74)+int(coordmp(k,1)*1000.)
				call random_seed(put=iseed)
				call random_number(rand_ini)
				stateNew(k,30)=(-log(1.d0-rand_ini))**(1.d0/0.14)
				stateNew(k,30)=stateNew(k,30)/1800000.d0
				endif
c				Get Actual Trial Stress	
				do i=1,3
					astr(k,i)=stateOld(k,9+i)
     * 					+twomu*strainInc(k,i)+alamda*trace
				enddo
				do i=4,6
					astr(k,i)=stateOld(k,9+i)+twomu*strainInc(k,i)
				enddo
c	-------------------------------------------------------------------	
c				Partially Convert to Voigt Form
				smean = third*(astr(k,1)+astr(k,2)+astr(k,3))				
				s11 = astr(k,1) - smean
				s22 = astr(k,2) - smean
				s33 = astr(k,3) - smean
c	-------------------------------------------------------------------	
c				Get Von Mises Stress				
				stateNew(k,19)=sqrt(op5*(s11*s11+s22*s22+s33*s33
     *				+two*astr(k,4)*astr(k,4)+two*astr(k,5)*astr(k,5)
     *	 			+two*astr(k,6)*astr(k,6)))	
c	-------------------------------------------------------------------	
c				Get Max Prin Stress	
				rKE(1,1)=s11
				rKE(2,2)=s22
				rKE(3,3)=s33
				rKE(1,2)=astr(k,4)
				rKE(2,1)=astr(k,4)
				rKE(2,3)=astr(k,5)
				rKE(3,2)=astr(k,5)
				rKE(1,3)=astr(k,6)
				rKE(3,1)=astr(k,6)
				rq=s11*s22*s33
				rq=rq+2.d0*rKE(1,2)*rKE(2,3)*rKE(1,3)
				rq=rq-rKE(1,1)*rKE(2,3)*rKE(2,3)
				rq=rq-rKE(2,2)*rKE(1,3)*rKE(1,3)
				rq=rq-rKE(3,3)*rKE(1,2)*rKE(1,2)	
				rq=rq/2.d0
				p=0.d0
				do i=1,3
					do j=1,3
						p=p+rKE(i,j)*rKE(i,j)
					enddo
				enddo					
				p=p/6.d0			
				if(p<1.e-6)then
					phi=(1.d0/3.d0)*(acos(0.d0)/2.d0)
				else				
					if(abs(rq)>abs(p**(1.5)))then
						phi=0.d0
					else			
						phi=(1.d0/3.d0)*acos(rq/p**(1.5))					
					endif
				endif
				if(phi<0.)then
					phi=phi+acos(0.d0)/3.d0
				endif				
				eig1=smean+2.d0*sqrt(p)*cos(phi)
				eig2=smean-sqrt(p)*(cos(phi)+sqrt(3.d0)*sin(phi))
				eig3=smean-sqrt(p)*(cos(phi)-sqrt(3.d0)*sin(phi))
				stateNew(k,16)=max(eig1,eig2,eig3)	
c	-------------------------------------------------------------------					
c				Recover Yield Surface
				if(stateOld(k,17)<=0.d0)then
					yieldOld=syield
				else
					yieldOld=stateOld(k,17)
				endif
c	-------------------------------------------------------------------					
c				Update Hardening Parameters
				rold=q*(one-exp(-b*stateOld(k,18)))
				hard=b*(q-rold)
c	-------------------------------------------------------------------	
c				Get equivalent plastic strain increment
				sigdif = stateNew(k,19) - yieldOld
				facyld = zero
				if(sigdif.gt.zero)facyld=one
				deqps=facyld*sigdif/(thremu+hard)
c	-------------------------------------------------------------------	
c				Update Yield Surface and Eq. Plastic Strain
				yieldNew = yieldOld + hard * deqps
				stateNew(k,18) = stateOld(k,18) + deqps
				stateNew(k,17)= yieldNew
c	-------------------------------------------------------------------					
c				Get Correction Factor for Trial Stress				
				factor = yieldNew / ( yieldNew + thremu * deqps )
c	-------------------------------------------------------------------									
c				Determine Actual Stress
				stateNew(k,10) = s11 * factor + smean
				stateNew(k,11) = s22 * factor + smean
				stateNew(k,12) = s33 * factor + smean
				stateNew(k,13) = astr(k,4) * factor
				stateNew(k,14) = astr(k,5) * factor
				stateNew(k,15) = astr(k,6) * factor
c	-------------------------------------------------------------------					
c				Update Damage Parameter
				if(totaltime>=1.5)then
					call apply_damage(stateOld,stateNew,k,nblock,
     *					nstatev,randnum,charlength,props,nprops,dt,	
     *	   				active,steptime,totaltime)	 
				endif
c	-------------------------------------------------------------------	
c				Determine Element Stress (Returned to Abaqus)
c				Element Stress = Material Stress*(1-D)
				do i=1,6
					stressNew(k,i)=stateNew(k,9+i)*(one-statenew(k,21))
				enddo
			endif
C 				Update the specific internal energy -
			stressPower = half * (
     1    		( stressOld(k,1)+stressNew(k,1) )*strainInc(k,1)
     1    +     ( stressOld(k,2)+stressNew(k,2) )*strainInc(k,2)
     1    +     ( stressOld(k,3)+stressNew(k,3) )*strainInc(k,3)
     1    + 	two*( stressOld(k,4)+stressNew(k,4) )*strainInc(k,4) )
C
        enerInternNew(k) = enerInternOld(k)+ stressPower / density(k)   
c			
		end do
		return 
      end subroutine vumat	  
c -------------------------------------------------------------------
c
c 	  This subroutine updates the value of the damage parameter based on 
c	  corrosion and/or ductile damage evolution. J. Grogan, 2011.
c	  
	  subroutine apply_damage(stateOld,stateNew,k,nblock,nstatev,
     *		 rrandnum,charlength,props,nprops,dt,iactive,steptime,
     *	 	 totaltime) 
c	
		include 'vaba_param.inc' 
c		
	    dimension stateNew(nblock,nstatev),charlength(nblock)
		dimension props(nprops),stateOld(nblock,nstatev)
c	-------------------------------------------------------------------	
c		Taken from values stored in common blocks in VUMAT		
		dimension iactive(400000)
		dimension rrandnum(400000)
c	-------------------------------------------------------------------				
c		Determine Characteristic Element Length 
		e_length=charlength(k)
c	-------------------------------------------------------------------	
c		Recover value of damage parameter
		if(stateOld(k,21)>0.)then
			damage=stateOld(k,21)
		else 
			damage=0.
		endif
c	-------------------------------------------------------------------			
c		Check if element is on exposed surface.
		do i=1,6
			icycle=0
c
c			If any surrounding elements have been deleted in the
c			previous inc, the number of exposed faces (SDV9) increases.
			if(iactive(stateNew(k,i))==1.)then
				do j=1,6				
c					Previously deleted element numbers are 
c					stored in SDV 22-28.					
					if(stateNew(k,i)==stateNew(k,22+j))then
						icycle=1
					endif
				enddo
				if(icycle==1)then
					cycle
				endif
				stateNew(k,9)=stateNew(k,9)+1.
				stateNew(k,22+i)=stateNew(k,i)
c
c				Current element assumes random number of deleted 
c				neighbouring element.				
				if(rrandnum(stateNew(k,i))>=stateNew(k,30))then
					stateNew(k,30)=rrandnum(stateNew(k,i))*0.85d0
				endif
			endif						
		enddo
c	-------------------------------------------------------------------								
c		Recover Corrosion Parameters
		ukinetic=props(6)
		stateNew(k,29)=ukinetic
		rand_num=stateNew(k,30)
		if((statenew(k,9)>0.99).or.(statenew(k,7)<6.))then
			if(totaltime<3.)then
				dam_inc=rand_num*(ukinetic/E_LENGTH)*dt
				damage=damage+dam_inc
			endif
		endif
		statenew(k,21)=damage
c	-------------------------------------------------------------------		
c		Remove Fully Damaged Elements
		if(statenew(k,18)>0.1515)then
			damage=1.d0
		endif
		if(damage>=0.999)then			
			statenew(k,20)=0.
			statenew(k,21)=1.
			iactive(statenew(k,8))=1.d0
			rrandnum(statenew(k,8))=statenew(k,30)
		endif
c	
		return
	  end subroutine apply_damage
c	-------------------------------------------------------------------		  	  	  
  
	  
		
	 
	 
	 
	 
	 
