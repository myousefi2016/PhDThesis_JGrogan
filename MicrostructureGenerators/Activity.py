# Import Neccesary Abaqus Modules
from abaqusConstants import *
from odbAccess import *
import sys
import os
odbfilename='CDIE-1.odb'
odb=openOdb(path=odbfilename)
aInst=odb.rootAssembly.instances['PART-1-1']
bInst=odb.rootAssembly.instances['PART-3-1']
yold=[]
ynew=[]
outFile = open('out.dat',"w")
for i in range(0,18):
	yold.append(0.)
	ynew.append(0.)
for eachFrame in odb.steps["Step-1"].frames:
	strain=abs(eachFrame.fieldOutputs["U"].getSubset(region=bInst).values[0].data[0])/6.
	for i in range(0,18):
		yold[i]=ynew[i]
	for i in range(0,18):
		label='SDV'+str(19+i)
		ynew[i]=abs(eachFrame.fieldOutputs[label].getSubset(region=aInst).values[0].data)
	sum=0.	
	for i in range(0,18):
		sum=sum+ynew[i]-yold[i]
	basalsum=0.
	for i in range(0,3):
		basalsum=basalsum+ynew[i]-yold[i]
	prismsum=0.
	for i in range(3,6):
		prismsum=prismsum+ynew[i]-yold[i]	
	pyrsum=0.
	for i in range(6,12):
		pyrsum=pyrsum+ynew[i]-yold[i]
	twinsum=0.
	for i in range(12,18):
		twinsum=twinsum+ynew[i]-yold[i]
	if sum!=0.:
		prismsum=prismsum/sum
		basalsum=basalsum/sum
		pyrsum=pyrsum/sum
		twinsum=twinsum/sum
	else:
		twinsum=0.	
		pyrsum=0.
		prismsum=0.
		basalsum=0.	
	outFile.write("%12.6f %12.6f %12.6f %12.6f %12.6f\n " % (basalsum,prismsum,pyrsum,twinsum,strain))
outFile.close()	