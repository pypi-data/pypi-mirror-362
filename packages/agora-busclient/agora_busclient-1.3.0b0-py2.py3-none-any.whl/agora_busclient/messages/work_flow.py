from .dict_of_str import DictOfStr

class WorkFlow:
    """
    Represents a WorkFlow with a specific Type and Properties.
    
    Attributes:
        Type (str): The type of the WorkFlow. 
        Properties (dict): A dictionary holding various properties related to the WorkFlow.
    """
  
    def __init__(self):
        """
        Initialize a WorkFlow instance with default attributes.
        """
        # Initialize the type as an empty string
        self.Type = ""
        
        # Initialize an empty dictionary for properties
        self.Properties = DictOfStr()

    @property
    def Properties(self):
        return self._properties

    @Properties.setter
    def Properties(self, value):
        if not isinstance(value, dict):
            raise TypeError("Properties must be a dictionary")

        for key, val in value.items():
            if not isinstance(key, str) or not isinstance(val, str):
                raise TypeError("All keys and values in Dictionary must be strings")

        self._properties = value