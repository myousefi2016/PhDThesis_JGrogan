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

# This is a pre-processor script for 3D ALE corrosion analysis.
# Author: J. Grogan - BMEC, NUI Galway. Created: 19/09/2012
from abaqusConstants import *
from abaqus import *
#
# Model Name
aModel=mdb.models['modelname']
# Part Name
aPart=aModel.parts['partname']
incFile=open('NodeData.inc','w')
#
numFaces=0
pstring=''
# Cycle through all element faces
for eachFace in aPart.elementFaces:
	# Check if Face is on external Surface
	if len(eachFace.getElements())==1:	
		numFaces=numFaces+1
		faceNodes=eachFace.getNodes()
		# Identify 'Fixed' Faces
		fixed=1
		try: 
			fSet=aPart.sets['Fixed']
			for eachNode in faceNodes:
				if eachNode not in fSet.nodes:
					fixed=0
					break
		except:
			fixed=0
		pstring=pstring+str(fixed)+' '				
		# Write Element Nodes		
		eNodes=[]
		for eachNode in eachFace.getElements()[0].getNodes():
			pstring=pstring+str(eachNode.label)+' '
		pstring=pstring+'\n'
		# Write Each Face Nodes and Corresponding Connected Nodes
		for eachNode in faceNodes:
			pstring=pstring+str(eachNode.label)+' '
			for eachEdge in eachNode.getElemEdges():
				for eachENode in eachEdge.getNodes():
					if eachENode.label != eachNode.label and eachENode in faceNodes:
						pstring=pstring+str(eachENode.label)+' '
			pstring=pstring+'\n'
#		
incFile.write(str(numFaces)+'\n')	
incFile.write(pstring)			
incFile.close()
