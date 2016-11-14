# Import Abaqus and External Modules
from abaqusConstants import *
from abaqus import *
import random
import regionToolset
import mesh
import step
import part
randomSeed=[41557]
for eachModel in range(0,1):
	#
	# Create Model Database 
	VerFile=Mdb(pathName="MStructure")
	VerModel=VerFile.models['Model-1']
	VerAssembly=VerModel.rootAssembly
	#
	# Underlying Geometry
	xSize=0.1
	ySize=0.05
	#
	# Microstructure Geometry
	charLength=0.00595 #Grain Side Length
	numX=15
	numY=5
	#
	# Other Parametersvgrain vumat
	meshSize=0.001
	analysis='Tension' # Options: Tension, Bending
	#
	# Draw Base Part	
	BasePart=VerModel.Part(name='Base', dimensionality=THREE_D,type=DEFORMABLE_BODY)
	BaseSketch = VerModel.ConstrainedSketch(name='Base',sheetSize=200.0)
#
	BaseSketch.Line(point1=(0.,0.),point2=(xSize,0.))
	BaseSketch.Line(point1=(xSize,0.),point2=(xSize,ySize))
	BaseSketch.Line(point1=(xSize,ySize),point2=(0.,ySize))
	BaseSketch.Line(point1=(0.,ySize),point2=(0.,0.))
	BasePart.BaseSolidExtrude(sketch=BaseSketch, depth=0.006)
	BasePart=VerModel.parts['Base']
#
# Draw Microstructure and Partition Base Part
	ParSketch=VerModel.ConstrainedSketch(name='Par',sheetSize=200)
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
	for eachFace in BasePart.faces:
		if eachFace.getNormal()==(0.0,0.0,1.0):
			targetFace=eachFace
	print targetFace
	BasePart.PartitionFaceBySketch(faces=targetFace, sketch=ParSketch)		
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
	BasePart.seedPart(size=meshSize)
	pickedRegions =(BasePart.faces, )
	elemType1 = mesh.ElemType(elemCode=CPEG8R, elemLibrary=STANDARD)
	BasePart.setElementType(regions=pickedRegions, elemTypes=(elemType1,))
	BasePart.generateMesh()
	#	
	#Steps
	VerModel.StaticStep(name='Step-1', previous='Initial', 
		maxNumInc=100000, initialInc=0.03, minInc=1e-07, maxInc=0.15, nlgeom=ON, timePeriod=20.)
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
	VerModel.SmoothStepAmplitude(name='Amp-1', timeSpan=TOTAL, data=(( 0.0, 0.0), (24.00, 1.0)))     
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