from __future__ import annotations
import numpy
import ocean.abyss.nodes
__all__ = ['Constant', 'Envmapground', 'Image', 'Linked', 'Texture', 'Uniform']
class Constant(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Constant
        
        .. raw:: html
    
            <iframe id=Constant" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/constant.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/constant.html"></iframe>
    
        
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
class Envmapground(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Envmapground
        
        .. raw:: html
    
            <iframe id=Envmapground" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/envmapground.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/envmapground.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAlbedomax(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the albedomax node 
        """
    def setAlbedomax(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the albedomax node 
        """
class Image(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Image
        
        .. raw:: html
    
            <iframe id=Image" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/image.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/image.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getUvscale(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the uvscale parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the image node 
        """
    def setUvscale(self, uvscale: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the uvscale parameter
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
class Texture(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Texture
        
        .. raw:: html
    
            <iframe id=Texture" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/texture.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/texture.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getGreypt(self) -> float:
        """
        Get the greypt parameter
        """
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getOffset(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the offset parameter
        """
    def getSaturation(self) -> float:
        """
        Get the saturation parameter
        """
    def getScale(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the scale parameter
        """
    def getStepalpha(self) -> bool:
        """
        Get the stepalpha parameter
        """
    def getUvtran(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setGreypt(self, greypt: float) -> bool:
        """
        Set the greypt parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the image node 
        """
    def setOffset(self, offset: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the offset parameter
        """
    def setSaturation(self, saturation: float) -> bool:
        """
        Set the saturation parameter
        """
    def setScale(self, scale: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the scale parameter
        """
    def setStepalpha(self, stepalpha: bool) -> bool:
        """
        Set the stepalpha parameter
        """
    def setUvtran(self, uvtran: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Uniform
        
        .. raw:: html
    
            <iframe id=Uniform" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/uniform.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/filtershader/uniform.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getSpectrum(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the spectrum node 
        """
    def setSpectrum(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the spectrum node 
        """
