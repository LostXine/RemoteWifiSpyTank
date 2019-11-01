# -*- coding:utf-8 -*-

from TCPManager import *
from UDPManager import *
import re

JPEG_SOI = bytes([0xff, 0xd8])
JPEG_EOF = bytes([0xff, 0xd9])
PACK_SOI = bytes([0x01, 0x50, 0x3c])

class RTSPManager:
    def __init__(self, _config):
        self.config_dict = _config
        self.cseq = 1
        self.trans_rtsp = ''
        self.session = ''
        self.repo_q = queue.Queue()
        self.client = TCPManager(self.config_dict['server_ip'], self.config_dict['server_port'], self.repo_callback, False)
        self.listener = UDPManager(self.config_dict['local_port'], self.decode_callback, True)
        
        self.data_cache = bytearray()
        self.img_cache = None

    def _get_rtsp_path(self):
        return 'rtsp://%s:%d/?action=stream RTSP/1.0\r\n' % \
        (self.config_dict['server_ip'], self.config_dict['server_port'])
    
    def _get_rtsp_session(self):
        if len(self.session):
            return 'Session: %s\r\n' % self.session
        else:
            return ''

    def _get_rtsp_tail(self):
        return 'CSeq: %d\r\nUser-Agent: Lavf57.71.100\r\n\r\n' % self.cseq

    def _send_rtsp_header(self, opt='OPTIONS', param='', url=None):
        if not url:
            url = self._get_rtsp_path()
        headers = opt + ' ' + url + param + self._get_rtsp_tail()
        self.client.response(headers.encode(encoding="utf-8"))
        self.cseq += 1
    
    def _send_rtsp_options(self):
        self._send_rtsp_header()
    
    def _send_rtsp_describe(self):
        self._send_rtsp_header('DESCRIBE', 'application/sdp\r\n')
        
    def _send_rtsp_setup(self):
        self._send_rtsp_header('SETUP', 'Transport: RTP/AVP/UDP;unicast;client_port=%d-%d\r\n' % (self.config_dict['local_port'], self.config_dict['local_port'] + 1), self.trans_rtsp)
    
    def _send_rtsp_play(self):
        self._send_rtsp_header('PLAY', 'Range: npt=0.000-\r\n' + self._get_rtsp_session())
    
    def _send_rtsp_teardown(self):
        self._send_rtsp_header('TEARDOWN', 'application/sdp\r\n' + self._get_rtsp_session())
    
    def _wait_for_response(self, timeout=2000):
        p = 0
        while p < timeout:
            if not self.repo_q.empty():
                return self.repo_q.get()
            time.sleep(0.01)
            p += 1
        raise socket.timeout
    
    def repo_callback(self, data, client):
        data = data.decode(encoding='utf-8')
        console_output('←%s:%d' % client)
        print('%s' % data)
        self.repo_q.put(data)
    
    def decode_callback(self, data, client):
        self.data_cache.extend(data)
        index = self.data_cache.rfind(JPEG_EOF)
        if index >= 0:
            # 一整包结束
            # soi = self.data_cache.find(JPEG_SOI)
            # print(soi)
            # 协议内容 (前20 byte)
            # 0     80  
            # 1-17  XX
            # 18-20 01 50 3c
            cache = bytes(self.data_cache[20:index + 2])
            self.img_cache = b''.join([i[:-17] for i in cache.split(PACK_SOI)])
            # print('%d%d' % (self.data_cache[index], self.data_cache[index + 1]))
            self.data_cache = self.data_cache[index + 2:]
    
    def _parse_rtsp_describe_repo(self, data):
        matchObj = re.search(r'content-base: (.*?)\r\n(.*)a=control:(.*?)\r\n', data, re.I|re.S) # 使匹配对大小写不敏感 使匹配包括换行在内的所有字符
        if matchObj:
            self.trans_rtsp = matchObj.group(1) + '/' + matchObj.group(3)
            return 0
        else:
            print("Failed to parse describe frame")
            return 1
        
    def _parse_rtsp_setup_repo(self, data):
        matchObj = re.search(r'session: (.*?)\r\n', data, re.I|re.S) # 使匹配对大小写不敏感 使匹配包括换行在内的所有字符
        if matchObj:
            self.session = matchObj.group(1)
        else:
            print("Failed to parse setup frame")
            return 1
    
    def start_loop(self):
        if self.client.start_loop():
            return 2 # 连接失败
        while True:
            try:
                self._send_rtsp_options()  # 查询可用命令
                self._wait_for_response()
                self._send_rtsp_describe() # 查询流媒体信息
                describe_repo = self._wait_for_response()
                if not self._parse_rtsp_describe_repo(describe_repo):
                    self._send_rtsp_setup()  # 准备流媒体客户端
                    setup_repo = self._wait_for_response()
                    if not self._parse_rtsp_setup_repo(setup_repo):
                        self.listener.start_loop()  # 监听udp数据
                        self._send_rtsp_play()  # 开始串流
                        return 0
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break
        self.stop_loop()
        return 1
    
    def stop_loop(self):
        self._send_rtsp_teardown()   # 停止RTSP
        self.client.stop_loop()
        self.listener.stop_loop()
    
    def get_image(self):
        return self.img_cache


    
