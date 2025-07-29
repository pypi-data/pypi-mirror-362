from typing import List
from .io_device_data import IoDeviceData
from .io_point import IoPoint
from .message_header import MessageHeader

class IoDataReportMsg:
    """ 
    Represents an IoDataReport message that includes versioning, header information, 
    and a list of IoDeviceData objects.
    """
  
    default_device_id = "999"

    def __init__(self):
        """
        Initialize an IoDataReportMsg instance with default attributes.
        
        Attributes:
            version (int): Version number of the IoDataReport message.
            header (MessageHeader): Header information for the IoDataReport message.
            device (List[IoDeviceData]): List of IoDeviceData objects included in the report.
        """
        self.version: int = 1
        self.header: MessageHeader = MessageHeader()
        self.header.Compressed: bool = False
        self.header.MessageType: str = "IODataReport"
        self.header.ConfigVersion: int = self.version
        self.device: List[IoDeviceData] = []

    def get_device_data(self, device_id: str) -> IoDeviceData:
        """
        Retrieve device data for a specific device ID.
        
        Args:
            device_id (str): Unique identifier for the IO Device.
        
        Returns:
            IoDeviceData: Device data for the given device ID, or None if not found.
        """
        return next((iod_item for iod_item in self.device if iod_item.id == device_id), None)

    def add_device_data(self, device_id: str, tagname: str, io_point: IoPoint):
        """
        Add IoPoint data to a specific device ID and tag name.
        
        Args:
            device_id (str): Unique identifier for the IO Device.
            tagname (str): The tag name to associate with the IoPoint.
            io_point (IoPoint): The IoPoint object to add.
        """
        if tagname:
            io_d_data = self.get_device_data(device_id)
            if io_d_data is None:
                device = IoDeviceData(device_id)
                self.device.append(device)
                io_d_data = device
            io_d_data.tags[tagname] = io_point

    def add_data(self, tagname: str, io_point: IoPoint):
        """
        Add IoPoint data to a default device ID and tag name.
        
        Args:
            tagname (str): The tag name to associate with the IoPoint.
            io_point (IoPoint): The IoPoint object to add.
        """
        self.add_device_data(IoDataReportMsg.default_device_id, tagname, io_point)

    def get(self, device_id: str, tagname: str) -> IoPoint:
        """
        Retrieve an IoPoint object for a specific device ID and tag name.
        
        Args:
            device_id (str): Unique identifier for the IO Device.
            tagname (str): The tag name associated with the IoPoint.
        
        Returns:
            IoPoint: The IoPoint object for the given device ID and tag name, or None if not found.
        """
        if tagname:
            io_d_data = self.get_device_data(device_id)
            return None if io_d_data is None else io_d_data.tags.get(tagname)
