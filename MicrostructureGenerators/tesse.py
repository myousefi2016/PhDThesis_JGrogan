#	Copyright (c) 2015 James A. Grogan
#
#       Permission is hereby granted, free of charge, to any person obtaining a copy
#       of this software and associated documentation files (the "Software"), to deal
#       in the Software without restriction, including without limitation the rights
#       to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#       copies of the Software, and to permit persons to whom the Software is
#       furnished to do so, subject to the following conditions:
#
#       The above copyright notice and this permission notice shall be included in
#       call copies or substantial portions of the Software.
#
#       THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#       IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#       FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#       AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#       LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#       OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#       THE SOFTWARE.
#
#       Author: J. Grogan
#       Initial Version: 2011

from abaqusConstants import *
from abaqus import *
import regionToolset
import sys
import random
import os
import subprocess
aModel=mdb.models['Model-1']
aPart=aModel.parts['Part-1']
num_grains=5
sizeX=1.
sizeY=1.
sizeZ=1.	
random.seed(1111)
qhullin=open('qhullin.dat','w')		
qhullin.write("%i \n"%(3))
qhullin.write("%i \n"%(num_grains*27))
for i in range(0,num_grains):
	xcor=random.random()*sizeX
	ycor=random.random()*sizeY
	zcor=random.random()*sizeZ	
	maxX=-sizeX
	maxY=-sizeY
	maxZ=-sizeZ
	for j in range(0,3):
		for k in range(0,3):
			for m in range(0,3):
				qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxX,ycor+maxY,zcor+maxZ))
				maxZ=maxZ+sizeZ
			maxY=maxY+sizeY
			maxZ=-sizeZ
		maxX=maxX+sizeX
		maxY=-sizeY
qhullin.close()
retcode=subprocess.call("qvoronoi.exe TI qhullin.dat Fi Fn o TO qhullout.dat")	
HullFile=open('qhullout.dat')
# Read Hyperplane Data
numPlanes=int(HullFile.readline())
hyps=[]
vhyp=[]
for i in range(0,numPlanes):
	hyps.append([])
	vhyp.append([])
for i in range(0,numPlanes):
	coords=HullFile.readline().split(' ')
	cell1=int(coords[0])
	cell2=int(coords[1])
	crd=[]
	for j in range(3,len(coords)-1):
		if coords[j]!='':
			crd.append(float(coords[j]))
	hyps[cell1].append([crd[0],crd[1],crd[2],crd[3]])
	hyps[cell2].append([crd[0],crd[1],crd[2],crd[3]])
# Read Vertex Neighbour Data
numVerts=int(HullFile.readline())
vNbr=[]
vCrd=[]
for i in range(0,numVerts+1):
	vNbr.append([])
	vCrd.append([])
for i in range(0,numVerts):
	vNbr[i].append(HullFile.readline().split(' '))
numVerts=int(HullFile.readline())
dat1=HullFile.readline().split(' ')
numVerts=int(dat1[0])
numCells=int(dat1[1])
# Read Vertex Coord Data
for i in range(0,numVerts):
	vCrd[i].append(HullFile.readline().split(' '))
# Read Cell Vertex Data
vCell=[]
for i in range(0,numCells):
	vCell.append([])
for i in range(0,numCells):
	vCell[i].append(HullFile.readline().split(' '))
# Find Vertices on Each Hyperplane on Each Cell
for i in range(0,numCells):
	for j in range(0,len(hyps[i])):		
		nx=hyps[i][j][0]
		ny=hyps[i][j][1]
		nz=hyps[i][j][2]
		off=hyps[i][j][3]
		vhyp=[]
		for k in range(0,int(vCell[i][0][0])):
			index=int(vCell[i][0][k])
			vx=float(vCrd[index][0][0])
			vy=float(vCrd[index][0][1])
			vz=float(vCrd[index][0][2])
			distance=nx*vx+ny*vy+nz*vz+off
			if abs(distance)<1.e-4: 
				vhyp.append(index)
		for k in range(0,len(vhyp)):
			for m in range(0,len(vhyp)):
				if k!=m:
					ax=float(vCrd[vhyp[k]][0][0])
					ay=float(vCrd[vhyp[k]][0][1])
					az=float(vCrd[vhyp[k]][0][2])
					bx=float(vCrd[vhyp[m]][0][0])
					by=float(vCrd[vhyp[m]][0][1])
					bz=float(vCrd[vhyp[m]][0][2])
					aPart.WirePolyLine(points=((ax,ay,az),(bx,by,bz)),mergeWire=OFF)
					
HullFile.close()							
