from datetime import datetime
from agora_config import config
from agora_utils import AgoraTimeStamp

class MessageHeader:
    """ 
    Represents a MessageHeader that includes source module, message type, 
    config version, message ID, and timestamp.
    """
  
    # Static variable for tracking the message ID
    message_id = -1

    def __init__(self):
        """
        Initialize a MessageHeader instance with default attributes.
        
        Attributes:
            SrcModule (str): Source module name, taken from the application config.
            MessageType (str): Type of the message, default is 'NotSet'.
            ConfigVersion (int): Configuration version, default is -1.
            MessageID (int): Unique identifier for the message.
            TimeStamp (float): Timestamp for the message, based on AgoraTimeStamp.
        """
        
        self.SrcModule: str = config["Name"]
        self.MessageType: str = "NotSet"
        self.ConfigVersion: int = -1
        if MessageHeader.message_id == -1:
            MessageHeader.message_id = MessageHeader.__get_message_id()
        MessageHeader.message_id = MessageHeader.message_id + 1
        self.MessageID: int = MessageHeader.message_id
        self.TimeStamp: float = AgoraTimeStamp()

    @staticmethod
    def __get_message_id() -> int:
        """
        Generate a message ID based on the number of seconds from the start of the year 
        to the current moment, multiplied by 10.
        
        Returns:
            int: A unique message ID based on the time elapsed from the start of the year.
        """
        
        utcnow = datetime.utcnow()
        beginning_of_year = datetime(utcnow.year, 1, 1)
        time_difference = utcnow - beginning_of_year
        return int(time_difference.total_seconds() * 10)
