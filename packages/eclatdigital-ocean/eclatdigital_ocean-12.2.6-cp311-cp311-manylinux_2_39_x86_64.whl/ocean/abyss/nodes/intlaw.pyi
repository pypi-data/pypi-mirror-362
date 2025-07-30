from __future__ import annotations
import numpy
import ocean.abyss.nodes
import typing
__all__ = ['Advfoil', 'Artistic', 'Cfresnel', 'Foil', 'Fresnel', 'Halffoil', 'Linked', 'Mixtabulated', 'Mm44', 'Null', 'Polarizer', 'Poltabulated', 'Simple', 'Thinfilm']
class Advfoil(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Advfoil
        
        .. raw:: html
    
            <iframe id=Advfoil" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/advfoil.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/advfoil.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getExternal(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the external node 
        """
    def getInternal(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the internal node 
        """
    def getThickness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the thickness node 
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the dielectricfunc node 
        """
    def setExternal(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the external node 
        """
    def setInternal(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the internal node 
        """
    def setThickness(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the thickness node 
        """
class Artistic(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Artistic
        
        .. raw:: html
    
            <iframe id=Artistic" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/artistic.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/artistic.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getR0(self) -> float:
        """
        Get the r0 parameter
        """
    def getReflection(self) -> float:
        """
        Get the reflection parameter
        """
    def getReflectioncolor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the reflectioncolor node 
        """
    def getTransmission(self) -> float:
        """
        Get the transmission parameter
        """
    def getTransmissioncolor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the transmissioncolor node 
        """
    def setR0(self, r0: float) -> bool:
        """
        Set the r0 parameter
        """
    def setReflection(self, reflection: float) -> bool:
        """
        Set the reflection parameter
        """
    def setReflectioncolor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the reflectioncolor node 
        """
    def setTransmission(self, transmission: float) -> bool:
        """
        Set the transmission parameter
        """
    def setTransmissioncolor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the transmissioncolor node 
        """
class Cfresnel(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Cfresnel
        
        .. raw:: html
    
            <iframe id=Cfresnel" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/cfresnel.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/cfresnel.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the dielectricfunc node 
        """
class Foil(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Foil
        
        .. raw:: html
    
            <iframe id=Foil" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/foil.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/foil.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getThickness(self) -> float:
        """
        Get the thickness parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the dielectricfunc node 
        """
    def setThickness(self, thickness: float) -> bool:
        """
        Set the thickness parameter
        """
class Fresnel(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Fresnel
        
        .. raw:: html
    
            <iframe id=Fresnel" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/fresnel.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/fresnel.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Halffoil(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Halffoil
        
        .. raw:: html
    
            <iframe id=Halffoil" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/halffoil.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/halffoil.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getThickness(self) -> float:
        """
        Get the thickness parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the dielectricfunc node 
        """
    def setThickness(self, thickness: float) -> bool:
        """
        Set the thickness parameter
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
class Mixtabulated(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Mixtabulated
        
        .. raw:: html
    
            <iframe id=Mixtabulated" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/mixtabulated.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/mixtabulated.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getEr(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er node 
        """
    def getIr(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir node 
        """
    def getT(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t node 
        """
    def setEr(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er node 
        """
    def setIr(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir node 
        """
    def setT(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t node 
        """
class Mm44(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Mm44
    """
    def __init__(self, name: str) -> None:
        ...
    def getEr11(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er11 node 
        """
    def getEr12(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er12 node 
        """
    def getEr13(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er13 node 
        """
    def getEr14(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er14 node 
        """
    def getEr21(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er21 node 
        """
    def getEr22(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er22 node 
        """
    def getEr23(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er23 node 
        """
    def getEr24(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er24 node 
        """
    def getEr31(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er31 node 
        """
    def getEr32(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er32 node 
        """
    def getEr33(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er33 node 
        """
    def getEr34(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er34 node 
        """
    def getEr41(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er41 node 
        """
    def getEr42(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er42 node 
        """
    def getEr43(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er43 node 
        """
    def getEr44(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the er44 node 
        """
    def getIr11(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir11 node 
        """
    def getIr12(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir12 node 
        """
    def getIr13(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir13 node 
        """
    def getIr14(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir14 node 
        """
    def getIr21(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir21 node 
        """
    def getIr22(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir22 node 
        """
    def getIr23(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir23 node 
        """
    def getIr24(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir24 node 
        """
    def getIr31(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir31 node 
        """
    def getIr32(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir32 node 
        """
    def getIr33(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir33 node 
        """
    def getIr34(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir34 node 
        """
    def getIr41(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir41 node 
        """
    def getIr42(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir42 node 
        """
    def getIr43(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir43 node 
        """
    def getIr44(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ir44 node 
        """
    def getT11(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t11 node 
        """
    def getT12(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t12 node 
        """
    def getT13(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t13 node 
        """
    def getT14(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t14 node 
        """
    def getT21(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t21 node 
        """
    def getT22(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t22 node 
        """
    def getT23(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t23 node 
        """
    def getT24(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t24 node 
        """
    def getT31(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t31 node 
        """
    def getT32(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t32 node 
        """
    def getT33(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t33 node 
        """
    def getT34(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t34 node 
        """
    def getT41(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t41 node 
        """
    def getT42(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t42 node 
        """
    def getT43(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t43 node 
        """
    def getT44(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the t44 node 
        """
    def setEr11(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er11 node 
        """
    def setEr12(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er12 node 
        """
    def setEr13(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er13 node 
        """
    def setEr14(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er14 node 
        """
    def setEr21(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er21 node 
        """
    def setEr22(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er22 node 
        """
    def setEr23(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er23 node 
        """
    def setEr24(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er24 node 
        """
    def setEr31(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er31 node 
        """
    def setEr32(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er32 node 
        """
    def setEr33(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er33 node 
        """
    def setEr34(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er34 node 
        """
    def setEr41(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er41 node 
        """
    def setEr42(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er42 node 
        """
    def setEr43(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er43 node 
        """
    def setEr44(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the er44 node 
        """
    def setIr11(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir11 node 
        """
    def setIr12(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir12 node 
        """
    def setIr13(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir13 node 
        """
    def setIr14(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir14 node 
        """
    def setIr21(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir21 node 
        """
    def setIr22(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir22 node 
        """
    def setIr23(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir23 node 
        """
    def setIr24(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir24 node 
        """
    def setIr31(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir31 node 
        """
    def setIr32(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir32 node 
        """
    def setIr33(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir33 node 
        """
    def setIr34(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir34 node 
        """
    def setIr41(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir41 node 
        """
    def setIr42(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir42 node 
        """
    def setIr43(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir43 node 
        """
    def setIr44(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ir44 node 
        """
    def setT11(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t11 node 
        """
    def setT12(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t12 node 
        """
    def setT13(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t13 node 
        """
    def setT14(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t14 node 
        """
    def setT21(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t21 node 
        """
    def setT22(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t22 node 
        """
    def setT23(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t23 node 
        """
    def setT24(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t24 node 
        """
    def setT31(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t31 node 
        """
    def setT32(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t32 node 
        """
    def setT33(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t33 node 
        """
    def setT34(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t34 node 
        """
    def setT41(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t41 node 
        """
    def setT42(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t42 node 
        """
    def setT43(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t43 node 
        """
    def setT44(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the t44 node 
        """
class Null(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Null
        
        .. raw:: html
    
            <iframe id=Null" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/null.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/null.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Polarizer(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Polarizer
        
        .. raw:: html
    
            <iframe id=Polarizer" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/polarizer.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/polarizer.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxes(self) -> str:
        """
        Get the axes parameter
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getAxesChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getM11(self) -> float:
        """
        Get the m11 parameter
        """
    def getM12(self) -> float:
        """
        Get the m12 parameter
        """
    def getM13(self) -> float:
        """
        Get the m13 parameter
        """
    def getM14(self) -> float:
        """
        Get the m14 parameter
        """
    def getM21(self) -> float:
        """
        Get the m21 parameter
        """
    def getM22(self) -> float:
        """
        Get the m22 parameter
        """
    def getM23(self) -> float:
        """
        Get the m23 parameter
        """
    def getM24(self) -> float:
        """
        Get the m24 parameter
        """
    def getM31(self) -> float:
        """
        Get the m31 parameter
        """
    def getM32(self) -> float:
        """
        Get the m32 parameter
        """
    def getM33(self) -> float:
        """
        Get the m33 parameter
        """
    def getM34(self) -> float:
        """
        Get the m34 parameter
        """
    def getM41(self) -> float:
        """
        Get the m41 parameter
        """
    def getM42(self) -> float:
        """
        Get the m42 parameter
        """
    def getM43(self) -> float:
        """
        Get the m43 parameter
        """
    def getM44(self) -> float:
        """
        Get the m44 parameter
        """
    def getMode(self) -> str:
        """
        Get the mode parameter
        """
    def getModeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getMultiplier(self) -> float:
        """
        Get the multiplier parameter
        """
    @typing.overload
    def getPhi(self) -> float:
        """
        Get the phi parameter
        """
    @typing.overload
    def getPhi(self) -> float:
        """
        Get the phi parameter
        """
    @typing.overload
    def getPx(self) -> float:
        """
        Get the px parameter
        """
    @typing.overload
    def getPx(self) -> float:
        """
        Get the px parameter
        """
    @typing.overload
    def getPy(self) -> float:
        """
        Get the py parameter
        """
    @typing.overload
    def getPy(self) -> float:
        """
        Get the py parameter
        """
    def getSubtype(self) -> str:
        """
        Get the subtype parameter
        """
    def getSubtypeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getTheta(self) -> float:
        """
        Get the theta parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def getXyz(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the xyz parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    @typing.overload
    def setAxes(self, axes: str) -> bool:
        """
        Set the axes parameter
        """
    def setM11(self, m11: float) -> bool:
        """
        Set the m11 parameter
        """
    def setM12(self, m12: float) -> bool:
        """
        Set the m12 parameter
        """
    def setM13(self, m13: float) -> bool:
        """
        Set the m13 parameter
        """
    def setM14(self, m14: float) -> bool:
        """
        Set the m14 parameter
        """
    def setM21(self, m21: float) -> bool:
        """
        Set the m21 parameter
        """
    def setM22(self, m22: float) -> bool:
        """
        Set the m22 parameter
        """
    def setM23(self, m23: float) -> bool:
        """
        Set the m23 parameter
        """
    def setM24(self, m24: float) -> bool:
        """
        Set the m24 parameter
        """
    def setM31(self, m31: float) -> bool:
        """
        Set the m31 parameter
        """
    def setM32(self, m32: float) -> bool:
        """
        Set the m32 parameter
        """
    def setM33(self, m33: float) -> bool:
        """
        Set the m33 parameter
        """
    def setM34(self, m34: float) -> bool:
        """
        Set the m34 parameter
        """
    def setM41(self, m41: float) -> bool:
        """
        Set the m41 parameter
        """
    def setM42(self, m42: float) -> bool:
        """
        Set the m42 parameter
        """
    def setM43(self, m43: float) -> bool:
        """
        Set the m43 parameter
        """
    def setM44(self, m44: float) -> bool:
        """
        Set the m44 parameter
        """
    def setMode(self, mode: str) -> bool:
        """
        Set the mode parameter
        """
    def setMultiplier(self, multiplier: float) -> bool:
        """
        Set the multiplier parameter
        """
    @typing.overload
    def setPhi(self, phi: float) -> bool:
        """
        Set the phi parameter
        """
    @typing.overload
    def setPhi(self, phi: float) -> bool:
        """
        Set the phi parameter
        """
    @typing.overload
    def setPx(self, px: float) -> bool:
        """
        Set the px parameter
        """
    @typing.overload
    def setPx(self, px: float) -> bool:
        """
        Set the px parameter
        """
    @typing.overload
    def setPy(self, py: float) -> bool:
        """
        Set the py parameter
        """
    @typing.overload
    def setPy(self, py: float) -> bool:
        """
        Set the py parameter
        """
    def setSubtype(self, subtype: str) -> bool:
        """
        Set the subtype parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setTheta(self, theta: float) -> bool:
        """
        Set the theta parameter
        """
    @typing.overload
    def setXyz(self, xyz: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
    @typing.overload
    def setXyz(self, xyz: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the xyz parameter
        """
class Poltabulated(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Poltabulated
        
        .. raw:: html
    
            <iframe id=Poltabulated" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/poltabulated.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/poltabulated.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getErp(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the erp node 
        """
    def getErs(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ers node 
        """
    def getIrp(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the irp node 
        """
    def getIrs(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the irs node 
        """
    def getTp(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the tp node 
        """
    def getTs(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the ts node 
        """
    def setErp(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the erp node 
        """
    def setErs(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ers node 
        """
    def setIrp(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the irp node 
        """
    def setIrs(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the irs node 
        """
    def setTp(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the tp node 
        """
    def setTs(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the ts node 
        """
class Simple(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Simple
        
        .. raw:: html
    
            <iframe id=Simple" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/simple.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/simple.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getR0(self) -> float:
        """
        Get the r0 parameter
        """
    def setR0(self, r0: float) -> bool:
        """
        Set the r0 parameter
        """
class Thinfilm(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Thinfilm
        
        .. raw:: html
    
            <iframe id=Thinfilm" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/thinfilm.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/intlaw/thinfilm.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getThickness(self) -> float:
        """
        Get the thickness parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the dielectricfunc node 
        """
    def setThickness(self, thickness: float) -> bool:
        """
        Set the thickness parameter
        """
