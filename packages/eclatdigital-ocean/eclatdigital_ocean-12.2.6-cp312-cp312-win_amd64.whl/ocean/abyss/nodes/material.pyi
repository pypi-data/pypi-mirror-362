from __future__ import annotations
import numpy
import ocean.abyss.nodes
import typing
__all__ = ['Axf_svbrdf', 'Blend', 'Clone', 'Doublesided', 'Generic', 'Idealreflpolarizer', 'Idealtranspolarizer', 'Linked', 'Multi', 'Null']
class Axf_svbrdf(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Axf_svbrdf
        
        .. raw:: html
    
            <iframe id=Axf_svbrdf" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/axf-svbrdf.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/axf-svbrdf.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getDiffuse_model(self) -> str:
        """
        Get the diffuse-model parameter
        """
    def getDiffuse_modelChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getFresnel(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the fresnel node 
        """
    def getRoughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the roughness node 
        """
    def getUvtran(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the uvtran parameter
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffuse node 
        """
    def setDiffuse_model(self, diffuse_model: str) -> bool:
        """
        Set the diffuse-model parameter
        """
    def setFresnel(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the fresnel node 
        """
    def setRoughness(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the roughness node 
        """
    def setUvtran(self, uvtran: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the uvtran parameter
        """
class Blend(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Blend
        
        .. raw:: html
    
            <iframe id=Blend" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/blend.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/blend.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getBlend(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the blend node 
        """
    def getForcestep(self) -> bool:
        """
        Get the forcestep parameter
        """
    def getMaterial_a(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the material_a node 
        """
    def getMaterial_b(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the material_b node 
        """
    def setBlend(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the blend node 
        """
    def setForcestep(self, forcestep: bool) -> bool:
        """
        Set the forcestep parameter
        """
    def setMaterial_a(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the material_a node 
        """
    def setMaterial_b(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the material_b node 
        """
class Clone(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Clone
    """
    def __init__(self, name: str) -> None:
        ...
    def getTarget(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the target node 
        """
    def setTarget(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the target node 
        """
class Doublesided(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Doublesided
        
        .. raw:: html
    
            <iframe id=Doublesided" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/doublesided.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/doublesided.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getMaterial_b(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the material_b node 
        """
    def getMaterial_f(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the material_f node 
        """
    def setMaterial_b(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the material_b node 
        """
    def setMaterial_f(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the material_f node 
        """
class Generic(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Generic
        
        .. raw:: html
    
            <iframe id=Generic" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/generic.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/generic.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getBsdf(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the bsdf node 
        """
    def setBsdf(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the bsdf node 
        """
class Idealreflpolarizer(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Idealreflpolarizer
        
        .. raw:: html
    
            <iframe id=Idealreflpolarizer" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/idealreflpolarizer.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/idealreflpolarizer.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getF(self) -> float:
        """
        Get the F parameter
        """
    def getM00(self) -> float:
        """
        Get the m00 parameter
        """
    def getM01(self) -> float:
        """
        Get the m01 parameter
        """
    def getM02(self) -> float:
        """
        Get the m02 parameter
        """
    def getM03(self) -> float:
        """
        Get the m03 parameter
        """
    def getM10(self) -> float:
        """
        Get the m10 parameter
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
    def getM20(self) -> float:
        """
        Get the m20 parameter
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
    def getM30(self) -> float:
        """
        Get the m30 parameter
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
    def getPhase(self) -> float:
        """
        Get the phase parameter
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
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    @typing.overload
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    @typing.overload
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    def getValue(self) -> str:
        """
        Get the value parameter
        """
    def getValueChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def setF(self, F: float) -> bool:
        """
        Set the F parameter
        """
    def setM00(self, m00: float) -> bool:
        """
        Set the m00 parameter
        """
    def setM01(self, m01: float) -> bool:
        """
        Set the m01 parameter
        """
    def setM02(self, m02: float) -> bool:
        """
        Set the m02 parameter
        """
    def setM03(self, m03: float) -> bool:
        """
        Set the m03 parameter
        """
    def setM10(self, m10: float) -> bool:
        """
        Set the m10 parameter
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
    def setM20(self, m20: float) -> bool:
        """
        Set the m20 parameter
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
    def setM30(self, m30: float) -> bool:
        """
        Set the m30 parameter
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
    def setPhase(self, phase: float) -> bool:
        """
        Set the phase parameter
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
    def setValabs(self, valabs: float) -> bool:
        """
        Set the valabs parameter
        """
    @typing.overload
    def setValabs(self, valabs: float) -> bool:
        """
        Set the valabs parameter
        """
    @typing.overload
    def setValabs(self, valabs: float) -> bool:
        """
        Set the valabs parameter
        """
    def setValue(self, value: str) -> bool:
        """
        Set the value parameter
        """
class Idealtranspolarizer(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Idealtranspolarizer
        
        .. raw:: html
    
            <iframe id=Idealtranspolarizer" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/idealtranspolarizer.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/idealtranspolarizer.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getF(self) -> float:
        """
        Get the F parameter
        """
    def getM00(self) -> float:
        """
        Get the m00 parameter
        """
    def getM01(self) -> float:
        """
        Get the m01 parameter
        """
    def getM02(self) -> float:
        """
        Get the m02 parameter
        """
    def getM03(self) -> float:
        """
        Get the m03 parameter
        """
    def getM10(self) -> float:
        """
        Get the m10 parameter
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
    def getM20(self) -> float:
        """
        Get the m20 parameter
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
    def getM30(self) -> float:
        """
        Get the m30 parameter
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
    def getPhase(self) -> float:
        """
        Get the phase parameter
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
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    @typing.overload
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    @typing.overload
    def getValabs(self) -> float:
        """
        Get the valabs parameter
        """
    def getValue(self) -> str:
        """
        Get the value parameter
        """
    def getValueChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def setF(self, F: float) -> bool:
        """
        Set the F parameter
        """
    def setM00(self, m00: float) -> bool:
        """
        Set the m00 parameter
        """
    def setM01(self, m01: float) -> bool:
        """
        Set the m01 parameter
        """
    def setM02(self, m02: float) -> bool:
        """
        Set the m02 parameter
        """
    def setM03(self, m03: float) -> bool:
        """
        Set the m03 parameter
        """
    def setM10(self, m10: float) -> bool:
        """
        Set the m10 parameter
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
    def setM20(self, m20: float) -> bool:
        """
        Set the m20 parameter
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
    def setM30(self, m30: float) -> bool:
        """
        Set the m30 parameter
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
    def setPhase(self, phase: float) -> bool:
        """
        Set the phase parameter
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
    def setValabs(self, valabs: float) -> bool:
        """
        Set the valabs parameter
        """
    @typing.overload
    def setValabs(self, valabs: float) -> bool:
        """
        Set the valabs parameter
        """
    @typing.overload
    def setValabs(self, valabs: float) -> bool:
        """
        Set the valabs parameter
        """
    def setValue(self, value: str) -> bool:
        """
        Set the value parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Linked
        
        .. raw:: html
    
            <iframe id=Linked" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/linked.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/linked.html"></iframe>
    
        
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
class Multi(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Multi
    """
    def __init__(self, name: str) -> None:
        ...
class Null(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Null
        
        .. raw:: html
    
            <iframe id=Null" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/null.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/material/null.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
