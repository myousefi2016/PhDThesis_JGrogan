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
c       Initial Version: 2013

      subroutine vuanisohyper_inv(nblock,nFiber,nInv,jElem,kIntPt,
     *	kLayer,kSecPt,cmname,nstatev, nfieldv, nprops,props,tempOld,
     *	tempNew,fieldOld,fieldNew,stateOld,sInvariant,zeta,uDev,duDi,
     *	d2uDiDi,stateNew)
c
      include 'vaba_param.inc'
c
      dimension  props(nprops),tempOld(nblock),
     *	fieldOld(nblock,nfieldv),stateOld(nblock,nstatev),
     *	tempNew(nblock), fieldNew(nblock,nfieldv),
     *	stateNew(nblock,nstatev),sInvariant(nblock,nInv),
     *	zeta(nblock,nFiber*(nFiber-1)/2),uDev(nblock),
     *	duDi(nblock,nInv),d2uDiDi(nblock,nInv*(nInv+1)/2)
c
		parameter(zero = 0.d0, one = 1.d0, two = 2.d0, three = 3.d0)
c		Material Properties
		u = props(1)
		rkap = props(2)
		rk1 = props(3)
		rk2 = props(4)
		rp = props(5)	
c		
c		Loop Over Each Element
		do k = 1,nblock			
c			Index Each Invariant according to Abaqus Convention
			i1 = 1
			i1i1 = 1
			i3 = 3
			i3i3 = 6
			i4 = 4
			i1i4 = 7
			i4i4 = 10
			i6 = 8
			i1i6 = 29
			i6i6 = 36		
c			Get Values of each Invariant
			ri1 = sinvariant(k,i1)
			ri4 = sinvariant(k,i4)
			ri6 = sinvariant(k,i6)						
c			Get Fibre Contributions to UDEV
			t = (one - rp) * (ri1 - three) * (ri1 - three)
			if(ri4>1.)then			
				t1 = rk2 * (t + rp * (ri4 - one) * (ri4 - one))
			else
				t1=0.
			endif
			if(ri6>1.)then	
				t2 = rk2 * (t + rp * (ri6 - one) * (ri6 - one))		
			else
				t2=0.
			endif
			et1 = exp(t1)
			et2 = exp(t2)
			term1 = rk1 / (two * rk2)
			ufibres = term1 * (et1 + et2 - two)
c			Get UDEV
			udev(k) = u * (ri1 - three) + ufibres	
c			Get dUdI1
			dt1di1 = rk2 * two * (one - rp) * (ri1 - three)
			dudi(k,i1) = term1 * dt1di1 * (et1 + et2) + u
c			Get dUdI4 and dUdI6
			if(ri4>1.)then
				dt1di4 = rk2 * two * rp * (ri4 - one)
			else
				dt1di4 = 0.
			endif
			if(ri6>1.)then
				dt2di6 = rk2 * two * rp * (ri6 - one)
			else
				dt2di6 = 0.
			endif
			dudi(k,i4) = term1 * dt1di4 * et1
			dudi(k,i6) = term1 * dt2di6 * et2
c			Get d2UdI1dI1
			d2t1di1di1 = rk2 * two * (one - rp)
			d2udidi(k,i1i1) = term1 * (d2t1di1di1 + dt1di1 * dt1di1)
			d2udidi(k,i1i1) = d2udidi(k,i1i1) * (et1 + et2)
c			Get d2UdI1dI4 and d2UdI4dI4
			d2udidi(k,i1i4) = term1 * dt1di4 * dt1di1 * et1
			d2t1di4di4 =  rk2 * two * rp 
			d2udidi(k,i4i4) = term1 * (dt1di4 * dt1di4 + d2t1di4di4)
			d2udidi(k,i4i4) = d2udidi(k,i4i4) * et1
c			Get d2UdI1dI6 and d2UdI6dI6
			d2udidi(k,i1i6) = term1 * dt2di6 * dt1di1 * et2
			d2t2di6di6 =  rk2 * two * rp 
			d2udidi(k,i6i6) = term1 * (dt2di6 * dt2di6 + d2t2di6di6)
			d2udidi(k,i6i6) = d2udidi(k,i6i6) * et2       			
		end do    
c     	For the compressible case
		if(rkap > zero) then
			do k = 1,nblock
				rj = sInvariant(k,i3)
				dudi(k,i3) = rkap * (rj-one)
c				duDi(k,i3) = (rkap/two) * (rj - one/rj)
				d2udidi(k,i3i3) = rkap 
c				d2uDiDi(k,i3i3)= (rkap/two) * (one + one/ rj / rj)
			end do
		end if
      return
      end	 	 	 	 
