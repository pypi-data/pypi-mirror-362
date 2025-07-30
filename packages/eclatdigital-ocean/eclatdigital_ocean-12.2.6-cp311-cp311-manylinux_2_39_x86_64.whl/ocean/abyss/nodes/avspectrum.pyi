from __future__ import annotations
import numpy
import ocean.abyss.nodes
__all__ = ['Linked', 'Table']
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Linked
    """
    def __init__(self, name: str) -> None:
        ...
    def getRaw(self) -> numpy.ndarray[numpy.float64]:
        ...
    def getTarget(self) -> str:
        """
        Get the target parameter
        """
    def setRaw(self, arg0: numpy.ndarray[numpy.float64]) -> bool:
        ...
    def setTarget(self, target: str) -> bool:
        """
        Set the target parameter
        """
class Table(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Table
        
        .. raw:: html
    
            <iframe id=Table" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/avspectrum.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/avspectrum.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getInterp(self) -> str:
        """
        Get the interp parameter
        """
    def getInterpChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getNumwl(self) -> int:
        """
        Get the numwl parameter
        """
    def getRaw(self) -> numpy.ndarray[numpy.float64]:
        ...
    def setInterp(self, interp: str) -> bool:
        """
        Set the interp parameter
        """
    def setNumwl(self, numwl: int) -> bool:
        """
        Set the numwl parameter
        """
    def setRaw(self, arg0: numpy.ndarray[numpy.float64]) -> bool:
        ...
