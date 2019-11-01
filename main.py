# -*- coding:utf-8 -*-

from RTSPManager import *
from HWManager import *
import numpy as np
import cv2
import datetime

config_dict = {
    'server_ip': '192.168.50.1',  # 车辆IP
    'server_port': 8080,          # RTSP视频控制端口TCP
    'local_port': 21836,          # RTSP本地视频接收端口UDP
    'control_port': 8081,         # 车辆控制端口TCP
    'control_header': bytes.fromhex('4750534f434b45540001ff000004')  # 控制指令头
}

def print_usage():
    print("Remote YD-211s Wifi Spy Tank 操作说明")
    print('-' * 10)
    print("0-9 设置速度(默认0)")
    print("w/s/a/d 前后与转向")
    print("r/f 升起/降下摄像头")
    print("x 停止所有运动")
    print("enter 保存当前图片")
    print("q/esc 退出")
    print("=" * 10)
        
def tank_main():
    print_usage()
    rtsp = RTSPManager(config_dict)  # 视频连接
    hw = HWManager(config_dict)      # 控制连接
    ret = rtsp.start_loop() 
    if ret:
        console_output("Failed to connect")
        return ret
    ret = hw.start_loop()
    if ret:
        rtsp.stop_loop()
        return ret
    
    action_dict = {
        ord('w'): hw.move_forward,
        ord('s'): hw.move_backward,
        ord('x'): hw.move_stop,
        ord('a'): hw.turn_left,
        ord('d'): hw.turn_right,
        ord('r'): hw.cam_rise,
        ord('f'): hw.cam_sink,
    }    
    
    while True:
        try:
            data = rtsp.get_image()
            if data:
                image_data = np.asarray(bytearray(data), dtype="uint8")
                image = cv2.imdecode(image_data, -1)
                cv2.imshow("camera", image)
                k = cv2.waitKey(20) & 0xff
                if k in [27, ord('q')]:
                    break
                elif k == 13:
                    if cv2.imwrite(datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f.jpg'), image):
                        console_output('Image saved successfully.')
                    else:
                        console_output('Failed to save image.')
                elif k in action_dict:
                    action_dict[k]()
                elif 47 < k < 58:
                    hw.set_speed(k - 48)
                else:
                    pass
                    # hw.move_stop()
        except cv2.error:
            traceback.print_exc()
            break
        except KeyboardInterrupt:
            break
    hw.move_stop()
    rtsp.stop_loop()
    hw.stop_loop()

if __name__ == '__main__':
    tank_main()

