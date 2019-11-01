# Remote Wifi Spy Tank YD-211S

![YD-211S](/YD-211S.png)
[Readme English Ver.](/readme_en.md)

本项目旨在分享一种操作Wifi视频坦克YD-211S的工具，为有志于学习图像处理、计算机视觉及人工智能的同学及吃瓜群众提供一种获得廉价可用的移动视觉平台新思路。本项目是非官方的非盈利项目，作者与该坦克的生产厂商、经销渠道等实体无任何商业合作关系。如果有幸能够帮助到您，请务必告诉作者让他开心一下。

### 现有功能
1. 使用计算机通过Wifi直接控制视频坦克的运动、摄像头的升降
2. 通过Wifi获取视频坦克拍摄的实时图像

### 更新计划
1. 破解对战模式中的控制代码
2. 破解对顶部绿灯与前进后退灯的单独控制（如果可能的话）

### 轻松上手 
1. 安装Python3与OpenCV
   ```
   pip install opencv-python
   ```
2. 启动坦克，连接到坦克的Wifi
   
3. 请视实际情况将[main.py](/main.py)中的config_dict修改为您的配置，然后运行main.py
```
config_dict = {
    'server_ip': '192.168.50.1',  # 车辆IP
    'server_port': 8080,          # RTSP视频控制端口TCP
    'local_port': 21836,          # RTSP本地视频接收端口UDP
    'control_port': 8081,         # 车辆控制端口TCP
    'control_header': bytes.fromhex('4750534f434b45540001ff000004')  # 控制指令头
}
```

### 操作方法
* x：停止所有运动
* w/s：前进/后退
* a/d：左/右转向
* r/f: 升起/降下摄像头
* 0-9：设置运动速度(默认0，最大可到0xf)
* Enter：保存当前图像
* q/Esc：退出程序

### 联系我
* Issue
* Email: lostxine@gmail.com
