#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 17:12:27 2018

@author: egissi
"""

import math
import array
import textwrap

EPSILON = 1e-6  # FIXME different EPSILON for different applications


class Vector(object):
    def __init__(self, *args):  # FIXME simplify
        self.x, self.y, self.z = 0., 0., 0.
        if len(args) == 3:  # Vector(1,2,3)
            self.x, self.y, self.z = args[0], args[1], args[2]
        elif len(args) == 1:  # Vector([1,2,3])
            a = args[0]
            if isinstance(a, dict):
                self.x, self.y, self.z = \
                    a.get('x', 0.0), a.get('y', 0.0), a.get('z', 0.0)
            elif a is not None and len(a) == 3:
                self.x, self.y, self.z = a[0], a[1], a[2]

    def __repr__(self):
        return 'Vector({0:.3f}, {1:.3f}, {2:.3f})'.format(
                self.x, self.y, self.z
                )

    def clone(self):
        return Vector(self.x, self.y, self.z)

    def negated(self):
        return Vector(-self.x, -self.y, -self.z)

    def __neg__(self):
        return self.negated()

    def plus(self, a):
        return Vector(self.x+a.x, self.y+a.y, self.z+a.z)

    def __add__(self, a):
        return self.plus(a)

    def minus(self, a):
        return Vector(self.x-a.x, self.y-a.y, self.z-a.z)

    def __sub__(self, a):
        return self.minus(a)

    def times(self, a):
        return Vector(self.x*a, self.y*a, self.z*a)

    def __mul__(self, a):
        return self.times(a)

    def dividedBy(self, a):
        return Vector(self.x/a, self.y/a, self.z/a)

    def __truediv__(self, a):
        return self.dividedBy(float(a))

    def __div__(self, a):
        return self.dividedBy(float(a))

    def dot(self, a):
        return self.x*a.x + self.y*a.y + self.z*a.z

    def lerp(self, a, t):
        """
        Linear interpolation from self to a.
        >>> Vector(0,0,1).lerp(Vector(10,0,1),.7)
        Vector(7.000, 0.000, 1.000)
        """
        return self.plus(a.minus(self).times(t))

    def length(self):
        return math.sqrt(self.dot(self))

    def unit(self):
        return self.dividedBy(self.length())

    def cross(self, a):
        return Vector(
            self.y * a.z - self.z * a.y,
            self.z * a.x - self.x * a.z,
            self.x * a.y - self.y * a.x,
            )

    def __getitem__(self, key):
        return (self.x, self.y, self.z)[key]

    def __setitem__(self, key, value):
        ll = [self.x, self.y, self.z]
        ll[key] = value
        self.x, self.y, self.z = ll

    def __len__(self):
        return 3

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return \
            math.isclose(self.x, other.x, rel_tol=EPSILON) and \
            math.isclose(self.y, other.y, rel_tol=EPSILON) and \
            math.isclose(self.z, other.z, rel_tol=EPSILON)

    def is_zero(self):
        return \
            math.isclose(self.x, 0., rel_tol=EPSILON) and \
            math.isclose(self.y, 0., rel_tol=EPSILON) and \
            math.isclose(self.z, 0., rel_tol=EPSILON)

    def is_collinear(self, b, c):
        """
        Return true if self, b, and c all lie on the same line.
        >>> a, b, c = Vector(0,0,0), Vector(1,0,0), Vector(2,0,0)
        >>> a.is_collinear(b, c)
        True
        >>> a, b, c = Vector(0,0,0), Vector(0,-1,0), Vector(0,-2,1)
        >>> a.is_collinear(b, c)
        False
        >>> a, b, c = Vector(0,0,0), Vector(0,0,0), Vector(0,0,0)
        >>> a.is_collinear(b, c)
        True
        """
        # Simpler
        return b.minus(self).cross(c.minus(self)).is_zero()
        # Proposed elsewhere, to correctly use epsilon FIXME
#        area_tri2 = abs((c-self).cross(b-self).length())
#        area_square = max(
#                (c-self).length() ** 2,
#                (b-self).length() ** 2,
#                (c-b).length() ** 2
#                )
#        if area_tri2 < EPSILON * area_square:
#            return True
#        return False


    def is_within(self, p, r):
        """
        Return true if q is between p and r (inclusive).
        >>> Vector(0,0,0).is_within(Vector(1,0,0), Vector(2,0,0))
        False
        >>> Vector(1.5,0,0).is_within(Vector(1,0,0), Vector(2,0,0))
        True
        """
        return (p.x <= self.x <= r.x or r.x <= self.x <= p.x) and \
               (p.y <= self.y <= r.y or r.y <= self.y <= p.y) and \
               (p.z <= self.z <= r.z or r.z <= self.z <= p.z)

    def is_strictly_within(self, p, r):
        """
        Return true if q is between p and r (exclusive).
        >>> Vector(1,0,0).is_within(Vector(1,0,0), Vector(2,0,0))
        True
        >>> Vector(1,0,0).is_strictly_within(Vector(1,0,0), Vector(2,0,0))
        False
        """
        return (p.x < self.x < r.x or r.x < self.x < p.x) and \
               (p.y < self.y < r.y or r.y < self.y < p.y) and \
               (p.z < self.z < r.z or r.z < self.z < p.z)


class Plane():
    def __init__(self, normal, distance):
        self.normal = Vector(normal).unit()
        self.distance = distance  # distance from (0, 0, 0)

    def __repr__(self):
        return 'Plane(normal={}, distance={})'.format(
                self.normal, self.distance
                )

    def clone(self):
        return Plane(self.normal.clone(), self.distance)

    @classmethod
    def from_points(cls, points):
        """
        Get a Plane from a list of points, after checking for collinearity.
        If collinear, return a None.
        >>> Plane.from_points(((0,0,0,),(1,0,0),(2,0,0),(3,0,1)))
        Plane(normal=Vector(0.000, -1.000, 0.000), distance=0)
        >>> Plane.from_points(((0,0,0,),(1,0,0),(2,0,0),(3,0,0)))
        Traceback (most recent call last):
        ...
        Exception: ('Plane.from_points(): Could not find a plane, points:', ((0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)))
        """
        len_points = len(points)
        for i, a in enumerate(points):
            a = Vector(a)
            b = Vector(points[(i + 1) % len_points])
            c = Vector(points[(i + 2) % len_points])
            normal = b.minus(a).cross(c.minus(a))
            if not normal.is_zero():
                return Plane(normal.unit(), normal.dot(a))
        raise Exception('Plane.from_points(): Could not find a plane, points:', points)

    def flip(self):
        """
        Flip self normal.
        >>> p = Plane(normal=(1,0,0), distance=5); p.flip() ; p
        Plane(normal=Vector(-1.000, -0.000, -0.000), distance=-5)
        """
        self.normal = -self.normal
        self.distance = -self.distance


class Geom():
    """
    Representation of a polygonal geometry
    """
    def __init__(self, verts=None, polygons=None, hid=None):
        self.hid = hid  # Geom name
        if verts is None:
            verts = ()
        if polygons is None:
            polygons = ((), )
        try:
            # Array of vertices coordinates, eg. [1.,2.,3., 2.,3.,4., ...]
            self.verts = array.array('f', verts)
            # List of list of polygon connectivities, eg. [[0,1,2,4], ...]
            self.polygons = [list(p[:]) for p in polygons]
        except TypeError:
            raise Exception('Geom.__init__(): Bad Geom(), hid:', hid)

    def __repr__(self):
        """
        >>> Geom((1.,2.,3., 1.,2.,3.,), ((1,2,3),(1,2,3,4),(1,2,3,4,5),), )
        Geom(
            (1.000,2.000,3.000,  1.000,2.000,3.000),
            [[1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]],
            )
        """
        strverts = ('{:.3f}'.format(v) for v in self.verts)
        strverts = list(zip(*[iter(strverts)] * 3))  # Join: ((1.,2.,3.,), ...)
        strverts = ',  '.join((','.join(v) for v in strverts))
        return 'Geom(\n    ({}),\n    {},\n    )'.format(
                strverts, self.polygons,
                )

    def clone(self):
        return Geom(
                verts=self.verts[:],
                polygons=[p[:] for p in self.polygons],
                )

    def append(self, geom):
        """
        Append other geom to self.
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> h = Geom((-1,-1,2, 1,-1,2, 0,1,2, 0,0,1), \
                     ((0,1,2), (3,1,0), (3,2,1), (3,0,2)) )  # but upside-down
        >>> g.append(h); g
        [0, 1, 2, 3, 4, 5, 6, 7]
        Geom(
            (-1.000,-1.000,0.000,  1.000,-1.000,0.000,  0.000,1.000,0.000,  0.000,0.000,1.000,  -1.000,-1.000,2.000,  1.000,-1.000,2.000,  0.000,1.000,2.000),
            [[2, 1, 0], [0, 1, 3], [1, 2, 3], [2, 0, 3], [4, 5, 6], [3, 5, 4], [3, 6, 5], [3, 4, 6]],
            )
        """
        # Extend verts
        original_nverts = self.get_nverts()
        self.verts.extend(geom.verts)
        # Extend polygons
        original_npolygons = self.get_npolygons()
        self.polygons.extend(geom.polygons)
        # Relink polygons to new iverts
        for i, polygon in enumerate(self.polygons[original_npolygons:]):
            for j, _ in enumerate(polygon):
                polygon[j] += original_nverts
        # Merge duplicate verts
        self.merge_duplicated_verts()
        return self.get_ipolygons()

    def flip(self):
        """
        Flip self polygons normals.
        >>> g = Geom((), ((1,2,3),(1,2,3,4),(1,2,3,4,5),), ); g.flip(); g
        Geom(
            (),
            [[3, 2, 1], [4, 3, 2, 1], [5, 4, 3, 2, 1]],
            )
        """
        for p in self.polygons:
            p.reverse()

    def get_polygon(self, ipolygon):
        """
        Get ipolygon connectivity.
        >>> g = Geom((), ((1,2,3),(1,2,3,4),(1,2,3,4,5),), ); g.get_polygon(1)
        [1, 2, 3, 4]
        """
        return self.polygons[ipolygon]

    def get_polygon_verts(self, ipolygon):
        """
        Get ipolygon verts.
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.get_polygon_verts(0)
        [Vector(0.000, 1.000, 0.000), Vector(1.000, -1.000, 0.000), Vector(-1.000, -1.000, 0.000)]
        """
        return [self.get_vert(ivert) for ivert in self.get_polygon(ipolygon)]

    def update_polygon(self, ipolygon, polygon):
        """
        Update ipolygon connectivity.
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.update_polygon(0, (0,0,0)); g.get_polygon(0)
        0
        [0, 0, 0]
        """
        self.polygons[ipolygon] = list(polygon)
        return ipolygon

    def append_polygon(self, polygon):
        """
        Append a polygon.
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.append_polygon((0,0,0)); g.get_polygon(4)
        4
        [0, 0, 0]
        """
        self.polygons.append(list(polygon))
        ipolygon = self.get_npolygons() - 1
        return ipolygon

    def get_npolygons(self):
        """
        Get the len of polygons
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.get_npolygons()
        4
        """
        return len(self.polygons)

    def get_ipolygons(self):
        """
        Get the list of ipolygon
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.get_ipolygons()
        [0, 1, 2, 3]
        """
        return list(range(len(self.polygons)))

    def get_plane_of_polygon(self, ipolygon):
        """
        Get plane containing ipolygon.
        >>> g = Geom((0,0,1, 1,0,1, 2,0,1, 0,1,1,), ((0,1,2,3), ))
        >>> g.get_plane_of_polygon(0)
        Plane(normal=Vector(0.000, -0.000, 1.000), distance=1.0)
        """
        return Plane.from_points(self.get_polygon_verts(ipolygon))

    def split_polygon(self, ipolygon, plane, coplanar_front,
                      coplanar_back, front, back):
        """
        Split ipolygon by a plane. Put the fragments in the inline lists.
        Add cut_ivert to bordering polygons.
        >>> g = Geom((-1,-1,0, 1,-1,0, 1,1,0, -1,1,0, -3, 1,0, -3,-1,0, \
                       3,-1,0, 3, 1,0, 1,3,0, -1,3,0, -1,-3,0,  1,-3,0),\
                     ((0,1,2,3), (5,0,3,4), (1,6,7,2), (3,2,8,9), (10,11,1,0))\
                    )  # Open clover on z=0, n=+k
        >>> h = g.clone()
        >>> #  y ↑
        >>> #   9─8
        >>> #   │ │
        >>> # 4─3─2─7
        >>> # │ │∙│ │→ x
        >>> # 5─0─1─6
        >>> #   │ │
        >>> #  10-11
        >>> coplanar_front, coplanar_back, front, back = [], [], [], []
        >>> g.split_polygon(0, Plane((1,0,0),0), \
                            coplanar_front, coplanar_back, front, back)
        >>> coplanar_front, coplanar_back, front, back
        ([], [], [0], [5])
        >>> g
        Geom(
            (-1.000,-1.000,0.000,  1.000,-1.000,0.000,  1.000,1.000,0.000,  -1.000,1.000,0.000,  -3.000,1.000,0.000,  -3.000,-1.000,0.000,  3.000,-1.000,0.000,  3.000,1.000,0.000,  1.000,3.000,0.000,  -1.000,3.000,0.000,  -1.000,-3.000,0.000,  1.000,-3.000,0.000,  0.000,-1.000,0.000,  0.000,1.000,0.000),
            [[12, 1, 2, 13], [5, 0, 3, 4], [1, 6, 7, 2], [3, 13, 2, 8, 9], [10, 11, 1, 12, 0], [0, 12, 13, 3]],
            )
        >>> coplanar_front, coplanar_back, front, back = [], [], [], []
        >>> h.split_polygon(0, Plane((0,1,0),0), \
                            coplanar_front, coplanar_back, front, back)
        >>> coplanar_front, coplanar_back, front, back
        ([], [], [0], [5])
        >>> h
        Geom(
            (-1.000,-1.000,0.000,  1.000,-1.000,0.000,  1.000,1.000,0.000,  -1.000,1.000,0.000,  -3.000,1.000,0.000,  -3.000,-1.000,0.000,  3.000,-1.000,0.000,  3.000,1.000,0.000,  1.000,3.000,0.000,  -1.000,3.000,0.000,  -1.000,-3.000,0.000,  1.000,-3.000,0.000,  1.000,0.000,0.000,  -1.000,0.000,0.000),
            [[12, 2, 3, 13], [5, 0, 13, 3, 4], [1, 6, 7, 2, 12], [3, 2, 8, 9], [10, 11, 1, 0], [0, 1, 12, 13]],
            )
        >>> coplanar_front, coplanar_back, front, back = [], [], [], []
        >>> g.split_polygon(0, Plane((0,0,1),0), \
                            coplanar_front, coplanar_back, front, back)
        >>> coplanar_front, coplanar_back, front, back
        ([0], [], [], [])
        >>> coplanar_front, coplanar_back, front, back = [], [], [], []
        >>> g.split_polygon(0, Plane((0,0,-1),0), \
                            coplanar_front, coplanar_back, front, back)
        >>> coplanar_front, coplanar_back, front, back
        ([], [0], [], [])
        """
        # Init
        COPLANAR = 0  # vertex of polygon within EPSILON distance from plane
        FRONT = 1     # vertex of polygon in front of the plane
        BACK = 2      # vertex of polygon at the back of the plane
        SPANNING = 3  # spanning polygon

        polygon = self.get_polygon(ipolygon)
        polygon_type = 0
        ivert_types = []
        polygon_nverts = len(polygon)

        # The edges to be split,
        # eg. {(2,3): 1} with {(ivert0,ivert1): cut_ivert, ...}
        # The opposite of the split edge is sent for easier search
        spl_edges = {}

        # Calc the distance between the ivert and the splitting plane
        # then classify the ivert, and update classification of the face
        for ivert in polygon:
            # Classify ivert using vert-plane distance
            distance = plane.normal.dot(self.get_vert(ivert)) - plane.distance
            ivert_type = -1
            if distance < -EPSILON * plane.distance:  # FIXME
                ivert_type = BACK
            elif distance > EPSILON * plane.distance:  # FIXME
                ivert_type = FRONT
            else:
                ivert_type = COPLANAR
            # Register ivert classification
            ivert_types.append(ivert_type)
            # Update polygon classification
            polygon_type |= ivert_type

        # Put the polygon in the correct list
        if polygon_type == COPLANAR:
            # Same or opposite normal?
            polygon_normal = self.get_plane_of_polygon(ipolygon).normal
            if plane.normal.dot(polygon_normal) > 0:
                coplanar_front.append(ipolygon)
            else:
                coplanar_back.append(ipolygon)
        elif polygon_type == FRONT:
            front.append(ipolygon)
        elif polygon_type == BACK:
            back.append(ipolygon)
        elif polygon_type == SPANNING:
            front_iverts = []
            back_iverts = []
            for i, ivert0 in enumerate(polygon):
                # Get the edge ivert0-ivert1
                j = (i+1) % polygon_nverts
                ivert1 = polygon[j]
                ivert0_type = ivert_types[i]
                ivert1_type = ivert_types[j]
                # Put ivert0 in the right lists
                # to build the new edge
                if ivert0_type != BACK:
                    front_iverts.append(ivert0)
                if ivert0_type != FRONT:
                    if ivert0_type != BACK:
                        back_iverts.append(ivert0)
                    else:
                        back_iverts.append(ivert0)
                if (ivert0_type | ivert1_type) == SPANNING:
                    # The edge is spanning, calc new vert
                    vert0 = self.get_vert(ivert0)
                    vert1 = self.get_vert(ivert1)
                    t = (plane.distance - plane.normal.dot(vert0)) \
                        / plane.normal.dot(vert1 - vert0)
                    cut_vert = vert0.lerp(vert1, t)
                    cut_ivert = self.append_vert(cut_vert)
                    # Register the split for domino to bordering polygons
                    spl_edges[(ivert1, ivert0)] = cut_ivert
                    # Append the new_vert to the right list
                    front_iverts.append(cut_ivert)
                    back_iverts.append(cut_ivert)

            # Update and append new polygons
            updated = False
            if len(front_iverts) >= 3:
                updated = True
                ipolygon = self.update_polygon(ipolygon, front_iverts)
                front.append(ipolygon)
            if len(back_iverts) >= 3:
                if updated:
                    ipolygon = self.append_polygon(back_iverts)
                else:
                    updated = True
                    ipolygon = self.update_polygon(ipolygon, back_iverts)
                back.append(ipolygon)

            # Add cut_vert to bordering polygons
            halfedges = self.get_halfedges()
            for spl_edge, cut_ivert in spl_edges.items():
                # Get the bordering polygon that is split by cut_ivert
                spl_ipolygon = halfedges.get(spl_edge, None)
                if spl_ipolygon is None:  # there is a border
                    continue
                # Calc and update the bordering polygon
                spl_polygon = self.get_polygon(spl_ipolygon)
                i = spl_polygon.index(spl_edge[0])  # find right edge
                spl_polygon.insert(i+1, cut_ivert)  # inject cut_ivert
                self.update_polygon(spl_ipolygon, spl_polygon)

    def get_vert(self, ivert):
        """
        Get ivert vert
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.get_vert(2)
        Vector(0.000, 1.000, 0.000)
        """
        return Vector(self.verts[3*ivert:3*ivert+3])

    def append_vert(self, vert):
        """
        Append a vert to the Geom, return its index.
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.append_vert((0,0,0))
        4
        """
        self.verts.extend(list(vert))
        return self.get_nverts()-1

    def get_nverts(self):
        """
        Get the len of vertices
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.get_nverts()
        4
        """
        return int(len(self.verts)/3)

    def get_iverts(self):
        """
        Get the range for verts
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.get_iverts()
        [0, 1, 2, 3]
        """
        return [i for i in range(int(len(self.verts)/3))]

    def merge_duplicated_verts(self):
        """
        Remove dup verts, and relink all polygons. No mod of polygons.
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1, 0,1,0, 0,1,0, 1,-1,0, 1,-1,0,), \
                     ((2,6,0), (0,1,3), (7,4,3), (5,0,3)) )  # Dup verts, 8>4
        >>> g.merge_duplicated_verts(); g
        Geom(
            (-1.000,-1.000,0.000,  1.000,-1.000,0.000,  0.000,1.000,0.000,  0.000,0.000,1.000),
            [[2, 1, 0], [0, 1, 3], [1, 2, 3], [2, 0, 3]],
            )
        """
        # Find unique verts and build ivert_to_ivert dict
        unique_pyverts = []
        ivert_to_ivert = {}
        nverts = self.get_nverts()
        for ivert in range(nverts):
            vert = self.get_vert(ivert)
            seen = False
            for i, selected_pyvert in enumerate(unique_pyverts):
                if (selected_pyvert - vert).is_zero():
                    seen = True
                    ivert_to_ivert[ivert] = i
                    break
            if not seen:
                unique_pyverts.append(vert)
                ivert_to_ivert[ivert] = len(unique_pyverts) - 1
        # Update face ivert links
        for i, polygon in enumerate(self.polygons):
            self.update_polygon(
                    i, [ivert_to_ivert[ivert] for ivert in polygon]
                    )
        # Flatten unique_pyverts to build new self.verts
        verts = array.array('f')
        for pyvert in unique_pyverts:
            verts.extend(pyvert)
        self.verts = verts

    # Edges

    def get_halfedges(self, ipolygons=None):
        """
        Get halfedges dict of ipolygons subset.
        halfedges are: {(1,2):7]} with {(ivert0, ivert1): ipolygon on the left}
        according to iface0 normal up
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
        >>> g.get_halfedges(ipolygons=None)
        {(2, 1): 0, (1, 0): 0, (0, 2): 0, (0, 1): 1, (1, 3): 1, (3, 0): 1, (1, 2): 2, (2, 3): 2, (3, 1): 2, (2, 0): 3, (0, 3): 3, (3, 2): 3}
        >>> g.get_halfedges(ipolygons=(1,2,3))
        {(0, 1): 1, (1, 3): 1, (3, 0): 1, (1, 2): 2, (2, 3): 2, (3, 1): 2, (2, 0): 3, (0, 3): 3, (3, 2): 3}
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((2,1,0), (0,1,3), (1,2,3), (3,0,2)) )  # Unorient tet
        >>> g.get_halfedges()
        Traceback (most recent call last):
        ...
        Exception: ('Geom.get_halfedges(): Non-manifold or unorientable at ipolygon:', 3)
        """
        if ipolygons is None:
            ipolygons = self.get_ipolygons()
        halfedges = dict()
        for ipolygon in ipolygons:
            polygon = self.get_polygon(ipolygon)
            polygon_nverts = len(polygon)
            for i in range(polygon_nverts):
                halfedge = (polygon[i], polygon[(i+1) % polygon_nverts])
                if halfedge in halfedges:
                    raise Exception('Geom.get_halfedges(): Non-manifold or unorientable at ipolygon:', ipolygon)
                halfedges[halfedge] = ipolygon
        return halfedges

    def get_border_halfedges(self, ipolygons=None):
        """
        Get border halfedges dict
        Eg: {(1,2):7]} with {(ivert0, ivert1): iface on the left}
        according to iface0 normal up
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((0,1,3), (1,2,3), (2,0,3)) )  # Open tet
        >>> g.get_border_halfedges()
        {(2, 0): 2, (1, 2): 1, (0, 1): 0}
        """
        halfedges = self.get_halfedges(ipolygons)
        border_halfedges = {}
        while halfedges:
            halfedge, ipolygon = halfedges.popitem()
            opposite = halfedge[1], halfedge[0]
            if opposite in halfedges:
                del halfedges[opposite]
            else:
                border_halfedges[halfedge] = ipolygon
        return border_halfedges

    def _earclip_of_polygon(self, polygon, start):
        polygon_nverts = len(polygon)
        # Special cases
        if polygon_nverts == 3:
            polygon_nverts == 2
        elif polygon_nverts == 4:
            polygon_nverts == 3
        # Get the first good ear
        for i in range(polygon_nverts-1):
            ivert0 = polygon[(start+i) % polygon_nverts]
            ivert1 = polygon[(start+i+1) % polygon_nverts]
            ivert2 = polygon[(start+i+2) % polygon_nverts]
            a = self.get_vert(ivert0)
            b = self.get_vert(ivert1)
            c = self.get_vert(ivert2)
            b_a, c_b, c_a = b.minus(a), c.minus(b), c.minus(a)
            cross = b_a.cross(c_a)
            length = b_a.length() + c_b.length() + c_a.length()
            if cross.length() > 0.:
                del(polygon[(start+i+1) % polygon_nverts])
                return polygon, (ivert0, ivert1, ivert2), length
        return polygon, None, 0.

    def get_tris_of_polygon(self, ipolygon):
        """
        Triangulate ipolygon with no zero-area tris
        >>> g = Geom((0,0,0, 1,0,0, 2,0,0, 3,0,0, 1,1,0, 0,1,0), \
                     ((0,1,2,3,4,5), ))  # Polyhedra, 6 edges, 3 collinear
        >>> g.get_tris_of_polygon(ipolygon=0)
        [(5, 0, 1), (5, 1, 2), (5, 2, 3), [3, 4, 5]]
        >>> g = Geom((0,0,0, 1,0,0, 2,0,0, 3,0,0), \
                     ((0,1,2,3,), ))    # Zero area polyhedra
        >>> g.get_tris_of_polygon(ipolygon=0)
        Traceback (most recent call last):
        ...
        Exception: ('Geom.get_tris_of_polygon(): Triangulation impossible, polygon:', [0, 1, 2, 3])
        >>> g = Geom((0,0,0, 1,0,0, 1,0,0, 3,1,0), \
                     ((0,1,2,3,), ))    # Zero lenght edge polyhedra
        >>> g.get_tris_of_polygon(ipolygon=0)
        Traceback (most recent call last):
        ...
        Exception: ('Geom.get_tris_of_polygon(): Zero area or edge, ipolygon:', 0)
        >>> g = Geom((0,0,0, 1,0,0, 2,0,0, 3,0,0, 3,1,0, 3,2,0, 3,3,0), \
                     ((0,1,2,3,4,5,6), ))  # Polyhedra, 7 edges, alignments
        >>> g.get_tris_of_polygon(ipolygon=0)  # Alignments, should work
        Traceback (most recent call last):
        ...
        Exception: ('Geom.get_tris_of_polygon(): Triangulation impossible, polygon:', [3, 4, 5, 6])
        """
        polygon = self.get_polygon(ipolygon)[:]  # work on a copy
        # Short cut case
        polygon_nverts = len(polygon)
        if polygon_nverts == 3:
            return polygon[:]
        # Search for triangulation
        tris = []
        start = 0
        while len(polygon) > 2 and len(polygon) - 1 > start:
            polygon, tri, length = self._earclip_of_polygon(polygon, start)
            if tri:
                start = 0
                tris.append(tri)
            else:
                start += 1
        if tris:
            return tris
        raise Exception('Geom.get_tris_of_polygon(): Triangulation impossible, polygon:', polygon)

    # STL

    def to_STL(self, filename):
        """
        Write self to STL file
        >>> g = Geom((-1.0, -1.0, -1.0,  -1.0, -1.0, 1.0,  -1.0, 1.0,  1.0, \
                      -1.0,  1.0, -1.0,   1.0,  1.0, 1.0,   1.0, 1.0, -1.0,\
                       1.0, -1.0, -1.0,   1.0, -1.0, 1.0), \
                    ((0,1,2,3), (7,6,5,4), (1,7,4,2), \
                     (0,3,5,6), (1,0,6,7), (2,4,5,3)) )  # A good cube
        >>> g.to_STL('../test/doctest.stl')
        to_STL: ../test/doctest.stl
        >>> Geom.from_STL('../test/doctest.stl')
        Geom(
            (-1.000,1.000,-1.000,  -1.000,-1.000,-1.000,  -1.000,-1.000,1.000,  -1.000,1.000,1.000,  1.000,1.000,1.000,  1.000,-1.000,1.000,  1.000,-1.000,-1.000,  1.000,1.000,-1.000),
            [[0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7], [3, 2, 5], [3, 5, 4], [6, 1, 0], [6, 0, 7], [5, 2, 1], [5, 1, 6], [0, 3, 4], [0, 4, 7]],
            )
        """
        with open(filename, 'w') as f:
            f.write('solid name\n')
            for ipolygon in range(self.get_npolygons()):
                tris = self.get_tris_of_polygon(ipolygon)
                for tri in tris:
                    f.write('facet normal 0 0 0\n')
                    f.write(' outer loop\n')
                    for ivert in tri:
                        f.write('  vertex {v[0]:.9f} {v[1]:.9f} {v[2]:.9f}\n'.format(
                                v=self.get_vert(ivert)))
                    f.write(' endloop\n')
                    f.write('endfacet\n')
            f.write('endsolid name\n')
        print('to_STL:', filename)

    @classmethod
    def from_STL(cls, filename):
        """
        Get new Geom from STL file
        Doctest in Geom.to_STL()
        """
        # Get STL mesh
        from stl import mesh
        mesh = mesh.Mesh.from_file(filename)
        verts, polygons, py_verts = [], [], []
        for iface, p in enumerate(mesh.points):
            # p is [-1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0]
            verts.extend(p)
            polygons.append((3*iface, 3*iface+1, 3*iface+2))
            py_verts.append((p[0], p[1], p[2]))
            py_verts.append((p[3], p[4], p[5]))
            py_verts.append((p[6], p[7], p[8]))
        g = Geom(verts, polygons)
        g.merge_duplicated_verts()
        g.check_geom_sanity()
        return g

    # Geometry sanity

    def check_loose_verts(self):
        """
        Check loose vertices: vertices that have no connectivity
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1, 0,0,0), \
                     ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Loose vert
        >>> g.check_loose_verts()
        Traceback (most recent call last):
        ...
        Exception: Geom.check_loose_verts(): Invalid GEOM, loose verts.
        """
        nverts = self.get_nverts()
        npolygons = self.get_npolygons()
        used_iverts = []
        for ipolygon in range(npolygons):
            used_iverts.extend(self.get_polygon(ipolygon))
        used_iverts = set(used_iverts)
        if nverts != len(used_iverts) or nverts != max(used_iverts) + 1:
            raise Exception("Geom.check_loose_verts(): Invalid GEOM, loose verts.")

    def check_degenerate_geometry(self):
        for ipolygon in range(self.get_npolygons()):
            self.get_tris_of_polygon(ipolygon)

    def check_is_solid(self):
        """
        Check surface:
        - 2-manifold and closed, each edge should join two faces,
        - orientable, adjoining faces should have same normals
        >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                     ((0,1,3), (1,2,3), (2,0,3)) )  # Open tet
        >>> g.check_is_solid()
        Traceback (most recent call last):
        ...
        Exception: ('Geom.check_is_solid(): Non closed at ipolygons:', [2, 1, 0])
        """
        border_halfedges = self.get_border_halfedges()
        if border_halfedges:
            raise Exception("Geom.check_is_solid(): Non closed at ipolygons:",
                            [b for b in border_halfedges.values()])

#def check_euler(self):  # FIXME test
#    """
#    Euler formula: nverts - nedges + nfaces = chi
#    Euler characteristic chi of the connected sum of g tori is:
#    chi = 2 − 2g, with g genus
#    g = 0, 1, 2, 3, ... => chi = 2, 0, -2, -4, ...
#    """
#    nverts = get_nverts(igeom)
#    nfaces = get_nfaces(igeom)
#    # Count edges
#    nedges = 0
#    seen_halfedges = []
#    halfedges = get_halfedges(igeom, get_ifaces(igeom))
#    for halfedge in halfedges:
#        opposite = halfedge[1], halfedge[0]
#        if halfedge in seen_halfedges or opposite in seen_halfedges:
#            continue
#        else:
#            seen_halfedges.append(halfedge)
#            nedges += 1
#    # Check Euler formula
#    chi = nverts - nedges + nfaces
#    if chi not in range(2, 100, 2):
#        raise Exception('Invalid GEOM, chi in Euler formula is:', chi)

    def check_geom_sanity(self):
        """
        Check geometry sanity

        If the mesh is correct and encloses a volume, this can be checked with
        prior tests: checking orientability, non-borders,
        non-self-intersecting.
        After that we can calculate its topological features and check if
        Euler's formula  C+V=A+2(S-H) is satisfied.
        If the mesh is not correct, many geometric algorithms will fail.
        The only solution in this case is the user repairing the mesh.
        >>> g = Geom((-1.0, -1.0, -1.0,  -1.0, -1.0, 1.0,  -1.0, 1.0,  1.0, \
                      -1.0,  1.0, -1.0,   1.0,  1.0, 1.0,   1.0, 1.0, -1.0,\
                       1.0, -1.0, -1.0,   1.0, -1.0, 1.0), \
                    ((0,1,2,3), (7,6,5,4), (1,7,4,2), \
                     (0,3,5,6), (1,0,6,7), (2,4,5,3)) )  # A good cube
        >>> g.check_geom_sanity()
        """
        self.check_loose_verts()
        self.check_degenerate_geometry()
        self.check_is_solid()
#        self.check_euler()
#        self.check_flat_polygons()
        # Check correct normals for a solid in fluid FIXME working here
        # Check self intersection  # FIXME not working

    # Boolean

    def union(self, geom):
        """
        Update current geom to represent union with geom.
        """
        # Create abd build BSP trees
        a = BSPNode(self)
        a.build()
        b = BSPNode(geom)
        b.build()

        # Remove each interior
        a.clip_to(b)
        b.clip_to(a)

        # Remove shared coplanars
        b.invert()
        b.clip_to(a)
        b.invert()

        # Join trees and geometries
        a.append(b)

        # Sync polygons from bsp tree to self
        new_polygons = []
        for ipolygon in a.get_all_ipolygons():
            new_polygons.append(self.get_polygon(ipolygon))
        self.polygons = new_polygons

        # Repair the mesh FIXME

# BSP tree

class BSPNode(object):
    """
    A node in a BSP tree.
    >>> g = Geom((-1,-1,0, 1,-1,0, 0,1,0, 0,0,1), \
                 ((2,1,0), (0,1,3), (1,2,3), (2,0,3)) )  # Good tet
    >>> n = BSPNode(geom=g); n.build(); n
    BSP tree - geom hid: None, ipolygons: [0]
        │ plane: Plane(normal=Vector(0.000, -0.000, -1.000), distance=0.0)
        ├─front_node: None
        └─back_node: geom hid: None, ipolygons: [1]
          │ plane: Plane(normal=Vector(0.000, -0.707, 0.707), distance=2.0)
          ├─front_node: None
          └─back_node: geom hid: None, ipolygons: [2]
            │ plane: Plane(normal=Vector(0.816, 0.408, 0.408), distance=1.0)
            ├─front_node: None
            └─back_node: geom hid: None, ipolygons: [3]
              │ plane: Plane(normal=Vector(-0.816, 0.408, 0.408), distance=1.0)
              ├─front_node: None
              └─back_node: None
    """
    def __init__(self, geom):
        # Tree
        self.plane = None       # Cutting Plane instance
        self.front_node = None  # Front BSPNode, for tree
        self.back_node = None   # Back BSPNode, for tree
        # Geom
        self.geom = geom        # Link to related geom
        self.ipolygons = []     # Coplanar ipolygons

    def __repr__(self):
        return 'BSP tree - {}'.format(self._repr_tree())

    def _repr_tree(self, back=True):
        # Get children trees
        front_tree = "None"
        if self.front_node:
            front_tree = self.front_node._repr_tree(back=False)
        back_tree = "None"
        if self.back_node:
            back_tree = self.back_node._repr_tree(back=True)
        # Join texts
        line = "│ "
        if back:
            line = "  "
        header = 'geom hid: {0}, ipolygons: {1}\n'.format(
            self.geom.hid,
            self.ipolygons,
            )
        text = '{3}│ plane: {0}\n{3}├─front_node: {1}\n{3}└─back_node: {2}'.format(
            self.plane,
            front_tree,
            back_tree,
            line,
        )
        return header + textwrap.indent(text, '  ')

    def clone(self):
        node = BSPNode(self.geom)
        if self.plane:
            node.plane = self.plane.clone()
        if self.front_node:
            node.front_node = self.front_node.clone()
        if self.back_node:
            node.back = self.back_node.clone()
        node.ipolygons = self.ipolygons[:]
        return node

    def invert(self):
        """
        Swap solid space and empty space.
        """
        # Flip normals
        self.geom.flip()
        self.plane.flip()
        # Invert tree
        if self.front_node:
            self.front_node.invert()
        if self.back_node:
            self.back_node.invert()
        # Swap front and back nodes
        temp = self.front_node
        self.front_node = self.back_node
        self.back_node = temp

    def clip_polygons(self, geom, ipolygons):
        """
        Recursively remove all geom ipolygons that are inside this BSP tree.
        """
        if not self.plane:
            return

        # Split all geom ipolygons by self.plane, accumulate fragments
        front = []  # front ipolygons
        back = []   # back ipolygons
        for ipolygon in ipolygons:
            geom.split_polygon(ipolygon, self.plane,
                               front, back, front, back)

        if self.front_node:
            front = self.front_node.clip_polygons(geom, front)

        if self.back_node:
            back = self.back_node.clip_polygons(geom, back)
        else:
            back = []  # Remove back polygons of a leaf without back_node

        front.extend(back)
        return front

    def clip_to(self, clipping_bsp):
        """
        Remove all polygons in this BSP tree that are inside the
        clipping BSP tree
        """
        self.ipolygons = clipping_bsp.clip_polygons(self.geom, self.ipolygons)
        if self.front_node:
            self.front_node.clip_to(clipping_bsp)
        if self.back_node:
            self.back_node.clip_to(clipping_bsp)

    def get_all_ipolygons(self):
        """
        Return a list of all ipolygons in this BSP tree.
        """
        ipolygons = self.ipolygons[:]
        if self.front_node:
            ipolygons.extend(self.front_node.get_all_ipolygons())
        if self.back_node:
            ipolygons.extend(self.back_node.get_all_ipolygons())
        return ipolygons

    def build(self, ipolygons=None):
        """
        Recursively build a BSP tree out of the geom polygons.
        When called on an existing tree, the new polygons (from the same geom)
        are filtered down to the bottom of the tree and become new nodes there.
        The splitting plane is set as the first polygon plane.
        """
        # Protect
        if ipolygons is None:
            ipolygons = self.geom.get_ipolygons()
        if not ipolygons:
            return None

        # Set the cutting plane
        i = 0
        if not self.plane:
            i = 1
            self.plane = self.geom.get_plane_of_polygon(ipolygons[0])
            self.ipolygons.append(ipolygons[0])

        # Split all polygons using self.plane
        front = []  # front ipolygons
        back = []   # back ipolygons
        for ipolygon in ipolygons[i:]:  # If got for plane, start from the 2nd
            # Coplanar front and back polygons go into self.ipolygons
            self.geom.split_polygon(ipolygon, self.plane,
                                    self.ipolygons, self.ipolygons,
                                    front, back)

        # Recursively build the BSP tree
        if len(front) > 0:
            if not self.front_node:
                self.front_node = BSPNode(self.geom)
            self.front_node.build(front)
        if len(back) > 0:
            if not self.back_node:
                self.back_node = BSPNode(self.geom)
            self.back_node.build(back)

    def append(self, other_bsp):  # FIXME test
        """
        Append other bsp tree to this.
        """
        # Append the other geom to self.geom
        new_ipolygons = self.geom.append(other_bsp.geom)
        # Build
        self.build(new_ipolygons)

    def sync_geom(self):
        """
        Sync polygons from self to self.geom
        """
        geom = self.geom
        new_polygons = []
        for ipolygon in self.get_all_ipolygons():
            new_polygons.append(geom.get_polygon(ipolygon))
        geom.polygons = new_polygons


if __name__ == "__main__":
    import doctest
    doctest.testmod()

#    name = "concave"
#
#    g = Geom.from_STL(filename='../test/{0}/{0}_a.stl'.format(name))
#    h = Geom.from_STL(filename='../test/{0}/{0}_b.stl'.format(name))
#
#    # Create and build BSP trees
#    a = BSPNode(g)
#    a.build()
#
#    b = BSPNode(h)
#    b.build()
#
#    # Remove each interior
#    a.clip_to(b)
#    b.clip_to(a)
#
#    # Remove shared coplanars
#    b.invert()
#    b.clip_to(a)
#    b.invert()
#
#    # Sync
#    a.sync_geom()
#    b.sync_geom()
#
#    # Join trees and geometries
#    # a.append(b)
#
#    g.to_STL(filename='../test/{0}/{0}_union.stl'.format(name))
