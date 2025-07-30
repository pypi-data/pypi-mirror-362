from __future__ import annotations
import numpy
import ocean.abyss.nodes
__all__ = ['Embedded', 'File', 'Inline', 'Linked']
class Embedded(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Embedded
        
        .. raw:: html
    
            <iframe id=Embedded" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/image/embedded.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/image/embedded.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getRaw(self) -> bytes:
        ...
    def setRaw(self, arg0: bytes) -> bool:
        ...
class File(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        File
        
        .. raw:: html
    
            <iframe id=File" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/image/file.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/image/file.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getPath(self) -> str:
        """
        Get the path parameter
        """
    def setPath(self, path: str) -> bool:
        """
        Set the path parameter
        """
class Inline(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Inline
        
        .. raw:: html
    
            <iframe id=Inline" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/image/inline.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/image/inline.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getFormat(self) -> str:
        """
        Get the format parameter
        """
    def getFormatChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getHeight(self) -> int:
        """
        Get the height parameter
        """
    def getRaw(self) -> numpy.ndarray[numpy.float32]:
        ...
    def getWidth(self) -> int:
        """
        Get the width parameter
        """
    def setFormat(self, format: str) -> bool:
        """
        Set the format parameter
        """
    def setHeight(self, height: int) -> bool:
        """
        Set the height parameter
        """
    def setRaw(self, arg0: numpy.ndarray[numpy.float32]) -> bool:
        ...
    def setWidth(self, width: int) -> bool:
        """
        Set the width parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Linked
        
        .. raw:: html
    
            <iframe id=Linked" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/image/linked.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/image/linked.html"></iframe>
    
        
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
