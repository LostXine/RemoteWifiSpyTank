# -*- coding:utf-8 -*-

"""
@file: UDPManager.py
@time: 2018/6/19 2:27
"""

import socket
import threading
import traceback
import queue
import time
from utils import console_output_no_line, console_output


class UDPManager:
    def __init__(self, udp_port, callback, bind=True):
        self.client = None
        self.receive_thread = None
        self.isBind = bind
        self.callback = callback
        self.q = queue.Queue()
        self.port = udp_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.is_running = False
        self.server.settimeout(1)
        if self.isBind:
            self.server.bind(('0.0.0.0', self.port))  # 允许外部连接
        else:
            self.client = ('127.0.0.1', self.port)
        
    def receive_loop(self):
        console_output('UDP:%d receive_loop start' % self.port)
        while self.is_running:
            try:
                data, self.client = self.server.recvfrom(2048)  # 接收数据和返回地址
                if self.callback:
                    self.callback(data, self.client)
            except socket.timeout:
                continue
            except ConnectionResetError:
                if self.isBind:
                    self.client = None
            except:
                if self.isBind:
                    self.client = None
                traceback.print_exc()
        console_output('UDP:%d receive_loop done' % self.port)
    
    def start_loop(self):
        self.is_running = True
        self.receive_thread = threading.Thread(target=UDPManager.receive_loop, args=(self,))
        self.receive_thread.start()

    def stop_loop(self):
        self.is_running = False
        self.receive_thread.join()
        self.server.close()
        
    def set_callback(self, cb):
        self.callback = cb
