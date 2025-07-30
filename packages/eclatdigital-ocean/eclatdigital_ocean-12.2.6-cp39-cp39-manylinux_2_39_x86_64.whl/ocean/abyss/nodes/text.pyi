from __future__ import annotations
import ocean.abyss.nodes
__all__ = ['Default', 'Linked']
class Default(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Default
    """
    def __init__(self, name: str) -> None:
        ...
    def getRaw(self) -> str:
        ...
    def setRaw(self, arg0: str) -> bool:
        ...
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Linked
        
        .. raw:: html
    
            <iframe id=Linked" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/text/linked.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/text/linked.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getRaw(self) -> str:
        ...
    def getTarget(self) -> str:
        """
        Get the target parameter
        """
    def setRaw(self, arg0: str) -> bool:
        ...
    def setTarget(self, target: str) -> bool:
        """
        Set the target parameter
        """
