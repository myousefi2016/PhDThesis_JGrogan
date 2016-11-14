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
c	-------------------------------------------------------------------

c	These subroutines control the velocity of exterior nodes in the
c	ALE adaptive mesh domain for 3D uniform corrosion analysis.	     
c	------------------------------------------------------------------
c	SUB UEXTERNALDB: This is used only at the begining of an analysis.
c	It populates the 'facet' and 'nbr' common block arrays.	  
	  subroutine uexternaldb(lop,lrestart,time,dtime,kstep,kinc)
		include 'aba_param.inc'
c	  	Common Block Declarations
		parameter (maxNodes=700000,maxFacets=700000)
		integer nbr(maxNodes,5),facet(maxFacets,12)
		real crd(maxNodes,3)
		common nbr,facet,crd
c	  	Other Declarations
		integer n(8)
		character*256 outdir
c	  
		if(lop==0.or.lop==4)then
			call getoutdir(outdir,lenoutdir)		
			nbr=0
			open(unit=101,file=outdir(1:lenoutdir)//'\nodedata.inc',
     1			status='old')
			read(101,*)numfaces
			do i=1,4*numfaces,4
				read(101,*)nfix,n(1),n(2),n(3),n(4),n(5),n(6),n(7),n(8)
c				facet(*,12)=fized face flag, facet(*,4-11)=element nodes			
				do j=1,4
					ind=i+j-1
					facet(ind,12)=nfix
					do k=1,8
						facet(ind,3+k)=n(k)
					enddo
				enddo
				do j=1,4
					ind=i+j-1
c					facet(*,1-3)=nodes in facet				
					read(101,*)facet(ind,1),facet(ind,2),facet(ind,3)
					node=facet(ind,1)
c					nbr(node,1)=counter for facets per node
					if(nbr(node,1)==0)nbr(node,1)=1
					nbr(node,1)=nbr(node,1)+1
c					nbr(node,>1)=facet number					
					nbr(node,nbr(node,1))=ind
				enddo
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
		dimension coords(3)
c	  	Common Block Declarations
		parameter (maxNodes=700000,maxFacets=700000)
		integer nbr(maxNodes,5),facet(maxFacets,12)
		real crd(maxNodes,3)
		common nbr,facet,crd
c		
		crd(node,1)=coords(1)
		crd(node,2)=coords(2)
		crd(node,3)=coords(3)
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
		parameter (maxNodes=700000,maxFacets=700000)
		integer nbr(maxNodes,5),facet(maxFacets,12)
		real crd(maxNodes,3)
		common nbr,facet,crd
c		Other Declarations		
		integer np(3)
		real fp(6,9),fc(6,3),fe(6,3),fn(6,3),a(3),b(3),c(3),d(3),q(3)
		real qnew(3),cp1(3),cp2(3),cp3(3)
		if(lnodetype>=3.and.lnodetype<=5)then
C			PRINT *,NODE,'IN'		
c			Analysis Parameters
			velocity=0.02d0
			tol=1.d-5
c
			numFacets=nbr(node,1)-1	
c			get facet point coords (fp).	
			do i=1,numFacets
				nFacet=nbr(node,i+1)
				do j=1,3
					nNode=facet(nFacet,j)
					if (j==1)nnode=node
					do k=1,3
						fp(i,3*(j-1)+k)=crd(nNode,k)
					enddo
c					print *,node,nNode
c					print *,crd(nNode,1),crd(nNode,2),crd(nNode,3)
				enddo
			enddo
c			get facet element centroid(fe)	
			fe=0.
			do i=1,numFacets
				nFacet=nbr(node,i+1)
				do j=1,8
					nNode=facet(nFacet,j+3)
					do k=1,3
						fe(i,k)=fe(i,k)+crd(nNode,k)/8.						
					enddo
				enddo
			enddo	
c			get facet centroids (fc)
			do i=1,numFacets
				do j=1,3
					fc(i,j)=(fp(i,j)+fp(i,j+3)+fp(i,j+6))/3.
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
				dp=0.
				do j=1,3
					dp=dp+c(j)*(fe(i,j)-fc(i,j))
				enddo
				rsign=1
				if(dp<0.)rsign=-1
				do j=1,3			
					fn(i,j)=rsign*c(j)/rlen
				enddo	
			enddo			
c			move non-fixed facets along unit normals - update fp
			dist=velocity*dtime
			do i=1,numFacets
				nFacet=nbr(node,i+1)
				if(facet(nFacet,12)/=1)then
					do j=1,3
						fp(i,j)=fp(i,j)+fn(i,j)*dist
						fp(i,j+3)=fp(i,j+3)+fn(i,j)*dist
						fp(i,j+6)=fp(i,j+6)+fn(i,j)*dist
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
						dp=0.								
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
							dp1=0.	
							dp2=0.
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
				dp=0.
				do i=1,3
					dp=dp+(q(i)-fp(1,i))*fn(1,i)
				enddo
				do i=1,3
					qnew(i)=q(i)-dp*fn(1,i)
				enddo
			elseif(method==2)then
c				get distances d from each plane to origin
				do i=1,3
					d(i)=0.
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
					d(i)=0.
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
				dp=0.
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
c			print *,node,a(1),a(2),a(3)
			do i=1,3
				uglobal(i) = a(i)
			enddo
			do i=1,ndim
				tlocal(i)=0.
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
	  
