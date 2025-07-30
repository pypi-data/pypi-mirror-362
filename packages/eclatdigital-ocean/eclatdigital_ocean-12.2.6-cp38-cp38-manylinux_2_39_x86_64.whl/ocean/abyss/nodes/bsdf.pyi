from __future__ import annotations
import ocean.abyss.nodes
__all__ = ['Additive', 'Black', 'Blend', 'Carpaint', 'Coateddiffuse', 'Doublesided', 'Equisolidtable', 'Fluo_lambertian', 'Fluo_oren_nayar', 'Glossy', 'Igloomatrix', 'Isomap', 'Lambertian', 'Lambertian_transmitter', 'Linked', 'Lobe', 'Null', 'Oren_nayar', 'Phong', 'Reflective', 'Reflective_diffraction_map', 'Refractive', 'Rusinkiewicztable', 'Simpleisotable', 'Sparklify', 'Specular', 'Switch', 'Velvet']
class Additive(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Additive
        
        .. raw:: html
    
            <iframe id=Additive" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/additive.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/additive.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Black(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Black
        
        .. raw:: html
    
            <iframe id=Black" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/black.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/black.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Blend(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Blend
        
        .. raw:: html
    
            <iframe id=Blend" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/blend.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/blend.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getBlend(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the blend node 
        """
    def setBlend(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the blend node 
        """
class Carpaint(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Carpaint
        
        .. raw:: html
    
            <iframe id=Carpaint" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/carpaint.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/carpaint.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffusionthickness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffusionthickness node 
        """
    def getDye(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dye node 
        """
    def getIor(self) -> float:
        """
        Get the ior parameter
        """
    def getParticle(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the particle node 
        """
    def getParticledisalignment(self) -> float:
        """
        Get the particledisalignment parameter
        """
    def getParticleroughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the particleroughness node 
        """
    def getParticlesize(self) -> float:
        """
        Get the particlesize parameter
        """
    def getPigment(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the pigment node 
        """
    def getSurfaceroughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the surfaceroughness node 
        """
    def setDiffusionthickness(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffusionthickness node 
        """
    def setDye(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the dye node 
        """
    def setIor(self, ior: float) -> bool:
        """
        Set the ior parameter
        """
    def setParticle(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the particle node 
        """
    def setParticledisalignment(self, particledisalignment: float) -> bool:
        """
        Set the particledisalignment parameter
        """
    def setParticleroughness(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the particleroughness node 
        """
    def setParticlesize(self, particlesize: float) -> bool:
        """
        Set the particlesize parameter
        """
    def setPigment(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the pigment node 
        """
    def setSurfaceroughness(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the surfaceroughness node 
        """
class Coateddiffuse(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Coateddiffuse
        
        .. raw:: html
    
            <iframe id=Coateddiffuse" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/coateddiffuse.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/coateddiffuse.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getCoatingthickness(self) -> float:
        """
        Get the coatingthickness parameter
        """
    def getDielectricfunc(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the dielectricfunc node 
        """
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def setCoatingthickness(self, coatingthickness: float) -> bool:
        """
        Set the coatingthickness parameter
        """
    def setDielectricfunc(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the dielectricfunc node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffuse node 
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the intlaw node 
        """
class Doublesided(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Doublesided
        
        .. raw:: html
    
            <iframe id=Doublesided" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/doublesided.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/doublesided.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getBack(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the back node 
        """
    def getFront(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the front node 
        """
    def setBack(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the back node 
        """
    def setFront(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the front node 
        """
class Equisolidtable(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Equisolidtable
        
        .. raw:: html
    
            <iframe id=Equisolidtable" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/equisolidtable.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/equisolidtable.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAniso_sym(self) -> int:
        """
        Get the aniso_sym parameter
        """
    def getKh_corr(self) -> bool:
        """
        Get the kh_corr parameter
        """
    def getNumphii(self) -> int:
        """
        Get the numphii parameter
        """
    def getNumthetai(self) -> int:
        """
        Get the numthetai parameter
        """
    def setAniso_sym(self, aniso_sym: int) -> bool:
        """
        Set the aniso_sym parameter
        """
    def setKh_corr(self, kh_corr: bool) -> bool:
        """
        Set the kh_corr parameter
        """
    def setNumphii(self, numphii: int) -> bool:
        """
        Set the numphii parameter
        """
    def setNumthetai(self, numthetai: int) -> bool:
        """
        Set the numthetai parameter
        """
class Fluo_lambertian(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Fluo_lambertian
        
        .. raw:: html
    
            <iframe id=Fluo_lambertian" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/fluo_lambertian.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/fluo_lambertian.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAbsorption(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the absorption node 
        """
    def getConcentrationParameter(self) -> float:
        """
        Get the concentrationParameter parameter
        """
    def getDiffusion(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffusion node 
        """
    def getEmission(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the emission node 
        """
    def getQuantumYield(self) -> float:
        """
        Get the quantumYield parameter
        """
    def setAbsorption(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the absorption node 
        """
    def setConcentrationParameter(self, concentrationParameter: float) -> bool:
        """
        Set the concentrationParameter parameter
        """
    def setDiffusion(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffusion node 
        """
    def setEmission(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the emission node 
        """
    def setQuantumYield(self, quantumYield: float) -> bool:
        """
        Set the quantumYield parameter
        """
class Fluo_oren_nayar(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Fluo_oren_nayar
        
        .. raw:: html
    
            <iframe id=Fluo_oren_nayar" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/fluo_oren_nayar.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/fluo_oren_nayar.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAbsorption(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the absorption node 
        """
    def getConcentrationParameter(self) -> float:
        """
        Get the concentrationParameter parameter
        """
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getEmission(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the emission node 
        """
    def getQuantumYield(self) -> float:
        """
        Get the quantumYield parameter
        """
    def getSigma(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sigma node 
        """
    def setAbsorption(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the absorption node 
        """
    def setConcentrationParameter(self, concentrationParameter: float) -> bool:
        """
        Set the concentrationParameter parameter
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffuse node 
        """
    def setEmission(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the emission node 
        """
    def setQuantumYield(self, quantumYield: float) -> bool:
        """
        Set the quantumYield parameter
        """
    def setSigma(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sigma node 
        """
class Glossy(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Glossy
        
        .. raw:: html
    
            <iframe id=Glossy" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/glossy.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/glossy.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getIor(self) -> float:
        """
        Get the ior parameter
        """
    def getRoughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the roughness node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffuse node 
        """
    def setIor(self, ior: float) -> bool:
        """
        Set the ior parameter
        """
    def setRoughness(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the roughness node 
        """
class Igloomatrix(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Igloomatrix
        
        .. raw:: html
    
            <iframe id=Igloomatrix" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/igloomatrix.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/igloomatrix.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getBrdf_back(self) -> dict:
        """
        Get the brdf_back parameter
        """
    def getBrdf_front(self) -> dict:
        """
        Get the brdf_front parameter
        """
    def getBtdf(self) -> dict:
        """
        Get the btdf parameter
        """
    def getNumphi(self) -> dict:
        """
        Get the numphi parameter
        """
    def getTheta(self) -> dict:
        """
        Get the theta parameter
        """
    def setBrdf_back(self, brdf_back: dict) -> bool:
        """
        Set the brdf_back parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setBrdf_front(self, brdf_front: dict) -> bool:
        """
        Set the brdf_front parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setBtdf(self, btdf: dict) -> bool:
        """
        Set the btdf parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setNumphi(self, numphi: dict) -> bool:
        """
        Set the numphi parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setTheta(self, theta: dict) -> bool:
        """
        Set the theta parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
class Isomap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Isomap
        
        .. raw:: html
    
            <iframe id=Isomap" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/isomap.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/isomap.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getThetas(self) -> dict:
        """
        Get the thetas parameter
        """
    def setThetas(self, thetas: dict) -> bool:
        """
        Set the thetas parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
class Lambertian(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Lambertian
        
        .. raw:: html
    
            <iframe id=Lambertian" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/lambertian.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/lambertian.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffuse node 
        """
class Lambertian_transmitter(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Lambertian_transmitter
        
        .. raw:: html
    
            <iframe id=Lambertian_transmitter" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/lambertiantransmitter.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/lambertiantransmitter.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffuse node 
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Linked
        
        .. raw:: html
    
            <iframe id=Linked" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/linked.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/linked.html"></iframe>
    
        
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
class Lobe(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Lobe
        
        .. raw:: html
    
            <iframe id=Lobe" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/lobe.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/lobe.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getLobe(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the lobe node 
        """
    def setLobe(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the lobe node 
        """
class Null(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Null
        
        .. raw:: html
    
            <iframe id=Null" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/null.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/null.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
class Oren_nayar(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Oren_nayar
        
        .. raw:: html
    
            <iframe id=Oren_nayar" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/oren_nayar.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/oren_nayar.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getSigma(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sigma node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffuse node 
        """
    def setSigma(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sigma node 
        """
class Phong(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Phong
        
        .. raw:: html
    
            <iframe id=Phong" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/phong.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/phong.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getExponent(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the exponent node 
        """
    def getIor(self) -> float:
        """
        Get the ior parameter
        """
    def getSpecular(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the specular node 
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffuse node 
        """
    def setExponent(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the exponent node 
        """
    def setIor(self, ior: float) -> bool:
        """
        Set the ior parameter
        """
    def setSpecular(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the specular node 
        """
class Reflective(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Reflective
        
        .. raw:: html
    
            <iframe id=Reflective" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/reflective.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/reflective.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def getRereflections(self) -> bool:
        """
        Get the rereflections parameter
        """
    def getRoughness(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the roughness node 
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the intlaw node 
        """
    def setRereflections(self, rereflections: bool) -> bool:
        """
        Set the rereflections parameter
        """
    def setRoughness(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the roughness node 
        """
class Reflective_diffraction_map(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Reflective_diffraction_map
        
        .. raw:: html
    
            <iframe id=Reflective_diffraction_map" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/reflective_diffraction_map.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/reflective_diffraction_map.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDispersion_power(self) -> float:
        """
        Get the dispersion_power parameter
        """
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def getLambda_map(self) -> float:
        """
        Get the lambda_map parameter
        """
    def getLambda_max(self) -> float:
        """
        Get the lambda_max parameter
        """
    def getLambda_min(self) -> float:
        """
        Get the lambda_min parameter
        """
    def getTheta_max(self) -> float:
        """
        Get the theta_max parameter
        """
    def setDispersion_power(self, dispersion_power: float) -> bool:
        """
        Set the dispersion_power parameter
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the intlaw node 
        """
    def setLambda_map(self, lambda_map: float) -> bool:
        """
        Set the lambda_map parameter
        """
    def setLambda_max(self, lambda_max: float) -> bool:
        """
        Set the lambda_max parameter
        """
    def setLambda_min(self, lambda_min: float) -> bool:
        """
        Set the lambda_min parameter
        """
    def setTheta_max(self, theta_max: float) -> bool:
        """
        Set the theta_max parameter
        """
class Refractive(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Refractive
        
        .. raw:: html
    
            <iframe id=Refractive" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/refractive.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/refractive.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def getRereflections(self) -> bool:
        """
        Get the rereflections parameter
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the intlaw node 
        """
    def setRereflections(self, rereflections: bool) -> bool:
        """
        Set the rereflections parameter
        """
class Rusinkiewicztable(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Rusinkiewicztable
        
        .. raw:: html
    
            <iframe id=Rusinkiewicztable" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/rusinkiewicztable.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/rusinkiewicztable.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getNum_phi_d(self) -> dict:
        """
        Get the num_phi_d parameter
        """
    def getNum_phi_h(self) -> dict:
        """
        Get the num_phi_h parameter
        """
    def getPhi_h_sym(self) -> int:
        """
        Get the phi_h_sym parameter
        """
    def getTheta_h(self) -> dict:
        """
        Get the theta_h parameter
        """
    def getTransmission(self) -> bool:
        """
        Get the transmission parameter
        """
    def getValues(self) -> dict:
        """
        Get the values parameter
        """
    def setNum_phi_d(self, num_phi_d: dict) -> bool:
        """
        Set the num_phi_d parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setNum_phi_h(self, num_phi_h: dict) -> bool:
        """
        Set the num_phi_h parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setPhi_h_sym(self, phi_h_sym: int) -> bool:
        """
        Set the phi_h_sym parameter
        """
    def setTheta_h(self, theta_h: dict) -> bool:
        """
        Set the theta_h parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setTransmission(self, transmission: bool) -> bool:
        """
        Set the transmission parameter
        """
    def setValues(self, values: dict) -> bool:
        """
        Set the values parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
class Simpleisotable(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Simpleisotable
        
        .. raw:: html
    
            <iframe id=Simpleisotable" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/simpleisotable.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/simpleisotable.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getNum_phi_out(self) -> int:
        """
        Get the num_phi_out parameter
        """
    def getPhi_out_sym(self) -> int:
        """
        Get the phi_out_sym parameter
        """
    def getTheta_in(self) -> dict:
        """
        Get the theta_in parameter
        """
    def getTheta_out(self) -> dict:
        """
        Get the theta_out parameter
        """
    def getValues(self) -> dict:
        """
        Get the values parameter
        """
    def setNum_phi_out(self, num_phi_out: int) -> bool:
        """
        Set the num_phi_out parameter
        """
    def setPhi_out_sym(self, phi_out_sym: int) -> bool:
        """
        Set the phi_out_sym parameter
        """
    def setTheta_in(self, theta_in: dict) -> bool:
        """
        Set the theta_in parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setTheta_out(self, theta_out: dict) -> bool:
        """
        Set the theta_out parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setValues(self, values: dict) -> bool:
        """
        Set the values parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
class Sparklify(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Sparklify
        
        .. raw:: html
    
            <iframe id=Sparklify" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/sparklify.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/sparklify.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAverage(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the average node 
        """
    def getDensity(self) -> float:
        """
        Get the density parameter
        """
    def getRoughness(self) -> dict:
        """
        Get the roughness parameter
        """
    def setAverage(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the average node 
        """
    def setDensity(self, density: float) -> bool:
        """
        Set the density parameter
        """
    def setRoughness(self, roughness: dict) -> bool:
        """
        Set the roughness parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
class Specular(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Specular
        
        .. raw:: html
    
            <iframe id=Specular" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/specular.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/specular.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getIntlaw(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the intlaw node 
        """
    def getIrtrmin_tweak(self) -> float:
        """
        Get the irtrmin_tweak parameter
        """
    def setIntlaw(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the intlaw node 
        """
    def setIrtrmin_tweak(self, irtrmin_tweak: float) -> bool:
        """
        Set the irtrmin_tweak parameter
        """
class Switch(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Switch
        
        .. raw:: html
    
            <iframe id=Switch" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/switch.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/switch.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getSwitch(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the switch node 
        """
    def setSwitch(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the switch node 
        """
class Velvet(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Velvet
        
        .. raw:: html
    
            <iframe id=Velvet" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/velvet.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/bsdf/velvet.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getDiffuse(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the diffuse node 
        """
    def getRebounce(self) -> float:
        """
        Get the rebounce parameter
        """
    def getSigma(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sigma node 
        """
    def getSpread(self) -> float:
        """
        Get the spread parameter
        """
    def setDiffuse(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the diffuse node 
        """
    def setRebounce(self, rebounce: float) -> bool:
        """
        Set the rebounce parameter
        """
    def setSigma(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sigma node 
        """
    def setSpread(self, spread: float) -> bool:
        """
        Set the spread parameter
        """
