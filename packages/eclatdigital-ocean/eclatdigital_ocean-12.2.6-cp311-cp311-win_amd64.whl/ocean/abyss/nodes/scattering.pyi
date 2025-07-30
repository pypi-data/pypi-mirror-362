from __future__ import annotations
import ocean.abyss.nodes
__all__ = ['Additive', 'Gegenbauerspectral', 'Henyeygreenstein', 'Henyeygreensteinspectral', 'Isotropic', 'Linked', 'Rayleigh', 'Tabulated']
class Additive(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Additive
        
        .. raw:: html
    
            <iframe id=Additive" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/additive.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/additive.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Gegenbauerspectral(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Gegenbauerspectral
        
        .. raw:: html
    
            <iframe id=Gegenbauerspectral" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/gegenbauerspectral.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/gegenbauerspectral.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAlpha(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the alpha node 
        """
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def getGGen(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the gGen node 
        """
    def setAlpha(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the alpha node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the density node 
        """
    def setGGen(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the gGen node 
        """
class Henyeygreenstein(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Henyeygreenstein
        
        .. raw:: html
    
            <iframe id=Henyeygreenstein" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/henyeygreenstein.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/henyeygreenstein.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def getG(self) -> float:
        """
        Get the g parameter
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the density node 
        """
    def setG(self, g: float) -> bool:
        """
        Set the g parameter
        """
class Henyeygreensteinspectral(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Henyeygreensteinspectral
        
        .. raw:: html
    
            <iframe id=Henyeygreensteinspectral" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/henyeygreensteinspectral.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/henyeygreensteinspectral.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def getG(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the g node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the density node 
        """
    def setG(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the g node 
        """
class Isotropic(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Isotropic
        
        .. raw:: html
    
            <iframe id=Isotropic" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/isotropic.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/isotropic.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the density node 
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
class Rayleigh(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Rayleigh
        
        .. raw:: html
    
            <iframe id=Rayleigh" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/rayleigh.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/rayleigh.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the density node 
        """
class Tabulated(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Tabulated
        
        .. raw:: html
    
            <iframe id=Tabulated" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/tabulated.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/scattering/tabulated.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDensity(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the density node 
        """
    def getPhasefunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the phasefunc node 
        """
    def setDensity(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the density node 
        """
    def setPhasefunc(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the phasefunc node 
        """
