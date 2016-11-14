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

# Draw a Square Grain
#
def DrawSquare(VerModel,part_type,rad,extrude_depth):
	from abaqusConstants import *
	from abaqus import *
	label='Base'
	if part_type==3:
		VerPart=VerModel.Part(name=label, dimensionality=THREE_D,type=DEFORMABLE_BODY)
	else:
		VerPart=VerModel.Part(name=label, dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
	VerPart.DatumPointByCoordinate((0,0,0))
	VerPart.DatumPointByCoordinate((1,0,0))
	VerPart.DatumPointByCoordinate((0,1,0))	
	pdatums=VerPart.datums
	VerPart.DatumPlaneByThreePoints(point1=pdatums[1], point2=pdatums[2], point3=pdatums[3])
	VerPart.DatumAxisByTwoPoint(point1=pdatums[1],point2=pdatums[2])
	partTransform = VerPart.MakeSketchTransform(sketchPlane=pdatums[4], sketchUpEdge=pdatums[5], 
		sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0,0,0))
	VerSketch = VerModel.ConstrainedSketch(name=label,sheetSize=200, transform=partTransform)
	VerSketch.Line(point1=(0.,0.),point2=(rad,0.))
	VerSketch.Line(point1=(rad,0.),point2=(rad,rad))
	VerSketch.Line(point1=(rad,rad),point2=(0.,rad))
	VerSketch.Line(point1=(0.,rad),point2=(0.,0.))
	if part_type==3:
		VerPart.BaseSolidExtrude(sketch=VerSketch,depth=extrude_depth)
	else:
		VerPart.BaseShell(sketch=VerSketch)
# Draw a Hexagonal Grain
#
def DrawHexagon(VerModel,part_type,rad,extrude_depth):
	from abaqusConstants import *
	from abaqus import *
	label='Base'
	VerAssembly=VerModel.rootAssembly	
	if part_type==3:
		VerPart=VerModel.Part(name=label, dimensionality=THREE_D,type=DEFORMABLE_BODY)
	else:
		VerPart=VerModel.Part(name=label, dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
	VerPart.DatumPointByCoordinate((0,0,0))
	VerPart.DatumPointByCoordinate((1,0,0))
	VerPart.DatumPointByCoordinate((0,1,0))	
	pdatums=VerPart.datums
	VerPart.DatumPlaneByThreePoints(point1=pdatums[1], point2=pdatums[2], point3=pdatums[3])
	VerPart.DatumAxisByTwoPoint(point1=pdatums[1],point2=pdatums[2])
	partTransform = VerPart.MakeSketchTransform(sketchPlane=pdatums[4], sketchUpEdge=pdatums[5], 
		sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0,0,0))
	VerSketch = VerModel.ConstrainedSketch(name=label,sheetSize=200, transform=partTransform)
	yheight=sin(radians(30.))
	xheight=cos(radians(30.))	
	VerSketch.Line(point1=(0.,0.),point2=(rad*xheight,rad*yheight))
	VerSketch.Line(point1=(rad*xheight,rad*yheight),point2=(rad*xheight,rad*yheight+rad))
	VerSketch.Line(point1=(rad*xheight,rad*yheight+rad),point2=(0.,2.*rad*yheight+rad))
	VerSketch.Line(point1=(0.,2.*rad*yheight+rad),point2=(-rad*xheight,rad*yheight+rad))
	VerSketch.Line(point1=(-rad*xheight,rad*yheight+rad),point2=(-rad*xheight,rad*yheight))
	VerSketch.Line(point1=(-rad*xheight,rad*yheight),point2=(0.,0.))
	if part_type==3:
		VerPart.BaseSolidExtrude(sketch=VerSketch,depth=extrude_depth)	
	else:
		VerPart.BaseShell(sketch=VerSketch)
	BasePart=VerModel.parts['Base']
	BasePartCells = BasePart.cells
	BasePartFaces = BasePart.faces
	BasePartVerts = BasePart.vertices
	if part_type==3:
		BasePart.PartitionCellByPlaneThreePoints(point1=BasePartVerts[4], point2=BasePartVerts[10], 
			point3=BasePartVerts[11], cells=BasePartCells)	
	else:		
		BasePart.PartitionFaceByShortestPath(point1=BasePartVerts[4], point2=BasePartVerts[1], 
			faces=BasePartFaces)		
# Draw a Dodecahedral Grain
#
def DrawDodec(VerModel,rad):
	from abaqusConstants import *
	from abaqus import *
	label='BaseTemp'
	VerAssembly=VerModel.rootAssembly	
	VerPart=VerModel.Part(name=label, dimensionality=THREE_D,type=DEFORMABLE_BODY)
	VerPart.DatumPointByCoordinate((0,0,0))
	VerPart.DatumPointByCoordinate((1,0,0))
	VerPart.DatumPointByCoordinate((0,1,0))	
	pdatums=VerPart.datums
	VerPart.DatumPlaneByThreePoints(point1=pdatums[1], point2=pdatums[2], point3=pdatums[3])
	VerPart.DatumAxisByTwoPoint(point1=pdatums[1],point2=pdatums[2])
	partTransform = VerPart.MakeSketchTransform(sketchPlane=pdatums[4], sketchUpEdge=pdatums[5], 
		sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0,0,0))
	VerSketch = VerModel.ConstrainedSketch(name=label,sheetSize=200, transform=partTransform)
	VerSketch.Line(point1=(0.,0.),point2=(sqrt(2.)*rad,rad))
	VerSketch.Line(point1=(sqrt(2.)*rad,rad),point2=(0.,2.*rad))
	VerSketch.Line(point1=(0.,2.*rad),point2=(-sqrt(2.)*rad,rad))
	VerSketch.Line(point1=(-sqrt(2.)*rad,rad),point2=(0.,0.))
	VerPart.BaseShell(sketch=VerSketch)
	for i in range (1,13):
		dodecname='dodec'+str(i)
		VerAssembly.Instance(name=dodecname,part=VerPart, dependent=ON)
	VerAssembly.translate(instanceList=('dodec2', ), vector=(0.,0.,-2.*sqrt(2.)*rad))
	VerAssembly.rotate(instanceList=('dodec3','dodec4', ), axisPoint=(0.0, 0.0, 0.0), 
		axisDirection=(0.0, 1., 0.0), angle=90.0)
	VerAssembly.translate(instanceList=('dodec3', ), vector=(sqrt(2.)*rad,0.,0.))	
	VerAssembly.translate(instanceList=('dodec4', ), vector=(-sqrt(2.)*rad,0.,0.))
	VerAssembly.translate(instanceList=('dodec3','dodec4', ), vector=(0.,0.,-sqrt(2.)*rad))
	VerAssembly.rotate(instanceList=('dodec5','dodec6','dodec7','dodec8',), 
		axisPoint=(-sqrt(2.)*rad, rad, 0.0), axisDirection=(0., 0., 1.), angle=90.0)
	VerAssembly.rotate(instanceList=('dodec5','dodec6','dodec7','dodec8',), 
		axisPoint=(-sqrt(2.)*rad, rad, 0.0), axisDirection=(0., 1., 0.), angle=-45.0)
	VerAssembly.rotate(instanceList=('dodec5','dodec6','dodec7','dodec8',), 
		axisPoint=(-sqrt(2.)*rad, rad, 0.0), axisDirection=(1., 0., 1.), angle=-45.0)
	VerAssembly.rotate(instanceList=('dodec6',), 
		axisPoint=(0., rad, -sqrt(2.)*rad), axisDirection=(0., 1., 0.), angle=90.0)
	VerAssembly.rotate(instanceList=('dodec7',), 
		axisPoint=(0., rad, -sqrt(2.)*rad), axisDirection=(0., 1., 0.), angle=180.0)	
	VerAssembly.rotate(instanceList=('dodec8',), 
		axisPoint=(0., rad, -sqrt(2.)*rad), axisDirection=(0., 1., 0.), angle=270.0)			
	VerAssembly.rotate(instanceList=('dodec9','dodec10','dodec11','dodec12',), 
		axisPoint=(-sqrt(2.)*rad, rad, 0.0), axisDirection=(0., 0., 1.), angle=-90.0)
	VerAssembly.rotate(instanceList=('dodec9','dodec10','dodec11','dodec12',), 
		axisPoint=(-sqrt(2.)*rad, rad, 0.0), axisDirection=(0., 1., 0.), angle=-45.0)
	VerAssembly.rotate(instanceList=('dodec9','dodec10','dodec11','dodec12',), 
		axisPoint=(-sqrt(2.)*rad, rad, 0.0), axisDirection=(1., 0., 1.), angle=45.0)	
	VerAssembly.rotate(instanceList=('dodec10',), 
		axisPoint=(0., rad, -sqrt(2.)*rad), axisDirection=(0., -1., 0.), angle=90.0)
	VerAssembly.rotate(instanceList=('dodec11',), 
		axisPoint=(0., rad, -sqrt(2.)*rad), axisDirection=(0., -1., 0.), angle=180.0)	
	VerAssembly.rotate(instanceList=('dodec12',), 
		axisPoint=(0., rad, -sqrt(2.)*rad), axisDirection=(0., -1., 0.), angle=270.0)
	VerAssembly.InstanceFromBooleanMerge(name='Base', instances=(
		VerAssembly.instances['dodec1'], 
		VerAssembly.instances['dodec2'], VerAssembly.instances['dodec3'], 
		VerAssembly.instances['dodec4'], VerAssembly.instances['dodec5'], 
		VerAssembly.instances['dodec6'], VerAssembly.instances['dodec7'], 
		VerAssembly.instances['dodec8'], VerAssembly.instances['dodec9'], 
		VerAssembly.instances['dodec10'],VerAssembly.instances['dodec11'],  
		VerAssembly.instances['dodec12'], ), 
		keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY)		
	VerPart=VerModel.parts['Base']
	VerPart.AddCells(faceList = VerPart.faces)
	for i in range (1,12):
		dodecname='dodec'+str(i)
		del VerAssembly.instances[dodecname]
	del VerAssembly.instances['Base-1']
# Draw a 2D Voronoi Tessellation
#
def Voronoi2D(VerModel,part_type,extrude_depth,num_grains,maxsize,hard_rad,random_seed):
	from abaqusConstants import *
	from abaqus import *
	import random
	import subprocess
	xlist=[0.]
	ylist=[0.]
	VerAssembly=VerModel.rootAssembly
	random.seed(random_seed)
	qhullin=open('qhullin.dat','w')
	qhullin.write("%i \n"%(2))
	qhullin.write("%i \n"%(num_grains*9))
	for i in range(0,num_grains):
		outside=False
		while outside==False:
			xcor=random.random()*maxsize
			ycor=random.random()*maxsize
			if hard_rad==0.:
				outside=True
				break
			if len(xlist)>1:
				distold=1000.
				for i in range(1,len(xlist)):
					distnew=(xcor-xlist[i])*(xcor-xlist[i])+(ycor-ylist[i])*(ycor-ylist[i])
					distnew=sqrt(distnew)
					if distnew<distold:
						distold=distnew
				if distold>=hard_rad:
					outside=True
			else:
				outside=True
		xlist.append(xcor)
		ylist.append(ycor)
		qhullin.write("%18.6f %18.6f \n"%(xcor,ycor))
		qhullin.write("%18.6f %18.6f \n"%(xcor+maxsize,ycor))
		qhullin.write("%18.6f %18.6f \n"%(xcor-maxsize,ycor))
		qhullin.write("%18.6f %18.6f \n"%(xcor,ycor+maxsize))
		qhullin.write("%18.6f %18.6f \n"%(xcor,ycor-maxsize))
		qhullin.write("%18.6f %18.6f \n"%(xcor+maxsize,ycor+maxsize))
		qhullin.write("%18.6f %18.6f \n"%(xcor-maxsize,ycor-maxsize))
		qhullin.write("%18.6f %18.6f \n"%(xcor+maxsize,ycor-maxsize))
		qhullin.write("%18.6f %18.6f \n"%(xcor-maxsize,ycor+maxsize))
	qhullin.close()
	scales=open('scales.dat','w')
	scales.write("%18.6f \n"%(maxsize))
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
	for i in range(0,num_cells):
		label='Cell'+str(i)
		if part_type==3:
			VerPart=VerModel.Part(name=label, dimensionality=THREE_D,type=DEFORMABLE_BODY)
		else:
			VerPart=VerModel.Part(name=label, dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
		# Constuct Datum Point At Each Node
		VerPart.DatumPointByCoordinate((0,0,0))
		VerPart.DatumPointByCoordinate((1,0,0))
		VerPart.DatumPointByCoordinate((0,1,0))	
		pdatums=VerPart.datums
		# Constuct Datum Plane on Element Face and Datum Axis Along Element Base
		VerPart.DatumPlaneByThreePoints(point1=pdatums[1], 
			point2=pdatums[2], point3=pdatums[3])
		VerPart.DatumAxisByTwoPoint(point1=pdatums[1],point2=pdatums[2])
		# Sketch New Part Geometry Over Original Element
		partTransform = VerPart.MakeSketchTransform(sketchPlane=pdatums[4], 
			sketchUpEdge=pdatums[5], 
			sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0,0,0))
		VerSketch = VerModel.ConstrainedSketch(name=label,sheetSize=200, 
			transform=partTransform)
		num_verts=int(FortranFile.readline())
		for j in range(0,num_verts):
			coords=FortranFile.readline().split(',')
			cordx.append([])
			cordy.append([])
			cordx[j]=float(coords[0])
			cordy[j]=float(coords[1])
		print i,num_verts
		for j in range(0,num_verts-1):				
			VerSketch.Line(point1=(cordx[j],cordy[j]),point2=(cordx[j+1],cordy[j+1]))
			x1.append([])
			y1.append([])
			x1[k]=cordx[j]
			y1[k]=cordy[j]
			x2.append([])
			y2.append([])
			x2[k]=cordx[j+1]
			y2[k]=cordy[j+1]
			k=k+1
		VerSketch.Line(point1=(cordx[num_verts-1],cordy[num_verts-1]),
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
		print i,num_verts,k
		if part_type==3:
			VerPart.BaseSolidExtrude(sketch=VerSketch, depth=extrude_depth)
		else:
			VerPart.Shell(sketchPlane=pdatums[4], sketchUpEdge=pdatums[5], sketchPlaneSide=SIDE1,
				sketchOrientation=BOTTOM, sketch=VerSketch)
		VerAssembly.Instance(name=label,part=VerPart)
	inst=[]
	inst.append([])
	for i in range(0,num_cells):
		inst[i]=VerAssembly.instances['Cell'+str(i)]
		if i<num_cells-1:
			inst.append([])
	VerAssembly.InstanceFromBooleanMerge(name='Merged',
		instances=inst,originalInstances=DELETE, keepIntersections=ON,domain=GEOMETRY)
# Draw a 3D Voronoi Tessellation
#
def Voronoi3D(VerModel,num_grains,maxsize,hard_rad,random_seed):
	from abaqusConstants import *
	from abaqus import *
	import random
	import subprocess
	xlist=[0.]
	ylist=[0.]
	zlist=[0.]
	VerAssembly=VerModel.rootAssembly
	random.seed(random_seed)
	qhullin=open('qhullin.dat','w')		
	qhullin.write("%i \n"%(3))
	qhullin.write("%i \n"%(num_grains*27))
	for i in range(0,num_grains):
		outside=False
		while outside==False:
			xcor=random.random()*maxsize
			ycor=random.random()*maxsize
			zcor=random.random()*maxsize
			if hard_rad==0.:
				outside=True
				break
			if len(xlist)>1:
				distold=1000.
				for i in range(1,len(xlist)):
					distnew=(xcor-xlist[i])*(xcor-xlist[i])+(ycor-ylist[i])*(ycor-ylist[i])
					distnew=distnew+(zcor-zlist[i])*(zcor-zlist[i])
					distnew=sqrt(distnew)
					if distnew<distold:
						distold=distnew
				if distold>=hard_rad:
					outside=True
			else:
				outside=True
		xlist.append(xcor)
		ylist.append(ycor)	
		zlist.append(zcor)	
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor,ycor,zcor))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxsize,ycor,zcor))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor-maxsize,ycor,zcor))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor,ycor+maxsize,zcor))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor,ycor-maxsize,zcor))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxsize,ycor+maxsize,zcor))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor-maxsize,ycor-maxsize,zcor))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxsize,ycor-maxsize,zcor))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor-maxsize,ycor+maxsize,zcor))	
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor,ycor,zcor+maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxsize,ycor,zcor+maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor-maxsize,ycor,zcor+maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor,ycor+maxsize,zcor+maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor,ycor-maxsize,zcor+maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxsize,ycor+maxsize,zcor+maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor-maxsize,ycor-maxsize,zcor+maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxsize,ycor-maxsize,zcor+maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor-maxsize,ycor+maxsize,zcor+maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor,ycor,zcor-maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxsize,ycor,zcor-maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor-maxsize,ycor,zcor-maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor,ycor+maxsize,zcor-maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor,ycor-maxsize,zcor-maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxsize,ycor+maxsize,zcor-maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor-maxsize,ycor-maxsize,zcor-maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor+maxsize,ycor-maxsize,zcor-maxsize))
		qhullin.write("%18.6f %18.6f %18.6f \n"%(xcor-maxsize,ycor+maxsize,zcor-maxsize))
	qhullin.close()
	scales=open('scales.dat','w')
	scales.write("%18.6f \n"%(maxsize))
	scales.close()
	retcode=subprocess.call("qvoronoi.exe TI qhullin.dat o Fi TO qhullout.dat")	
	retcode=subprocess.call("Voronoi3DPost.exe")
	FortranFile=open('fortranout.dat')
	num_cells=int(FortranFile.readline())
	cordx=[]
	cordy=[]
	cordz=[]
	x1=[]
	y1=[]
	x2=[]
	y2=[]
	k=0
	for k in range(0,num_cells):
		ibreak=0
		num_hyp=int(FortranFile.readline())
		for i in range(0,num_hyp):
			label='C'+str(k)+'H'+str(i)
			VerPart=VerModel.Part(name=label, dimensionality=THREE_D,type=DEFORMABLE_BODY) 
			# Constuct Datum Point At Each Node
			num_verts=int(FortranFile.readline())
			for j in range(0,num_verts):
				coords=FortranFile.readline().split(',')
				cordx.append([])
				cordy.append([])
				cordz.append([])
				cordx[j]=float(coords[0])
				cordy[j]=float(coords[1])
				cordz[j]=float(coords[2])
				VerPart.DatumPointByCoordinate((cordx[j],cordy[j],cordz[j]))
			pdatums=VerPart.datums
			p1x=pdatums[1].pointOn[0]
			p1y=pdatums[1].pointOn[1]
			p1z=pdatums[1].pointOn[2]
			tol=1.e-4
			for m in range(2,num_verts+1):
				px=pdatums[m].pointOn[0]
				py=pdatums[m].pointOn[1]
				pz=pdatums[m].pointOn[2]			
				p1pk=sqrt((p1x-px)*(p1x-px)+(p1y-py)*(p1y-py)+(p1z-pz)*(p1z-pz))
				if p1pk>tol:
					index1=m
					p2x=px
					p2y=py
					p2z=pz
					break
			for m in range(2,num_verts+1):
				if m!=index1:
					px=pdatums[m].pointOn[0]
					py=pdatums[m].pointOn[1]
					pz=pdatums[m].pointOn[2]			
					p1pk=sqrt((p1x-px)*(p1x-px)+(p1y-py)*(p1y-py)+(p1z-pz)*(p1z-pz))
					p2pk=sqrt((p2x-px)*(p2x-px)+(p2y-py)*(p2y-py)+(p2z-pz)*(p2z-pz))
					if p1pk>tol:
						if p2pk>tol:						
							index2=m
							break
			VerPart.DatumPlaneByThreePoints(point1=pdatums[1], point2=pdatums[index1], point3=pdatums[index2])
			VerPart.DatumAxisByTwoPoint(point1=pdatums[1],point2=pdatums[index1])
			partTransform = VerPart.MakeSketchTransform(sketchPlane=pdatums[num_verts+1],
				sketchUpEdge=pdatums[num_verts+2], sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0.,0.,0.))	
			sklabel='Skbase'+'C'+str(k)+'H'+str(i)
			VerSketch=VerModel.ConstrainedSketch(name=sklabel,sheetSize=200, transform=partTransform)			
			VerPart.projectReferencesOntoSketch(sketch=VerSketch, filter=COPLANAR_EDGES)
			verts=VerSketch.vertices
			centroidx=0.
			centroidy=0.
			angle=[]
			jnum=[]
			for j in range(0,num_verts):
				centroidx=centroidx+verts[j].coords[0]
				centroidy=centroidy+verts[j].coords[1]
			centroidx=centroidx/float(num_verts)
			centroidy=centroidy/float(num_verts)
			for j in range(0,num_verts):
				pointx=verts[j].coords[0]-centroidx
				pointy=verts[j].coords[1]-centroidy
				vertangle=atan2(pointy,pointx)	
				if vertangle<0.:
					vertangle=2*pi+vertangle
				angle.append(vertangle)
				jnum.append(j)
			icheck=0
			while icheck==0:
				icheck=1
				for j in range(1,num_verts):
					if angle[j]<angle[j-1]:
						temp1=angle[j-1]
						temp2=jnum[j-1]
						angle[j-1]=angle[j]
						angle[j]=temp1
						jnum[j-1]=jnum[j]
						jnum[j]=temp2
						icheck=0
			for j in range(1,num_verts):
				x1=verts[jnum[j]].coords[0]
				x2=verts[jnum[j-1]].coords[0]
				y1=verts[jnum[j]].coords[1]
				y2=verts[jnum[j-1]].coords[1]
				VerSketch.Line(point1=(x1,y1),point2=(x2,y2))
			VerSketch.Line(point1=(verts[jnum[num_verts-1]].coords[0],
				verts[jnum[num_verts-1]].coords[1]),
				point2=(verts[jnum[0]].coords[0],verts[jnum[0]].coords[1]))	
			VerPart.Shell(sketchPlane=pdatums[num_verts+1], sketchPlaneSide=SIDE1,
				sketchUpEdge=pdatums[num_verts+2],sketchOrientation=BOTTOM,sketch=VerSketch) 	
			label='Part'+'C'+str(k)+'H'+str(i)
			VerAssembly.Instance(name=label,part=VerPart)
		if ibreak==1:
			continue
		inst=[]
		inst.append([])	
		for i in range(0,num_hyp):
			inst[i]=VerAssembly.instances['Part'+'C'+str(k)+'H'+str(i)]
			if i<num_hyp-1:
				inst.append([])
		VerAssembly.InstanceFromBooleanMerge(name='Merged'+str(k),
			instances=inst,originalInstances=DELETE, keepIntersections=ON,domain=GEOMETRY)				
		shellpart=VerModel.parts['Merged'+str(k)]
		try:
			shellpart.AddCells(faceList = shellpart.faces)
		except AbaqusException,errormessage:
			print errormessage, 'Not Merged'
		VerAssembly.Instance(name='Part'+str(k),part=shellpart, dependent=ON)
		del VerAssembly.instances['Merged'+str(k)+'-1']
		for i in range(0,num_hyp):
			del VerModel.sketches['Skbase'+'C'+str(k)+'H'+str(i)]
			del VerModel.parts['C'+str(k)+'H'+str(i)]
		print float(k)/float(num_cells)
	inst=[]
	inst.append([])
	for i in range(0,num_cells):
		inst[i]=VerAssembly.instances['Part'+str(i)]
		if i<num_cells-1:
			inst.append([])
	VerAssembly.InstanceFromBooleanMerge(name='Merged',
		instances=inst,originalInstances=DELETE, keepIntersections=ON,domain=GEOMETRY)
# Make a Boolean Template Part
#
def BooleanPart(VerModel,part_type,rad,extrude_depth,
	num_high,num_wide,num_thick,shape,dimension,scalex,scaley,scalez):
	from abaqusConstants import *
	from abaqus import *
	VerAssembly=VerModel.rootAssembly
	booSketch=VerModel.ConstrainedSketch(name='BSmall', sheetSize=20.0)
	if shape==1:
		vert1x=0.
		vert1y=0.
		vert2x=rad*num_high
		vert2y=0.
		vert3x=rad*num_high
		vert3y=rad*num_wide
		vert4x=0.
		vert4y=rad*num_wide
		edepth=extrude_depth*num_thick
	if shape==2:
		yheight=sin(radians(30.))
		xheight=cos(radians(30.))	
		vert1x=0.
		vert1y=rad*yheight+rad/2.
		vert2x=rad*xheight*(float(num_high)-1.)*2.
		vert2y=rad*yheight+rad/2.
		vert3x=rad*xheight*(float(num_high)-1.)*2.
		vert3y=rad*yheight+rad/2.+(float(num_wide)-1.)*(rad+rad*yheight)
		vert4x=0.
		vert4y=rad*yheight+rad/2.+(float(num_wide)-1.)*(rad+rad*yheight)
		edepth=extrude_depth*num_thick
	if shape==3:
		vert1x=0.
		vert1y=rad
		vert2x=sqrt(2.)*rad*(2.*float(num_high)-1.)
		vert2y=rad
		vert3x=sqrt(2.)*rad*(2.*float(num_high)-1.)
		vert3y=rad*(2.*float(num_wide)-1.)
		vert4x=0.
		vert4y=rad*(2.*float(num_wide)-1.)
		edepth=sqrt(2.)*rad*(2.*float(num_thick)-1.)
	if shape==4:
		vert1x=0.
		vert1y=0.
		vert2x=scalex
		vert2y=0.
		vert3x=scalex
		vert3y=scaley
		vert4x=0.
		vert4y=scaley
		if dimension==2:
			edepth=extrude_depth
		else:
			edepth=scalez		
	booSketch.Line(point1=(vert1x,vert1y), point2=(vert2x, vert2y))			
	booSketch.Line(point1=(vert2x, vert2y), point2=(vert3x, vert3y))
	booSketch.Line(point1=(vert3x, vert3y), point2=(vert4x, vert4y))			
	booSketch.Line(point1=(vert4x, vert4y), point2=(vert1x, vert1y))			
	if part_type==3:
		booPart=VerModel.Part(name='BSmall', dimensionality=THREE_D,type=DEFORMABLE_BODY) 
		booPart.BaseSolidExtrude(sketch=booSketch, depth=edepth)
	else:
		booPart=VerModel.Part(name='BSmall', dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY) 
		booPart.BaseShell(sketch=booSketch)	
	booSketchB=VerModel.ConstrainedSketch(name='BBig', sheetSize=20.0)
	booSketchB.Line(point1=(vert1x-10.,vert1y-10.), point2=(vert2x+10., vert2y-10.))			
	booSketchB.Line(point1=(vert2x+10., vert2y-10.), point2=(vert3x+10., vert3y+10.))
	booSketchB.Line(point1=(vert3x+10., vert3y+10.), point2=(vert4x-10., vert4y+10.))			
	booSketchB.Line(point1=(vert4x-10., vert4y+10.), point2=(vert1x-10., vert1y-10.))	
	if part_type==3:
		booPartb=VerModel.Part(name='BBig', dimensionality=THREE_D,type=DEFORMABLE_BODY) 
		booPartb.BaseSolidExtrude(sketch=booSketchB, depth=edepth*10.)
	else:
		booPartb=VerModel.Part(name='BBig', dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY) 
		booPartb.BaseShell(sketch=booSketchB)	
	VerAssembly.Instance(name='BSmall',part=booPart, dependent=ON)
	VerAssembly.Instance(name='BBig',part=booPartb, dependent=ON)
	if shape==3:
		if part_type==3:
			VerAssembly.translate(instanceList=('BSmall', ), 
				vector=(0.,0.,-sqrt(2.)*rad))
			VerAssembly.translate(instanceList=('BBig', ), 
				vector=(0.,0.,-sqrt(2.)*rad*5.))
	if shape==4:
		if part_type==3:
			VerAssembly.translate(instanceList=('BBig', ), 
				vector=(0.,0.,-edepth*5.))
	VerAssembly.InstanceFromBooleanCut(name='Template', 
		instanceToBeCut=VerAssembly.instances['BBig'], 
		cuttingInstances=(VerAssembly.instances['BSmall'], ), 
		originalInstances=DELETE)
# Pattern base parts for multilpe grains
#
def PatternParts(num_high,num_wide,num_thick,VerPart,rad,shape,VerModel):
	from abaqusConstants import *
	from abaqus import *
	VerAssembly=VerModel.rootAssembly
	yheight=sin(radians(30.))
	xheight=cos(radians(30.))
	icount=0
	for i in range(0,num_high):
		for j in range(0,num_wide):
			for k in range(0,num_thick):				
				label='Part'+str(icount)				
				VerAssembly.Instance(name=label,part=VerPart, dependent=ON)				
				# Square
				if shape==1:
					VerAssembly.translate(instanceList=(label, ), 
						vector=(i*rad,j*rad,k*rad))
				# Hexagon
				if shape==2:
					if j%2==0:
						VerAssembly.translate(instanceList=(label, ), 
							vector=(i*xheight*rad*2.,j*rad*(1.+yheight),k*rad))
					else:
						VerAssembly.translate(instanceList=(label, ), 
							vector=(i*xheight*rad*2.+xheight*rad,j*rad*(1.+yheight),k*rad))
				# Dodecahedron
				if shape==3:
					if j%2==0:
						VerAssembly.translate(instanceList=(label, ), 
							vector=(i*rad*2.*sqrt(2.),j*2.*rad,2.*k*rad*sqrt(2.)))
					else:
						VerAssembly.translate(instanceList=(label, ), 
							vector=(i*rad*2.*sqrt(2.)+sqrt(2.)*rad,j*2.*rad,2.*k*rad*sqrt(2.)+sqrt(2.)*rad))
				icount=icount+1
	inst=[]
	inst.append([])
	for i in range(0,icount):
		inst[i]=VerAssembly.instances['Part'+str(i)]
		if i<icount-1:
			inst.append([])
	VerAssembly.InstanceFromBooleanMerge(name='Merged',
		instances=inst,originalInstances=DELETE, keepIntersections=ON,domain=GEOMETRY)
# Output vertices and element connectivity for corrosion analysis
#
def VertsConn(VerPart,dimension):
	from abaqusConstants import *
	from abaqus import *
	vertout=open('vertout.dat','w')
	vertout.write("%i\n"%(len(VerPart.cells)))	
	k=1.
	for eachcell in VerPart.cells:
		print k/float(len(VerPart.cells))
		cellElements=eachcell.getElements()
		vertout.write("%i\n"%(len(cellElements)))
		cellFaces=eachcell.getFaces()
		for eachElement in cellElements:
			vertout.write("%i\n"%(eachElement.label))
			Adj_Elem=eachElement.getAdjacentElements()
			vertout.write("%i\n"%(len(Adj_Elem)))
			for i in range(0,len(Adj_Elem)):
				vertout.write("%i\n"%(Adj_Elem[i].label))
			centroidx=0.
			centroidy=0.
			centroidz=0.
			dmin=1000.
			for eachNode in eachElement.getNodes():
				centroidx=centroidx+eachNode.coordinates[0]
				centroidy=centroidy+eachNode.coordinates[1]
				centroidz=centroidz+eachNode.coordinates[2]
			num_nodes=float(len(eachElement.getNodes()))
			centroidx=centroidx/num_nodes
			centroidy=centroidy/num_nodes
			centroidz=centroidz/num_nodes
			for i in range(0,len(cellFaces)):
				eachFace=VerPart.faces[cellFaces[i]]
				facex=eachFace.pointOn[0][0]
				facey=eachFace.pointOn[0][1]
				facez=eachFace.pointOn[0][2]
				normalx=eachFace.getNormal()[0]
				normaly=eachFace.getNormal()[1]
				normalz=eachFace.getNormal()[2]
				if dimension==2:
					if normalx==0.:
						if normaly==0.:
							if abs(normalz)==1:
								continue
				else:
					if len(Adj_Elem)<6:
						if normalx==0.:
							if normaly==0.:
								if abs(normalz)==1:
									continue
				dfcx=facex-centroidx
				dfcy=facey-centroidy
				dfcz=facez-centroidz
				distance=abs(dfcx*normalx+dfcy*normaly+dfcz*normalz)
				if distance<dmin:
					dmin=distance
			vertout.write("%18.6f\n"%(dmin))
		k=k+1
	vertout.close()	
# Generate Materials and Sections
#	
def MatGen(ana_type,VerPart,VerModel,part_type,meshsize,random_seed):
	from abaqusConstants import *
	from abaqus import *
	import random
	if ana_type==2:
		VerModel.Material(name='Magnesium')
		VerModel.materials['Magnesium'].Density(table=((1e-05, ), ))
		VerModel.materials['Magnesium'].Depvar(deleteVar=20, n=30)
		VerModel.materials['Magnesium'].UserMaterial(
			mechanicalConstants=(44000.0, 0.35, 138.7, 16.0, 165.0,0.5))
		if part_type==3:
			regions=VerPart.cells
		else:
			regions=VerPart.faces
		VerModel.HomogeneousSolidSection(name='Magnesium', 
			material='Magnesium', thickness=meshsize)
		VerPart.SectionAssignment(region=(regions,), 
			sectionName='Magnesium', offset=0.0, offsetField='')
	else:
		labelcount=1
		if part_type==3:
			regions=VerPart.cells
		else:
			regions=VerPart.faces
		random.seed(random_seed)
		for eachregion in regions:
			rand1=(random.random()-0.5)*2.
			rand2=(random.random()-0.5)*2.
			rand3=(random.random()-0.5)*2.
			rand4=(random.random()-0.5)*2.
			rand5=(random.random()-0.5)*2.
			rand6=(rand1*rand4+rand2*rand5)/(-rand3)
			mlabel='Mat'+str(labelcount)
			VerModel.Material(name=mlabel)
			VerModel.materials[mlabel].Density(table=((1e-05, ), ))
			VerModel.materials[mlabel].Depvar(deleteVar=124, n=124)
			VerModel.materials[mlabel].UserMaterial(
				mechanicalConstants=(200000.0, 0.3, 					
				rand1, rand2, rand3,1.,0.,0.,rand4,rand5,rand6,0.,0.,1.,					
				10.,0.001,541.5,109.5,60.8,1.,1.,0.5,1.))
			VerModel.HomogeneousSolidSection(name=mlabel, 
				material=mlabel, thickness=meshsize)
			VerPart.SectionAssignment(region=(eachregion,), 
				sectionName=mlabel, offset=0.0, offsetField='')
			labelcount=labelcount+1
# Shape 1 BCs and Constraints  - Uniaxial Tension
#	
def S1BCs(iNodes,VerModel,num_high,num_wide,num_thick,shape,
		dimension,extrude_depth,rad,scalex,scaley,scalez):	
	from abaqusConstants import *
	from abaqus import *
	import regionToolset
	VerAssembly=VerModel.rootAssembly
	Min=-0.001
	Max=0.001
	fwide=float(num_wide)
	fhigh=float(num_high)
	fthick=float(num_thick)
	if shape==1:
#		BC LEFT	
		XMnBL=Min
		XMxBL=Max
		YMnBL=Min
		YMxBL=fwide*rad+Max
		ZMnBL=Min
		ZMxBL=Max+extrude_depth	
#		BC BACK
		XMnBBK=Min
		XMxBBK=fhigh*rad+Max
		YMnBBK=Min
		YMxBBK=fwide*rad+Max	
		ZMnBBK=Min
		ZMxBBK=Max
#		BC Bottom
		XMnBBT=Min
		XMxBBT=fhigh*rad+Max
		YMnBBT=Min
		YMxBBT=Max	
		ZMnBBT=Min
		ZMxBBT=Max+extrude_depth
#		BC Right
		XMnBR=fhigh*rad+Min
		XMxBR=fhigh*rad+Max
		YMnBR=Min
		YMxBR=fwide*rad+Max
		ZMnBR=Min
		ZMxBR=Max+extrude_depth	
#		RP
		XRP=fhigh*rad
		YRP=fwide*rad*0.5
		ZRP=extrude_depth*0.5	
	if shape==2:
		yheight=sin(radians(30.))
		xheight=cos(radians(30.))	
#		BC LEFT	
		XMnBL=Min
		XMxBL=Max
		YMnBL=rad*yheight+rad/2.+Min
		YMxBL=rad*yheight+rad/2.+(fwide-1.)*(rad+rad*yheight)+Max
		ZMnBL=Min
		ZMxBL=Max+extrude_depth	
#		BC BACK
		XMnBBK=Min
		XMxBBK=rad*xheight*(fhigh-1.)*2.+Max
		YMnBBK=rad*yheight+rad/2.+Min
		YMxBBK=rad*yheight+rad/2.+(fwide-1.)*(rad+rad*yheight)+Max
		ZMnBBK=Min
		ZMxBBK=Max
#		BC Bottom
		XMnBBT=Min
		XMxBBT=rad*xheight*(fhigh-1.)*2.+Max
		YMnBBT=rad*yheight+rad/2.+Min
		YMxBBT=rad*yheight+rad/2.+Max	
		ZMnBBT=Min
		ZMxBBT=Max+extrude_depth
#		BC Right
		XMnBR=rad*xheight*(fhigh-1.)*2.+Min
		XMxBR=rad*xheight*(fhigh-1.)*2.+Max
		YMnBR=rad*yheight+rad/2.+Min
		YMxBR=rad*yheight+rad/2.+(fwide-1.)*(rad+rad*yheight)+Max
		ZMnBR=Min
		ZMxBR=Max+extrude_depth	
#		RP
		XRP=rad*xheight*(fhigh-1.)*2.
		YRP=rad*yheight+rad/2.+(fwide-1.)*(rad+rad*yheight)*0.5
		ZRP=extrude_depth*0.5
	if shape==4:
#		BC LEFT	
		XMnBL=Min
		XMxBL=Max
		YMnBL=Min
		YMxBL=scaley+Max
		ZMnBL=Min
		ZMxBL=Max+extrude_depth	
#		BC BACK
		XMnBBK=Min
		XMxBBK=scalex+Max
		YMnBBK=Min
		YMxBBK=scaley+Max	
		ZMnBBK=Min
		ZMxBBK=Max
#		BC Bottom
		XMnBBT=Min
		XMxBBT=scalex+Max
		YMnBBT=Min
		YMxBBT=Max	
		ZMnBBT=Min
		ZMxBBT=Max+extrude_depth
#		BC Right
		XMnBR=scalex+Min
		XMxBR=scalex+Max
		YMnBR=Min
		YMxBR=scaley+Max
		ZMnBR=Min
		ZMxBR=Max+extrude_depth	
#		RP
		XRP=scalex
		YRP=scaley*0.5
		ZRP=extrude_depth*0.5	
#
	total_length=(XMxBR-Max)-(XMnBL-Min)
	BLeft=iNodes.getByBoundingBox(xMin=XMnBL,xMax=XMxBL,yMin=YMnBL,yMax=YMxBL,zMin=ZMnBL,zMax=ZMxBL)			
	BBack=iNodes.getByBoundingBox(xMin=XMnBBK,xMax=XMxBBK,yMin=YMnBBK,yMax=YMxBBK,zMin=ZMnBBK,zMax=ZMxBBK)		
	BBot=iNodes.getByBoundingBox(xMin=XMnBBT,xMax=XMxBBT,yMin=YMnBBT,yMax=YMxBBT,zMin=ZMnBBT,zMax=ZMxBBT)			
	BRight=iNodes.getByBoundingBox(xMin=XMnBR,xMax=XMxBR,yMin=YMnBR,yMax=YMxBR,zMin=ZMnBR,zMax=ZMxBR) 
	Ref1=VerAssembly.ReferencePoint(point=(XRP,YRP,ZRP))		
#	
	BLregion=regionToolset.Region(nodes=BLeft)
	BBregion=regionToolset.Region(nodes=BBot)
	BBKregion=regionToolset.Region(nodes=BBack)	
	BRregion=regionToolset.Region(nodes=BRight)	
	VerModel.DisplacementBC(name='LeftX', createStepName='Initial', 
		region=BLregion, u1=0.0, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, 
		ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM) 
	VerModel.DisplacementBC(name='BottomY', createStepName='Initial', 
		region=BBregion, u1=UNSET, u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, 
		ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM) 
	VerModel.DisplacementBC(name='BackZ', createStepName='Initial', 
		region=BBKregion, u1=UNSET, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, 
		ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM)
#
	id1=VerAssembly.features['RP-1'].id
	RPoint=regionToolset.Region(referencePoints=(VerAssembly.referencePoints[id1],))
	VerAssembly.Set(referencePoints=(VerAssembly.referencePoints[id1],), name='RPoint')
	VerAssembly.Set(nodes=BRight, name='BRight')
	VerModel.Equation(name='Constraint-1', terms=((1.0, 'BRight', 1), ( -1.0, 'RPoint', 1))) 
	VerModel.SmoothStepAmplitude(name='Load', timeSpan=STEP, data=((0.0, 0.0), (1.0, 1.0)))	
	VerModel.DisplacementBC(name='RPNode', createStepName='Load', 
		region=RPoint, u1=total_length*0.17, u2=0., u3=UNSET, ur1=UNSET, ur2=UNSET, 
		ur3=UNSET, amplitude='Load', fixed=OFF, distributionType=UNIFORM) 	
