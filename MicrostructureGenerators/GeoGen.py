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

# GrainGen V2.0
# This script generates idealised and representative meshed micro-structure geometries 
# in 2-D and 3-D through the Abaqus geometry kernel. - J. Grogan, 09/06/2011 
#
# Import Abaqus and External Modules
from abaqusConstants import *
from abaqus import *
import random
import subprocess
import regionToolset
import mesh
import step
import part
import interaction
import GeomModules
#
# Create Model Database 
VerFile=Mdb(pathName="MStructure")
VerModel=VerFile.models['Model-1']
VerAssembly=VerModel.rootAssembly
#
# Assign Model Parameters
shape=1 # 1 - Square, 2- Hex, 3 -Dodec, 4- Voronoi
part_type=3 # 2 - Shell, 3 - Solid
dimension=3 # 2 - 2D, 3 - 3D
rad=0.00595	# Characteristic Dimension (except Voronoi)
meshsize=0.001 # Global Mesh Seed Size
num_high=20 # Number of Grains in X-Dir
num_wide=3 # Number of Grains in Y-Dir
num_thick=3 # Number of Grains in Z-Dir
num_grains=210# Target Number of Grains (Voronoi Only)
scalex=3.4 # Voronoi Part Scale X-Dir (Voronoi Only)
scaley=1. # Voronoi Part Scale Y-Dir (Voronoi Only)
scalez=1. # Voronoi Part Scale Z-Dir (Voronoi Only)
ana_type=1 # 1 - Crystal Plasticity, 2 - Corrosion
hard_rad=0.0 # Hardcore voronoi min. radius (Voronoi Only)
random_seed=2244763 # Random seed for voronoi grain generation or random vector generation
#
# Choose Script Function - Set to 1 to activate
assemble_grains = 1 # Assemble Multiple Grains and Merge Them
boolean_cut = 1 # Perform Boolean Cut Operation
mesh_part = 0 # Mesh the Final Geometry
mat_props = 0 # Assign Material Properties
bound_conds = 0 # Generate steps and apply BCs
write_output =0 # Write Output File
post_proc = 0 # Postprocess INP file (Corrosion Only)
#
# For 2-D Solids thickness is set equal to one element
if dimension==3:
	extrude_depth=rad
else:
	extrude_depth=meshsize
	num_thick=1
#
# Draw a Square Grain
if shape==1:
	GeomModules.DrawSquare(VerModel,part_type,rad,extrude_depth)
#
# Draw a Hexagonal Grain
if shape==2:
	GeomModules.DrawHexagon(VerModel,part_type,rad,extrude_depth)
#
# Draw a Dodecahedral Grain
if shape==3:
	GeomModules.DrawDodec(VerModel,rad)	
#
# Draw a Voronoi Tessellation
if shape==4:
	if dimension==2:
		maxsize=max(scalex,scaley)
		GeomModules.Voronoi2D(VerModel,part_type,extrude_depth,num_grains,maxsize,hard_rad,random_seed)
	else:
		maxsize=max(scalex,scaley,scalez)
		GeomModules.Voronoi3D(VerModel,num_grains,maxsize,hard_rad,random_seed)
#		
# Assemble Base Parts
if assemble_grains==1:
	if shape<=3:
		VerPart=VerModel.parts['Base']
		GeomModules.PatternParts(num_high,num_wide,num_thick,VerPart,rad,shape,VerModel)
#
# Make a Boolean Template
if boolean_cut==1:
	if shape>1:
		GeomModules.BooleanPart(VerModel,part_type,rad,extrude_depth,num_high,
			num_wide,num_thick,shape,dimension,scalex,scaley,scalez)
		BoolPart=VerModel.parts['Template']
	#		
	#Perform Boolean Cut
	if shape==1:
		VerPart=VerModel.parts['Merged']
		del VerAssembly.instances['Merged-1']       
	else:
		VerAssembly.InstanceFromBooleanCut(name='FinalPart', 
			instanceToBeCut=VerAssembly.instances['Merged-1'], 
			cuttingInstances=(VerAssembly.instances['Template-1'], ), 
			originalInstances=DELETE)
		del VerAssembly.instances['FinalPart-1']
		VerPart=VerModel.parts['FinalPart']
#
# Mesh Part
if mesh_part==1:
	if shape<3:
		VerPart.setMeshControls(regions=VerPart.cells, elemShape=HEX, technique=STRUCTURED)
	if shape==3:
		VerPart.setMeshControls(regions=VerPart.cells, elemShape=TET, technique=FREE)
	if shape==4:
		if dimension==2:
		    VerPart.setMeshControls(regions=VerPart.cells, elemShape=HEX, technique=SWEEP, 
				algorithm=ADVANCING_FRONT)			
		else:
			VerPart.setMeshControls(regions=VerPart.cells, elemShape=TET, technique=FREE)
	VerPart.seedPart(size=meshsize)
	VerPart.generateMesh()
#	
# For Corrosion Analysis Output Part Vertices and Element Connectivity
if ana_type==2:
	GeomModules.VertsConn(VerPart,dimension)
	ecor=open('ecor.dat','w')
	for eachface in VerPart.faces:
		if len(eachface.getAdjacentFaces())<7.:
			xnor=eachface.getNormal()[0]
			ynor=eachface.getNormal()[1]
			znor=eachface.getNormal()[2]
			if (xnor==0.)and(znor==0.):
#				if (ynor==1.)or(ynor==-1.):	
				if (ynor==1.):					
					ecor.write("%6.4f %6.4f %6.4f\n"%(xnor,ynor,znor))
	ecor.close()
#
#Generate Materials and Sections
if mat_props==1:
	GeomModules.MatGen(ana_type,VerPart,VerModel,part_type,meshsize,random_seed)
#	
#Steps and Boundary Conditions
if bound_conds==1:
	VerModel.ExplicitDynamicsStep(name='Corrode', previous='Initial', 
		massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, 0.0, 1e-06, 
		BELOW_MIN, 0, 0, 0.0, 0.0, 0, None), ))
	VerModel.ExplicitDynamicsStep(name='Load', previous='Corrode', 
		timePeriod=1.)
	VerModel.steps['Corrode'].Restart(numberIntervals=2,overlay=OFF,timeMarks=OFF) 
	VerModel.steps['Load'].Restart(numberIntervals=2,overlay=OFF, timeMarks=OFF)
	VerModel.FieldOutputRequest(name='F-Output-1', 
		createStepName='Corrode', variables=('A', 'CSTRESS', 'LE', 'PE', 
		'PEEQ', 'RF', 'S', 'SDV', 'STATUS', 'U','V'), numIntervals=100)	 		
	#	
	#Loads and BCs
	VerAssembly.Instance(name='CorPart',part=VerPart, dependent=ON)
	iNodes=VerAssembly.instances['CorPart'].nodes
#	GeomModules.S1BCs(iNodes,VerModel,num_high,num_wide,num_thick,shape,
#		dimension,extrude_depth,rad,scalex,scaley,scalez)	
#
#VerAssembly.Instance(name='CorPart',part=VerPart, dependent=ON)
#Create Job and write input file
if write_output ==1:
	VerFile.Job(name='GeomGenTemp', model='Model-1', type=ANALYSIS, 		
		explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE,userSubroutine='',  
		parallelizationMethodExplicit=DOMAIN,numDomains=1,multiprocessingMode=DEFAULT, numCpus=1) 				
	VerFile.jobs['GeomGenTemp'].writeInput(consistencyChecking=OFF)
#
# Perform Postprocessing for corrosion analysis
if post_proc ==1:
	retcode=subprocess.call("GeomGenPost2.exe")
