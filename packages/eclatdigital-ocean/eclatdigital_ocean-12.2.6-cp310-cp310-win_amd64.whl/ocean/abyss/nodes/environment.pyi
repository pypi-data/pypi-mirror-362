from __future__ import annotations
import numpy
import ocean.abyss.nodes
import typing
__all__ = ['Additive', 'Black', 'Ciesky', 'Directsun', 'Disc', 'Envmap', 'Hosek', 'Linked', 'Perezsky', 'Preetham', 'Uniform']
class Additive(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Additive
        
        .. raw:: html
    
            <iframe id=Additive" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/additive.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/additive.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Black(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Black
    """
    def __init__(self, name: str) -> None:
        ...
class Ciesky(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Ciesky
        
        .. raw:: html
    
            <iframe id=Ciesky" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/ciesky.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/ciesky.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getA(self) -> float:
        """
        Get the a parameter
        """
    def getB(self) -> float:
        """
        Get the b parameter
        """
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getC(self) -> float:
        """
        Get the c parameter
        """
    def getD(self) -> float:
        """
        Get the d parameter
        """
    def getE(self) -> float:
        """
        Get the e parameter
        """
    def getLz(self) -> float:
        """
        Get the lz parameter
        """
    def getMode(self) -> str:
        """
        Get the mode parameter
        """
    def getModeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSkytype(self) -> str:
        """
        Get the skytype parameter
        """
    def getSkytypeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSunpos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def getZenith(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the zenith parameter
        """
    def setA(self, a: float) -> bool:
        """
        Set the a parameter
        """
    def setB(self, b: float) -> bool:
        """
        Set the b parameter
        """
    def setBase(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the base node 
        """
    def setC(self, c: float) -> bool:
        """
        Set the c parameter
        """
    def setD(self, d: float) -> bool:
        """
        Set the d parameter
        """
    def setE(self, e: float) -> bool:
        """
        Set the e parameter
        """
    def setLz(self, lz: float) -> bool:
        """
        Set the lz parameter
        """
    def setMode(self, mode: str) -> bool:
        """
        Set the mode parameter
        """
    def setSkytype(self, skytype: str) -> bool:
        """
        Set the skytype parameter
        """
    def setSunpos(self, sunpos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
    def setZenith(self, zenith: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the zenith parameter
        """
class Directsun(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Directsun
        
        .. raw:: html
    
            <iframe id=Directsun" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/directsun.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/directsun.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAirmass(self) -> float:
        """
        Get the airmass parameter
        """
    def getDni(self) -> float:
        """
        Get the dni parameter
        """
    def getSunpos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def setAirmass(self, airmass: float) -> bool:
        """
        Set the airmass parameter
        """
    def setDni(self, dni: float) -> bool:
        """
        Set the dni parameter
        """
    def setSunpos(self, sunpos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
class Disc(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Disc
        
        .. raw:: html
    
            <iframe id=Disc" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/disc.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/disc.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDirection(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the direction parameter
        """
    def getRadius(self) -> float:
        """
        Get the radius parameter
        """
    def getSpectrum(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the spectrum node 
        """
    def setDirection(self, direction: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the direction parameter
        """
    def setRadius(self, radius: float) -> bool:
        """
        Set the radius parameter
        """
    def setSpectrum(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the spectrum node 
        """
class Envmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Envmap
        
        .. raw:: html
    
            <iframe id=Envmap" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/envmap.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/envmap.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getFront(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the front parameter
        """
    def getImage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the image node 
        """
    def getNormalize(self) -> str:
        """
        Get the normalize parameter
        """
    def getNormalizeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    def setBase(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the base node 
        """
    def setFront(self, front: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the front parameter
        """
    def setImage(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the image node 
        """
    def setNormalize(self, normalize: str) -> bool:
        """
        Set the normalize parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    @typing.overload
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
class Hosek(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Hosek
        
        .. raw:: html
    
            <iframe id=Hosek" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/hosek.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/hosek.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAlbedo(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the albedo node 
        """
    def getSunpos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def getSunscale(self) -> float:
        """
        Get the sunscale parameter
        """
    def getTurbidity(self) -> float:
        """
        Get the turbidity parameter
        """
    def getZenith(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the zenith parameter
        """
    def setAlbedo(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the albedo node 
        """
    def setSunpos(self, sunpos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
    def setSunscale(self, sunscale: float) -> bool:
        """
        Set the sunscale parameter
        """
    def setTurbidity(self, turbidity: float) -> bool:
        """
        Set the turbidity parameter
        """
    def setZenith(self, zenith: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the zenith parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Linked
        
        .. raw:: html
    
            <iframe id=Linked" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/linked.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/linked.html"></iframe>
    
        
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
class Perezsky(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Perezsky
        
        .. raw:: html
    
            <iframe id=Perezsky" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/perezsky.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/perezsky.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getA(self) -> float:
        """
        Get the a parameter
        """
    def getB(self) -> float:
        """
        Get the b parameter
        """
    def getBase(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the base node 
        """
    def getC(self) -> float:
        """
        Get the c parameter
        """
    def getD(self) -> float:
        """
        Get the d parameter
        """
    def getDhi(self) -> float:
        """
        Get the dhi parameter
        """
    def getDhitype(self) -> str:
        """
        Get the dhitype parameter
        """
    def getDhitypeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getE(self) -> float:
        """
        Get the e parameter
        """
    def getSunpos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def getZenith(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the zenith parameter
        """
    def setA(self, a: float) -> bool:
        """
        Set the a parameter
        """
    def setB(self, b: float) -> bool:
        """
        Set the b parameter
        """
    def setBase(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the base node 
        """
    def setC(self, c: float) -> bool:
        """
        Set the c parameter
        """
    def setD(self, d: float) -> bool:
        """
        Set the d parameter
        """
    def setDhi(self, dhi: float) -> bool:
        """
        Set the dhi parameter
        """
    def setDhitype(self, dhitype: str) -> bool:
        """
        Set the dhitype parameter
        """
    def setE(self, e: float) -> bool:
        """
        Set the e parameter
        """
    def setSunpos(self, sunpos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
    def setZenith(self, zenith: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the zenith parameter
        """
class Preetham(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Preetham
        
        .. raw:: html
    
            <iframe id=Preetham" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/preetham.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/preetham.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAlbedo(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the albedo node 
        """
    def getAtmosphere(self) -> bool:
        """
        Get the atmosphere parameter
        """
    def getSunpos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the sunpos parameter
        """
    def getTurbidity(self) -> float:
        """
        Get the turbidity parameter
        """
    def getZenith(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the zenith parameter
        """
    def setAlbedo(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the albedo node 
        """
    def setAtmosphere(self, atmosphere: bool) -> bool:
        """
        Set the atmosphere parameter
        """
    def setSunpos(self, sunpos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the sunpos parameter
        """
    def setTurbidity(self, turbidity: float) -> bool:
        """
        Set the turbidity parameter
        """
    def setZenith(self, zenith: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the zenith parameter
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Uniform
        
        .. raw:: html
    
            <iframe id=Uniform" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/uniform.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/environment/uniform.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getNormalize(self) -> str:
        """
        Get the normalize parameter
        """
    def getNormalizeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSpectrum(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the spectrum node 
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    @typing.overload
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    def setNormalize(self, normalize: str) -> bool:
        """
        Set the normalize parameter
        """
    def setSpectrum(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the spectrum node 
        """
    @typing.overload
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
    @typing.overload
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
