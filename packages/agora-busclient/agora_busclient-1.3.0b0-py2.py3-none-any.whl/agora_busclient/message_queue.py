import queue
from typing import List
from .messages import MessageDecoder, IoDataReportMsg, RequestMsg, EventMsg
from agora_logging import LogLevel, logger


class MessageQueue:
    '''
    Provides the managed queues of messages arriving from the MQTT Broker.
    '''
    def __init__(self):
        """
        Initializes the queues for each message type.
        """
        self.data_in_q: queue.Queue = queue.Queue()
        self.request_in_q: queue.Queue = queue.Queue()
        self.event_in_q: queue.Queue = queue.Queue()
        self.application_messages_q: queue.Queue = queue.Queue()
        self.decoder: MessageDecoder = MessageDecoder()

    def __parse_topic(self, topic_str) -> str:
        str_array = topic_str.split('/')
        if len(str_array) > 2:
            str_result = '/'.join(str_array[2:])
        else:
            str_result = topic_str
        return str_result.lower() 

    def process_message(self, msg):
        """
        Store message to corresponding queue

        Args:
            msg (bytes): message received
        """
        topic = msg.topic
        payload = msg.payload
        self.store_to_queue(topic, payload)

    def store_to_queue(self, topic, payload):
        '''
        Stores message to the queues based on the topic
        '''
        topic_name = self.__parse_topic(topic)
        logger.trace(f"topic received {topic}")
        if topic_name is None:
            return 0
        if topic_name == "datain":
            try:
                msg = self.decoder.decode(
                    payload.decode("utf-8"), IoDataReportMsg)
                if msg is None:
                    logger.error(
                        f"DataIn Message: Failed to parse '{payload}'")
                self.data_in_q.put(msg)
            except Exception as e:
                logger.write(LogLevel.ERROR, str(e))
                logger.write(LogLevel.ERROR,
                             "Unable to read the json from DataIn message")
        elif topic_name == "requestin":
            try:
                msg = self.decoder.decode(payload.decode("utf-8"), RequestMsg)
                if msg is None:
                    logger.error(
                        f"Request Message: Failed to parse '{payload}'")
                self.request_in_q.put(msg)
            except Exception as e:
                logger.exception(
                    e, "Unable to read json from RequestIn message.")
        elif topic_name == "eventin":
            try:
                msg = self.decoder.decode(payload.decode("utf-8"), EventMsg)
                if msg is None:
                    logger.error(
                        f"Event Message: Failed to parse '{payload}'")
                self.event_in_q.put(msg)
            except Exception as e:
                logger.exception(
                    e, "Unable to read json from EventIn message.")
        else:
            self.application_messages_q.put((topic_name, payload))
        
    def __array_from_queue(self, q: queue.Queue):
        items = []
        try:
            while not q.empty():
                item = q.get_nowait()
                items.append(item)
        except queue.Empty:
            logger.trace("Queue is empty")
        return items

    def get_data_messages(self) -> List[IoDataReportMsg]:
        '''Returns a list of IoDataReportMsg's'''
        return self.__array_from_queue(self.data_in_q)

    def get_application_messages(self):
        '''
        Returns a list of the received raw application messages which 
        are not handled by DataIn, RequestIn. or EventIn
        '''
        return self.__array_from_queue(self.application_messages_q)

    def get_request_messages(self) -> List[RequestMsg]:
        '''Returns a list of received RequestMsg's'''
        return self.__array_from_queue(self.request_in_q)

    def get_event_messages(self) -> List[EventMsg]:
        '''Returns a list of EventMsg's'''
        return self.__array_from_queue(self.event_in_q)

    def has_data_messages(self) -> bool:
        '''Returns 'true' is any data messages are available.'''
        return not self.data_in_q.empty()

    def has_application_messages(self) -> bool:
        '''Returns 'true' is any application messages are available.'''
        return not self.application_messages_q.empty()

    def has_request_messages(self) -> bool:
        '''Returns 'true' is any request messages are available.'''
        return not self.request_in_q.empty()
    
    def has_event_messages(self) -> bool:
        '''Returns 'true' is any event messages are available.'''
        return not self.event_in_q.empty()
