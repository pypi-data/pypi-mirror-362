import json
from agora_config import config
from agora_logging import logger
from .messages import IoDataReportMsg, MessageEncoder, RequestMsg, MessageHeader, EventMsg
from .mqtt_client import MqttClient
from .base_mqtt_client import BaseMqttClient


class BusClientSingleton:
    _instance = None
    """
    Connects to the mqtt-net-server and handles sending and receiving messages
    """
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.subscriptions = set()
        self.bus = BaseMqttClient()
        config.observe("AEA2:BusClient", self.reconnect)

    @property
    def messages(self):
        '''
        Returns the internal bus client's queued messages
        '''
        return self.bus.messages

    def connect(self, sec: float) -> None:
        '''
        Connects the BusClient.
        
        Configuration settings used:

        - 'Name': The name used to represent the client to the MQTT Broker.\n
        - 'AEA2:BusClient':
            - 'Server': (optional) The host name or IP of the MQTT Broker.  Default is '127.0.0.1'
            - 'Port': (optional) The port of the MQTT Broker.  Default is '707'
            - 'Subscriptions': (optional) List of topics to subscribe to. Ex. ["DataIn", "RequestIn", "EventIn"]
            - 'Username': (optional) The username to connect with.  Default is ''
            - 'Password': (optional) The password to connect with.  Default is ''
        '''
        if config["AEA2:BusClient:Mock"] == "True":
            logger.warn("Mocking BusClient based upon configuration settings 'AEA2:BusClient:Mock'")
            self.bus = BaseMqttClient()
        else:
            self.bus = MqttClient()
        self.bus.configure()
        self.bus.log_config()
        logger.info("bus_client connecting")
        self.bus.connect(sec)
        if self.is_connected():
            logger.info("bus_client connected")

    def disconnect(self):
        '''
        Disconnects the BusClient
        '''
        if self.bus.is_connected():
            self.bus.disconnect()

    def reconnect(self, _ = None) -> None:
        '''
        Reconnects the BusClient.  Mostly this happens if the configuration has changed.
        '''
        logger.info(f"BusClient: Received new configuration - reconnecting")
        self.disconnect()
        self.connect(3)

    def is_connected(self) -> bool:
        '''
        Returns whether the BusClient is connected or not.
        '''
        return self.bus.is_connected()

    def send_message(self, topic: str, header: MessageHeader, payload: str) -> None:
        '''
        Sends a message to 'topic', combining 'header' and 'payload' into a json representation.
        '''
        if not self.bus.is_connected():
            logger.error(
                "Cannot send message, BusClient is not connected to the broker")
            return
        headerJson = json.dumps(header, cls=MessageEncoder)
        payload_str = json.dumps(payload)
        if payload_str[0] != '"':
            payload_str = json.dumps(payload_str)
        message = f"""{{
            "header": {headerJson},
            "payload": {payload_str}
        }}"""
        self.bus.send_message(topic, message)

    def send_raw_message(self, topic: str, payload: str) -> None:
        '''
        Sends a raw message (still a string) to 'topic'
        '''
        if not self.bus.is_connected():
            logger.error(
                "Cannot send message, BusClient is not connected to the broker")
            return
        self.bus.send_message(topic, payload)

    def send_data(self, msg: IoDataReportMsg, msgTopic="DataOut") -> None:
        '''
        Sends an IoDataReportMsg to 'msgTopic' which defaults to 'DataOut' if not specified.
        '''
        payload = json.dumps(msg, cls=MessageEncoder)
        self.send_raw_message(msgTopic, payload)

    def send_request(self, msg: RequestMsg, msgTopic="RequestOut") -> int:
        '''
        Sends a RequestMsg to 'msgTopic' which defaults to 'RequestOut' if not specified.
        '''
        payload = json.dumps(msg, cls=MessageEncoder)
        self.send_raw_message(msgTopic, payload)
        return msg.header.MessageID
    
    def send_event(self, msg: EventMsg, msgTopic="EventOut") -> int:
        '''
        Sends an EventMsg to 'msgTopic' which defaults to 'EventOut' if not specified.
        '''        
        payload = json.dumps(msg, cls=MessageEncoder)
        self.send_raw_message(msgTopic, payload)
        return msg.EventId

    def configure(self) -> None:
        '''
        Configures the internal bus client.
        '''
        self.bus.configure()


'''
The singleton instance of the bus_client.
'''
bus_client = BusClientSingleton()
