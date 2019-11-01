# Remote Wifi Spy Tank YD-211S

![YD-211S](/YD-211S.png)
[Readme Chinese Ver.](/readme.md)

This project offers a remote controller of Wifi Spy Tank YD-211S on PC. So people who are interested in image processing, computer vision, even artificial intelligence can use this tank as a budget mobile platform. Neither the manufacturer or the distributor of this tank sponsored this unofficial nonprofit project.

I'll be very happy to know if this project helps you somehow.

### Current Features
1. Control all motors of the spy tank
2. Grab video stream from the spy tank

### Todo
1. Hack the battle mode
2. Hack the lights on tank（If possible）

### Quick Start 
1. Install Python3 and OpenCV
   ```
   pip install opencv-python
   ```
2. Connect your PC to the Wifi of tank
   
3. Change config_dict in [main.py](/main.py) if needed, run main.py
```
config_dict = {
    'server_ip': '192.168.50.1',  # IP address of the tank
    'server_port': 8080,          # TCP port of RTSP command frame
    'local_port': 21836,          # Local UDP port to receive RTSP stream
    'control_port': 8081,         # TCP port of motor control frames
    'control_header': bytes.fromhex('4750534f434b45540001ff000004')  # Header of motor control frame
}
```

### Usage
* x：Stop all motors
* w/s：Move forward/backward
* a/d：Turn left/right
* r/f: Raise/sink camera
* 0-9：Set motor speed(Default:0，Max:0xf)
* Enter：Save current image
* q/Esc：Quit

### Contact Me
* Issue
* Email: lostxine@gmail.com
