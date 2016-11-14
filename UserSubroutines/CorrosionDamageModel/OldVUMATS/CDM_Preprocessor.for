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

c	User Subroutines for simulating corrosion in Abaqus/Explicit.
c
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
c -------------------------------------------------------------------
		include 'vaba_param.inc' 
		dimension strainInc(nblock,ndir+nshr),stressOld(nblock,ndir+nshr), 
     6 	stressNew(nblock,ndir+nshr)
c
		character*80 cmname
c		
		parameter (one = 1.d0, two = 2.d0)
c				
		if(steptime==0.)then
			do k=1,nblock
				e = 44000.
				xnu = 0.3
				twomu = e / ( one + xnu )
				alamda = xnu * twomu / ( one - two * xnu )
c				
				trace=strainInc(k,1)+strainInc(k,2)+strainInc(k,3)
				stressNew(k,1)=stressOld(k,1)
     * 				+twomu*strainInc(k,1)+alamda*trace
				stressNew(k,2)=stressOld(k,2)
     * 				+twomu*strainInc(k,2)+alamda*trace
				stressNew(k,3)=stressOld(k,3)
     * 				+twomu*strainInc(k,3)+alamda*trace
				stressNew(k,4)=stressOld(k,4)+twomu*strainInc(k,4)
				stressNew(k,5)=stressOld(k,5)+twomu*strainInc(k,5)
				stressNew(k,6)=stressOld(k,6)+twomu*strainInc(k,6)	
			enddo
		else
c				
			call get_elem_con
		endif
	  end subroutine
c	  	  
	  subroutine get_elem_con
	  	include 'vaba_param.inc' 
c	  
		character*256 jobname,outdir,filename,input
		common neighbour(400000,6,6)
		common active(400000,2)
		common active_temp(400000,2)
		common ele(400000,9)
		common cpr(400000)
		common iseed(400000)
		integer iseed
		real cpr
		integer neighbour
		integer active
		integer active_temp
		integer ele
		integer com_nodes
		integer node_store(100)
		integer output(6)
		integer ipair(6)
		integer notpair(6)
		integer isize
c		
c		set-1 - 2288795
		iseed=2288795
c		set-2 - 752347
c		iseed=752347
c		set-3 - 100887
c		iseed=100887
c		set-4 - 9921267
c		iseed=9921267
c		set-5 - 57269
c		iseed=57269
c		
c		Open INP file for reading.
c
		call vgetjobname(jobname,lenjobname)
		call vgetoutdir(outdir,lenoutdir)
		filename=outdir(1:lenoutdir)//'\'//
     * 		jobname(1:lenjobname)//'.inp' 
		open(unit=17,file=filename(1:lenoutdir+			        
     * 		lenjobname+5),status='unknown')
		filename=outdir(1:lenoutdir)//'\neighbours_'//
     *		jobname(1:lenjobname)//'.inc'
		open(unit=18,file=filename(1:lenoutdir+lenjobname+			        
     * 		16),status='unknown')
		filename=outdir(1:lenoutdir)//'\elsets_'//
     *		jobname(1:lenjobname)//'.inc'
		open(unit=19,file=filename(1:lenoutdir+lenjobname+			        
     * 		12),status='unknown')	 
c		
		ncnt=0
		nelcnt=0
		icheck=1
c		
c		Skip down to *Element in INP File
c	 
		do while (index(input,'*Element')==0)
			read(17,'(a)')input
		end do
c							
c		Read in Element Nodal Connectivity	
c	
		do while(.true.)
			read(17,*)input								
	 		if(index(input,'*')==0)then
				backspace(17)
				nelcnt=nelcnt+1	
				read(17,*)ele(nelcnt,1),ele(nelcnt,2),
     * 				ele(nelcnt,3),ele(nelcnt,4),ele(nelcnt,5),
     *	 			ele(nelcnt,6),ele(nelcnt,7),ele(nelcnt,8),
     *	 			ele(nelcnt,9)
			else
				exit
			endif
		end do
c
		isize=nelcnt
c		Get Element Connectivity
		call get_surf	
c		call random_seed(size=isize)
		call random_seed(put=iseed(1:isize))
		call random_number(cpr(1:isize))
c
		do i=1,nelcnt
			cpr(i)=(-log(1.d0-cpr(i)))**(1.d0/0.14)
		enddo
		write(18,*)'*INITIAL CONDITIONS,TYPE=SOLUTION'
		do ele_loop1=1,nelcnt
			num_neighbours=1          
			do ele_loop2=1,nelcnt
				elecheck=0  
				com_nodes=0
				do nlp1=2,9
					do nlp2=2,9
					  if(ele(ele_loop2,nlp1)==ele(ele_loop1,nlp2))then
							if(ele_loop1/=ele_loop2)then
								com_nodes=com_nodes+1
							  node_store(com_nodes)=ele(ele_loop1,nlp2)
								if(com_nodes==4)then
								elecheck=1
!								call vgetinternal('AADEGPART',ele
!     *								(ele_loop2,1),1,intnum2,jrcd)
!								call vgetinternal('AADEGPART',ele
!     *								(ele_loop1,1),1,intnum1,jrcd)
								intnum1=ele(ele_loop1,1)
								intnum2=ele(ele_loop2,1)
								neighbour(intnum1,num_neighbours,1)
     *								=intnum2
	 							neighbour(intnum1,1,2)
     *								=num_neighbours
								do i=1,4
								  neighbour(intnum1,num_neighbours,i+2)
     *								=node_store(i)
								enddo
								endif	 
							end if
					  end if
					enddo
				enddo
				if(elecheck==1)then
					num_neighbours=num_neighbours+1
				endif
			enddo
			int_point_num=intnum1
			ipair=0
			output=0
			numpairs=0
c			
c			Determine which faces of an element are opposite each other
c
			do i=1,num_neighbours-1
				do k=1,num_neighbours-1
					ibreak=0
					if(i/=k)then
						do m=1,6
							if((i==ipair(m)).or.(k==ipair(m)))then
								ibreak=1
							endif
						enddo
						if(ibreak==1)then
							cycle
						endif
						icheck=0
						do j=1,4
							do m=1,4
							if(neighbour(int_point_num,i,j+2)==
     *							neighbour(int_point_num,k,m+2))then							
								icheck=1
							endif
							enddo
						enddo
						if (icheck==0)then
							numpairs=numpairs+2	
							ipair(numpairs-1)=i
							ipair(numpairs)=k
						endif
					endif
				enddo
			enddo
c			
c			Order SDV's in convenient format for Main Analysis
c			
			k=0
			do i=1,num_neighbours-1
				icheck=0
				do j=1,numpairs
					if(i==ipair(j))then
						icheck=1
					endif
				enddo
				if(icheck==0)then
					k=k+1
					notpair(k)=i
				endif
			enddo
			do i=1,numpairs,2
				output(i)=neighbour(int_point_num,ipair(i),1)
				output(i+1)=neighbour(int_point_num,ipair(i+1),1)
				if(int_point_num==13)then
				print *,i
				endif
			enddo
			do i=1,k
				output(numpairs+i)=
     *				neighbour(int_point_num,notpair(i),1)	
			enddo
c			
c			Write output to Abaqus Input file for main analysis	
c	
c			cpr=rand(0)
			write(19,*)'*Elset, elset=e',int_point_num,
     *			', instance=AADEGPART'
	 		write(19,*)int_point_num,','
			write(18,'(a,8(i6,a))')'e',int_point_num,',',
     *		   output(1),',',output(2),',',output(3),',',output(4),',',
     *	 	   output(5),',',output(6),',',numpairs/2,','
			write(18,'(8(i6,a))')active(int_point_num,1),',',
     *		   active(int_point_num,2),',',0,',',0,',',0,',',
     *	 	   0,',',0,',',0,',' 
			write(18,'(8(i6,a))')0,',',0,',',0,',',0,',',1,',',
     *		   0,',',0,',',0,','
			write(18,'(6(i6,a),f18.6)')0,',',0,',',0,',',0,',',0,',',
     *		   0,',',cpr(int_point_num)			
	   enddo
		call xplb_exit		
		return
	  end subroutine get_elem_con
c
c -------------------------------------------------------------------
c
c 	  get_surf - This subroutine reads element numbers in any surface
c				 that has been named 'Corrosion'. 
c	  	  
	  subroutine get_surf
	  	include 'vaba_param.inc' 
c	  
	  	character*256 input,test_string,output
		common neighbour(400000,6,6)
		common active(400000,2)
		common active_temp(400000,2)
		common ele(400000,9)
		common cpr(400000)
		common iseed(400000)
		integer iseed
		real cpr
		integer neighbour
		integer active
		integer active_temp
		integer ele
c		
	    num_active=0
c
c		Find the first Corrosion keyword in the INP file
c		
	    do while (index(input,'Corrosion')==0)
			read(17,'(a)')input
		end do
c		
c		For any *Surface definition with the Corrosion Keyword
c		read in element numbers.
c		
		do while (index(input,'*Surface')==0)
			if(index(input,'Corrosion')/=0)then
c			
c				If the generate keyword is found element numbering
c				can be generated automatically.	
c			
				if(index(input,'generate')/=0)then
					read(17,'(3i)')isurf1,isurf2,isurf3
					do i=isurf1,isurf2,isurf3
						num_active=num_active+1
						active(num_active,1)=i
					enddo       
				else
c				
c				If not it must be generated manually. An entire line is
c				read from file and then split into individual element
c				number using ',' as a delimiter.
c				
					read(17,'(a)')input			
					do while(index(input,'*')==0)		
						index_left=1
						do index_right=1,128
							test_string=input(index_right:index_right)
							if((test_string==',').or.
     *							(index_right==128))then
c	 							Necessary to convert character input to
c								Integer output.
								write(output,*)input
     *								(index_left:index_right-1)
								num_active=num_active+1
								read(output,'(i)')ihold
								active(num_active,1)=ihold
								index_left=index_right+1
							endif
						enddo
						read(17,'(a)')input	
					enddo
					backspace(17)
				endif
			endif
			read(17,'(a)')input
		enddo
		do i=1,num_active
		call vgetinternal('AADEGPART',active(i,1),1,intnum,jrcd)			
c			active_temp(i,1)=intnum
			active_temp(i,1)=active(i,1)
		enddo
		active=0
		do i=1,num_active
c			First Face Exposed		
			if(active(active_temp(i,1),2)==0)then
				active(active_temp(i,1),1)=active(active_temp(i,1),1)+4
c			Second Face Exposed				
			elseif(active(active_temp(i,1),2)==1)then
				active(active_temp(i,1),1)=active(active_temp(i,1),1)+2
c				Single Element Test - 2 Faces In Plane				
c				active(active_temp(i,1),1)=8					
c			Third Face Exposed				
			elseif(active(active_temp(i,1),2)==2)then
				active(active_temp(i,1),1)=active(active_temp(i,1),1)+1
c				Single Element Test - 3 Faces In Plane				
C				active(active_temp(i,1),1)=8
			elseif(active(active_temp(i,1),2)==3)then
				active(active_temp(i,1),1)=8		
			endif			
			active(active_temp(i,1),2)=active(active_temp(i,1),2)+1
c			active(active_temp(i,1),11)=0
		enddo
	  end subroutine get_surf
c	  
c -------------------------------------------------------------------
c
c 	  vusdfld - This subroutine is neccesary due to a limitation in
c				Abaqus/Explicit in which element numbering is not
c				passed into VUMAT. It is generated here and passed 
c 				into VUMAT as a state variable.
c	  
	  subroutine vusdfld(
     *   nblock,nstatev,nfieldv,nprops,ndir,nshr,jElem,kIntPt, 
     *   kLayer,kSecPt,stepTime,totalTime,dt,cmname,coordMp,  
     *   direct,T,charLength,props,stateOld,stateNew,field)  
c
		include 'vaba_param.inc'
c
		dimension props(nprops),jElem(nblock),coordMp(nblock,*),
     *  	direct(nblock,3,3),T(nblock,3,3),charLength(nblock),          
     *		stateOld(nblock,nstatev),stateNew(nblock,nstatev),          
     *		field(nblock,nfieldv)          
c         
		character*80 cmname
c
		do k = 1, nblock
			statenew(k,17)=jElem(k)
			field(k,1)=0.0
		end do
c
		return
      end subroutine vusdfld
c
c -------------------------------------------------------------------	  
	  
		
	 
	 
	 
	 
	 
