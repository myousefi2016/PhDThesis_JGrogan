! This program takes output from the QHULL package and converts it into
! a format suitable for use with the GeomGen script
! J.Grogan 05/08/11
program Voronoi3DPost
!
!	Parameters
	parameter(max_verts=500000,max_cells=50000,max_verts_in_cell=100)
	parameter(max_hyps=500000,max_hyp_in_cell=100,max_verts_on_hyp=50)
!	
!	Variables 
    character(len=256)full_line,test_string
	integer	num_verts(max_cells)
    integer vert_list(max_cells,max_verts_in_cell)
	integer facet(2,max_hyps)
    integer hyp_list(max_cells,max_hyp_in_cell)
	integer num_cell_hyp(max_cells) 
	integer cell_status(max_cells)
	integer	num_hyp_verts(max_cells,max_hyp_in_cell)
    integer hyp_vert_list(max_cells,max_hyp_in_cell,max_verts_on_hyp)              
    double precision xv_cor(max_verts)
    double precision yv_cor(max_verts)
    double precision zv_cor(max_verts)
    double precision cor(3,max_hyps)
    double precision offset(max_hyps)
	double precision xcor,ycor,zcor
	double precision dotrprod,distance,tol
	logical xtrue,ytrue,ztrue
! 
!	Open output files  
    open(unit=12,file='fortranout.dat',status='unknown')
!	
!	Open scales file	
	open(unit=15,file='scales.dat',status='unknown')
    read(15,*)rmaxscale
!
!	Read tessellation results from QHULL
    open(unit=11,file='qhullout.dat',status='unknown')
	read(11,*)
	read(11,*)num_total_verts,num_cells
!
!	Read in all vertice co-ordinates   
    do i=1,num_total_verts
       read(11,*)xv_cor(i),yv_cor(i),zv_cor(i)
    enddo
! 
!	Read in vertice labels for each voronoi cell    
    do i=1,num_cells
         read(11,*)num_verts(i)
		 backspace(11)
		 if(num_verts(i)>9)then
			read(11,'(i3,a256)')idummy,full_line
		else
			read(11,'(i2,a256)')idummy,full_line
		endif
         ileft=1
         num_points=1
         do iright=1,256
             test_string=full_line(iright:iright)
             if((test_string==' ').or.(iright==256))then       
                 read(full_line(ileft:iright-1),'(i6)')vert_list(i,num_points)
                 if(num_points==num_verts(i))exit
                 ileft=iright+1 
                 num_points=num_points+1                             
             endif
         enddo
    enddo 
!  
!	Read in bounded hyperplane cell labels and co-ordinates 
     read(11,*)num_hyp
     do i=1,num_hyp
       read(11,*)dummy,facet(1,i),facet(2,i),cor(1,i),cor(2,i),cor(3,i),offset(i)
     enddo
!
!	Determine hyperplanes of each cell
	do i=1,num_cells
    	num_hy=1
    	do j=1,num_hyp
        	if((facet(1,j)==i-1).or.(facet(2,j)==i-1))then
            	hyp_list(i,num_hy)=j
                num_cell_hyp(i)=num_hy
                num_hy=num_hy+1
            endif
        enddo
    enddo
!
!	Check if any cell vertices are outside the chosen tolerance     
    do i=1,num_cells
        cell_status(i)=1
		if(num_verts(i)<3)cycle
		ibreak=0
		do j=1,num_verts(i)
			do k=1,num_verts(i)
				if(j==k)cycle
				x1=xv_cor(vert_list(i,j)+1)
				y1=yv_cor(vert_list(i,j)+1)
				z1=zv_cor(vert_list(i,j)+1)
				x2=xv_cor(vert_list(i,k)+1)
				y2=yv_cor(vert_list(i,k)+1)
				z2=zv_cor(vert_list(i,k)+1)
				dist=sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)+(z2-z1)*(z2-z1))
				if (dist<1.e-5)ibreak=1
			enddo
		enddo
		if(ibreak==1)cycle
        do j=1,num_verts(i)
			xcor=xv_cor(vert_list(i,j)+1)
			ycor=yv_cor(vert_list(i,j)+1)
			zcor=zv_cor(vert_list(i,j)+1)
			rmax=1.1*rmaxscale
			rmin=-0.1
			xtrue=(xcor<rmax).and.(xcor>rmin)
			ytrue=(ycor<rmax).and.(ycor>rmin)
			ztrue=(zcor<rmax).and.(zcor>rmin)
            if(xtrue.and.ytrue.and.ztrue)cell_status(i)=0
        enddo
    enddo
!
!	For all cells within tolerance determine vertices on each hyperplane
	num_skipped=0
	tol=1.e-5*rmaxscale
	do i=1,num_cells
    	if(cell_status(i)/=0)then
        	num_skipped=num_skipped+1
            cycle
        endif
        do j=1,num_cell_hyp(i)
          	nverts_on_hyp=1
            do k=1,num_verts(i)
              	dotprod1=cor(1,hyp_list(i,j))*xv_cor(vert_list(i,k)+1)
              	dotprod2=cor(2,hyp_list(i,j))*yv_cor(vert_list(i,k)+1)
              	dotprod3=cor(3,hyp_list(i,j))*zv_cor(vert_list(i,k)+1)
              	distance=dotprod1+dotprod2+dotprod3+offset(hyp_list(i,j))
              	if(abs(distance)<tol)then               
                	hyp_vert_list(i,j,nverts_on_hyp)=vert_list(i,k)
                    num_hyp_verts(i,j)=nverts_on_hyp
                    nverts_on_hyp=nverts_on_hyp+1                   
              	endif
            enddo
        enddo
    enddo		
!	Write output for the of co-orindates of vertices on each hyperplane
!	that make up a cell.	
    write(12,*)num_cells-num_skipped
	do i=1,num_cells
    	if(cell_status(i)/=0)cycle
        write(12,*)num_cell_hyp(i)
        do j=1,num_cell_hyp(i)
			write(12,*)num_hyp_verts(i,j)
			do k=1,num_hyp_verts(i,j)
				xcor=xv_cor(hyp_vert_list(i,j,k)+1)
				ycor=yv_cor(hyp_vert_list(i,j,k)+1)
				zcor=zv_cor(hyp_vert_list(i,j,k)+1)
				write(12,'(2(f20.15,a),f20.15)')xcor,',',ycor,',',zcor
			enddo
        enddo
    enddo
end program
