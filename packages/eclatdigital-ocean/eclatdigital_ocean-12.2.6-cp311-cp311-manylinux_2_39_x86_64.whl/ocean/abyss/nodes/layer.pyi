from __future__ import annotations
import ocean.abyss.nodes
__all__ = ['Generic', 'Linked']
class Generic(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Generic
        
        .. raw:: html
    
            <iframe id=Generic" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/layer/generic.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/layer/generic.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getVisible(self) -> bool:
        """
        Get the visible parameter
        """
    def setVisible(self, visible: bool) -> bool:
        """
        Set the visible parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Linked
        
        .. raw:: html
    
            <iframe id=Linked" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/layer/linked.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/layer/linked.html"></iframe>
    
        
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
