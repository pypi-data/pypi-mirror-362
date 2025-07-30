from __future__ import annotations
import ocean.abyss.nodes
__all__ = ['Default', 'Linked']
class Default(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Default
        
        .. raw:: html
    
            <iframe id=Default" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/colloid.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/colloid.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> float:
        """
        Get the density parameter
        """
    def getParticle(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the Particle node 
        """
    def getSizedistribution(self) -> dict:
        """
        Get the sizedistribution parameter
        """
    def setDensity(self, density: float) -> bool:
        """
        Set the density parameter
        """
    def setParticle(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the Particle node 
        """
    def setSizedistribution(self, sizedistribution: dict) -> bool:
        """
        Set the sizedistribution parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
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
