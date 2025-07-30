# -*- coding: UTF-8 -*-
'''
@File    :   dataStructure.py
@Time    :   2025/01/06 15:30:00
@Author  :   Jiajie Liu
@Version :   1.0
@Contact :   ljj26god@163.com
@Desc    :   This file contains necessary data structures for using vector driver.
'''

import ctypes
import time
from enum import Enum

MAX_MSG_LEN = 8
XL_CANFD_MAX_EVENT_SIZE = 128
XL_CANFD_RX_EVENT_HEADER_SIZE = 32
XL_CAN_MAX_DATA_LEN = 128
XL_CONFIG_MAX_CHANNELS = 64
XL_MAX_LENGTH = 31

# XL_CAN_EXT_MSG_ID = 0x80000000
XL_CAN_EXT_MSG_ID = 2147483648
XLeventTag_transmit = 10
flags = 0
activate_channel_flag = 0
dlc = 8
userName = ''
rx_queue_size = ctypes.c_uint(1)
xlInterfaceVersion = ctypes.c_uint(1)
busType = ctypes.c_uint(1)

XLuint64 = ctypes.c_uint64
XLstatus = ctypes.c_short
XLportHandle = ctypes.c_long
XLaccessMark = ctypes.c_uint

hwtype_dict = {
    0: "XL_HWTYPE_NONE",
    1: "XL_HWTYPE_VIRTUAL",
    2: "XL_HWTYPE_CANCARDX",
    6: "XL_HWTYPE_CANAC2PCI",
    12: "XL_HWTYPE_CANCARDY",
    15: "XL_HWTYPE_CANCARDXL",
    21: "XL_HWTYPE_CANCASEXL",
    23: "XL_HWTYPE_CANCASEXL_LOG_OBSOLETE",
    25: "XL_HWTYPE_CANBOARDXL",
    27: "XL_HWTYPE_CANBOARDXL_PXI",
    29: "XL_HWTYPE_VN2600",
    37: "XL_HWTYPE_VN3300",
    39: "XL_HWTYPE_VN3600",
    41: "XL_HWTYPE_VN7600",
    43: "XL_HWTYPE_CANCARDXLE",
    45: "XL_HWTYPE_VN8900",
    47: "XL_HWTYPE_VN8950",
    53: "XL_HWTYPE_VN2640",
    55: "XL_HWTYPE_VN1610",
    57: "XL_HWTYPE_VN1630",
    59: "XL_HWTYPE_VN1640",
    61: "XL_HWTYPE_VN8970",
    63: "XL_HWTYPE_VN1611",
    64: "XL_HWTYPE_VN5240",
    65: "XL_HWTYPE_VN5610",
    66: "XL_HWTYPE_VN5620",
    67: "XL_HWTYPE_VN7570",
    68: "XL_HWTYPE_VN5650",
    69: "XL_HWTYPE_IPCLIENT",
    71: "XL_HWTYPE_IPSERVER",
    73: "XL_HWTYPE_VX1121",
    75: "XL_HWTYPE_VX1131",
    77: "XL_HWTYPE_VT6204",
    79: "XL_HWTYPE_VN1630_LOG",
    81: "XL_HWTYPE_VN7610",
    83: "XL_HWTYPE_VN7572",
    85: "XL_HWTYPE_VN8972",
    87: "XL_HWTYPE_VN0601",
    89: "XL_HWTYPE_VN5640",
    91: "XL_HWTYPE_VX0312",
    94: "XL_HWTYPE_VH6501",
    95: "XL_HWTYPE_VN8800",
    96: "XL_HWTYPE_IPCL8800",
    97: "XL_HWTYPE_IPSRV8800",
    98: "XL_HWTYPE_CSMCAN",
    101: "XL_HWTYPE_VN5610A",
    102: "XL_HWTYPE_VN7640",
    104: "XL_HWTYPE_VX1135",
    105: "XL_HWTYPE_VN4610",
    107: "XL_HWTYPE_VT6306",
    108: "XL_HWTYPE_VT6104A",
    109: "XL_HWTYPE_VN5430",
    110: "XL_HWTYPE_VTSSERVICE",
    112: "XL_HWTYPE_VN1530",
    113: "XL_HWTYPE_VN1531",
    114: "XL_HWTYPE_VX1161A",
    115: "XL_HWTYPE_VX1161B",
    120: "XL_MAX_HWTYPE"
}

def get_hwtype_name(hwtype_value):
    return hwtype_dict.get(hwtype_value, "Unknown HWTYPE")

class CAN(ctypes.Structure):
    _fields_ = [
        ("bitRate", ctypes.c_uint),
        ("sjw", ctypes.c_ubyte),
        ("tseg1", ctypes.c_ubyte),
        ("tseg2", ctypes.c_ubyte),
        ("sam", ctypes.c_ubyte),
        ("outputMode", ctypes.c_ubyte),
        ("reserved", ctypes.c_ubyte * 7),
        ("canOpMode", ctypes.c_ubyte)
    ]
class CANFD(ctypes.Structure):
    _fields_ = [
        ("arbitrationBitRate", ctypes.c_uint),
        ("sjwAbr", ctypes.c_ubyte),
        ("tseg1Abr", ctypes.c_ubyte),
        ("tseg2Abr", ctypes.c_ubyte),
        ("samAbr", ctypes.c_ubyte),
        ("outputMode", ctypes.c_ubyte),
        ("sjwDbr", ctypes.c_ubyte),
        ("tseg1Dbr", ctypes.c_ubyte),
        ("tseg2Dbr", ctypes.c_ubyte),
        ("dataBitRate", ctypes.c_uint),
        ("canOpMode", ctypes.c_ubyte)
    ]
class MOST(ctypes.Structure):
    _fields_ = [
        ("activeSpeedGrade", ctypes.c_uint),
        ("compatibleSpeedGrade", ctypes.c_uint),
        ("inicFwVersion", ctypes.c_uint)
    ]

class FlexRay(ctypes.Structure):
    _fields_ = [
        ("status", ctypes.c_uint),
        ("cfgMode", ctypes.c_uint),
        ("baudrate", ctypes.c_uint)
    ]
class Ethernet(ctypes.Structure):
    _fields_ = [
        ("macAddr", ctypes.c_ubyte * 6),
        ("connector", ctypes.c_ubyte),
        ("phy", ctypes.c_ubyte),
        ("link", ctypes.c_ubyte),
        ("speed", ctypes.c_ubyte),
        ("clockMode", ctypes.c_ubyte),
        ("bypass", ctypes.c_ubyte)
    ]
class Tx(ctypes.Structure):
    _fields_ = [
        ("bitrate", ctypes.c_uint),
        ("parity", ctypes.c_uint),
        ("minGap", ctypes.c_uint)
    ]

class Rx(ctypes.Structure):
    _fields_ = [
        ("bitrate", ctypes.c_uint),
        ("minBitrate", ctypes.c_uint),
        ("maxBitrate", ctypes.c_uint),
        ("parity", ctypes.c_uint),
        ("minGap", ctypes.c_uint),
        ("autoBaudrate", ctypes.c_uint)
    ]
class Dir(ctypes.Union):
    _fields_ = [
        ("tx", Tx),
        ("rx", Rx),
        ("raw", ctypes.c_ubyte * 24)
    ]
class A429(ctypes.Structure):
    _fields_ = [
        ("channelDirection", ctypes.c_ushort),
        ("res1", ctypes.c_ushort),
        ("dir", Dir)
    ]
class Data(ctypes.Union):
    _fields_ = [
        ("can", CAN),
        ("canFD", CANFD),
        ("most", MOST),
        ("flexray", FlexRay),
        ("ethernet", Ethernet),
        ("a429", A429),
        ("raw", ctypes.c_ubyte * 28)
    ]
class XLbusParams(ctypes.Structure):
    _fields_ = [
        ("busType", ctypes.c_uint),
        ("data", Data)
    ]
class XLchannelConfig(ctypes.Structure):
    # _pack_ = 1
    _fields_ = [
        ("name", ctypes.c_char * (XL_MAX_LENGTH+1)),
        ("hwType", ctypes.c_ubyte),
        ("hwIndex", ctypes.c_ubyte),
        ("hwChannel", ctypes.c_ubyte),
        ("transceiverType", ctypes.c_ushort),
        ("transceiverState", ctypes.c_uint),
        ("channelIndex", ctypes.c_ubyte),
        ("channelMask", XLuint64),
        ("channelCapabilities", ctypes.c_uint),
        ("channelBusCapabilities", ctypes.c_uint),
        ("isOnBus", ctypes.c_ubyte),
        ("connectedBusType", ctypes.c_uint),
        ("busParams", XLbusParams),
        ("driverVersion", ctypes.c_uint),
        ("interfaceVersion", ctypes.c_uint),
        ("raw_data", ctypes.c_uint * 10),
        ("serialNumber", ctypes.c_uint),
        ("articleNumber", ctypes.c_uint),
        ("transceiverName", ctypes.c_char * (XL_MAX_LENGTH + 1)),
        ("specialCabFlags", ctypes.c_uint),
        ("dominantTimeout", ctypes.c_uint),
        ("reserved", ctypes.c_uint * 8)
    ]

class XLdriverConfig (ctypes.Structure):
    _fields_ = [
        ("dllVersion", ctypes.c_uint),
        ("channelCount", ctypes.c_uint),
        ("reserved", ctypes.c_uint * 10),
        ("channel", XLchannelConfig * XL_CONFIG_MAX_CHANNELS)
    ]

class XLcanMsg(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_ulong),
        ("flags", ctypes.c_ushort),
        ("dlc", ctypes.c_ushort),
        ("res1", XLuint64),
        ("data", ctypes.c_ubyte * MAX_MSG_LEN),
        ("res2", XLuint64)
    ]
class s_xl_can_msg(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_ulong),
        ("flags", ctypes.c_ushort),
        ("dlc", ctypes.c_ushort),
        ("res1", XLuint64),
        ("data", ctypes.c_ubyte * MAX_MSG_LEN),
        ("res2", XLuint64),
    ]
class s_xl_chip_state(ctypes.Structure):
    _fields_ = [
        ("busStatus", ctypes.c_ubyte),
        ("txErrorCounter", ctypes.c_ubyte),
        ("rxErrorCounter", ctypes.c_ubyte),
    ]

class s_xl_sync_pulse(ctypes.Structure):
    _fields_ = [
        ("pulseCode", ctypes.c_ubyte),
        ("time", XLuint64),
    ]

class s_xl_tag_data(ctypes.Union):
    _fields_ = [
        ("msg", s_xl_can_msg),
        ("chipState", s_xl_chip_state),
        ("syncPulse", s_xl_sync_pulse),
    ]

XLeventTag = int
class XLevent(ctypes.Structure):
    _fields_ = [
        ("tag", ctypes.c_ubyte),
        ("chanIndex", ctypes.c_ubyte),
        ("transId", ctypes.c_ushort),
        ("portHandle", ctypes.c_ushort),
        ("flags", ctypes.c_ubyte),
        ("reserved", ctypes.c_ubyte),
        ("timeStamp", XLuint64),
        ("tagData", s_xl_tag_data)
    ]

class XL_CAN_EV_RX_MSG(ctypes.Structure):
    _fields_ = [
        ("canId", ctypes.c_uint),
        ("msgFlags", ctypes.c_uint),
        ("crc", ctypes.c_uint),
        ("reserved1", ctypes.c_ubyte * 12),
        ("totalBitCnt", ctypes.c_ushort),
        ("dlc", ctypes.c_ubyte),
        ("reserved", ctypes.c_ubyte * 5),
        ("data", ctypes.c_ubyte * XL_CAN_MAX_DATA_LEN)
    ]

class XL_CAN_EV_TX_REQUEST(ctypes.Structure):
    _fields_ = [
        ("canId", ctypes.c_uint),
        ("msgFlags", ctypes.c_uint),
        ("dlc", ctypes.c_ubyte),
        ("reserved1", ctypes.c_ubyte),
        ("reserved", ctypes.c_ushort),
        ("data", ctypes.c_ubyte * XL_CAN_MAX_DATA_LEN)
    ]

class XL_CAN_EV_CHIP_STATE(ctypes.Structure):
    _fields_ = [
        ("busStatus", ctypes.c_ubyte),
        ("txErrorCounter", ctypes.c_ubyte),
        ("rxErrorCounter", ctypes.c_ubyte),
        ("reserved", ctypes.c_ubyte),
        ("reserved0", ctypes.c_uint)
    ]
class XL_CAN_EV_ERROR(ctypes.Structure):
    _fields_ = [
        ("errorCode", ctypes.c_ubyte),
        ("reserved", ctypes.c_ubyte * 95)
    ]
class XL_SYNC_PULSE_EV(ctypes.Structure):
    _fields_ = [
        ("triggerSource", ctypes.c_uint),
        ("reserved", ctypes.c_uint),
        ("time", XLuint64)
    ]

XL_CAN_EV_SYNC_PULSE = XL_SYNC_PULSE_EV

class XLcanRxEvent(ctypes.Structure):
    class TagData(ctypes.Union):
        _fields_ = [
            ("raw", ctypes.c_ubyte * (XL_CANFD_MAX_EVENT_SIZE - XL_CANFD_RX_EVENT_HEADER_SIZE)),
            ("canRxOkMsg", XL_CAN_EV_RX_MSG),
            ("canTxOkMsg", XL_CAN_EV_RX_MSG),
            ("canTxRequest", XL_CAN_EV_TX_REQUEST),
            ("canError", XL_CAN_EV_ERROR),
            ("canChipState", XL_CAN_EV_CHIP_STATE),
            ("canSyncPulse", XL_CAN_EV_SYNC_PULSE)
        ]

    _fields_ = [
        ("size", ctypes.c_uint),
        ("tag", ctypes.c_ushort),
        ("channelIndex", ctypes.c_ushort),
        ("userHandle", ctypes.c_uint),
        ("flagsChip", ctypes.c_ushort),
        ("reserved0", ctypes.c_ushort),
        ("reserved1", XLuint64),
        ("timeStampSync", XLuint64),
        ("tagData", TagData)
    ]

class BusType(Enum):
    NONE = 0x00000000
    CAN = 0x00000001
    LIN = 0x00000002
    FLEXRAY = 0x00000004
    AFDX = 0x00000008  # former BUS_TYPE_BEAN
    MOST = 0x00000010
    DAIO = 0x00000040  # IO cab/piggy
    J1708 = 0x00000100
    KLINE = 0x00000800
    ETHERNET = 0x00001000
    A429 = 0x00002000

class CanMessage():
    def __init__(self, id, data, period, duration = 30):
        self.id = id
        self.data = data
        self.period = period
        self.duration = duration

class ReceivedCanMessage():
    def __init__(self, message_id, data, timestamp = time.time(), systemTimeStamp = None):
        self.message_id = message_id
        self.data = data
        self.timeStamp = timestamp
        self.systemTimeStamp = systemTimeStamp

    def getMessageID(self):
        return self.message_id

    def getData(self):
        return self.data

class ReceivedCanMessageDecode():
    def __init__(self, message, decode_signals,decoded_signals_raw):
        self.message = message
        self.decode_signals = decode_signals
        self.decoded_signals_raw = decoded_signals_raw


    def getMessageName(self):
        return self.message

    def getDecodeSignals(self):
        return self.decode_signals

    def getDecodeSignalsRaw(self):
        return self.decoded_signals_raw



