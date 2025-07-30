# -*- coding: UTF-8 -*-
'''
@File    :   xldriver.py
@Time    :   2025/01/06 15:30:00
@Author  :   Jiajie Liu
@Version :   1.0
@Contact :   ljj26god@163.com
@Desc    :   This file reads dll file from vector official website and utilize necessary functions for sending CAN messages.
'''

import ctypes, os
from simpleCan.util import dataStructure as ds

util_path = os.path.dirname(os.path.abspath(__file__))
simpleCan_path = os.path.dirname(util_path)
dll_file_path = os.path.join(simpleCan_path, 'dll_file')
dll_path = os.path.join(dll_file_path, 'vxlapi64.dll')
_xlapi_dll = ctypes.windll.LoadLibrary(dll_path)
libc = ctypes.CDLL("msvcrt.dll")

# initialize functions
xlOpenDriver = _xlapi_dll.xlOpenDriver

xlGetDriverConfig = _xlapi_dll.xlGetDriverConfig

xlGetApplConfig = _xlapi_dll.xlGetApplConfig

xlGetChannelMask = _xlapi_dll.xlGetChannelMask

xlOpenPort = _xlapi_dll.xlOpenPort

xlGetSyncTime = _xlapi_dll.xlGetSyncTime

xlResetClock = _xlapi_dll.xlResetClock

xlActivateChannel = _xlapi_dll.xlActivateChannel

xlCanTransmit = _xlapi_dll.xlCanTransmit
xlCanTransmit.argtypes = [
    ds.XLportHandle,
    ds.XLaccessMark,
    ctypes.POINTER(ctypes.c_uint),
    ctypes.POINTER(ds.XLevent),
]
xlCanTransmit.restype = ds.XLstatus

xlReceive = _xlapi_dll.xlReceive
xlReceive.argtypes = [
    ds.XLportHandle,
    ctypes.POINTER(ctypes.c_uint),
    ctypes.POINTER(ds.XLevent),
]

xlCanReceive = _xlapi_dll.xlCanReceive
xlCanReceive.argtypes = [
    ds.XLportHandle,
    ctypes.POINTER(ds.XLcanRxEvent),
]

xlDeactivateChannel = _xlapi_dll.xlDeactivateChannel
xlClosePort = _xlapi_dll.xlClosePort
xlCloseDriver = _xlapi_dll.xlCloseDriver

xlGetErrorString = _xlapi_dll.xlGetErrorString

libc.memset.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_size_t]
libc.memset.restype = ctypes.c_void_p

######################################################################################

appName = ctypes.create_string_buffer(b'CANalyzer')
pAppName = ctypes.pointer(appName)
appChannel = ctypes.c_uint()
HwType = ctypes.c_uint()
pHwType = ctypes.pointer(HwType)
HwIndex = ctypes.c_uint()
pHwIndex = ctypes.pointer(HwIndex)
HwChannel = ctypes.c_uint()
pHwChannel = ctypes.pointer(HwChannel)
busTypex = ctypes.c_uint()
time = ctypes.c_uint()
pTime = ctypes.pointer(time)

xldriverConfig = ds.XLdriverConfig()
pxldriverConfig = ctypes.pointer(xldriverConfig)

portHandle = ds.XLportHandle()
pPortHandle = ctypes.pointer(portHandle)

userName = ds.userName
channelMask = ctypes.c_uint()
permissionMask = ctypes.c_uint64()
pPermissionMask = ctypes.pointer(permissionMask)
rx_queue_size = ds.rx_queue_size
xlInterfaceVersion = ds.xlInterfaceVersion
busType = ds.busType

XLeventTag_transmit = ds.XLeventTag_transmit
flags = ds.flags
activate_channel_flag = ds.activate_channel_flag
dlc = ds.dlc


