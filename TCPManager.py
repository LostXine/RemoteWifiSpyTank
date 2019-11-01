# -*- coding:utf-8 -*-

"""
@file: TCPManager.py
@time: 2018/6/19 2:27
"""

import socket
import threading
import traceback
import queue
import time
from utils import console_output


class TCPManager:
    def __init__(self, tcp_addr, tcp_port, callback, bind=True):
        self.client = None
        self.receive_thread = None
        self.send_thread = None
        self.isBind = bind
        self.callback = callback
        self.q = queue.Queue()
        self.port = tcp_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = False
        self.server.settimeout(1)
        if self.isBind:
            self.server.bind(('127.0.0.1', self.port))  # 只允许本机连接
        else:
            self.client = (tcp_addr, self.port)
        
    def receive_loop(self):
        console_output('TCP:%d receive_loop start' % self.port)
        while self.is_running:
            try:
                data = self.server.recv(512)  # 接收数据和返回地址
                if self.callback:
                    self.callback(data, self.client)
            except socket.timeout:
                continue
            except:
                if self.isBind:
                    self.client = None
                traceback.print_exc()
                self.is_running = False
        console_output('TCP:%d receive_loop done' % self.port)

    def send_loop(self):
        console_output('TCP:%d send_loop start' % self.port)
        while self.is_running:
            if not self.q.empty():
                data = self.q.get()
                if self.client is not None:
                    try:
                        self.server.send(data)
                        # console_output('→%s:%d' % self.client)
                        # print('%s' % data)
                    except:
                        traceback.print_exc()
                        self.is_running = False
            if self.q.empty():
                time.sleep(0.01)
        console_output('TCP:%d send_loop done' % self.port)
    
    def start_loop(self):
        self.is_running = True
        try:
            self.server.connect(self.client)
        except socket.timeout:
            self.is_running = False
            console_output('TCP:%d send_loop failed' % self.port)
            return 1
        self.receive_thread = threading.Thread(target=TCPManager.receive_loop, args=(self,))
        self.send_thread = threading.Thread(target=TCPManager.send_loop, args=(self,))
        self.receive_thread.start()
        self.send_thread.start()
        return 0

    def stop_loop(self):
        self.is_running = False
        self.receive_thread.join()
        self.send_thread.join()
        self.server.close()

    def response(self, msg):
        self.q.put(msg)

    def set_callback(self, cb):
        self.callback = cb
        
if __name__ == '__main__':
    client = TCPManager('192.168.50.1', 8081, None, False)
    if not client.start_loop():
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
        client.stop_loop()
    
    
