from __future__ import annotations
import numpy
import ocean.abyss.nodes
__all__ = ['Bsdfcapture', 'Defaultrawinstrument', 'Fisheyecam', 'Fouriercam', 'Idealrectcam', 'Imported', 'Irradorthoview', 'Irradperspview', 'Irradsphereview', 'Lightmap', 'Linked', 'Materialirrad', 'Orthocam', 'Realrectcam', 'Spherecam', 'Stdcam']
class Bsdfcapture(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Bsdfcapture
        
        .. raw:: html
    
            <iframe id=Bsdfcapture" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/bsdfcapture.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/bsdfcapture.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAniso_sym(self) -> str:
        """
        Get the aniso_sym parameter
        """
    def getAniso_symChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getAnisotropy(self) -> str:
        """
        Get the anisotropy parameter
        """
    def getAnisotropyChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getIntent(self) -> str:
        """
        Get the intent parameter
        """
    def getIntentChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getNormal(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the normal parameter
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getReflection(self) -> str:
        """
        Get the reflection parameter
        """
    def getReflectionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getResolution(self) -> str:
        """
        Get the resolution parameter
        """
    def getResolutionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSpotradius(self) -> float:
        """
        Get the spotradius parameter
        """
    def getTangent(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the tangent parameter
        """
    def getTransmission(self) -> str:
        """
        Get the transmission parameter
        """
    def getTransmissionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def setAniso_sym(self, aniso_sym: str) -> bool:
        """
        Set the aniso_sym parameter
        """
    def setAnisotropy(self, anisotropy: str) -> bool:
        """
        Set the anisotropy parameter
        """
    def setIntent(self, intent: str) -> bool:
        """
        Set the intent parameter
        """
    def setNormal(self, normal: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the normal parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setReflection(self, reflection: str) -> bool:
        """
        Set the reflection parameter
        """
    def setResolution(self, resolution: str) -> bool:
        """
        Set the resolution parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setSpotradius(self, spotradius: float) -> bool:
        """
        Set the spotradius parameter
        """
    def setTangent(self, tangent: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the tangent parameter
        """
    def setTransmission(self, transmission: str) -> bool:
        """
        Set the transmission parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
class Defaultrawinstrument(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Defaultrawinstrument
        
        .. raw:: html
    
            <iframe id=Defaultrawinstrument" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/defaultrawinstrument.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/defaultrawinstrument.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Fisheyecam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Fisheyecam
        
        .. raw:: html
    
            <iframe id=Fisheyecam" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/fisheyecam.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/fisheyecam.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getProjection(self) -> str:
        """
        Get the projection parameter
        """
    def getProjectionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: float) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocusdistance(self, focusdistance: float) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setProjection(self, projection: str) -> bool:
        """
        Set the projection parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: float) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_width(self, sensor_width: float) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Fouriercam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    Fouriercam
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getLensradius(self) -> float:
        """
        Get the lensradius parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getProjection(self) -> str:
        """
        Get the projection parameter
        """
    def getProjectionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getSpotradius(self) -> float:
        """
        Get the spotradius parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setLensradius(self, lensradius: float) -> bool:
        """
        Set the lensradius parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setProjection(self, projection: str) -> bool:
        """
        Set the projection parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: float) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_width(self, sensor_width: float) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setSpotradius(self, spotradius: float) -> bool:
        """
        Set the spotradius parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Idealrectcam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Idealrectcam
        
        .. raw:: html
    
            <iframe id=Idealrectcam" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/idealrectcam.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/idealrectcam.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocallength(self) -> float:
        """
        Get the focallength parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_shift_x(self) -> float:
        """
        Get the sensor_shift_x parameter
        """
    def getSensor_shift_y(self) -> float:
        """
        Get the sensor_shift_y parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: float) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocallength(self, focallength: float) -> bool:
        """
        Set the focallength parameter
        """
    def setFocusdistance(self, focusdistance: float) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: float) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_shift_x(self, sensor_shift_x: float) -> bool:
        """
        Set the sensor_shift_x parameter
        """
    def setSensor_shift_y(self, sensor_shift_y: float) -> bool:
        """
        Set the sensor_shift_y parameter
        """
    def setSensor_width(self, sensor_width: float) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Imported(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Imported
        
        .. raw:: html
    
            <iframe id=Imported" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/imported.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/imported.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getRtfs(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the rtfs node 
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_offset(self) -> float:
        """
        Get the sensor_offset parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setRtfs(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the rtfs node 
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setSensor_offset(self, sensor_offset: float) -> bool:
        """
        Set the sensor_offset parameter
        """
    def setSensor_width(self, sensor_width: float) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Irradorthoview(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Irradorthoview
        
        .. raw:: html
    
            <iframe id=Irradorthoview" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/irradorthoview.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/irradorthoview.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getHeight(self) -> float:
        """
        Get the height parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWidth(self) -> float:
        """
        Get the width parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setHeight(self, height: float) -> bool:
        """
        Set the height parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWidth(self, width: float) -> bool:
        """
        Set the width parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Irradperspview(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Irradperspview
        
        .. raw:: html
    
            <iframe id=Irradperspview" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/irradperspview.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/irradperspview.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getFocallength(self) -> float:
        """
        Get the focallength parameter
        """
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setFocallength(self, focallength: float) -> bool:
        """
        Set the focallength parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: float) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_width(self, sensor_width: float) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Irradsphereview(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Irradsphereview
        
        .. raw:: html
    
            <iframe id=Irradsphereview" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/irradsphereview.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/irradsphereview.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Lightmap(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Lightmap
        
        .. raw:: html
    
            <iframe id=Lightmap" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/lightmap.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/lightmap.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getMaterial(self) -> str:
        """
        Get the material parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUmax(self) -> float:
        """
        Get the umax parameter
        """
    def getUmin(self) -> float:
        """
        Get the umin parameter
        """
    def getUv_window(self) -> str:
        """
        Get the uv_window parameter
        """
    def getUv_windowChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getVmax(self) -> float:
        """
        Get the vmax parameter
        """
    def getVmin(self) -> float:
        """
        Get the vmin parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setMaterial(self, material: str) -> bool:
        """
        Set the material parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUmax(self, umax: float) -> bool:
        """
        Set the umax parameter
        """
    def setUmin(self, umin: float) -> bool:
        """
        Set the umin parameter
        """
    def setUv_window(self, uv_window: str) -> bool:
        """
        Set the uv_window parameter
        """
    def setVmax(self, vmax: float) -> bool:
        """
        Set the vmax parameter
        """
    def setVmin(self, vmin: float) -> bool:
        """
        Set the vmin parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Linked(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Linked
        
        .. raw:: html
    
            <iframe id=Linked" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/linked.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/linked.html"></iframe>
    
        
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
class Materialirrad(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Materialirrad
        
        .. raw:: html
    
            <iframe id=Materialirrad" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/materialirrad.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/materialirrad.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getMatlist(self) -> dict:
        """
        Get the matlist parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def setMatlist(self, matlist: dict) -> bool:
        """
        Set the matlist parameter
                            Table is passed as a dict with this format:
        
                            .. code-block:: python
        
                                table = {"colname_0": np.array(...),"colname_1": np.array(...)}
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
class Orthocam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Orthocam
        
        .. raw:: html
    
            <iframe id=Orthocam" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/orthocam.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/orthocam.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getHeight(self) -> float:
        """
        Get the height parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWidth(self) -> float:
        """
        Get the width parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setHeight(self, height: float) -> bool:
        """
        Set the height parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWidth(self, width: float) -> bool:
        """
        Set the width parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Realrectcam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Realrectcam
        
        .. raw:: html
    
            <iframe id=Realrectcam" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/realrectcam.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/realrectcam.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAcoma(self) -> float:
        """
        Get the acoma parameter
        """
    def getAcurvature(self) -> float:
        """
        Get the acurvature parameter
        """
    def getAradial(self) -> float:
        """
        Get the aradial parameter
        """
    def getAspherical(self) -> float:
        """
        Get the aspherical parameter
        """
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocallength(self) -> float:
        """
        Get the focallength parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAcoma(self, acoma: float) -> bool:
        """
        Set the acoma parameter
        """
    def setAcurvature(self, acurvature: float) -> bool:
        """
        Set the acurvature parameter
        """
    def setAradial(self, aradial: float) -> bool:
        """
        Set the aradial parameter
        """
    def setAspherical(self, aspherical: float) -> bool:
        """
        Set the aspherical parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: float) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocallength(self, focallength: float) -> bool:
        """
        Set the focallength parameter
        """
    def setFocusdistance(self, focusdistance: float) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: float) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_width(self, sensor_width: float) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Spherecam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Spherecam
        
        .. raw:: html
    
            <iframe id=Spherecam" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/spherecam.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/spherecam.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getRadius(self) -> float:
        """
        Get the radius parameter
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: float) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocusdistance(self, focusdistance: float) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setRadius(self, radius: float) -> bool:
        """
        Set the radius parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
class Stdcam(ocean.abyss.nodes.Node, ocean.abyss.nodes.CNodeHandler):
    """
    
        Stdcam
        
        .. raw:: html
    
            <iframe id=Stdcam" src="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/stdcam.html"loading="lazy" alt="https://docs.eclat-digital.com/ocean2024-docs/reference/nodes/instrument/stdcam.html"></iframe>
    
        
    """
    def __init__(self, name: str) -> None:
        ...
    def getAutofocus(self) -> bool:
        """
        Get the autofocus parameter
        """
    def getFnumber(self) -> float:
        """
        Get the fnumber parameter
        """
    def getFocallength(self) -> float:
        """
        Get the focallength parameter
        """
    def getFocusdistance(self) -> float:
        """
        Get the focusdistance parameter
        """
    def getForwards(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the forwards parameter
        """
    def getPixelfilter(self) -> str:
        """
        Get the pixelfilter parameter
        """
    def getPixelfilterChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getPos(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the pos parameter
        """
    def getProjection(self) -> str:
        """
        Get the projection parameter
        """
    def getProjectionChoices(self) -> list:
        """
        Retrieve the possible choices
        """
    def getSensor(self) -> ocean.abyss.nodes.Node:
        """
                    Retrieve the sensor node 
        """
    def getSensor_ar(self) -> float:
        """
        Get the sensor_ar parameter
        """
    def getSensor_shift_x(self) -> float:
        """
        Get the sensor_shift_x parameter
        """
    def getSensor_shift_y(self) -> float:
        """
        Get the sensor_shift_y parameter
        """
    def getSensor_width(self) -> float:
        """
        Get the sensor_width parameter
        """
    def getShutter(self) -> float:
        """
        Get the shutter parameter
        """
    def getUp(self) -> numpy.ndarray[numpy.float32]:
        """
        Get the up parameter
        """
    def getWlmax(self) -> float:
        """
        Get the wlmax parameter
        """
    def getWlmin(self) -> float:
        """
        Get the wlmin parameter
        """
    def getXresolution(self) -> int:
        """
        Get the xresolution parameter
        """
    def getYresolution(self) -> int:
        """
        Get the yresolution parameter
        """
    def setAutofocus(self, autofocus: bool) -> bool:
        """
        Set the autofocus parameter
        """
    def setFnumber(self, fnumber: float) -> bool:
        """
        Set the fnumber parameter
        """
    def setFocallength(self, focallength: float) -> bool:
        """
        Set the focallength parameter
        """
    def setFocusdistance(self, focusdistance: float) -> bool:
        """
        Set the focusdistance parameter
        """
    def setForwards(self, forwards: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the forwards parameter
        """
    def setPixelfilter(self, pixelfilter: str) -> bool:
        """
        Set the pixelfilter parameter
        """
    def setPos(self, pos: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the pos parameter
        """
    def setProjection(self, projection: str) -> bool:
        """
        Set the projection parameter
        """
    def setSensor(self, arg0: ocean.abyss.nodes.Node) -> bool:
        """
                    Set the sensor node 
        """
    def setSensor_ar(self, sensor_ar: float) -> bool:
        """
        Set the sensor_ar parameter
        """
    def setSensor_shift_x(self, sensor_shift_x: float) -> bool:
        """
        Set the sensor_shift_x parameter
        """
    def setSensor_shift_y(self, sensor_shift_y: float) -> bool:
        """
        Set the sensor_shift_y parameter
        """
    def setSensor_width(self, sensor_width: float) -> bool:
        """
        Set the sensor_width parameter
        """
    def setShutter(self, shutter: float) -> bool:
        """
        Set the shutter parameter
        """
    def setUp(self, up: numpy.ndarray[numpy.float32]) -> bool:
        """
        Set the up parameter
        """
    def setWlmax(self, wlmax: float) -> bool:
        """
        Set the wlmax parameter
        """
    def setWlmin(self, wlmin: float) -> bool:
        """
        Set the wlmin parameter
        """
    def setXresolution(self, xresolution: int) -> bool:
        """
        Set the xresolution parameter
        """
    def setYresolution(self, yresolution: int) -> bool:
        """
        Set the yresolution parameter
        """
