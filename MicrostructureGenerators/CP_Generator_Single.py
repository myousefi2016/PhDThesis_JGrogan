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

# GrainGen V3.0
# This script generates idealised and representative meshed micro-structure geometries 
# in 2-D through the Abaqus geometry kernel. - J. Grogan, 25/09/2011 
#
# Import Abaqus and External Modules
from abaqusConstants import *
from abaqus import *
import random
import regionToolset
import mesh
import step
import part
import interaction
import subprocess
randomSeed=[39928822]
randomSeed.append(39764)
randomSeed.append(19230045)
randomSeed.append(452398)
randomSeed.append(872315)
randomSeed.append(794738)
randomSeed.append(224492579)
randomSeed.append(96502382)
randomSeed.append(4921299)
randomSeed.append(3113145)
randomSeed.append(36677835)
for eachModel in range(0,1):
	#
	# Create Model Database 
	VerFile=Mdb(pathName="MStructure")
	VerModel=VerFile.models['Model-1']
	VerAssembly=VerModel.rootAssembly
	#
	# Assign Model Parameters
	#
	# Underlying Geometry
	xSize=0.01
	ySize=0.01
	#
	# Microstructure Geometry
	charLength=0.01# Grain Side Length
	numX=1
	numY=1
	numGrains=82 # Voronoi Only
	hardRad=0.00 # Voronoi Only
	#
	# Other Parametersvgrain vumat
	grainType='Square' # Options: Square, Hexagon, Voronoi
	meshSize=0.001
	analysis='Tension' # Options: Tension, Bending
	#
	# Draw Base Part	
	BasePart=VerModel.Part(name='Base', dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
	BasePart.DatumPointByCoordinate((0,0,0))
	BasePart.DatumPointByCoordinate((xSize,0,0))
	BasePart.DatumPointByCoordinate((0,ySize,0))	
	pdatums=BasePart.datums
	BasePart.DatumPlaneByThreePoints(point1=pdatums[1], point2=pdatums[2], point3=pdatums[3])
	BasePart.DatumAxisByTwoPoint(point1=pdatums[1],point2=pdatums[2])
	partTransform = BasePart.MakeSketchTransform(sketchPlane=pdatums[4], sketchUpEdge=pdatums[5], 
		sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0,0,0))
	BaseSketch = VerModel.ConstrainedSketch(name='Base',sheetSize=200, transform=partTransform)
#
	BaseSketch.Line(point1=(0.,0.),point2=(xSize,0.))
	BaseSketch.Line(point1=(xSize,0.),point2=(xSize,ySize))
	BaseSketch.Line(point1=(xSize,ySize),point2=(0.,ySize))
	BaseSketch.Line(point1=(0.,ySize),point2=(0.,0.))
	BasePart.BaseShell(sketch=BaseSketch)
	BasePart=VerModel.parts['Base']
#
# Draw Microstructure and Partition Base Part
	ParSketch=VerModel.ConstrainedSketch(name='Base',sheetSize=200, transform=partTransform)
	if grainType=='Square':
		offset=0.
		for i in range(0,numX):
			ParSketch.Line(point1=(offset,0.),point2=(offset,numY*charLength))
			offset=offset+charLength
		offset=0.
		for i in range(0,numY):
			ParSketch.Line(point1=(0.,offset),point2=(numX*charLength,offset))
			offset=offset+charLength
	elif grainType=='Hexagon':	
		yLength=sin(radians(30.))*charLength
		xLength=cos(radians(30.))*charLength
		offsetX=0.
		for i in range(0,numX):
			offsetY=0.
			for j in range(0,numY):
				if j%2==0:
					xPos=offsetX
				else:
					xPos=offsetX+xLength
				ParSketch.Line(point1=(xLength+xPos,-yLength+offsetY),point2=(xLength+xPos,yLength+offsetY))
				ParSketch.Line(point1=(xLength+xPos,+yLength+offsetY),point2=(xPos,2.*yLength+offsetY))
				ParSketch.Line(point1=(xLength+xPos,-yLength+offsetY),point2=(xPos,-2.*yLength+offsetY))
				offsetY=offsetY+3.*yLength
			offsetX=offsetX+2.*xLength
	elif grainType=='Voronoi':
		random.seed(randomSeed[eachModel])
		qhullin=open('qhullin.dat','w')
		qhullin.write("%i \n"%(2))
		qhullin.write("%i \n"%(numGrains*9))
		xlist=[0.]
		ylist=[0.]
	#
	#Generate Point Seeds - Hardcore Voronoi Method Optional
		for i in range(0,numGrains):
			outside=False
			while outside==False:
				xcor=random.random()*xSize
				ycor=random.random()*ySize
				if hardRad==0.:
					outside=True
					break
				if len(xlist)>1:
					distold=1000.
					for i in range(1,len(xlist)):
						distnew=(xcor-xlist[i])*(xcor-xlist[i])+(ycor-ylist[i])*(ycor-ylist[i])
						distnew=sqrt(distnew)
						if distnew<distold:
							distold=distnew
					if distold>=hardRad:
						outside=True
				else:
					outside=True
			xlist.append(xcor)
			ylist.append(ycor)
			qhullin.write("%18.6f %18.6f \n"%(xcor,ycor))
			qhullin.write("%18.6f %18.6f \n"%(xcor+xSize,ycor))
			qhullin.write("%18.6f %18.6f \n"%(xcor-xSize,ycor))
			qhullin.write("%18.6f %18.6f \n"%(xcor,ycor+ySize))
			qhullin.write("%18.6f %18.6f \n"%(xcor,ycor-ySize))
			qhullin.write("%18.6f %18.6f \n"%(xcor+xSize,ycor+ySize))
			qhullin.write("%18.6f %18.6f \n"%(xcor-xSize,ycor-ySize))
			qhullin.write("%18.6f %18.6f \n"%(xcor+xSize,ycor-ySize))
			qhullin.write("%18.6f %18.6f \n"%(xcor-xSize,ycor+ySize))
		qhullin.close()
			#
			# Generate tesselation externally and post-process results
		scales=open('scales.dat','w')
		scales.write("%18.6f %18.6f \n"%(xSize,ySize))
		scales.close()
		retcode=subprocess.call("qhull.exe v Qbb TI qhullin.dat o TO qhullout.dat")	
		retcode=subprocess.call("Voronoi2DPost.exe")
		FortranFile=open('fortranout.dat')	
		num_cells=int(FortranFile.readline())
		cordx=[]
		cordy=[]
		x1=[]
		y1=[]
		x2=[]
		y2=[]
		k=0
		#
		# Generate Partition Sketch
		for i in range(0,num_cells):
			num_verts=int(FortranFile.readline())
			for j in range(0,num_verts):
				coords=FortranFile.readline().split(',')
				cordx.append([])
				cordy.append([])
				cordx[j]=float(coords[0])
				cordy[j]=float(coords[1])
			for j in range(0,num_verts-1):				
				ParSketch.Line(point1=(cordx[j],cordy[j]),point2=(cordx[j+1],cordy[j+1]))
				x1.append([])
				y1.append([])
				x1[k]=cordx[j]
				y1[k]=cordy[j]
				x2.append([])
				y2.append([])
				x2[k]=cordx[j+1]
				y2[k]=cordy[j+1]
				k=k+1
			ParSketch.Line(point1=(cordx[num_verts-1],cordy[num_verts-1]),
				point2=(cordx[0],cordy[0]))
			x1.append([])
			y1.append([])
			x1[k]=cordx[num_verts-1]
			y1[k]=cordy[num_verts-1]
			x2.append([])
			y2.append([])
			x2[k]=cordx[0]
			y2[k]=cordy[0]
			k=k+1
			print i
#	BasePart.PartitionFaceBySketch(faces=BasePart.faces, sketch=ParSketch)		
	#	
	# Generate Sections and Section Assignments
	labelcount=1
	regions=BasePart.faces
	for eachregion in regions:
		mlabel='Mat'+str(labelcount)
		VerModel.PEGSection(name=mlabel, material=mlabel, thickness=0.01, 
			wedgeAngle1=0.0, wedgeAngle2=0.0)
		BasePart.SectionAssignment(region=(eachregion,), 
			sectionName=mlabel, offset=0.0, offsetField='')
		labelcount=labelcount+1
	#
	# Mesh Part
	BasePart.ReferencePoint(point=(0.0, 0.0, 0.0))
	if grainType=='Square':
		BasePart.setMeshControls(regions=BasePart.faces, elemShape=QUAD, technique=STRUCTURED)
	elif grainType=='Hexagon':
		offsetX=0.
		offsetY=0.
		ParSketch2=VerModel.ConstrainedSketch(name='Hex',sheetSize=200, transform=partTransform)
		for i in range(0,2*numX):
			ParSketch2.Line(point1=(offsetX,0.),point2=(offsetX,2.*charLength*numY))	
			offsetX=offsetX+xLength
		for i in range(0,numY):
			ParSketch2.Line(point1=(0.,offsetY),point2=(2.*charLength*numX,offsetY))	
			offsetY=offsetY+3.*yLength
		BasePart.PartitionFaceBySketch(faces=BasePart.faces, sketch=ParSketch2)	
		BasePart.setMeshControls(regions=BasePart.faces, elemShape=QUAD, technique=SWEEP)
	elif grainType=='Voronoi':
		BasePart.setMeshControls(regions=BasePart.faces, elemShape=QUAD_DOMINATED, technique=FREE)
	BasePart.seedPart(size=meshSize)
	pickedRegions =(BasePart.faces, )
	elemType1 = mesh.ElemType(elemCode=CPEG8R, elemLibrary=STANDARD)
	#elemType1 = mesh.ElemType(elemCode=CPEG4R, elemLibrary=STANDARD,hourglassControl=ENHANCED)
	BasePart.setElementType(regions=pickedRegions, elemTypes=(elemType1,))
	BasePart.generateMesh()
	#	
	#Steps
	VerModel.StaticStep(name='Step-1', previous='Initial', 
		maxNumInc=100000, initialInc=0.03, minInc=1e-07, maxInc=0.15, nlgeom=ON, timePeriod=35.)
	VerModel.fieldOutputRequests['F-Output-1'].setValues(variables=(
		'LE', 'RF', 'S', 'U'), timeInterval=0.2, timeMarks=OFF)
	#	
	#Boundary Conditions	
	VerAssembly.Instance(name='Strut',part=BasePart, dependent=ON)
	iNodes=VerAssembly.instances['Strut'].nodes
	toler=0.01*meshSize
	Left=iNodes.getByBoundingBox(xMin=-toler,xMax=toler,yMin=-toler,yMax=ySize+toler)	
	BLeft=iNodes.getByBoundingBox(xMin=-toler,xMax=toler,yMin=-toler,yMax=toler)	
	Right=iNodes.getByBoundingBox(xMin=xSize-toler,xMax=xSize+toler,yMin=toler,yMax=ySize+toler)
	BRight=iNodes.getByBoundingBox(xMin=xSize-toler,xMax=xSize+toler,yMin=-toler,yMax=toler)		
	#	
	Lregion=regionToolset.Region(nodes=Left)
	BLregion=regionToolset.Region(nodes=BLeft)
	Rregion=regionToolset.Region(nodes=Right)	
	BRregion=regionToolset.Region(nodes=BRight)	
	#
	VerModel.SmoothStepAmplitude(name='Amp-1', timeSpan=TOTAL, data=(( 0.0, 0.0), (48.00, 2.0)))     
	VerModel.DisplacementBC(name='LeftX', createStepName='Initial', 
		region=Lregion, u1=0.0, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, 
		ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM) 
	VerModel.DisplacementBC(name='BottomY1', createStepName='Initial', 
		region=BLregion, u1=UNSET, u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, 
		ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM)
	if analysis=='Tension':
		VerModel.DisplacementBC(name='Tension', createStepName='Step-1', 
			region=BRregion, u1=0.5*xSize, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, 
			ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM) 
		VerModel.DisplacementBC(name='BottomY2', createStepName='Initial', 
			region=BRregion, u1=UNSET, u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, 
			ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM) 
		VerModel.boundaryConditions['Tension'].setValues(amplitude='Amp-1') 
	else:
		VerModel.DisplacementBC(name='Bending', createStepName='Step-1', 
			region=BRregion, u1=UNSET, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, 
			ur3=-6., amplitude=UNSET, fixed=OFF, distributionType=UNIFORM)
		VerModel.boundaryConditions['Bending'].setValues(amplitude='Amp-1') 		
	#
	VerAssembly.Set(nodes=Right, name='Right')
	VerAssembly.Set(nodes=BRight, name='BRight')
	if analysis=='Tension':
		VerModel.Equation(name='Constraint-1', terms=((1.0, 'Right', 1), ( -1.0, 'BRight', 1))) 
	else:
		region1=VerAssembly.sets['BRight']
		region2=VerAssembly.sets['Right']
		VerModel.MultipointConstraint(name='Constraint-2', 
			controlPoint=region1, surface=region2, mpcType=BEAM_MPC, 
			userMode=DOF_MODE_MPC, userType=0, csys=None)	
	#
	#Create Job and write input file
	if grainType=='Square':
		letter1='S'
	elif grainType=='Hexagon':
		letter1='H'
	elif grainType=='Voronoi':
		letter1='V'
	if analysis=='Tension':
		letter2='T'
	else:
		letter2='B'
	label='W'+str(numY)+'L'+str(numX)+letter1+letter2+str(eachModel)
	VerFile.Job(name=label, model='Model-1', type=ANALYSIS,userSubroutine='ucrystal.for') 				
	VerFile.jobs[label].writeInput(consistencyChecking=OFF)
#	VerFile.close()
