from abaqusConstants import *
from abaqus import *
import random	
incFile=open('Ori29.dat','w')
# seeds 1-10	
#random.seed(79789)	
#random.seed(673673)
#random.seed(868256)
#random.seed(15675676)
#random.seed(8836572)
# seeds 20-29
random.seed(6753679)	
random.seed(88822657)
random.seed(267567)
random.seed(833683655)
random.seed(566445)
for i in range(1,1000):
	# Generate 'c' direction
	angle1=random.random()*2.*pi
	sigma=0.02 # extruded rod
	a2=random.normalvariate(1., sigma) 
	if a2>1.:
		a2=1.-(a2-1.)
	angle2=acos(a2)
#	angle2=acos(random.random())	# homogeneous	
	cx=cos(angle1)*cos(angle2)
	cy=sin(angle1)*cos(angle2)
	cz=sin(angle2)
	# Get arbitary normal to C
	nx=cos(angle1)*cos(angle2+pi/2.)
	ny=sin(angle1)*cos(angle2+pi/2.)
	nz=sin(angle2+pi/2.)
	# Rotate about random angle 
	a3=random.random()*2.*pi
	xx=nx*(cos(a3)+cx*cx*(1.-cos(a3)))+ny*(cx*cy*(1.-cos(a3))-cz*sin(a3))+nz*(cx*cz*(1.-cos(a3))+cy*sin(a3))
	xy=nx*(cx*cy*(1.-cos(a3))+cz*sin(a3))+ny*(cos(a3)+cy*cy*(1.-cos(a3)))+nz*(cy*cz*(1.-cos(a3))-cx*sin(a3))
	xz=nx*(cz*cx*(1.-cos(a3))-cy*sin(a3))+ny*(cz*cy*(1.-cos(a3))+cx*sin(a3))+nz*(cos(a3)+cz*cz*(1.-cos(a3)))
	# Y-Axis is normal to C and X
	yx=xy*cz-xz*cy
	yy=xz*cx-xx*cz
	yz=xx*cy-xy*cx
	incFile.write('*MATERIAL, NAME=Mat '+str(i)+ '\n')
	incFile.write('*USER MATERIAL, CONSTANTS=22, UNSYMM \n')
	incFile.write('45000.,0.3,'+str(xx)+','+str(xy)+','+str(xz)+','+str(yx)+','+str(yy)+','+str(yz)+' \n')
	incFile.write('4.,1.,0.,10.,20.,150.,7500.,40., \n')
	incFile.write('260.,7500.,5.,200.,0.11,10. \n')	
	incFile.write('*Depvar \n')
	incFile.write(str(163)+' \n')	
incFile.close()	