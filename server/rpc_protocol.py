# coding=utf-8
"""
author = jamon
"""

import asyncio
import struct
import traceback
import ujson

from share.ob_log import logger
from share.encodeutil import AesEncoder
from server.ob_protocol import ObProtocol, DataException
from server.ob_service import rpc_service
from server.global_object import GlobalObject


class RpcProtocol(ObProtocol):
    """消息协议，包含消息处理"""

    def __init__(self):
        self.handfrt = "iii"  # (int, int, int)  -> (message_length, command_id, version)
        self.head_len = struct.calcsize(self.handfrt)
        self.identifier = 0

        self.encode_ins = AesEncoder(GlobalObject().rpc_password, encode_type=GlobalObject().rpc_encode_type)
        self.version = 0

        self._buffer = b""    # 数据缓冲buffer
        self._head = None     # 消息头, list,   [message_length, command_id, version]
        self.transport = None
        super().__init__()

    def pack(self, data, command_id):
        """
        打包消息， 用於傳輸
        :param data:  傳輸數據
        :param command_id:  消息ID
        :return:
        """
        data = self.encode_ins.encode(data)
        data = "%s" % data
        length = data.__len__() + self.head_len
        head = struct.pack(self.handfrt, length, command_id, self.version)
        return str(head + data)

    def process_data(self, data):
        self._buffer += data
        _buffer = None

        if self._head is None:
            if len(self._buffer) < self.head_len:
                return
            self._head = self._buffer[:self.head_len]       # 包头
            self._buffer = self._buffer[self.head_len:]

        if len(self._buffer) > self._head[0]:
            data = self.encode_ins.decode_aes(self._buffer[:self._head[0]])   # 解密
            if not data:
                raise DataException()
            self.message_handle(self._head[1], self._head[2], data)

            _buffer = self._buffer[self._head[0]:]
            self._buffer = b""
            self._head = None
        return _buffer

    def message_handle(self, command_id, version, data):
        """
        实际处理消息
        :param command_id:
        :param version:
        :param data:
        :return:
        """
        result = rpc_service.call_target(command_id, data)
        self.transport.write(self.pack(command_id, result))

    def connection_made(self, transport):
        self.transport = transport
        # self.address = transport.get_extra_info('peername')
        logger.debug('connection accepted')

    def data_received(self, data):
        logger.debug('received {!r}'.format(data))
        while data:     # 解决TCP粘包问题
            data = self.process_data(data)

    def eof_received(self):
        logger.debug('received EOF')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if error:
            logger.error('ERROR: {}'.format(error))
        else:
            logger.debug('closing')
        super().connection_lost(error)

