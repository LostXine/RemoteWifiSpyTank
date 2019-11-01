# -*- coding:utf-8 -*-

from TCPManager import *
from utils import *

class HWManager:
    def __init__(self, _config):
        self.config_dict = _config
        self.client = TCPManager(self.config_dict['server_ip'], self.config_dict['control_port'], self.status_callback, False)
        self.loop_thread = None
        self.is_running = False
        self.send_buf = bytearray.fromhex('20d02080')
        self.move_speed = 0 # 0x0-0xf
    
    def main_loop(self):
        while self.is_running:
            timing_start = time.perf_counter()
            self._send_status()
            # 控制发送频率
            time.sleep(max(1/20 - time.perf_counter() + timing_start, 0))
    
    def status_callback(self, data, client):
        # 解析坦克发回的状态，后续使用
        pass
    
    def _send_status(self):
        # 设置速度
        if self.send_buf[1] >= 0xd0:
            self.send_buf[1] = merge_bytes(self.send_buf[1], self.move_speed)
        # 最后一个hex为校验，前7个hex取XOR后取反即可
        self.send_buf[-1] = merge_bytes(self.send_buf[-1], 0)
        xor = 0x0f
        for i in self.send_buf:
            xor ^= (i >> 4)
            xor ^= (i & 0x0f)
        self.send_buf[-1] = merge_bytes(self.send_buf[-1], xor)
        data = self.config_dict['control_header'] + bytes(self.send_buf)
        # print(data[-4:].hex())
        self.client.response(data)
    
    def set_speed(self, _speed):
        console_output("Change speed to %d" % _speed)
        self.move_speed = _speed
    
    def move_stop(self):
        self.send_buf = bytearray.fromhex('20d02080')
    
    def move_forward(self):
        self.send_buf = bytearray.fromhex('30d02090')
        
    def move_backward(self):
        self.send_buf = bytearray.fromhex('00d020a0')
        
    def turn_left(self):
        self.send_buf = bytearray.fromhex('24d02080')
        
    def turn_right(self):
        self.send_buf = bytearray.fromhex('28d02080')
        
    def cam_rise(self):
        self.send_buf[0] = merge_bytes(self.send_buf[0], merge_hex(self.send_buf[0], 2))
        
    def cam_sink(self):
        self.send_buf[0] = merge_bytes(self.send_buf[0], merge_hex(self.send_buf[0], 1))
    
    def start_loop(self):
        self.is_running = True
        if self.client.start_loop():
            return 2 # 连接失败
        self.loop_thread = threading.Thread(target=HWManager.main_loop, args=(self,))
        self.loop_thread.start()
        return 0
        
    def stop_loop(self):
        self.is_running = False
        if self.loop_thread:
            self.loop_thread.join()
        self.client.stop_loop()
    
        