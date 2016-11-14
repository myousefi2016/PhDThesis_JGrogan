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
c       Initial Version: 2012

c	These subroutines control the velocity of exterior nodes in the
c	ALE adaptive mesh domain for 3D uniform corrosion analysis.	     
c	------------------------------------------------------------------
c	SUB UEXTERNALDB: This is used only at the begining of an analysis.
c	It populates the 'facet' and 'nbr' common block arrays.	  
	  subroutine uexternaldb(lop,lrestart,time,dtime,kstep,kinc)
		include 'aba_param.inc'
c	  	Common Block Declarations
		parameter (maxNodes=40000,maxFacets=100000)
		integer ndata(maxNodes,2),facet(maxFacets,18)
		real crd(maxNodes,3),tmp(maxNodes)
		common ndata,facet,crd,tmp
c	  	Other Declarations
		integer n(16)
		character*256 outdir		
c	  
		if(lop==0.or.lop==4)then
			call getoutdir(outdir,lenoutdir)		
			open(unit=101,file=outdir(1:lenoutdir)//'/NodeData.inc',
     1			status='old')
			read(101,*)numNodes
			ntotalFacets=1
			do i=1,numNodes
				read(101,*)nodeLabel,numFacets
				ndata(nodeLabel,1)=ntotalFacets
				ndata(nodeLabel,2)=numFacets				
				do j=1,numFacets
					read(101,*)nbr1,nbr2
					read(101,*)n(1),n(2),n(3),n(4),n(5),n(6),n(7),n(8)
					read(101,*)n(9),n(10),n(11),n(12),n(13),n(14),n(15),n(16)
					facet(ntotalFacets-1+j,1)=nbr1
					facet(ntotalFacets-1+j,2)=nbr2
					do k=3,18
						facet(ntotalFacets-1+j,k)=n(k-2)
					enddo			
				enddo
				ntotalFacets=ntotalFacets+numFacets
			enddo
			close(unit=101)
		endif
		return
      end
c	------------------------------------------------------------------
c	SUB UFIELD: This is used at the start of each analysis increment.
c	It populates the 'crd' common block array.	 	  
      subroutine ufield(field,kfield,nsecpt,kstep,kinc,time,node,
     1 	coords,temp,dtemp,nfield)
		include 'aba_param.inc'
		dimension coords(3),TEMP(NSECPT)
c	  	Common Block Declarations
		parameter (maxNodes=40000,maxFacets=100000)
		integer ndata(maxNodes,2),facet(maxFacets,18)
		real crd(maxNodes,3),tmp(maxNodes)
		common ndata,facet,crd,tmp
c		
		crd(node,1)=coords(1)
		crd(node,2)=coords(2)
		crd(node,3)=coords(3)
		tmp(node)=temp(1)
		return
      end	
c	------------------------------------------------------------------
c	SUB UMESHMOTION: This is used at the start of each mesh sweep.
c	It calculates the velocity of each node in the local coord system.	  
      subroutine umeshmotion(uref,ulocal,node,nndof,lnodetype,alocal,
     $  ndim,time,dtime,pnewdt,kstep,kinc,kmeshsweep,jmatyp,jgvblock,
     $  lsmooth)
        include 'aba_param.inc'
c     	user defined dimension statements
        dimension ulocal(*),uglobal(ndim),tlocal(ndim)
        dimension alocal(ndim,*),time(2)
c	  	Common Block Declarations
		parameter (maxNodes=40000,maxFacets=100000)
		integer ndata(maxNodes,2),facet(maxFacets,18)
		real crd(maxNodes,3),tmp(maxNodes)
		common ndata,facet,crd,tmp
c		Other Declarations		
		integer np(3)
		real fp(4,9),fc(4,3),fe(4,3),fn(4,3),a(3),b(3),Amat(4,4)
		real c(3),d(3),q(3),qnew(3),cp1(3),cp2(3),cp3(3),dist(4)
		real pt(3),qd(3,2),p1(3),p2(3),rn(8,4)
		integer flabel(10,3)
		if(lnodetype>=3.and.lnodetype<=5)then
c			print *,node,time(1),'in'
c			Analysis Parameters
			tol=1.d-5
			numFacets=ndata(node,2)	
c			get facet point coords (fp).	
			do i=1,numFacets
				nFacet=ndata(node,1)-1+i
				nbr1=facet(nFacet,1)
				nbr2=facet(nFacet,2)					
				do k=1,3
					fp(i,k)=crd(node,k)
					fp(i,k+3)=crd(nbr1,k)
					fp(i,k+6)=crd(nbr2,k)
				enddo
			enddo			
c			get facet element centroid(fe)	
			fe=0.d0
			do i=1,numFacets
				nFacet=ndata(node,1)-1+i
				do j=1,8
					nNode=facet(nFacet,j+10)
					do k=1,3
						fe(i,k)=fe(i,k)+crd(nNode,k)/8.d0						
					enddo
				enddo
			enddo				
c			get facet centroids (fc)
			do i=1,numFacets
				do j=1,3
					fc(i,j)=(fp(i,j)+fp(i,j+3)+fp(i,j+6))/3.d0
				enddo
			enddo
c			get facet normals (fn)
			do i=1,numFacets
				do j=1,3
					a(j)=fp(i,j+3)-fp(i,j)
					b(j)=fp(i,j+6)-fp(i,j)
				enddo
				call crossprod(a,b,c)
				rlen=sqrt(c(1)*c(1)+c(2)*c(2)+c(3)*c(3))
c				get inward pointing unit normal
				dp=0.d0
				do j=1,3
					dp=dp+c(j)*(fe(i,j)-fc(i,j))
				enddo
				rsign=1
				if(dp<0.)rsign=-1
				do j=1,3			
					fn(i,j)=rsign*c(j)/rlen
				enddo	
			enddo
c			get facet velocity
c			PNEWDT=10000.
			if_check=0
			do i=1,numFacets
				nFacet=ndata(node,1)-1+i
c				check if facet has neighbours
				if(Facet(nFacet,3)==0)then
					dist(i)=0.d0
				else
					do j=1,8
						rn(j,1)=crd(Facet(nFacet,2+j),1)
						rn(j,2)=crd(Facet(nFacet,2+j),2)
						rn(j,3)=crd(Facet(nFacet,2+j),3)
						rn(j,4)=tmp(Facet(nFacet,2+j))
					enddo
					call getFlabels(flabel)
					do j=1,10
						label1=flabel(j,1)
						label2=flabel(j,2)
						label3=flabel(j,3)
						do k=1,3
							Amat(1,k)=1.d0
						enddo
						Amat(1,4)=0.d0
						do k=1,3
							Amat(k+1,1)=rn(label1,k)
							Amat(k+1,2)=rn(label2,k)
							Amat(k+1,3)=rn(label3,k)
							Amat(k+1,4)=fn(i,k)							
						enddo
						call getDet(Amat,Det1)
						if (Det1==0)cycle
						Amat(1,4)=1.d0
						do k=1,3
							Amat(k+1,4)=fc(i,k)
						enddo	
						call getDet(Amat,Det2) 
						t=-det2/det1																
						do k=1,3
							pt(k)=fc(i,k)+fn(i,k)*t
							p1(k)=rn(label1,k)
							p2(k)=rn(label2,k)
						enddo						
						call getDist(p1,p2,d21) 
						do k=1,3
							p1(k)=rn(label1,k)
							p2(k)=rn(label3,k)
						enddo      
						call getDist(p1,p2,d31) 
						do k=1,3
							p1(k)=rn(label2,k)
							p2(k)=rn(label3,k)
						enddo      
						call getDist(p1,p2,d23)  						
						qd(1,1)=0.d0
						qd(1,2)=0.d0
						qd(2,1)=sqrt(d21)
						qd(2,2)=0.d0
						qd(3,1)=(d21-d23+d31)/(2.d0*sqrt(d21))  
						term=4.d0*d21*d31-(d21-d23+d31)**2
						qd(3,2)=sqrt(term/(4.d0*d21))        
						if(qd(3,2)<0)qd(3,2)=-qd(3,2)				
						do k=1,3
							p1(k)=rn(label1,k)
							p2(k)=pt(k)
						enddo      
						call getDist(p1,p2,d1t)	
						do k=1,3
							p1(k)=rn(label2,k)
							p2(k)=pt(k)
						enddo      
						call getDist(p1,p2,d2t)	        	
						do k=1,3
							p1(k)=rn(label3,k)
							p2(k)=pt(k)
						enddo 				
						call getDist(p1,p2,d3t)	
						x=(d21-d2t+d1t)/(2.d0*sqrt(d21))
						y1=sqrt((4.d0*d21*d1t-(d21-d2t+d1t)**2)
     $						/(4.d0*d21))						
						d1=(x-qd(3,1))*(x-qd(3,1))
						d2=(y1-qd(3,2))*(y1-qd(3,2))
						dst=d1+d2
						if((dst>=d3t-0.0001).or.(dst<=d3t+0.0001))then
						  y=y1
						else
						  y=-y1
						endif	
						t1=(x-qd(3,1))/(qd(1,1)-qd(3,1))
						t2=(y-qd(3,2))/(qd(1,2)-qd(3,2))
						t3=(qd(2,1)-qd(3,1))/(qd(1,1)-qd(3,1))
						t4=(qd(2,2)-qd(3,2))/(qd(1,2)-qd(3,2))
						t=(t1-t2)/(t3-t4)
						term=t*(qd(3,2)-qd(2,2))+y-qd(3,2)
						s=term/(qd(1,2)-qd(3,2))											
						if((s>=0.).and.(t>=0.).and.(1.-s-t>=0.))then
						  temp=rn(label1,4)*s+rn(label2,4)*t
						  temp=temp+rn(label3,4)*(1.-s-t)
						  dx=(pt(1)-fc(i,1))*(pt(1)-fc(i,1))
						  dy=(pt(2)-fc(i,2))*(pt(2)-fc(i,2))
						  dz=(pt(3)-fc(i,3))*(pt(3)-fc(i,3))
						  grad=(13.4d0-temp)/(sqrt(dx+dy+dz))
						  exit
						endif
					enddo	
					vel=grad*1.0575d0*0.507013518d0/(1735.d0-13.4d0)
					dist(i)=vel*dtime
					dtnew=abs(0.5d-3/(vel*dtime))
					if(dtnew<PNEWDT)pnewdt=dtnew
					if(pnewdt*dtime>=0.002)PNEWDT=0.002d0/dtime
c					if(dtime>=0.002)PNEWDT=1.d0
				end if								
			enddo		
c			move non-fixed facets along unit normals - update fp
			do i=1,numFacets
				nFacet=ndata(node,i+1)
				if(facet(nFacet,12)/=1)then
					do j=1,3
						fp(i,j)=fp(i,j)+fn(i,j)*dist(i)
						fp(i,j+3)=fp(i,j+3)+fn(i,j)*dist(i)
						fp(i,j+6)=fp(i,j+6)+fn(i,j)*dist(i)
					enddo
				endif
			enddo
c			get old node position (q)
			do i=1,3
				q(i)=crd(node,i)
			enddo
c			determine method to get qnew and relevant planes	
c			method depends on # of unique normal directions
			numpairs=0
			if(numfacets==1)then
				method=1
			else
				numdir=0
				do i=1,numfacets-1
					do j=i+1,numfacets											
						dp=0.d0								
						do k=1,3
							dp=dp+fn(i,k)*fn(j,k)
						enddo											
						if(abs(dp)<1.-tol.or.abs(dp)>1.+tol)then
							np(1)=i
							np(2)=j
							numdir=2
						endif
						if (numdir==2)continue
					enddo
					if(numdir==2)continue
				enddo		
				if(numdir==2)then
					method=3
					do i=1,numfacets
						if(i/=np(1).and.i/=np(2))then
							dp1=0.d0	
							dp2=0.d0
							do j=1,3
								dp1=dp1+fn(np(1),j)*fn(i,j)
								dp2=dp2+fn(np(2),j)*fn(i,j)
							enddo											
							if(abs(dp1)<1.-tol.or.abs(dp1)>1.+tol)then							
								if(abs(dp2)<1.-tol.or.
     $								abs(dp2)>1.+tol)then
									np(3)=i
									numdir=3
									method=2
								endif
							endif	
						endif
					enddo
				else
					method=1
				endif
			endif
c			Get new node position		
			if(method==1)then						
c				get projection of old point q onto any plane
c				qnew = q - ((q - p1).n)*n
				dp=0.d0
				do i=1,3
					dp=dp+(q(i)-fp(1,i))*fn(1,i)
				enddo
				do i=1,3
					qnew(i)=q(i)-dp*fn(1,i)
				enddo
			elseif(method==2)then
c				get distances d from each plane to origin
				do i=1,3
					d(i)=0.d0
					do j=1,3
						d(i)=d(i)-fn(np(i),j)*fp(np(i),j)
					enddo
				enddo
c				get n1 x n2				
				do i=1,3
					a(i)=fn(np(1),i)
					b(i)=fn(np(2),i)
				enddo
				call crossprod(a,b,cp1)
c				get n2 x n3
				do i=1,3
					a(i)=fn(np(2),i)
					b(i)=fn(np(3),i)
				enddo
				call crossprod(a,b,cp2)
c				get n3 x n1
				do i=1,3
					a(i)=fn(np(3),i)
					b(i)=fn(np(1),i)
				enddo				
				call crossprod(a,b,cp3)
c				get intersection of 3 planes
c				qnew = (-d1(n2 x n3)-d2(n3 x n1)-d3(n1 x n2))/(n1.(n2 x n3))
				denom=fn(np(1),1)*cp2(1)+fn(np(1),2)*cp2(2)
     $				+fn(np(1),3)*cp2(3)	
				do i=1,3
					qnew(i)=-(d(1)*cp2(i)+d(2)*cp3(i)+d(3)*cp1(i))
     $					/denom		
				enddo
			else
c				find line of intersection of planes given by a point
c				and vector
				do i=1,2
					d(i)=0.d0
					do j=1,3
						d(i)=d(i)-fn(np(i),j)*fp(np(i),j)
					enddo
				enddo
c				get n1 x n2				
				do i=1,3
					a(i)=fn(np(1),i)
					b(i)=fn(np(2),i)
				enddo
				call crossprod(a,b,cp1)			
				rlen=sqrt(cp1(1)*cp1(1)+cp1(2)*cp1(2)+cp1(3)*cp1(3))
				do i=1,3
					a(i)=d(2)*fn(np(1),i)-d(1)*fn(np(2),i)
				enddo
c				get (d2n1 - d1n2) x (n1 x n2)			
				call crossprod(a,cp1,cp2)
c				a = unit vector along line
c				b = point on line			
				do i=1,3
					a(i)=cp1(i)/rlen
					b(i)=cp2(i)/(rlen*rlen)
				enddo
c				get projection of node onto line
c				bq'=((bq).a)*a
				dp=0.d0
				do i=1,3
					dp=dp+(q(i)-b(i))*a(i)
				enddo
				do i=1,3
					qnew(i)=b(i)+dp*a(i)
				enddo
			endif	  
			do i=1,3
				a(i)=(qnew(i)-q(i))/dtime
			enddo
c			print *,node,time(1),pnewdt,a(1),a(2),a(3)
			do i=1,3
				uglobal(i) = a(i)
			enddo	
			do i=1,ndim
				tlocal(i)=0.d0
				do j=1,ndim
					tlocal(i)=tlocal(i)+uglobal(j)*alocal(j,i)
				enddo
			enddo
			do i=1,ndim
				ulocal(i)=tlocal(i)
			enddo			
		endif
		lsmooth=1
		return
      end
c	  Return cross product(c) for input vectors (a, b)
	  subroutine crossprod(a,b,c)
		include 'aba_param.inc'				
		real a(3),b(3),c(3)
		c(1)=a(2)*b(3)-a(3)*b(2)
		c(2)=a(3)*b(1)-a(1)*b(3)
		c(3)=a(1)*b(2)-a(2)*b(1)	
		return
      end
	  subroutine getFlabels(flabel)
		 include 'aba_param.inc'	
		 integer flabel(10,3)
		 flabel(1,1)=6
		 flabel(1,2)=8
		 flabel(1,3)=7
		 flabel(2,1)=6
		 flabel(2,2)=7
		 flabel(2,3)=5
		 flabel(3,1)=6
		 flabel(3,2)=2
		 flabel(3,3)=4
		 flabel(4,1)=6
		 flabel(4,2)=4
		 flabel(4,3)=8
		 flabel(5,1)=5
		 flabel(5,2)=1
		 flabel(5,3)=3
		 flabel(6,1)=5
		 flabel(6,2)=3
		 flabel(6,3)=7
		 flabel(7,1)=3
		 flabel(7,2)=4
		 flabel(7,3)=8
		 flabel(8,1)=3
		 flabel(8,2)=8
		 flabel(8,3)=7
		 flabel(9,1)=1
		 flabel(9,2)=2
		 flabel(9,3)=6
		 flabel(10,1)=1
		 flabel(10,2)=6
		 flabel(10,3)=5
		 return
	  end subroutine
      subroutine getDet(A,Det)
	    include 'aba_param.inc'
      	real A(4,4)	
			A1=A(3,3)*A(4,4)-A(3,4)*A(4,3)
            A2=A(3,4)*A(4,2)-A(3,2)*A(4,4)
            A3=A(3,2)*A(4,3)-A(3,3)*A(4,2)
            B1=A(1,1)*(A(2,2)*A1+A(2,3)*A2+A(2,4)*A3)
			A1=A(3,3)*A(4,4)-A(3,4)*A(4,3)
            A2=A(3,4)*A(4,1)-A(3,1)*A(4,4)
            A3=A(3,1)*A(4,3)-A(3,3)*A(4,1)
            B2=A(1,2)*(A(2,1)*A1+A(2,3)*A2+A(2,4)*A3)
            A1=A(3,2)*A(4,4)-A(3,4)*A(4,2)
            A2=A(3,4)*A(4,1)-A(3,1)*A(4,4)
            A3=A(3,1)*A(4,2)-A(3,2)*A(4,1)
			B3=A(1,3)*(A(2,1)*A1+A(2,2)*A2+A(2,4)*A3)
			A1=A(3,2)*A(4,3)-A(3,3)*A(4,2)
            A2=A(3,3)*A(4,1)-A(3,1)*A(4,3)
            A3=A(3,1)*A(4,2)-A(3,2)*A(4,1)
            B4=A(1,4)*(A(2,1)*A1+A(2,2)*A2+A(2,3)*A3)                       
            DET =B1-B2+B3-B4                         
       end subroutine 	  
       subroutine getDist(p1,p2,dist)
	   	include 'aba_param.inc'
       	real p1(3),p2(3)
       	     d21x=(p2(1)-p1(1))*(p2(1)-p1(1))
     		 d21y=(p2(2)-p1(2))*(p2(2)-p1(2))
             d21z=(p2(3)-p1(3))*(p2(3)-p1(3))
        	 dist=d21x+d21y+d21z 	         
        end subroutine	  
