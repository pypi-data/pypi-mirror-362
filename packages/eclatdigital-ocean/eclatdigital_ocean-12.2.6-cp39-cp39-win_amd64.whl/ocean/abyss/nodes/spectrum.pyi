from __future__ import annotations
import numpy
import ocean.abyss.nodes
__all__ = ['Abbenumber', 'Blackbody', 'Cauchy', 'Cie_xyz', 'Linked', 'Preset', 'Rgb', 'Square', 'Tabulated', 'Triangle', 'Uniform']
class Abbenumber(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Abbenumber
        
        .. raw:: html
    
            <iframe id=Abbenumber" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/abbenumber.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/abbenumber.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getNd(self) -> float:
        """
        Get the nd parameter
        """
    def getVd(self) -> float:
        """
        Get the Vd parameter
        """
    def setNd(self, nd: float) -> bool:
        """
        Set the nd parameter
        """
    def setVd(self, Vd: float) -> bool:
        """
        Set the Vd parameter
        """
class Blackbody(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Blackbody
        
        .. raw:: html
    
            <iframe id=Blackbody" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/blackbody.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/blackbody.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getGain(self) -> float:
        """
        Get the gain parameter
        """
    def getTemp(self) -> float:
        """
        Get the temp parameter
        """
    def setGain(self, gain: float) -> bool:
        """
        Set the gain parameter
        """
    def setTemp(self, temp: float) -> bool:
        """
        Set the temp parameter
        """
class Cauchy(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Cauchy
        
        .. raw:: html
    
            <iframe id=Cauchy" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/cauchy.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/cauchy.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getB(self) -> float:
        """
        Get the b parameter
        """
    def getC(self) -> float:
        """
        Get the c parameter
        """
    def setB(self, b: float) -> bool:
        """
        Set the b parameter
        """
    def setC(self, c: float) -> bool:
        """
        Set the c parameter
        """
class Cie_xyz(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Cie_xyz
        
        .. raw:: html
    
            <iframe id=Cie_xyz" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/cie-xyz.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/cie-xyz.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getMode(self) -> str:
        """
        Get the mode parameter
        """
    def getModeChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getXyz(self) -> dict:
        """
        Get the xyz parameter
        """
    def setMode(self, mode: str) -> bool:
        """
        Set the mode parameter
        """
    def setXyz(self, xyz: dict) -> bool:
        """
        Set the xyz parameter
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
class Preset(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Preset
        
        .. raw:: html
    
            <iframe id=Preset" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/preset.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/preset.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getGain(self) -> float:
        """
        Get the gain parameter
        """
    def getValue(self) -> str:
        """
        Get the value parameter
        """
    def getValueChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def setGain(self, gain: float) -> bool:
        """
        Set the gain parameter
        """
    def setValue(self, value: str) -> bool:
        """
        Set the value parameter
        """
class Rgb(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Rgb
        
        .. raw:: html
    
            <iframe id=Rgb" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/rgb.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/rgb.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getGamma(self) -> float:
        """
        Get the gamma parameter
        """
    def getRgb(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the rgb parameter
        """
    def setGamma(self, gamma: float) -> bool:
        """
        Set the gamma parameter
        """
    def setRgb(self, rgb: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the rgb parameter
        """
class Square(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Square
        
        .. raw:: html
    
            <iframe id=Square" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/square.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/square.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getBase(self) -> float:
        """
        Get the base parameter
        """
    def getMax(self) -> float:
        """
        Get the max parameter
        """
    def getMin(self) -> float:
        """
        Get the min parameter
        """
    def getTop(self) -> float:
        """
        Get the top parameter
        """
    def setBase(self, base: float) -> bool:
        """
        Set the base parameter
        """
    def setMax(self, max: float) -> bool:
        """
        Set the max parameter
        """
    def setMin(self, min: float) -> bool:
        """
        Set the min parameter
        """
    def setTop(self, top: float) -> bool:
        """
        Set the top parameter
        """
class Tabulated(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Tabulated
        
        .. raw:: html
    
            <iframe id=Tabulated" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/tabulated.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/tabulated.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getData(self) -> dict:
        """
        Get the data parameter
        """
    def getRaw(self) -> numpy.ndarray[numpy.float32]:
        ...
    def setData(self, data: dict) -> bool:
        """
        Set the data parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setRaw(self, arg0: numpy.ndarray[numpy.float32]) -> bool:
        ...
class Triangle(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Triangle
    """
    def __init__(self, name: str) -> None:
        ...
    def getCenter(self) -> float:
        """
        Get the center parameter
        """
    def getMax(self) -> float:
        """
        Get the max parameter
        """
    def getMin(self) -> float:
        """
        Get the min parameter
        """
    def getTop(self) -> float:
        """
        Get the top parameter
        """
    def setCenter(self, center: float) -> bool:
        """
        Set the center parameter
        """
    def setMax(self, max: float) -> bool:
        """
        Set the max parameter
        """
    def setMin(self, min: float) -> bool:
        """
        Set the min parameter
        """
    def setTop(self, top: float) -> bool:
        """
        Set the top parameter
        """
class Uniform(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Uniform
        
        .. raw:: html
    
            <iframe id=Uniform" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/uniform.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/spectrum/uniform.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getValue(self) -> float:
        """
        Get the value parameter
        """
    def setValue(self, value: float) -> bool:
        """
        Set the value parameter
        """
