####################################################################
# Python Open Dynamics Engine Wrapper
#
# Copyright (C) 2003, Matthias Baas (baas@ira.uka.de)
#
# You may distribute under the terms of the BSD license, as
# specified in the files license*.txt.
# -------------------------------------------------------------
# Open Dynamics Engine
# Copyright (c) 2001-2003, Russell L. Smith.
# All rights reserved. 
####################################################################

include "declarations.pyx"

# The World should keep a reference to joints/bodies, so that they won't
# be deleted.

"""Python Open Dynamics Engine (ODE) wrapper.

This module contains classes and functions that wrap the functionality
of the Open Dynamics Engine (ODE) which can be found at 
http://opende.sourceforge.net.

There are the following classes and functions:

- World
- Body
- JointGroup
- Contact
- Space
- Mass

Joint classes:

- BallJoint
- HingeJoint
- Hinge2Joint
- SliderJoint
- UniversalJoint
- FixedJoint
- ContactJoint

Geom classes:

- GeomSphere
- GeomBox
- GeomPlane
- GeomCCylinder
- GeomRay
- GeomTransform

Functions:

- CloseODE()
- collide()

"""

############################# Constants ###############################

paramLoStop        = 0
paramHiStop        = 1
paramVel           = 2
paramFMax          = 3
paramFudgeFactor   = 4
paramBounce        = 5
paramCFM           = 6
paramStopERP       = 7
paramStopCFM       = 8
paramSuspensionERP = 9
paramSuspensionCFM = 10

ParamLoStop        = 0
ParamHiStop        = 1
ParamVel           = 2
ParamFMax          = 3
ParamFudgeFactor   = 4
ParamBounce        = 5
ParamCFM           = 6
ParamStopERP       = 7
ParamStopCFM       = 8
ParamSuspensionERP = 9
ParamSuspensionCFM = 10

ParamLoStop2        = 256+0
ParamHiStop2        = 256+1
ParamVel2           = 256+2
ParamFMax2          = 256+3
ParamFudgeFactor2   = 256+4
ParamBounce2        = 256+5
ParamCFM2           = 256+6
ParamStopERP2       = 256+7
ParamStopCFM2       = 256+8
ParamSuspensionERP2 = 256+9
ParamSuspensionCFM2 = 256+10

ContactMu2	= 0x001
ContactFDir1	= 0x002
ContactBounce	= 0x004
ContactSoftERP	= 0x008
ContactSoftCFM	= 0x010
ContactMotion1	= 0x020
ContactMotion2	= 0x040
ContactSlip1	= 0x080
ContactSlip2	= 0x100

ContactApprox0 = 0x0000
ContactApprox1_1	= 0x1000
ContactApprox1_2	= 0x2000
ContactApprox1	= 0x3000

Infinity = dInfinity

######################################################################

# Lookup table for geom objects: C ptr -> Python object
_geom_c2py_lut = {}

# Mass 
include "mass.pyx"

# Contact
include "contact.pyx"

# World
include "world.pyx"

# Body
include "body.pyx"

# Joint classes
include "joints.pyx"

# Space
include "space.pyx"

# Geom classes
include "geoms.pyx"

    
def collide(geom1, geom2):
    """Generate contact information for two objects.

    Given two geometry objects that potentially touch (geom1 and geom2),
    generate contact information for them. Internally, this just calls
    the correct class-specific collision functions for geom1 and geom2.

    [flags specifies how contacts should be generated if the objects
    touch. Currently the lower 16 bits of flags specifies the maximum
    number of contact points to generate. If this number is zero, this
    function just pretends that it is one - in other words you can not
    ask for zero contacts. All other bits in flags must be zero. In
    the future the other bits may be used to select other contact
    generation strategies.]

    If the objects touch, this returns a list of Contact objects,
    otherwise it returns an empty list.
    """
    
    cdef dContactGeom c[10]
    cdef long id1
    cdef long id2
    cdef int i, n
    cdef Contact cont

    id1 = geom1._id()
    id2 = geom2._id()

    n = dCollide(<dGeomID>id1, <dGeomID>id2, 10, c, sizeof(dContactGeom))
    res = []
    i=0
    while i<n:
        cont = Contact()
        cont._contact.geom = c[i]
        res.append(cont)
        i=i+1

    return res

def CloseODE():
    dCloseODE()

######################################################################

environment = Body(None)