# XODE Importer for PyODE
# Copyright (C) 2004 Timothy Stranex

"""
XODE Geom Parser
@author: U{Timothy Stranex<mailto:timothy@stranex.com>}
"""

import ode
import errors, node, joint, body, transform

class Geom(node.TreeNode):
    """
    Represents an C{ode.Geom} object and corresponds to the <geom> tag.
    """

    def __init__(self, name, parent):
        node.TreeNode.__init__(self, name, parent)

        self._space = self.getFirstAncestor(ode.Space).getODEObject()
        self._transformed = False
        
        try:
            self._body = self.getFirstAncestor(ode.Body)
        except node.AncestorNotFoundError:
            self._body = None

    def takeParser(self, parser):
        """
        Handle further parsing. It should be called immediately after the <geom>
        tag has been encountered.
        """

        self._parser = parser
        self._parser.push(startElement=self._startElement,
                          endElement=self._endElement)

    def _startElement(self, name, attrs):
        nodeName = attrs.get('name', None)
        
        if (name == 'transform'):
            t = transform.Transform()
            t.takeParser(self._parser, self, attrs)
            self._transformed = True
        elif (name == 'box'):
            self._parseGeomBox(attrs)
        elif (name == 'cappedCylinder'):
            self._parseGeomCCylinder(attrs)
        elif (name == 'cone'):
            raise NotImplementedError()
        elif (name == 'cylinder'):
            raise NotImplementedError()
        elif (name == 'plane'):
            self._parseGeomPlane(attrs)
        elif (name == 'ray'):
            self._parseGeomRay(attrs)
        elif (name == 'sphere'):
            self._parseGeomSphere(attrs)
        elif (name == 'trimesh'):
            raise NotImplementedError()
        elif (name == 'geom'):
            g = Geom(nodeName, self)
            g.takeParser(self._parser)
        elif (name == 'body'):
            b = body.Body(nodeName, self, attrs)
            b.takeParser(self._parser)
        elif (name == 'joint'):
            j = joint.Joint(nodename, self)
            j.takeParser(self._parser)
        elif (name == 'jointgroup'):
            pass
        elif (name == 'ext'):
            pass
        else:
            raise errors.ChildError('geom', name)

    def _endElement(self, name):
        if (name == 'geom'):
            obj = self.getODEObject()
            
            if (obj is None):
                raise errors.InvalidError('No geom type element found.')

            if (not obj.placeable()):
                # Non-placeable geoms cannot be attached to bodies or be
                # transformed
                self._parser.pop()
                return

            if (self._body is None):
                # The Geom is independant so it can have its own transform
                
                t = self.getTransform()
                obj.setPosition(t.getPosition())
                obj.setRotation(t.getRotation())
            elif (self._transformed):
                # The Geom is attached to a body so to transform it, it must
                # by placed in a GeomTransform and its transform is relative
                # to the body.

                t = self.getTransform(self._body)
                obj.setPosition(t.getPosition())
                obj.setRotation(t.getRotation())
                
                trans = ode.GeomTransform(self._space)
                trans.setGeom(obj)
                trans.setBody(self._body.getODEObject())
                
                self.setODEObject(trans)
            else:
                obj.setBody(self._body.getODEObject())
            
            self._parser.pop()

    def _parseGeomBox(self, attrs):
        def start(name, attrs):
            if (name == 'ext'):
                pass
            else:
                raise errors.ChildError('box', name)

        def end(name):
            if (name == 'box'):
                self._parser.pop()

        lx = float(attrs['sizex'])
        ly = float(attrs['sizey'])
        lz = float(attrs['sizez'])

        self.setODEObject(ode.GeomBox(self._space, (lx, ly, lz)))
        self._parser.push(startElement=start, endElement=end)

    def _parseGeomCCylinder(self, attrs):
        def start(name, attrs):
            if (name == 'ext'):
                pass
            else:
                raise errors.ChildError('cappedCylinder', name)

        def end(name):
            if (name == 'cappedCylinder'):
                self._parser.pop()

        radius = float(attrs['radius'])
        length = float(attrs['length'])

        self.setODEObject(ode.GeomCCylinder(self._space, radius, length))
        self._parser.push(startElement=start, endElement=end)

    def _parseGeomSphere(self, attrs):
        def start(name, attrs):
            if (name == 'ext'):
                pass
            else:
                raise errors.ChildError('sphere', name)

        def end(name):
            if (name == 'sphere'):
                self._parser.pop()

        radius = float(attrs['radius'])

        self.setODEObject(ode.GeomSphere(self._space, radius))
        self._parser.push(startElement=start, endElement=end)

    def _parseGeomPlane(self, attrs):
        def start(name, attrs):
            if (name == 'ext'):
                pass
            else:
                raise errors.ChildError('plane', name)

        def end(name):
            if (name == 'plane'):
                self._parser.pop()

        a = float(attrs['a'])
        b = float(attrs['b'])
        c = float(attrs['c'])
        d = float(attrs['d'])

        self.setODEObject(ode.GeomPlane(self._space, (a, b, c), d))
        self._parser.push(startElement=start, endElement=end)

    def _parseGeomRay(self, attrs):
        def start(name, attrs):
            if (name == 'ext'):
                pass
            else:
                raise errors.ChildError('ray', name)

        def end(name):
            if (name == 'ray'):
                self._parser.pop()

        length = float(attrs['length'])

        self.setODEObject(ode.GeomRay(self._space, length))
        self._parser.push(startElement=start, endElement=end)