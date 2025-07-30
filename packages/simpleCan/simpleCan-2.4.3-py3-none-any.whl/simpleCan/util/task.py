# -*- coding: UTF-8 -*-
'''
@File    :   task.py
@Time    :   2025/01/06 15:30:00
@Author  :   Jiajie Liu
@Version :   1.0
@Contact :   ljj26god@163.com
@Desc    :   This file contains Task class that utilize thread for handling period and duration for messages.
'''

import threading, logging, time, asyncio
from simpleCan.util import can_func, dataStructure as ds


class SendMessageTask:
    def __init__(self, message_id=None, data=None, channel = 1,  period=0, duration=0):
        self.message_id = message_id
        self.data = data
        self.period = period
        self.channel = channel
        self.duration = duration
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.thread = threading.Thread(target=self.run_loop)

    def get_messageID(self):
        return self.message_id

    def get_messageData(self):
        return self.data

    async def sendMessage_task(self):  # append sendData task with parameter period and duration
        end_time = time.time() + self.duration
        while time.time() < end_time:
            can_func.sendMessage(messageID=self.message_id, data=self.data, channel=self.channel)
            await asyncio.sleep(self.period)
            if self._stop_event.is_set():
                break

    def run_loop(self):
        asyncio.run(self.sendMessage_task())

    def task_run(self):
        self.thread.start()

    def task_modifyData(self, newData):
        with self._lock:
            self.data = newData

    def task_stop(self):
        self._stop_event.set()
        self.thread.join()


class RecvMessageTask:
    @classmethod
    def recvTargetMessage(self, message_id, offset=0, duration=10) -> ds.ReceivedCanMessage:
        end_time = time.time() + duration
        start_time = int(time.time())  # assert that newest message is received, instead of the first
        # message from message buffer
        while time.time() < end_time:
            result = can_func.recvMessage()
            if result is not None and result.message_id == message_id and result.timeStamp > start_time + offset:
                # needs to wait until receive message buffer has been cleared
                logging.info(
                    'received target message ' + str(hex(result.message_id)) + ' at time ' + str(
                        result.timeStamp) + ' DDU system time ' + str(result.systemTimeStamp))
                return result

    @classmethod
    def recvMessage(self) -> ds.ReceivedCanMessage:
        return can_func.recvMessage()


