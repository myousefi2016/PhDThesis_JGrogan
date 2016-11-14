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
     *  	four = 4.d0,third = 1.d0 / 3.d0, half = 0.5d0, op5 = 1.5d0,
     *		max_elements=100000)
c	-------------------------------------------------------------------	
c		Common blocks store element details for all elements.
		common el_position_new(max_elements,3)
		common el_position_old(max_elements,3)
		common el_time_new(max_elements)
		common el_time_old(max_elements)
		common el_status_new(max_elements)
		common el_status_old(max_elements)
c							
		integer el_status_new,el_status_old
		real el_position_new,el_position_old,el_time_new,el_time_old			
c
c		SDV 16-SDV 2+16: Neighbour Labels
c		SDV 1: Element Label
c		SDV 2: Number of Neighbouring Elements
c		SDV 3: Random Number Assignment
c		SDV 4: Minimum Distance to Corrosion Surface
c		SDV 5-10: Equivalent Stress Components
c		SDV 11: VonMisses Stress
c		SDV 12: Yield Stress
c		SDV 13: PEEQ
c		SDV 14: Damage
c		SDV 15: Delete
c
		do k=1,nblock
c	-------------------------------------------------------------------	
c			Update SDVs	
			do i=1,stateOld(k,2)+15
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
c				Get Actual Trial Stress	
				do i=1,3
					astr(k,i)=stateOld(k,4+i)
     * 					+twomu*strainInc(k,i)+alamda*trace
				enddo
				do i=4,6
					astr(k,i)=stateOld(k,4+i)
     *					+twomu*strainInc(k,i)	
				enddo
c	-------------------------------------------------------------------	
c				Partially Convert to Voigt Form
				smean = third*(astr(k,1)+astr(k,2)+astr(k,3))				
				s11 = astr(k,1) - smean
				s22 = astr(k,2) - smean
				s33 = astr(k,3) - smean
c	-------------------------------------------------------------------	
c				Get Von Mises Stress				
				stateNew(k,11)=sqrt(
     *				op5*(s11*s11+s22*s22+s33*s33+
     *				two*astr(k,4)*astr(k,4)+
     *	 			two*astr(k,5)*astr(k,5)+
     *	 			two*astr(k,6)*astr(k,6)))	
c	-------------------------------------------------------------------							
c				Recover Yield Surface
				if(stateOld(k,12)<=0.d0)then
					yieldOld=syield
				else
					yieldOld=stateOld(k,12)
				endif
c	-------------------------------------------------------------------					
c				Update Hardening Parameters
				rold=q*(one-exp(-b*stateOld(k,13)))
				hard=b*(q-rold)
c	-------------------------------------------------------------------	
c				Get equivalent plastic strain increment
				sigdif = stateNew(k,11) - yieldOld
				facyld = zero
				if(sigdif.gt.zero)facyld=one
				deqps=facyld*sigdif/(thremu+hard)
c	-------------------------------------------------------------------	
c				Update Yield Surface and Eq. Plastic Strain
				yieldNew = yieldOld + hard * deqps
				stateNew(k,13) = stateOld(k,13) + deqps
				stateNew(k,12)= yieldNew
c	-------------------------------------------------------------------					
c				Get Correction Factor for Trial Stress				
				factor = yieldNew / ( yieldNew + thremu * deqps )
c	-------------------------------------------------------------------									
c				Determine Actual Stress
				stateNew(k,5) = s11 * factor + smean
				stateNew(k,6) = s22 * factor + smean
				stateNew(k,7) = s33 * factor + smean
				stateNew(k,8) = astr(k,4) * factor
				stateNew(k,9) = astr(k,5) * factor
				stateNew(k,10) = astr(k,6) * factor
c	-------------------------------------------------------------------					
c				Update Damage Parameter
				if(totaltime>=0.0)then
					tprev=totaltime-dt
					tol=dt*0.1d0
c -------------------------------------------------------------------				
c					Determine Characteristic Element Length 
					e_length=charlength(k)
c	------------------------------------------------------------------
c					Recover value of damage parameter
					damage=stateOld(k,14)
c	-------------------------------------------------------------------	
c					Get distance to exposed surface
					distmin=stateOld(k,4)
					num_nbr=stateold(k,2)
					do i=1,num_nbr
						tnew=el_time_new(stateold(k,i+15))
						told=el_time_old(stateold(k,i+15))
						istat=0
						if((tnew>tprev-tol).and.(tnew<tprev+tol))then
							nestat=el_status_new(stateold(k,i+15))
							if(nestat==2)then
								xnbr=el_position_new(stateold(k,i+15),1)
								ynbr=el_position_new(stateold(k,i+15),2)
								znbr=el_position_new(stateold(k,i+15),3)
								istat=1
							endif
						elseif((told>tprev-tol).and.(told<tprev+tol))then
							nestat=el_status_old(stateold(k,i+15))
							if(nestat==2)then
								xnbr=el_position_old(stateold(k,i+15),1)
								ynbr=el_position_old(stateold(k,i+15),2)
								znbr=el_position_old(stateold(k,i+15),3)
								istat=1
							endif	
						else
							write(*,*)'TStamp',tprev,i,tnew,told
							call xplb_exit
						endif							
						if(istat==1)then
							distance=sqrt(
     *						  (xnbr-coordMP(k,1))*(xnbr-coordMP(k,1))+
     *						  (ynbr-coordMP(k,2))*(ynbr-coordMP(k,2))+
     *						  (znbr-coordMP(k,3))*(znbr-coordMP(k,3)))
							if(distance<distmin)distmin=distance
						endif
					enddo
					statenew(k,4)=distmin
					b_dist=stateold(k,3)
c	-------------------------------------------------------------------								
c					Recover Corrosion Parameters
					isurf=0.
					if(distmin<1.1*e_length)isurf=1.
					ukinetic=props(6)
					if(isurf==1)then
						rprox=(1.1*e_length-distmin)/(1.1*e_length)
						bprox=5*(1.1*e_length-b_dist)/(1.1*e_length)
						if(bprox<0.)bprox=0.d0
						ukinetic=ukinetic*(rprox+bprox)
						if(totaltime<3.)then
							dam_inc=(ukinetic/E_LENGTH)*dt
							damage=damage+dam_inc
						endif
					endif
					statenew(k,14)=damage
c	-------------------------------------------------------------------		
c					Remove Fully Damaged Elements
					if(statenew(k,13)>0.1515)then
						damage=1.d0
					endif
					if(damage>=0.999)then			
						statenew(k,15)=0.
						statenew(k,14)=1.
						ielstat=2
					else
						ielstat=1
					endif	   					 
				endif
c	-------------------------------------------------------------------	
c				Determine Element Stress (Returned to Abaqus)
c				Element Stress = Material Stress*(1-D)
				do i=1,6
					stressNew(k,i)=stateNew(k,4+i)*
     *					(one-statenew(k,14))
				enddo
c	-------------------------------------------------------------------				
c				Update element data from previous increment	
				ielabel=stateold(k,1)
				do i=1,3
					el_position_old(ielabel,i)=el_position_new(ielabel,i)
					el_position_new(ielabel,i)=coordMP(k,i)
				enddo
				el_time_old(ielabel)=el_time_new(ielabel)
				el_time_new(ielabel)=totaltime
				el_status_old(ielabel)=el_status_new(ielabel)
				el_status_new(ielabel)=ielstat				
			endif
c	-------------------------------------------------------------------				
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
c	-------------------------------------------------------------------		  	  	  
  
	  
		
	 
	 
	 
	 
	 
