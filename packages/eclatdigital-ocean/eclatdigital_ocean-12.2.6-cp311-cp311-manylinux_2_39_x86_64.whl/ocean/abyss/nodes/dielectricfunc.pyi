from __future__ import annotations
import ocean.abyss.nodes
__all__ = ['Linked', 'Na', 'Nk']
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Linked
        
        .. raw:: html
    
            <iframe id=Linked" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/dielectricfunc/linked.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/dielectricfunc/linked.html"></iframe>
    
        
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
class Na(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Na
        
        .. raw:: html
    
            <iframe id=Na" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/dielectricfunc/absorbance.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/dielectricfunc/absorbance.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getA(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the a node 
        """
    def getN(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the n node 
        """
    def setA(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the a node 
        """
    def setN(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the n node 
        """
class Nk(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Nk
        
        .. raw:: html
    
            <iframe id=Nk" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/dielectricfunc/complex.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/dielectricfunc/complex.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getK(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the k node 
        """
    def getN(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the n node 
        """
    def setK(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the k node 
        """
    def setN(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the n node 
        """
