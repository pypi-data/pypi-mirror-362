import json
from .iodatareport_message import IoDataReportMsg, IoDeviceData, IoPoint
from .io_tag_data_dict import IoTagDataDict
from .message_header import MessageHeader
from .work_flow import WorkFlow
from .media_data import MediaData
from .event_msg import EventMsg
from .request_msg import RequestMsg


class MessageEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, IoPoint):
            d = dict()
            if o.value != None:
                d['value'] = o.value
            if o.value_str != None:
                d['value_str'] = o.value_str
            if o.quality_code != None:
                d['quality_code'] = o.quality_code
            if o.timestamp != None:
                d['timestamp'] = int(o.timestamp)
            if o.metadata != None:
                d['metadata'] = o.metadata
            return d
        elif isinstance(o, IoTagDataDict):
            d = dict()
            for key, val in o.items():
                d[key] = self.default(val)
            return d
        elif isinstance(o, IoDeviceData):
            d = dict()
            d['id'] = str(o.id)
            d['tags'] = self.default(o.tags)
            return d
        elif isinstance(o, MessageHeader):
            d = dict()
            d['SrcModule'] = o.SrcModule
            d['MessageType'] = o.MessageType
            d['ConfigVersion'] = o.ConfigVersion
            d['MessageID'] = o.MessageID
            d['TimeStamp'] = int(o.TimeStamp)
            return d
        elif isinstance(o, IoDataReportMsg):
            d = dict()
            d['header'] = self.default(o.header)
            lst = list()
            for device in o.device:
                lst.append(self.default(device))
            d['device'] = lst
            return d
        elif isinstance(o, RequestMsg):
            d = dict()
            d['header'] = self.default(o.header)
            d['payload'] = o.payload
            lst = list()
            for device in o.device:
                lst.append(self.default(device))
            d['device'] = lst
            d['response'] = o.response
            return d
        elif isinstance(o, WorkFlow):
            d = dict()         
            d['Properties'] = o.Properties         
            if o.Type != None:
                d['Type'] = o.Type               
            return d
        elif isinstance(o, MediaData):
            d = dict()
            d['Type'] = o.Type
            d['Id'] = o.Id
            d['ZoneId'] = o.ZoneId
            d['CameraId'] = o.CameraId
            d['MotTrackerId'] = o.MotTrackerId
            d['EdgeFilename'] = o.EdgeFilename
            d['MotEdgeFilename'] = o.MotEdgeFilename
            d['MIMEType'] = o.MIMEType
            d['AltText'] = o.AltText
            d['RawData'] = o.RawData
            d['DetectedStart_tm'] = int(o.DetectedStart_tm)
            d['DetectedEnd_tm'] = int(o.DetectedEnd_tm)
            return d
        elif isinstance(o, EventMsg):
            d = dict()            
            d['EventId'] = o.EventId
            d['GroupId'] = o.GroupId
            d['GatewayId'] = o.GatewayId
            d['SlaveId'] = o.SlaveId
            d['ControllerId'] = o.ControllerId          
            d['Start_tm'] = int(o.Start_tm)
            d['End_tm'] = int(o.End_tm)
            d['DetectedStart_tm'] = int(o.DetectedStart_tm)
            d['DetectedEnd_tm'] = int(o.DetectedEnd_tm)            
            d['Sent_tm'] = int(o.Sent_tm)
            d['Created_tm'] = int(o.Created_tm)
            d['Detected_tm'] = int(o.Detected_tm)
          
            lst = list()
            for mediaData in o.mediaDataRef:
                lst.append(self.default(mediaData))
            d['mediaData'] = lst            
            d['workFlow'] = o.workFlow
            d['Version'] = o.Version            
            return d
        return super().default(o)
