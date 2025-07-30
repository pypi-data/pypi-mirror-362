from __future__ import annotations
import ocean.abyss.nodes
__all__ = ['Ciexyz', 'Custom', 'Energy', 'Linked', 'Spectralbox']
class Ciexyz(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Ciexyz
        
        .. raw:: html
    
            <iframe id=Ciexyz" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/sensor/ciexyz.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/sensor/ciexyz.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getY_only(self) -> bool:
        """
        Get the y_only parameter
        """
    def setY_only(self, y_only: bool) -> bool:
        """
        Set the y_only parameter
        """
class Custom(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Custom
        
        .. raw:: html
    
            <iframe id=Custom" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/sensor/custom.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/sensor/custom.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Energy(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Energy
        
        .. raw:: html
    
            <iframe id=Energy" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/sensor/energy.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/sensor/energy.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
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
class Spectralbox(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Spectralbox
        
        .. raw:: html
    
            <iframe id=Spectralbox" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/sensor/spectralbox.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/sensor/spectralbox.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getFirstwl(self) -> float:
        """
        Get the firstwl parameter
        """
    def getLastwl(self) -> float:
        """
        Get the lastwl parameter
        """
    def getNumpoints(self) -> int:
        """
        Get the numpoints parameter
        """
    def setFirstwl(self, firstwl: float) -> bool:
        """
        Set the firstwl parameter
        """
    def setLastwl(self, lastwl: float) -> bool:
        """
        Set the lastwl parameter
        """
    def setNumpoints(self, numpoints: int) -> bool:
        """
        Set the numpoints parameter
        """
