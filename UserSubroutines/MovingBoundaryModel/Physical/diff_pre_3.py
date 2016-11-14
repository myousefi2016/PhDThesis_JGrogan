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
# enter model name
aModel=mdb.models['modelname']	
# enter part name				
aPart=aModel.parts['partname']
incFile=open('NodeData.inc','w')						
#	Cycle through all interface nodes
interfaceNodes=aPart.sets['InterfaceN'].nodes
interfaceElements=aPart.sets['InterfaceE'].elements
pstring=str(len(interfaceNodes))+' \n'
ic=0
for eachNode in interfaceNodes:
	nodeLabel=eachNode.label
	nodeFaces=eachNode.getElemFaces()
	nodeEdges=eachNode.getElemEdges()
	numFacets=len(nodeFaces)
	nstring=' '
	numFaces=0
	for eachFace in nodeFaces:
		# Check if face is on outer boundary
		faceElems=eachFace.getElements()
		bound=0
		if len(faceElems)==1:
			if faceElems[0] in interfaceElements:
				bound=1
		# Check if face is on interface
		interface=0
		faceNodes=eachFace.getNodes()
		for eachFNode in faceNodes:
			if eachFNode in interfaceNodes:
				interface=interface+1
		if interface==4 or bound==1:
			facetNodes=[]
			numFaces=numFaces+1
			for eachFNode in eachFace.getNodes():		
				if eachFNode.label!=nodeLabel:
					for eachEdge in eachFNode.getElemEdges():
						if eachEdge in nodeEdges:
							facetNodes.append(eachFNode)	
			nstring=nstring+str(facetNodes[0].label)+' '+str(facetNodes[1].label)+' \n'			
			faceElems=eachFace.getElements()
			if bound==0:
				if faceElems[0] in interfaceElements:
					intNodes=faceElems[0].getNodes()
					nbrElem=faceElems[1]
				else:
					nbrElem=faceElems[0]
					intNodes=faceElems[1].getNodes()
				nbrNodes=nbrElem.getNodes()
				n1=eachNode
				n2=facetNodes[0]
				n3=facetNodes[1]
				for eachFNode in faceNodes:
					if eachFNode!=n1 and eachFNode!=n2 and eachFNode!=n3:
						n4=eachFNode
						break
				for eachEEdge in n1.getElemEdges():
					for eachENode in eachEEdge.getNodes():
						if eachENode in nbrNodes and eachENode!=n1 and eachENode!=n2 and eachENode!=n3:
							n5=eachENode
							break
				for eachEEdge in n2.getElemEdges():
					for eachENode in eachEEdge.getNodes():
						if eachENode in nbrNodes and eachENode!=n1 and eachENode!=n2 and eachENode!=n4:
							n6=eachENode
							break
				for eachEEdge in n3.getElemEdges():
					for eachENode in eachEEdge.getNodes():
						if eachENode in nbrNodes and eachENode!=n1 and eachENode!=n4 and eachENode!=n3:
							n7=eachENode
							break
				for eachEEdge in n4.getElemEdges():
					for eachENode in eachEEdge.getNodes():
						if eachENode in nbrNodes and eachENode!=n4 and eachENode!=n2 and eachENode!=n3:
							n8=eachENode
							break																		
				nstring=nstring+str(n1.label)+' '+str(n2.label)+' '+str(n3.label)+' '+str(n4.label)+' '
				nstring=nstring+str(n5.label)+' '+str(n6.label)+' '+str(n7.label)+' '+str(n8.label)+' '
				nstring=nstring+'\n'
				for eachNNode in intNodes:
					nstring=nstring+str(eachNNode.label)+' '			
			else:
				nstring=nstring+'0 0 0 0 0 0 0 0 \n'
				for eachNNode in faceElems[0].getNodes():
					nstring=nstring+str(eachNNode.label)+' '			
			nstring=nstring+'\n'	
	pstring=pstring+str(nodeLabel)+' '+str(numFaces)+' \n'+nstring
	ic=ic+1
	print ic,len(interfaceNodes)
incFile.write(pstring)			
incFile.close()			
