from .io_point import IoPoint
from typing import Dict

class IoTagDataDict(Dict[str, IoPoint]):
    """ 
    Represents a dictionary of IO tags mapped to their respective IoPoint instances.
    Inherits from Python's built-in Dict class and overrides some methods to ensure 
    type safety and specific functionality related to IoPoints.
    """
  
    def __init__(self, *args, **kwargs):
        """
        Initialize an IoTagDataDict instance. Calls the superclass constructor 
        to inherit the properties of a standard Python dictionary.
        
        Args:
            *args: Variable length argument list passed to the Dict constructor.
            **kwargs: Arbitrary keyword arguments passed to the Dict constructor.
        """
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: str, value: IoPoint):
        """
        Overrides the standard dictionary __setitem__ method to include a type check.
        Ensures that values being set are instances of IoPoint.
        
        Args:
            key (str): The tag (key) against which the IoPoint object is to be stored.
            value (IoPoint): The IoPoint object to be stored against the key.
        
        Raises:
            ValueError: If the value is not an instance of IoPoint.
        """
        if not isinstance(value, IoPoint):
            raise ValueError("Value must be an instance of IoPoint")
        super().__setitem__(key, value)
