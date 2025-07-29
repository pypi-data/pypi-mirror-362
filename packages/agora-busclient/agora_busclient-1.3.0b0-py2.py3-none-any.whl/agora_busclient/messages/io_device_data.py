from .io_tag_data_dict import IoTagDataDict

class IoDeviceData:
    """ 
    Represents an IO Device that contains a collection of IO tags. 
    Each IoDeviceData object has an ID and a dictionary of tags mapped to IoPoint objects.
    """
  
    def __init__(self, id: str):
        """
        Initialize an IoDeviceData instance.
        
        Args:
            id (str): Unique identifier for the IO Device.
        
        Attributes:
            id (str): Unique identifier for the IO Device.
            tags (IoTagDataDict): Dictionary that holds IoPoint objects, 
                                  keyed by their corresponding tag names.
        """
        self.id: str = str(id)
        self.tags: IoTagDataDict = IoTagDataDict()
