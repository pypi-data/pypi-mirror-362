from agora_config import config
from agora_logging import logger
from .message_queue import MessageQueue, IoDataReportMsg
from typing import Set


class BaseMqttClient():
    """
    Base class for MQTT Client, providing the core functionalities.
    Allows the use of a mock MQTT client when configured.
    Refer to the configuration 'AEA2:BusClient:Mock' to set the mock state.

    Attributes:
        messages (MessageQueue): Queue to store messages.
        server (str): Server address. Defaults to "127.0.0.1".
        port (int): Port number. Defaults to 707.
        username (str): Username for the MQTT client.
        password (str): Password for the MQTT client.
        topics (Set): Set of topics for the client to subscribe to.
        connected (bool): Connection state of the MQTT client.
    """
    def __init__(self):
        """Initialize MQTT client with default settings."""
        self.messages: MessageQueue = MessageQueue()
        self.server = "127.0.0.1"
        self.port = 707
        self.username = None
        self.password = None
        self.topics: Set = set()
        self.connected: bool = False

    def is_connected(self) -> bool:
        """Check if the MQTT client is connected.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self.connected

    def disconnect(self) -> None:
        """Disconnect the MQTT client."""
        self.connected = False

    def connect(self, limit_sec: int) -> None:
        """Connect the MQTT client, with a time limit.

        Args:
            limit_sec (int): Time limit in seconds for the connection.
        """
        self.connected = True

    def update_topics(self, topics: Set) -> None:
        """Update the topics for the MQTT client to subscribe to.

        Args:
            topics (Set): New set of topics to subscribe to.
        """

        self.topics = topics

    def send_message(self, topic: str, payload):
        """Send a message to a specified topic.

        Args:
            topic (str): The topic to send the message to.
            payload: The message payload.
        """
        if self.is_connected():
            if topic == "DataOut":
                self.messages.store_to_queue("DataIn", payload.encode("utf-8"))
            elif topic == "RequestOut":
                self.messages.store_to_queue("RequestIn", payload.encode("utf-8"))
            elif topic == "EventOut":
                self.messages.store_to_queue("EventIn", payload.encode("utf-8"))
            else:
                self.messages.store_to_queue(topic, payload.encode("utf-8"))
        else:
            logger.warn("Trying to send_message, but bus_client is not connected. (BaseMqttClient)")

    @staticmethod
    def convert_to_int(value, default) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def configure(self) -> None:
        '''
        Configures the BusClient.  
        
        Configuration settings used:

        - 'Name': The name used to represent the client to the MQTT Broker.\n
        - 'AEA2:BusClient':
            - 'Server': (optional) The host name or IP of the MQTT Broker.  Default is '127.0.0.1'
            - 'Port': (optional) The port of the MQTT Broker.  Default is '707'
            - 'Subscriptions': (optional) List of topics to subscribe to. Ex. ["DataIn", "RequestIn", "EventIn"]
            - 'Username': (optional) The username to connect with.  Default is ''
            - 'Password': (optional) The password to connect with.  Default is ''
        '''
        self.server = config.get("AEA2:BusClient:Server", "127.0.0.1")
        self.port = self.convert_to_int(config.get("AEA2:BusClient:Port", "707"), 707)
        
        topics: Set = set()

        use_data_in = bool(config["AEA2:BusClient:UseDataIn"])
        if use_data_in:
            logger.warn(
                "Setting 'AEA2:BusClient:UseDataIn' has been deprecated.  Add 'DataIn' directly within 'AEA2:BusClient:Subscriptions' array instead.")
            topics.add("DataIn")

        use_request_in = bool(config["AEA2:BusClient:UseRequests"])
        if use_request_in:
            logger.warn(
                "Setting 'AEA2:BusClient:UseRequests' has been deprecated.  Add 'RequestIn' directly within 'AEA2:BusClient:Subscriptions' array instead.")
            topics.add("RequestIn")

        device_id = config.get("AEA2:BusClient:DeviceId", "999")
        try:
            IoDataReportMsg.default_device_id = str(device_id)
        except:
            IoDataReportMsg.default_device_id = "999"

        subscriptions = config["AEA2:BusClient:Subscriptions"]
        if subscriptions != "":
            topics = topics.union(set(subscriptions))

        self.username = config["AEA2:BusClient:Username"]
        self.password = config["AEA2:BusClient:Password"]

        self.update_topics(topics)

    def log_config(self) -> None:
        """Log the current configuration to the console."""
        logger.info(f"MQTT Client Name: {config['Name']}")
        logger.info("AEA2:BusClient:")
        logger.info(f"--- Server: {self.server}")
        logger.info(f"--- Port: {self.port}")
        logger.info(f"--- DeviceId: {IoDataReportMsg.default_device_id}")
        if len(self.topics) > 0:
            logger.info("--- Subscriptions:")
            for sub in self.topics:
                logger.info(f"   --- {sub}")
        else:
            logger.info("--- Subscriptions: <None>")
