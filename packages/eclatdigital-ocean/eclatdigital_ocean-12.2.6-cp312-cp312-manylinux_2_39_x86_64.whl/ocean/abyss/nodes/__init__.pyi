from __future__ import annotations
import numpy
import typing
from . import avspectrum
from . import bsdf
from . import colloid
from . import dielectricfunc
from . import emitter
from . import environment
from . import filter
from . import filtershader
from . import geometries
from . import image
from . import instrument
from . import intlaw
from . import layer
from . import material
from . import medium
from . import normalshader
from . import output
from . import roughness
from . import scalarshader
from . import scattering
from . import sensor
from . import setup
from . import spectrum
from . import text
__all__ = ['CInstanceHandler', 'CNodeHandler', 'CSceneHandler', 'Instance', 'Node', 'Scene', 'avspectrum', 'bsdf', 'colloid', 'dielectricfunc', 'emitter', 'environment', 'filter', 'filtershader', 'geometries', 'image', 'instrument', 'intlaw', 'layer', 'material', 'medium', 'normalshader', 'output', 'roughness', 'scalarshader', 'scattering', 'sensor', 'setup', 'spectrum', 'text']
class CInstanceHandler:
    pass
class CNodeHandler:
    pass
class CSceneHandler:
    pass
class Instance(CInstanceHandler):
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def copy(self) -> Instance:
        """
         Copy an instance
                    
                    .. note:: 
        
                        The underlying material (if any) is shared with the original
        """
    def geometryName(self) -> str:
        """
        Retrieve the geometry name
        """
    def getPtr(self) -> int:
        """
        Get pointer to data as an integer
        """
    def getTransform(self) -> numpy.ndarray[numpy.float64]:
        """
        Retrieve the 4x4 transformation matrix (which defined the translation, orientation and scale of the geometry)
        """
    def material(self) -> Node:
        """
        Get the material used by this instance
        """
    def print(self) -> str:
        """
        Return the instance as an ocxml string
        """
    def setGeometryName(self, arg0: str) -> None:
        """
        Set the geometry used by its name
        """
    def setMaterial(self, mat: Node, fallback: bool = False, keepOriginal: bool = True) -> None:
        """
        Set the material used by this instance.
        """
    def setTransform(self, arg0: numpy.ndarray[numpy.float64]) -> bool:
        """
        Set the 4x4 transformation matrix
        """
    def write(self, file: typing.Any) -> None:
        """
        Write data to a python file object
        """
class Node(CNodeHandler):
    """
    
            A scene node.
    
            This is the parent class of nodes.
        
        
    """
    def __init__(self, className: str, typeName: str, name: str) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def children(self) -> list[Node]:
        """
        Retrieve the list of childrens of this node
        """
    def className(self) -> str:
        """
        Retrieve the className of this child
        """
    def clone(self) -> Node:
        """
        Return a clone of this node. Childrens are shared with the original
        """
    def comments(self) -> str:
        """
        Retrieve comments of this node
        """
    def copy(self) -> Node:
        """
        Return a copy of this node. All its nodes are also copied
        """
    def getChild(self, name: str) -> Node:
        """
        Get a child named "name" from this node
        """
    def getChildList(self) -> list[Node]:
        """
        Retrieve the list of varying childs
        """
    def getListChild(self, name: str) -> Node:
        """
        Retrieve a child named "name" in the varying child list
        """
    def getPtr(self) -> int:
        """
        Get pointer to data as an integer
        """
    def isIdentical(self, node: CNodeHandler) -> bool:
        """
        Check if this node and node point to the same data
        """
    def isListType(self) -> bool:
        """
        Is this node has a variable list of childs
        """
    def listClass(self) -> str:
        """
        Retrieve the className of the variable list of childs
        """
    def name(self) -> str:
        """
        Retrieve the name of the node
        """
    def print(self) -> str:
        """
        Return the node as an ocxml string
        """
    def setChild(self, child: Node) -> bool:
        """
        Set a child. If a child in the list has the same name it is replaced by this one
        """
    def setComments(self, comment: str) -> None:
        """
        Set comments to this node
        """
    def setName(self, name: str) -> bool:
        """
        Set node name
        """
    def typeName(self) -> str:
        """
        Retrieve the typeName of this child
        """
    def write(self, file: typing.Any) -> None:
        """
        Write data to a python file object
        """
class Scene(CSceneHandler):
    class Format:
        """
        Enum for scene format options
        
        Members:
        
          OCXML : Ascii xml format
        
          OCBIN : Binary format
        
          OCXMLZ : Ascii gziped xml format
        
          OCBINZ : Binary gziped binary format
        """
        OCBIN: typing.ClassVar[Scene.Format]  # value = <Format.OCBIN: 1>
        OCBINZ: typing.ClassVar[Scene.Format]  # value = <Format.OCBINZ: 3>
        OCXML: typing.ClassVar[Scene.Format]  # value = <Format.OCXML: 0>
        OCXMLZ: typing.ClassVar[Scene.Format]  # value = <Format.OCXMLZ: 2>
        __members__: typing.ClassVar[dict[str, Scene.Format]]  # value = {'OCXML': <Format.OCXML: 0>, 'OCBIN': <Format.OCBIN: 1>, 'OCXMLZ': <Format.OCXMLZ: 2>, 'OCBINZ': <Format.OCBINZ: 3>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    OCBIN: typing.ClassVar[Scene.Format]  # value = <Format.OCBIN: 1>
    OCBINZ: typing.ClassVar[Scene.Format]  # value = <Format.OCBINZ: 3>
    OCXML: typing.ClassVar[Scene.Format]  # value = <Format.OCXML: 0>
    OCXMLZ: typing.ClassVar[Scene.Format]  # value = <Format.OCXMLZ: 2>
    def __init__(self, arg0: str) -> None:
        ...
    @typing.overload
    def add(self, node: Node, keepOriginal: bool = True) -> Node:
        """
        Add an Node to the scene, this method copies the node and put it in the scene, you can choose to delete the original from memory (keepOriginal=False) or to keep it
        """
    @typing.overload
    def add(self, mesh: geometries.Mesh, keepOriginal: bool = True) -> geometries.Mesh:
        """
        Add a Mesh to the scene, this method copies the geom and put it in the scene, you can choose to delete the original from memory (keepOriginal=False) or to keep it
        """
    @typing.overload
    def add(self, cone: geometries.Cone, keepOriginal: bool = True) -> geometries.Cone:
        """
        Add a Cone to the scene, this method copies the geom and put it in the scene, you can choose to delete the original from memory (keepOriginal=False) or to keep it
        """
    @typing.overload
    def add(self, sphere: geometries.Sphere, keepOriginal: bool = True) -> geometries.Sphere:
        """
        Add a Sphere to the scene, this method copies the geom and put it in the scene, you can choose to delete the original from memory (keepOriginal=False) or to keep it
        """
    @typing.overload
    def add(self, instance: Instance, layers: list[list[str]] = [], keepOriginal: bool = True) -> int:
        """
         "Add an Instance to the scene, 
                
                **layers** is an array of arrays that represents layers. 
                See the example to understand how to configure nested layers.
        
                Example: 
        
                .. code-block:: python
        
                    scene = abyss.nodes.Scene("my_scene")
                    setup = abyss.nodes.setup.Default("default")
                
                    # define some layers
                    layer_main = abyss.nodes.layer.Generic("main")
                    layer_0 = abyss.nodes.layer.Generic("layer_0")
                    layer_1 = abyss.nodes.layer.Generic("layer_1")
                    layer_0.setChild(layer_1) # nested layer
                    layer_main.setChild(layer_0)
        
                    # add layers to the setup
                    setup.setLayers(layer_main)
                    # add setup to the scene
                    scene.add(setup)
                    # create and configure instances:
                    sphere = abyss.nodes.geometries.Sphere("sphere", 4.0)
                    scene.add(sphere)
                    instance0 = abyss.nodes.Instance()
                    instance0.setGeometryName("sphere")
                    instance1 = instance0.copy()
        
                    # add instance to layers and instance to the scene
                    # makes instance0 to be in layer layer_0
                    scene.add(instance0, [[layer_0.name()]])
                    # makes instance1 to be in layer_0/layer_1
                    scene.add(instance1, [[layer_0.name()],[layer_0.name(), layer_1.name()]])
        
        
                .. note::
                
                    This method copies the instance and put it in the scene.
                    you can choose to delete the original from memory (keepOriginal=False) or to keep it")
        """
    def addImport(self, arg0: str, arg1: bool, arg2: int, arg3: str) -> bool:
        """
        Add an import tag or load it
        """
    def addSearchPath(self, arg0: str) -> None:
        """
        Add a path to search for assets
        """
    def clear(self) -> None:
        """
        Clear all
        """
    def clearGeometry(self) -> None:
        """
        Clear all geometries
        """
    def clearInstances(self) -> None:
        """
        Clear all instances
        """
    def clearNodes(self) -> None:
        """
        Clear all nodes
        """
    def findNodes(self, class_name: str = '', type_name: str = '', name: str = '') -> list[Node]:
        """
        Get node in this scene  with this classname, typename and name
        """
    def getActiveSetup(self) -> str:
        """
        Get the name of the active setup
        """
    def getCones(self) -> list[geometries.Cone]:
        """
        Get all geometries of type cone
        """
    def getGeometries(self) -> list[geometries.Geometry]:
        """
        Get all geometries from scene
        """
    def getInstances(self) -> list[Instance]:
        """
        Get all instances from scene
        """
    def getMeshes(self) -> list[geometries.Mesh]:
        """
        Get all geometries of type mesh
        """
    def getNodes(self) -> list[Node]:
        """
        Get all nodes from scene
        """
    def getSpheres(self) -> list[geometries.Sphere]:
        """
        Get all geometries of type sphere
        """
    def name(self) -> str:
        """
        Get scene name
        """
    def print(self) -> str:
        """
        Return the scene as str (ocxml format)
        """
    def read(self, arg0: str) -> bool:
        """
        Read an Ocean'scene from a file
        """
    def readBytes(self, arg0: bytes) -> bool:
        """
        Read an Ocean'scene from a Bytes object
        """
    @typing.overload
    def remove(self, arg0: Node) -> bool:
        """
        Remove a node from scene
        """
    @typing.overload
    def remove(self, arg0: geometries.Geometry) -> bool:
        """
        Remove a geometry from scene
        """
    @typing.overload
    def remove(self, arg0: Instance) -> bool:
        """
        Remove an instance from scene
        """
    @typing.overload
    def remove(self, arg0: int) -> None:
        """
        Remove an object from scene using its memory adress. Use scene.remove( obj.getPtr() )
        """
    def setActiveSetup(self, arg0: str) -> bool:
        """
        Set the name of the active setup
        """
    def setName(self, arg0: str) -> None:
        """
        Set scene name
        """
    def write(self, file: typing.Any, format: Scene.Format = ...) -> None:
        """
        write scene to a file object or a BytesIO
        
                Usage:
        
                .. code-block:: python
                    
                    #...
                    # assuming an ocean.abyss.nodes.Scene scene has been created and filled.
                    #
                    # You can save a scene as ocxml, ocbin, ocxmlz, ocbinz (z means gzipped).
                    # It can be saved in a file or in a io.BytesIO or io.StringIO
                    # Make sure to use binary streams (open with 'b' or BytesIO) for non ascii format (all but ocxml)
                    
                    #Write to an ocxml file
                    with open(scene.name()+".ocxml", 'w') as f:
                        scene.write(f, abyss.nodes.Scene.Format.OCXML)
        
                    #Write to an ocbin file (note the 'b' as binary)
                    with open(scene.name()+".ocbin", 'wb') as f:
                        scene.write(f, abyss.nodes.Scene.Format.OCBIN)
        
                    #Write to an ocxmlz (gziped ocxml) file (note the 'b' as binary)
                    with open(scene.name()+".ocbin", 'wb') as f:
                        scene.write(f, abyss.nodes.Scene.Format.OCXMLZ)
                
                    #Write to an ocbinz (gziped ocbin) file (note the 'b' as binary)
                    with open(scene.name()+".ocbin", 'wb') as f:
                        scene.write(f, abyss.nodes.Scene.Format.OCBINZ)
        
                    #Write to a bytesIO
                    import io
        
                    bin=io.BytesIO()
                    scene.write(bin, abyss.nodes.Scene.Format.OCBIN)
                    # scene.write(bin, abyss.nodes.Scene.Format.OCBINZ)
                    # scene.write(bin, abyss.nodes.Scene.Format.OCXMLZ)
        
                    #Write to a StringIO
                    
                    bin=io.StringIO()
                    scene.write(bin, abyss.nodes.Scene.Format.OCXML)
        """
