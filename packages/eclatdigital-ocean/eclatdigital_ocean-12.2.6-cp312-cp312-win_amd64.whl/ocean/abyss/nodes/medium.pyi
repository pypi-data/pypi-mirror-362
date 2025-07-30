from __future__ import annotations
import ocean.abyss.nodes
__all__ = ['Linked', 'Mie', 'Simple']
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Linked
        
        .. raw:: html
    
            <iframe id=Linked" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/medium/linked.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/medium/linked.html"></iframe>
    
        
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
class Mie(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Mie
        
        .. raw:: html
    
            <iframe id=Mie" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/medium/mie.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/medium/mie.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getHost(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the Host node 
        """
    def getPrecedence(self) -> int:
        """
        Get the precedence parameter
        """
    def setHost(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the Host node 
        """
    def setPrecedence(self, precedence: int) -> bool:
        """
        Set the precedence parameter
        """
class Simple(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Simple
        
        .. raw:: html
    
            <iframe id=Simple" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/medium/simple.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/medium/simple.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getPrecedence(self) -> int:
        """
        Get the precedence parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the dielectricfunc node 
        """
    def setPrecedence(self, precedence: int) -> bool:
        """
        Set the precedence parameter
        """
