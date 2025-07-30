from __future__ import annotations
import ocean.abyss.nodes
__all__ = ['Ashikhminshirley', 'Beckmann', 'Cosine', 'Flat', 'Isotable', 'Linked', 'Map', 'Mix', 'Phong', 'Trowbridge', 'Ward']
class Ashikhminshirley(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Ashikhminshirley
        
        .. raw:: html
    
            <iframe id=Ashikhminshirley" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/ashikhminshirley.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/ashikhminshirley.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getNu(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the nu node 
        """
    def getNv(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the nv node 
        """
    def setNu(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the nu node 
        """
    def setNv(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the nv node 
        """
class Beckmann(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Beckmann
        
        .. raw:: html
    
            <iframe id=Beckmann" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/beckmann.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/beckmann.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getRoughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the roughness node 
        """
    def setRoughness(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the roughness node 
        """
class Cosine(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Cosine
        
        .. raw:: html
    
            <iframe id=Cosine" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/cosine.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/cosine.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Flat(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Flat
        
        .. raw:: html
    
            <iframe id=Flat" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/flat.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/flat.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Isotable(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Isotable
        
        .. raw:: html
    
            <iframe id=Isotable" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/isotable.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/isotable.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDistribution(self) -> dict:
        """
        Get the distribution parameter
        """
    def setDistribution(self, distribution: dict) -> bool:
        """
        Set the distribution parameter
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
class Map(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Map
        
        .. raw:: html
    
            <iframe id=Map" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/map.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/map.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getMap(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the map node 
        """
    def getZscale(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the zscale node 
        """
    def setMap(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the map node 
        """
    def setZscale(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the zscale node 
        """
class Mix(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Mix
        
        .. raw:: html
    
            <iframe id=Mix" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/mix.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/mix.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getWeights(self) -> dict:
        """
        Get the weights parameter
        """
    def setWeights(self, weights: dict) -> bool:
        """
        Set the weights parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
class Phong(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Phong
        
        .. raw:: html
    
            <iframe id=Phong" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/phong.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/phong.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getExponent(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the exponent node 
        """
    def setExponent(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the exponent node 
        """
class Trowbridge(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Trowbridge
        
        .. raw:: html
    
            <iframe id=Trowbridge" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/trowbridge.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/trowbridge.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getNu(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the nu node 
        """
    def setNu(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the nu node 
        """
class Ward(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Ward
        
        .. raw:: html
    
            <iframe id=Ward" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/ward.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/roughness/ward.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getNu(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the nu node 
        """
    def setNu(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the nu node 
        """
