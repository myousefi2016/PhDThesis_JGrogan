from abaqusConstants import *
from abaqus import *
import random
outFile = open('ori.dat',"w")
random.seed(658468764)	
# Generate 'c' direction
for i in range(0,500):
	angle1=random.random()*2.*pi
	sigma=0.02 # extruded rod
	a2=random.normalvariate(1., sigma) 
	if a2>1.:
		a2=1.-(a2-1.)
#	a2=acos(random.random())	# homogeneous	
	angle2=acos(a2)
	cx=cos(angle1)*cos(angle2)
	cy=sin(angle1)*cos(angle2)
	cz=sin(angle2)
	# Get Stereo Projection
#	sx=cx*(1.-(cz/(1.+cz)))
#	sy=cy*(1.-(cz/(1.+cz)))
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
	#Tests
outFile.close()
