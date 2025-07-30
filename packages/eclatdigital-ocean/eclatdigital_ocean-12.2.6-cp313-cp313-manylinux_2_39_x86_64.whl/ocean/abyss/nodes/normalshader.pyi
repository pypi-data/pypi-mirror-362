from __future__ import annotations
import numpy
import ocean.abyss.nodes
__all__ = ['Blend', 'Bumpmap', 'Heightmap', 'Linked', 'Normalmap', 'Switch', 'Uniform']
class Blend(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Blend
        
        .. raw:: html
    
            <iframe id=Blend" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/blendnormal.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/blendnormal.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getBlend(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the blend node 
        """
    def setBlend(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the blend node 
        """
class Bumpmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Bumpmap
        
        .. raw:: html
    
            <iframe id=Bumpmap" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/bumpmap.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/bumpmap.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getUvtran(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the image node 
        """
    def setMultiplier(self, multiplier: float) -> bool:
        """
        Set the multiplier parameter
        """
    def setUvtran(self, uvtran: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Heightmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Heightmap
        
        .. raw:: html
    
            <iframe id=Heightmap" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/heightmap.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/heightmap.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getUvscale(self) -> float:
        """
        Get the uvscale parameter
        """
    def getZscale(self) -> float:
        """
        Get the zscale parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the image node 
        """
    def setUvscale(self, uvscale: float) -> bool:
        """
        Set the uvscale parameter
        """
    def setZscale(self, zscale: float) -> bool:
        """
        Set the zscale parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Linked
    """
    def __init__(self, name: str) -> None:
        ...
    def getTarget(self) -> str:
        """
        Get the target parameter
        """
    def setTarget(self, target: str) -> bool:
        """
        Set the target parameter
        """
class Normalmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Normalmap
        
        .. raw:: html
    
            <iframe id=Normalmap" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/normalmap.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/normalmap.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    def getUvtran(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the image node 
        """
    def setMultiplier(self, multiplier: float) -> bool:
        """
        Set the multiplier parameter
        """
    def setUvtran(self, uvtran: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Switch(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Switch
        
        .. raw:: html
    
            <iframe id=Switch" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/switchnormal.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/switchnormal.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getSwitch(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the switch node 
        """
    def setSwitch(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the switch node 
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Uniform
        
        .. raw:: html
    
            <iframe id=Uniform" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/uniformnormal.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/normalshader/uniformnormal.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDirection(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the direction parameter
        """
    def setDirection(self, direction: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the direction parameter
        """
