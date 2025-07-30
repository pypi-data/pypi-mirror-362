from __future__ import annotations
import numpy
import ocean.abyss.nodes
import typing
__all__ = ['CGeomHandler', 'Cone', 'Geometry', 'Mesh', 'Sphere']
class CGeomHandler:
    pass
class Cone(Geometry, CGeomHandler):
    @typing.overload
    def __init__(self, arg0: str, arg1: float, arg2: bool) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: str, arg1: float) -> None:
        ...
    def getRtop(self) -> float:
        ...
    def setRtop(self, arg0: float) -> bool:
        ...
class Geometry(CGeomHandler):
    def __repr__(self) -> str:
        ...
    def getMaterial(self) -> ocean.abyss.nodes.Node:
        """
        Retrieve the associated material
        """
    def getMaterialName(self) -> str:
        """
        Retrieve the associated material name
        """
    def getPtr(self) -> int:
        """
        Get pointer to data as an integer
        """
    def name(self) -> str:
        """
        Retrieve the geometry name
        """
    def numPrimitives(self) -> int:
        """
        Retrieve the number of primitives
        """
    def print(self) -> str:
        """
        Return the node as an ocxml string
        """
    @typing.overload
    def setMaterial(self, arg0: str) -> None:
        """
        Associate a material named 'name' to this mesh
        """
    @typing.overload
    def setMaterial(self, arg0: ocean.abyss.nodes.Node) -> None:
        """
        Associate a material to this mesh
        """
    def setName(self, arg0: str) -> None:
        """
        Set the geometry name
        """
    def typeName(self) -> str:
        """
        Get the geometry type 'mesh', 'sphere' or 'cone'
        """
    def write(self, file: typing.Any) -> None:
        """
        Write data to a python file object
        """
class Mesh(Geometry, CGeomHandler):
    def __init__(self, name: str, vertices: numpy.ndarray[numpy.float64], normals: numpy.ndarray[numpy.float32], triangles: numpy.ndarray[numpy.int32], uvs: numpy.ndarray[numpy.float32] = ...) -> None:
        ...
    def copy(self) -> Mesh:
        """
        Create a copy of this mesh
        """
    def getTriangleNormals(self) -> numpy.ndarray[numpy.float32]:
        """
        Retrieve the triangle normals as a numpy array
        """
    def getTriangles(self) -> numpy.ndarray[numpy.int32]:
        """
        Retrieve the triangles indices as a numpy array
        """
    def getUvs(self) -> numpy.ndarray[numpy.float32]:
        """
        Retrieve the uvs as a numpy array
        """
    def getVertices(self) -> numpy.ndarray[numpy.float64]:
        """
        Retrieve the vertices as a numpy array
        """
    def getVextexNormals(self) -> numpy.ndarray[numpy.float32]:
        """
        Retrieve the vertex normals as a numpy array
        """
class Sphere(Geometry, CGeomHandler):
    def __init__(self, name: str, radius: float, reverse: bool = False) -> None:
        """
        Build a Sphere with its name, its radius [m] and reverse which inverse normals if set to true
        """
    def getRadius(self) -> float:
        """
        Retrieve the sphere radius [m]
        """
    def setRadius(self, arg0: float) -> bool:
        """
        Set the sphere radius [m]
        """
