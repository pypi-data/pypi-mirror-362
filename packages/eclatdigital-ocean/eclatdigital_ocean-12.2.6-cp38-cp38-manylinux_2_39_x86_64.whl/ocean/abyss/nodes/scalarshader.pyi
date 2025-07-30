from __future__ import annotations
import numpy
import ocean.abyss.nodes
__all__ = ['Angular', 'Linked', 'Random', 'Texture', 'Uniform']
class Angular(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Angular
        
        .. raw:: html
    
            <iframe id=Angular" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scalarshader/angular.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scalarshader/angular.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAngularscale(self) -> str:
        """
        Get the angularscale parameter
        """
    def getAngularscaleChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getChannel(self) -> str:
        """
        Get the channel parameter
        """
    def getGreypt(self) -> float:
        """
        Get the greypt parameter
        """
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getOffset(self) -> float:
        """
        Get the offset parameter
        """
    def getScale(self) -> float:
        """
        Get the scale parameter
        """
    def getUvtran(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setAngularscale(self, angularscale: str) -> bool:
        """
        Set the angularscale parameter
        """
    def setChannel(self, channel: str) -> bool:
        """
        Set the channel parameter
        """
    def setGreypt(self, greypt: float) -> bool:
        """
        Set the greypt parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the image node 
        """
    def setOffset(self, offset: float) -> bool:
        """
        Set the offset parameter
        """
    def setScale(self, scale: float) -> bool:
        """
        Set the scale parameter
        """
    def setUvtran(self, uvtran: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the uvtran parameter
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
class Random(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Random
        
        .. raw:: html
    
            <iframe id=Random" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scalarshader/random.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scalarshader/random.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getSeed(self) -> int:
        """
        Get the seed parameter
        """
    def setSeed(self, seed: int) -> bool:
        """
        Set the seed parameter
        """
class Texture(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Texture
        
        .. raw:: html
    
            <iframe id=Texture" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scalarshader/texture.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scalarshader/texture.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getChannel(self) -> str:
        """
        Get the channel parameter
        """
    def getGreypt(self) -> float:
        """
        Get the greypt parameter
        """
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getOffset(self) -> float:
        """
        Get the offset parameter
        """
    def getScale(self) -> float:
        """
        Get the scale parameter
        """
    def getUvtran(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setChannel(self, channel: str) -> bool:
        """
        Set the channel parameter
        """
    def setGreypt(self, greypt: float) -> bool:
        """
        Set the greypt parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the image node 
        """
    def setOffset(self, offset: float) -> bool:
        """
        Set the offset parameter
        """
    def setScale(self, scale: float) -> bool:
        """
        Set the scale parameter
        """
    def setUvtran(self, uvtran: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Uniform
        
        .. raw:: html
    
            <iframe id=Uniform" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scalarshader/uniform.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scalarshader/uniform.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
