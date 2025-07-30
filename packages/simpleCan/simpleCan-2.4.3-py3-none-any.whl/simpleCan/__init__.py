import logging
import random

from simpleCan.util import dataStructure as ds, can_func, dbcReader
from simpleCan.util.task import SendMessageTask, RecvMessageTask
from simpleCan.util.messageList import MessageList

__all__ = ['SimpleCan']

__author__ = 'Jiajie Liu'


class SimpleCan:

    def __init__(self, openChannel=None, **args):
        if openChannel is None:
            openChannel = [1, 3]
        self.tasklist = []  # list of threads
        self.messageList = MessageList()
        self.dbcReader = dbcReader.DBCReader(**args)
        self.openChannel = openChannel
        can_func.setup(openChannel=openChannel)

    def env_run(self, channel=1, duration=360):
        self.messageList.clearMessageList()
        self.messageList.load_default_messageList()
        messageList = self.messageList.get_messageList()
        self.clearTaskList()
        for i in range(len(messageList)):
            self.tasklist.append(SendMessageTask(message_id=messageList[i].id,
                                                 data=messageList[i].data,
                                                 period=messageList[i].period,
                                                 channel=channel,
                                                 duration=duration))
        for task in self.tasklist:
            task.task_run()

    def sendMessage(self, message_id, data, period, channel=1, duration=30):
        task = SendMessageTask(message_id=message_id,
                               data=data,
                               period=period,
                               channel=channel,
                               duration=duration)
        self.tasklist.append(task)
        task.task_run()

    def modifyMessage(self, message_id, data):
        try:
            for sendMessageTask in self.tasklist:
                if sendMessageTask.get_messageID() == message_id:
                    sendMessageTask.task_modifyData(newData=data)

        except Exception as e:
            logging.error(e)

    def stopMessage(self, message_id):
        try:
            for task in self.tasklist:
                if task.get_messageID() == message_id:
                    task.task_stop()
        except Exception as e:
            logging.error(e)

    def recvTargetMessage(self, messageId, offset=0, duration=10) -> ds.ReceivedCanMessage:
        return RecvMessageTask.recvTargetMessage(message_id=messageId, offset=offset, duration=duration)

    def recvMessage(self) -> ds.ReceivedCanMessage:
        return RecvMessageTask.recvMessage()

    def getTaskList(self):
        return self.tasklist

    def clearTaskList(self):
        self.tasklist = []

    def endAllTasks(self):
        for task in self.tasklist:
            task.task_stop()

    def __del__(self):
        self.endAllTasks()
        can_func.teardown()

    ####### DBC related functionalities ###############################################################################
    ####### Below functions can only be used if dbc file is loaded ####################################################

    def sendMessageDBC(self, messageName, database='yellowCan', channel=1, duration=30, **kwargs):
        canMessage = self.dbcReader.generateCanMessage(message=messageName, database=database, duration=duration,
                                                       **kwargs)
        self.sendMessage(message_id=canMessage.id, data=canMessage.data, channel=channel, period=canMessage.period,
                         duration=duration)

    def sendMessageDBC_OneFrame(self, messageName, database='yellowCan', channel=1, **kwargs):
        canMessage = self.dbcReader.generateCanMessage(message=messageName, database=database, **kwargs)
        can_func.sendMessage(messageID=canMessage.id, data=canMessage.data, channel=channel)

    def modifyMessageDBC(self, messageName, **kwargs):
        canMessage = self.dbcReader.generateCanMessage(message=messageName, **kwargs)
        self.modifyMessage(message_id=canMessage.id, data=canMessage.data)

    def stopMessageDBC(self, messageName):
        canMessage = self.dbcReader.generateCanMessage(message=messageName)
        self.stopMessage(message_id=canMessage.id)

    def recvTargetMessageDBC(self, messageName, offset=0, duration=10) -> ds.ReceivedCanMessageDecode:
        try:
            messageId = self.dbcReader.getMessageIdByName(messageName)
            recvMessage = self.recvTargetMessage(messageId=messageId, offset=offset, duration=duration)
            return self.dbcReader.decodeCanMessage(message_id=recvMessage.getMessageID(), data=recvMessage.data)
        except Exception as e:
            logging.error(e)

    def recvMessageDBC(self) -> ds.ReceivedCanMessageDecode:
        try:
            recvMessage = self.recvMessage()
            if recvMessage is not None:
                return self.dbcReader.decodeCanMessage(message_id=recvMessage.getMessageID(), data=recvMessage.data)
            return None
        except Exception as e:
            logging.error(f"Read message error: {e}")

    def sendAllMessagesFromDBC(self, channel=1, duration=30):
        canTxMessageList = self.dbcReader.getcanTxMessageList()
        for canMessage in canTxMessageList:
            self.sendMessage(message_id=canMessage.id, data=canMessage.data, period=canMessage.period, channel=channel,
                             duration=duration)

    def sendAllMessagesFromDBCrdValue(self, period_minimum=10, period_maximum=1000, channel=1, duration=30000000000000):
        canTxMessageList = self.dbcReader.getcanTxMessageList()
        for canMessage in canTxMessageList:
            self.sendMessage(message_id=canMessage.id, period=random.randint(period_minimum, period_maximum) / 1000,
                             channel=channel,
                             data=[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                                   random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                                   random.randint(0, 255),
                                   random.randint(0, 255)], duration=duration)

    ####### DBC functionss ###############################################################################
    def getMessageByName(self, messageName):
        try:
            return self.dbcReader.getMessageByName((messageName))
        except Exception as e:
            logging.error(e)
