from abaqus import *
from abaqusConstants import *
import __main__
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
Mdb()


inp=open("UC.txt","r")
ucl1=eval(inp.readline().replace("\r\n",""))
r1=eval(inp.readline().replace("\r\n",""))
num1=eval(inp.readline().replace("\r\n",""))

R= ucl1*3

x=[]
y=[]
z=[]


import random
import math
num=num1
ucl=ucl1
r=r1

for i in range(0,num):
    x1=eval(inp.readline().replace("\r\n",""))
    x=x+[x1]
    y1=eval(inp.readline().replace("\r\n",""))
    y=y+[y1]
    z1=eval(inp.readline().replace("\r\n",""))
    z=z+[z1]

Uclx=ucl
Uclz=ucl
        
#:---------------------  Creating Matrix --------------------------------------------
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(ucl, ucl))
p = mdb.models['Model-1'].Part(name='Matrix', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Matrix']
p.BaseSolidExtrude(sketch=s, depth=ucl)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Matrix']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
#:---------------------  Creating Matrix --------------------------------------------

#:----------------   Creating Cylenderical Shape Sphere -----------------------------
 
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
engineeringFeatures=ON)
mdb.models['Model-1'].Material(name='Graphene')
mdb.models['Model-1'].materials['Graphene'].Conductivity(table=((2000, ), ))



mdb.models['Model-1'].Material(name='Polymer')
mdb.models['Model-1'].materials['Polymer'].Conductivity(table=((0.25, ), ))



mdb.models['Model-1'].HomogeneousSolidSection(name='Polymer',material='Polymer', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(name='Graphene', material='Graphene',thickness=None)
p = mdb.models['Model-1'].parts['Matrix']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(cells=cells)
p = mdb.models['Model-1'].parts['Matrix']
p.SectionAssignment(region=region, sectionName='Polymer', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='')

session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF,engineeringFeatures=OFF)
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=R*5)

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s.FixedConstraint(entity=g[2])
s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, r), point2=(0.0, -r), 
    direction=CLOCKWISE)
s.Line(point1=(0.0, r), point2=(0.0, -r))
s.VerticalConstraint(entity=g[4])
p = mdb.models['Model-1'].Part(name='Graphene', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Graphene']
p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Graphene']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

  
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,engineeringFeatures=ON)
p = mdb.models['Model-1'].parts['Graphene']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#f ]', ), )
region = regionToolset.Region(cells=cells)
p = mdb.models['Model-1'].parts['Graphene']
p.SectionAssignment(region=region, sectionName='Graphene', offset=0.0,offsetType=MIDDLE_SURFACE, offsetField='')

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Matrix']
a.Instance(name='Matrix-1', part=p, dependent=ON)

#:----------------  End of  Creating Cylenderical Shape Graphene  ------------------------------
 
#:----------------   Assemblies of the Graphene  -----------------------------------

vacancy=()
merg=()
for i in range(num):
    a = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Graphene']
    a.Instance(name='Graphene'+str(i), part=p, dependent=ON)
    a = mdb.models['Model-1'].rootAssembly
    a.translate(instanceList=('Graphene'+str(i), ), vector=(x[i], y[i], z[i]))
    vacancy=vacancy+(a.instances['Graphene'+str(i)], )

a1 = mdb.models['Model-1'].rootAssembly
i1 = a1.instances['Matrix-1']
leaf = dgm.LeafFromInstance((i1, ))
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanCut(name='NC2',instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Matrix-1'], 
cuttingInstances=(vacancy), 
originalInstances=SUPPRESS)
for i in range(num):
    a1 = mdb.models['Model-1'].rootAssembly
    a1.features['Graphene'+str(i)].resume()

#:----------------   End of Assemblies of the Graphene  ------------------------------

#:----------------   Merging the Graphene with Matrix   ------------------------------

for i in range(num):
    merg=merg+(a.instances['Graphene'+str(i)], )

a1 = mdb.models['Model-1'].rootAssembly
a1.InstanceFromBooleanMerge(name='NCT', instances=(merg),keepIntersections=ON, originalInstances=DELETE, domain=GEOMETRY)
a1 = mdb.models['Model-1'].rootAssembly

a = mdb.models['Model-1'].rootAssembly
del a.features['Matrix-1']

#:----------------   End of Merging the Graphene with Matrix   ------------------------

#:----------------   Job Defination ---------------------------------------------------
 
mdb.Job(name='TBC', model='Model-1', description='', type=ANALYSIS, atTime=None, 
    waitMinutes=0, waitHours=0, queue=None, memory=99, memoryUnits=PERCENTAGE, 
    getMemoryFromAnalysis=True, explicitPrecision=SINGLE, 
    nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
    contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
    multiprocessingMode=DEFAULT, numCpus=1, numDomains=1)
 
#:---------------   End of Job Defination  -------------------------------------------- 

#:---------------  Cutting The Redundant PParticles -----------------------------------

p = mdb.models['Model-1'].parts['NCT']
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
p = mdb.models['Model-1'].parts['NCT']
p.DatumAxisByPrincipalAxis(principalAxis=XAXIS)
p = mdb.models['Model-1'].parts['NCT']
d2 = p.datums
t = p.MakeSketchTransform(sketchPlane=d2[3], sketchUpEdge=d2[4], 
        sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0.0, 
        0.0, 0.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=323.45, gridSpacing=8.08, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['NCT']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.rectangle(point1=(0.0, 0.0), point2=(Uclx, -Uclx))
s.rectangle(point1=(-2*Uclx, -2*Uclx), point2=(3*Uclx, 3*Uclx))
p = mdb.models['Model-1'].parts['NCT']
d1 = p.datums
p.CutExtrude(sketchPlane=d1[3], sketchUpEdge=d1[4], sketchPlaneSide=SIDE1, 
        sketchOrientation=BOTTOM, sketch=s, flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']


p = mdb.models['Model-1'].parts['NCT']
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
p = mdb.models['Model-1'].parts['NCT']
p.DatumAxisByPrincipalAxis(principalAxis=XAXIS)
p = mdb.models['Model-1'].parts['NCT']
d2 = p.datums
t = p.MakeSketchTransform(sketchPlane=d2[3], sketchUpEdge=d2[4], 
        sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0.0, 
        0.0, 0.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=323.45, gridSpacing=8.08, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['NCT']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.rectangle(point1=(0.0, 0.0), point2=(Uclx, -Uclx))
s.rectangle(point1=(-2*Uclx, -2*Uclx), point2=(3*Uclx, 3*Uclx))
p = mdb.models['Model-1'].parts['NCT']
d1 = p.datums
p.CutExtrude(sketchPlane=d1[3], sketchUpEdge=d1[4], sketchPlaneSide=SIDE1, 
        sketchOrientation=BOTTOM, sketch=s, flipExtrudeDirection=OFF)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']


p = mdb.models['Model-1'].parts['NCT']
p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=Uclx)

p = mdb.models['Model-1'].parts['NCT']
d2 = p.datums
t = p.MakeSketchTransform(sketchPlane=d2[9], sketchUpEdge=d2[7], 
sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0.0, 0.0, 
        148.464))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=702.45, gridSpacing=17.56, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['NCT']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
s1.rectangle(point1=(0.0, 0.0), point2=(Uclx, Uclx))
s1.rectangle(point1=(-2*Uclx, -2*Uclx), point2=(3*Uclx, 3*Uclx))
p = mdb.models['Model-1'].parts['NCT']
d1 = p.datums
p.CutExtrude(sketchPlane=d1[9], sketchUpEdge=d1[7], sketchPlaneSide=SIDE1, 
        sketchOrientation=BOTTOM, sketch=s1, flipExtrudeDirection=OFF)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']


#:------------ End of Cutting The Redundant PParticles --------------------------


#:---------------  Thermal boundary conductance definition -----------------------------------

mdb.models['Model-1'].ContactProperty('IntProp-1')
mdb.models['Model-1'].interactionProperties['IntProp-1'].ThermalConductance(definition=TABULAR, clearanceDependency=ON, pressureDependency=OFF, 
temperatureDependencyC=OFF, massFlowRateDependencyC=OFF, dependenciesC=0, clearanceDepTable=((0.03, 0.0), (0.0, 0.1)))


#:---------------  Creating the Support Parts --------------------------
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=2000.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(point1=(0.0, 0.0), point2=(Uclx, Uclx))
p = mdb.models['Model-1'].Part(name='Support', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Support']
p.BaseSolidExtrude(sketch=s1, depth=Uclx/50)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Support']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

    
mdb.models['Model-1'].Material(name='Support')
mdb.models['Model-1'].materials['Support'].Elastic(table=((10000000.0, 0.2), ))
mdb.models['Model-1'].materials['Support'].Conductivity(table=((10000000.0, ), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Support', material='Support', thickness=None)
p = mdb.models['Model-1'].parts['Support']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(cells=cells)
p = mdb.models['Model-1'].parts['Support']
p.SectionAssignment(region=region, sectionName='Support', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)


#:------------ End of Creating the Support Parts -----------------------

#:-----------  Step and LOAD Defination -------------------------

mdb.models['Model-1'].HeatTransferStep(name='TC', previous='Initial', response=STEADY_STATE, maxNumInc=100000, amplitude=RAMP)

a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['NCT-1'].faces
side1Faces1 = s1.findAt(((1,Uclx/2,0.0),))
region = regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-1'].SurfaceHeatFlux(name='HOT', createStepName='TC', 
        region=region, magnitude=1.0)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['NC2-1'].faces
side1Faces1 = s1.findAt(((Uclx/2,Uclx/2,Uclx),))
region = regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-1'].SurfaceHeatFlux(name='COLD', createStepName='TC', 
        region=region, magnitude=-1.0)

a1 = mdb.models['Model-1'].rootAssembly
a1.makeIndependent(instances=(a1.instances['NCT-1'], ))
a1 = mdb.models['Model-1'].rootAssembly
a1.makeIndependent(instances=(a1.instances['NC2-1'], ))
#:-----------  Step and LOAD Defination -------------------------


#:---------------  Support Z --------------------------

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Support']
a.Instance(name='SupportZ-1', part=p, dependent=ON)
p1 = a.instances['SupportZ-1']
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('SupportZ-1', ), vector=(0.0, 0.0, Uclx))

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Support']
a.Instance(name='SupportZ-2', part=p, dependent=ON)
p1 = a.instances['SupportZ-2']
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('SupportZ-2', ), vector=(0.0, 0.0, -Uclx/50))


#:---------------  Support X --------------------------

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Support']
a.Instance(name='SupportX-1', part=p, dependent=ON)

p1 = a.instances['SupportX-1']
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('SupportX-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, -1.0, 0.0), angle=90.0)
a.translate(instanceList=('SupportX-1', ), vector=(-Uclx/50, 0.0, 0.0))


a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Support']
a.Instance(name='SupportX-2', part=p, dependent=ON)
p1 = a.instances['SupportX-2']
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('SupportX-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, -1.0, 0.0), angle=90.0)
a.translate(instanceList=('SupportX-1', ), vector=(Uclz+2*Uclx/50, 0.0, 0.0))

#:---------------  Support Y --------------------------

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Support']
a.Instance(name='SupportY-1', part=p, dependent=ON)

p1 = a.instances['SupportY-1']
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('SupportY-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(1.0, 0.0, 0.0), angle=90.0)
a.translate(instanceList=('SupportY-1', ), vector=(0.0, -Uclx/50, 0.0))


a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Support']
a.Instance(name='SupportY-2', part=p, dependent=ON)
p1 = a.instances['SupportY-2']
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('SupportY-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(1.0, 0.0, 0.0), angle=90.0)
a.translate(instanceList=('SupportY-1', ), vector=(0.0, Uclz+2*Uclx/50, 0.0))