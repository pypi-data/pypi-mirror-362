from datetime import datetime
from agora_utils import AgoraTimeStamp
from agora_config import config
from .media_data import MediaData
from .work_flow import WorkFlow
from typing import List

class EventMsg:
    """ 
    Represents an event message with various attributes such as IDs, timestamps, 
    media data, and workflow details.
    """

    # Static variable for tracking the event ID
    event_id = -1

    def __init__(self):
        """
        Initialize an EventMsg instance with default attributes.

        Attributes:
            EventId (int): Unique identifier for the event message.
            GroupId (str): Group identifier, taken from the application config.
            GatewayId (str): Gateway identifier, taken from the application config.
            SlaveId (int): Default is 999.
            ControllerId (str): Device identifier, taken from the application config.
            Start_tm, End_tm, DetectedStart_tm, DetectedEnd_tm, Sent_tm, Created_tm, Detected_tm (int): Timestamps for various events.
            mediaDataRef (List[MediaData]): List to store references to MediaData objects.
            workFlow (WorkFlow): WorkFlow object to store the event's workflow details.
            Version (str): Schema version of the event message.
        """

        # Event ID logic
        if EventMsg.event_id == -1:
            EventMsg.event_id = self.__get_event_id()
        EventMsg.event_id = EventMsg.event_id + 1
        self.EventId = EventMsg.event_id
        
        # ID and group setup from configuration
        self.GroupId = config.get("GROUP_ID", "")
        self.GatewayId = config.get("GATEWAY_ID", "")
        self.SlaveId = 999
        self.ControllerId = config.get("DEVICE_ID", "")

        # Initialize timestamps
        self.Start_tm = 0
        self.End_tm = 0
        self.DetectedStart_tm = 0
        self.DetectedEnd_tm = 0
        self.Sent_tm = 0
        self.Created_tm = 0
        self.Detected_tm = 0

        # Initialize MediaData references and WorkFlow
        self.mediaDataRef: List[MediaData] = []
        self.workFlow = WorkFlow()

        # Schema version
        self.Version = "1.0.27"

    def __get_event_id(self):
        """
        Generate an event ID based on the number of seconds from the start of the 
        year to the current moment, multiplied by 10.

        Returns:
            int: A unique event ID based on the time elapsed from the start of the year.
        """

        utcnow = datetime.utcnow()
        beginning_of_year = datetime(utcnow.year, 1, 1)
        time_difference = utcnow - beginning_of_year
        return int(time_difference.total_seconds() * 10)
