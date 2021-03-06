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

import math
from abaqusConstants import *
from abaqus import *

part = mdb.models['Model-1'].parts['orphan']
height = 2.4
radius = height / (2.0 * math.pi)

coorindates = []
for eachnode in part.nodes:
	theta = eachnode.coordinates[1]/radius
	newy = (radius-eachnode.coordinates[2])*math.cos(theta)
	newz = (radius-eachnode.coordinates[2])*math.sin(theta)
        coorindates.append((eachnode.coordinates[0], newy, newz))

part.editNode(nodes=part.nodes, coordinates = coorindates)
