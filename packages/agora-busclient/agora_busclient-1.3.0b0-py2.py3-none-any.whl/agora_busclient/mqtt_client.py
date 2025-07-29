import logging
import time
from .base_mqtt_client import BaseMqttClient
import paho.mqtt.client as mqtt
from agora_logging import logger
from agora_config import config


class MqttClient(BaseMqttClient):
    '''
    Provides MQTT client capabilities for sending and receiving MQTT messages to MQTT Broker.

    The Client ID for the MQTT Client is the 'Name' configuration setting.
    '''
    def __init__(self):
        super().__init__()
        #self.client = mqtt.Client(client_id=config['Name'], protocol=mqtt.MQTTv5)
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1, client_id=config['Name'])
        self.client.connected_flag = False

    def is_connected(self) -> bool:
        return self.client.is_connected()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def update_topics(self, topics):
        if self.is_connected() and len(self.topics) > 0:
            for topic in topics:
                try:
                    self.client.unsubscribe(topic)
                except:
                    continue
        super().update_topics(topics)
        if self.is_connected() and len(self.topics) > 0:
            for topic in self.topics:
                self.client.subscribe(topics)

    def connect(self, limit_sec: int):
        def on_connect(client, user_data, flags, rc):
            results = {
                0: f"MQTT Client : Connection accepted",
                1: f"MQTT Client : Connection refused: incorrect protocol version",
                2: f"MQTT Client : Connection refused: invalid client identifier",
                3: f"MQTT Client : Connection refused: server unavailable",
                4: f"MQTT Client : Connection refused: bad username or password",
                5: f"MQTT Client : Connection refused: not authorized"
            }
            logger.trace(results.get(rc, f"MQTT Client: Unknown rc code"))
            if rc == 0:
                logger.trace(
                    "MQTT Client: Connected with result code {0}" .format(rc))
                self.__subscribe()
            else:
                logger.warn(
                    "MQTT Client: Failed to connect with result code {0}: Connection refused incorrect protocol version".format(str(rc)))

        def on_message(client, user_data, msg):
            self.messages.process_message(msg)

        def on_disconnect(client, user_data, rc):
            if rc != 0:
                logger.warn(f"Unexpected disconnection: (rc = {rc})")

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect
        if self.username != "" and self.password != "":
            logger.trace(f"Authenticating connection for '{self.username}'")
            self.client.username_pw_set(self.username, self.password)
            logger.trace(f"MQTT Client connected to {self.server}:{self.port}")
        try:
            self.client.connect(
                host=self.server, port=int(self.port), keepalive=60)
        except Exception as e:
            logger.error(
                f"Failed to connect to {self.server}:{self.port} :{str(e)}")
            return 0

        self.client.loop_start()  # start the client loop to allow it to reconnect automatically

        count = 0
        while not self.is_connected() and count/10 < limit_sec:
            count = count + 1
            time.sleep(.1)

        if self.is_connected():
            logger.trace(f"MQTT Client connected to {self.server}:{self.port}")
        else:
            logger.trace(
                f"MQTT Client unable to connect to {self.server}:{self.port}")

    def __subscribe(self):
        if self.is_connected():
            try:
                if len(self.topics) > 0:
                    logger.trace(f'MQTT Client: Subscribing to topics: ({self.topics})')
                    for topic in self.topics:
                        self.client.subscribe(topic)
                else:
                    logger.trace(f'MQTT Client: No subscriptions specified.')
                return True
            except Exception as e:
                logging.exception(
                    e, f'Error configuring MQTT client: {str(e)}')
                return False
        else:
            logger.error(
                "MQTT Client: Subscribe requested while not connected.")

    def send_message(self, topic: str, payload: str) -> None:
        try:
            logger.trace(f'MQTT Client: Publishing payload to: {topic}')
            bytes_payload = payload
            ret_val = self.client.publish(topic, bytes_payload, 0, retain=False)
            if ret_val[0] == 0:
                logger.trace(f'Success, message published, Number of message: {ret_val[1]}')
            else:
                logger.error(f'Message was not published, ret val: {ret_val}')
        except Exception as e:
            logger.error(e, f"Error trying to publish the message : {str(e)}")
