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
#       Initial Version: 2012

# Import Neccesary Abaqus Modules
from abaqusConstants import *
from abaqus import *
from odbAccess import *
import regionToolset
import sys
import os
import interaction
import random

mname='modelname' # Enter model name here
mtype=1
jobName=mname
aModel=mdb.models[mname]
aAss=aModel.rootAssembly

bPart=aModel.parts['partname'] # Enter part name here
random.seed(2344564)

incFile=open('NBR.inc','w')
onSurf=[]
for i in range(0,300000):
	onSurf.append(0)
incFile.write("*INITIAL CONDITIONS,TYPE=SOLUTION \n")
if mtype==1:
	for eachSN in bPart.sets['CSURF'].elements:
		onSurf[eachSN.label]=1
	for eachElement in bPart.elements:
		label=eachElement.label
		nbrs=[]
		for eachNbr in eachElement.getAdjacentElements():
			nbrs.append(eachNbr.label)
		for i in range(0,6-len(eachElement.getAdjacentElements())):
			nbrs.append(0)
		if onSurf[label]==1:
			rnum=random.weibullvariate(1.,0.2)
		else:
			rnum=0.		
		# enter instance name
		incFile.write("Assembly.instancename.%i, %i, %i, %i, %i, %i, %i, %i, \n"%(label,label,
				nbrs[0],nbrs[1],nbrs[2],nbrs[3],nbrs[4],nbrs[5]))								
		incFile.write("%i, %f, %i, %i, \n"%(0,rnum,onSurf[label],0))								
incFile.close()	
	
