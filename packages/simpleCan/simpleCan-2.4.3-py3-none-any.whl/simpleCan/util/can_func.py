#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@File    :   can_func.py
@Time    :   2025/2/18 9:55
@Author  :   CLZMFQ
@Version :   1.0
@Contact :   ljj26god@163.com
@Desc    :   This package realizes functionality of sending can message
'''

from simpleCan.util import xldriver, dataStructure as ds
import logging, ctypes, time

def sendMessage(messageID, data, messageCount=1, channel = 1):
    canID = ds.XL_CAN_EXT_MSG_ID | messageID
    myXLevent = (ds.XLevent * messageCount)()
    message_count = ctypes.c_uint(messageCount)
    try:
        xldriver.libc.memset(myXLevent, 0, ctypes.sizeof(myXLevent))
        for i in range(messageCount):
            myXLevent[i].tag = xldriver.XLeventTag_transmit
            myXLevent[i].tagData.msg.id = canID
            myXLevent[i].tagData.msg.flags = xldriver.flags
            for j in range(len(data)):
                myXLevent[i].tagData.msg.data[j] = data[j]
            myXLevent[i].tagData.msg.dlc = xldriver.dlc
        accessMark = 2**(channel-1)
        result = xldriver.xlCanTransmit(xldriver.portHandle, accessMark, message_count, myXLevent)
        if result == 0:
            logging.info('send message ' + str(hex(messageID)) + ' result ' + str(result))
        else:
            logging.error('send message ' + str(hex(messageID)) + ' result ' + str(result))
    except Exception as e:
        logging.error(f"Error: {e}")

def recvMessage() -> ds.ReceivedCanMessage:
    xLevent = ds.XLevent()
    pxLevent = ctypes.pointer(xLevent)
    pEventCount = ctypes.pointer(ctypes.c_uint(1))
    xlstatus = xldriver.xlReceive(xldriver.portHandle, pEventCount, pxLevent)
    timeStamp = time.time()
    if xlstatus == 0:
        msgID = xLevent.tagData.msg.id & 0x1FFFFFFF
        msgData = list(xLevent.tagData.msg.data)
        systemTimeStamp = xLevent.timeStamp
        logging.info(
            'received message ' + str(hex(msgID)) + ' timestamp ' + str(timeStamp) + ' system time ' + str(systemTimeStamp))
        return ds.ReceivedCanMessage(message_id=msgID, data=msgData, timestamp=timeStamp,
                                     systemTimeStamp=systemTimeStamp)

def getSyncTime():
    xlstatus = xldriver.xlGetSyncTime(xldriver.portHandle, xldriver.pTime)
    logging.info('xl get sync time result is ' + str(xlstatus))
    return xldriver.time


def setup(openChannel=[1]):
    xlstatus = xldriver.xlOpenDriver()
    logging.info('open driver result is ' + str(xlstatus))

    xlstatus = xldriver.xlGetDriverConfig(xldriver.pxldriverConfig)
    logging.info('get driver config result is ' + str(xlstatus))

    xlstatus = xldriver.xlGetApplConfig(xldriver.pAppName, xldriver.appChannel, xldriver.pHwType, xldriver.pHwIndex,
                                        xldriver.pHwChannel, xldriver.busTypex)
    logging.info('get appl config result is ' + str(xlstatus))
    logging.info('hardware type is ' + ds.get_hwtype_name(xldriver.HwType.value))

    accessMask = 0
    for channel in openChannel:
        accessMask = accessMask + 2**(channel-1)
    channelMask = accessMask
    xldriver.permissionMask.value = channelMask

    xlstatus = xldriver.xlOpenPort(xldriver.pPortHandle,
                                   xldriver.userName,
                                   accessMask,
                                   xldriver.pPermissionMask,
                                   xldriver.rx_queue_size,
                                   xldriver.xlInterfaceVersion,
                                   xldriver.busType)

    logging.info('port handler value is ' + str(xldriver.portHandle))

    assert xlstatus != -1
    logging.info('open port result is ' + str(xlstatus))
    xlstatus = xldriver.xlActivateChannel(xldriver.portHandle,
                                          accessMask,
                                          xldriver.busType,
                                          xldriver.activate_channel_flag)
    logging.info('Activate channel result is ' + str(xlstatus))

    xlstatus = xldriver.xlResetClock(xldriver.portHandle)

    logging.info('xl reset clock result is ' + str(xlstatus))

def teardown():
    xlstatus = xldriver.xlDeactivateChannel(xldriver.portHandle)
    logging.info('deactivate channel result is ' + str(xlstatus))

    xlstatus = xldriver.xlClosePort(xldriver.portHandle)
    logging.info('close port result is ' + str(xlstatus))

    xlstatus = xldriver.xlCloseDriver()
    logging.info('close driver result is ' + str(xlstatus))
