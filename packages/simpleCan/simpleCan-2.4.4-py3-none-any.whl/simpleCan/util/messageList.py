# -*- coding: UTF-8 -*-
'''
@File    :   messageList.py
@Time    :   2025/01/06 15:30:00
@Author  :   Jiajie Liu
@Version :   1.0
@Contact :   ljj26god@163.com
@Desc    :   This file contains reads a excel file to set up CAN message environment. It also creates a list of tasks to manage all the tasks.
'''

from simpleCan.util import dataStructure as ds

class MessageList:

    def __init__(self):
        self.messageList = []

    def appendCanMessage(self, message:ds.CanMessage):
        self.messageList.append(message)
    def load_default_messageList(self):
        defaultMessageList = DefaultMessageList()
        for i in range(len(defaultMessageList.messageList)):
            self.messageList.append(defaultMessageList.messageList[i])

    def clearMessageList(self):
        self.messageList = []
    def get_messageList(self):
        return self.messageList

    def printMessageList(self):
        for i in range(len(self.messageList)):
            print(self.messageList[i].id)
            print(self.messageList[i].data)
            print(self.messageList[i].period)

class DefaultMessageList():
    def __init__(self):
        self.messageList = []
        self.messageList.append(ds.CanMessage(id=419343920, data=[0,203,94,91,0,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=285183505, data=[0,0,0,40,0,0,192,15], period=0.1))
        self.messageList.append(ds.CanMessage(id=285183761, data=[0,0,128,0,192,0,0,0], period=0.1))
        self.messageList.append(ds.CanMessage(id=419392071, data=[0,0,0,0,0,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=419410206, data=[0,0,0,0,16,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=419351088, data=[0,0,0,0,0,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=419351040, data=[0,0,0,0,0,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=419351087, data=[0,0,0,0,0,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=419351079, data=[0,0,0,0,0,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=419351043, data=[0,0,0,0,0,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=419351091, data=[0,0,0,0,0,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=418382091, data=[0,0,0,0,0,0,0,0], period=1))
        self.messageList.append(ds.CanMessage(id=418382091, data=[0,0,0,0,0,0,0,0], period=0.1))
        self.messageList.append(ds.CanMessage(id=436158800, data=[0,0,0,0,0,0,0,0], period=0.02))
        self.messageList.append(ds.CanMessage(id=218066778, data=[0,0,0,0,0,0,0,0], period=0.02))










