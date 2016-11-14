! This program takes output from the QHULL package and converts it into
! a format suitable for use with the GeomGen script
! J.Grogan 05/08/11
program Voronoi2DPost
!
!	Parameters
	parameter(max_verts=1000000,max_cells=100000,max_verts_in_cell=100)
!
!	Variables	
	character(len=256)full_line,test_string
    integer vnum(max_cells,max_verts_in_cell),num_verts(max_cells)
	integer in_tol(max_cells)
    real xv_cor(max_verts)
    real yv_cor(max_verts)
	logical xtrue
	logical ytrue
!	
!	Read Scales	
    open(unit=15,file='scales.dat',status='unknown')
    read(15,*)xscale,yscale
!
!	Read in vertex co-ordinates
	open(unit=11,file='qhullout.dat',status='unknown')
	read(11,*)
    read(11,*)num_verts_tot,num_cells,dummy
    do i=1,num_verts_tot
      read(11,*)xv_cor(i),yv_cor(i)
    enddo
!
!	Read in vertices on each cell
    do i=1,num_cells
         read(11,*)num_verts(i)
		 backspace(11)
		 read(11,'(i2,a256)')idummy,full_line
         ileft=1
         num_points=1
         do iright=1,256
             test_string=full_line(iright:iright)
             if((test_string==' ').or.(iright==256))then       
                 read(full_line(ileft:iright-1),'(i6)')vnum(i,num_points)
                 if(num_points==num_verts(i))exit
                 ileft=iright+1 
                 num_points=num_points+1                             
             endif
         enddo
    enddo 
!
!	Check if cells are within specified region		
    open(unit=12,file='fortranout.dat',status='unknown')
    num_inside_cells=num_cells
    do i=1,num_cells
		icheck=0
		do j=1,num_verts(i)
			xcor=xv_cor(vnum(i,j)+1)
			ycor=yv_cor(vnum(i,j)+1)
			if(abs(xcor)==10.101)then
				icheck=0
				exit
			endif
			rmax_x=1.1*xscale
			rmax_y=1.1*yscale
			rmin=-0.1
			xtrue=(xcor<rmax_x).and.(xcor>rmin)
			ytrue=(ycor<rmax_y).and.(ycor>rmin)
			if(xtrue.and.ytrue)icheck=icheck+1
		enddo
		if(icheck<1)then
			in_tol(i)=2
			num_inside_cells=num_inside_cells-1
		else
			in_tol(i)=1
		endif
	enddo
!
!	Write vertex coordinates for each cell	
    write(12,*)num_inside_cells
    do i=1,num_cells
		if(in_tol(i)==1)then
			write(12,*)num_verts(i)
			do j=1,num_verts(i)
				write(12,*)xv_cor(vnum(i,j)+1),',',yv_cor(vnum(i,j)+1)
			enddo
		else
			cycle
		endif
    enddo
    close(unit=11)    
    close(unit=12)
end program