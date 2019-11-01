# -*- coding:utf-8 -*-

"""
@file: utils.py
@time: 2018/7/4 11:03
"""

import datetime
import cv2


def put_text_center(img, text):
    size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 1, thickness=2)
    position = (int(img.shape[1] / 2 - size[0][0] / 2), int(img.shape[0] / 2))
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_COMPLEX, 1,
                (0, 0, 0), thickness=3)
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_COMPLEX, 1,
                (0, 0, 255), thickness=2)
    return img


def put_double_text(img, context, position, scale, color):
    cv2.putText(img, context, position, cv2.FONT_HERSHEY_SIMPLEX,
                scale, (0, 0, 0), thickness=3)
    cv2.putText(img, context, position, cv2.FONT_HERSHEY_SIMPLEX,
                scale, color, thickness=2)
                    
                    
def put_text_left_top(img, text):
    cv2.rectangle(img, (0, 0), (47, 10), (0, 100, 0), -1)
    cv2.putText(img, text, (3, 8), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))
    return img


def console_output(msg):
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f] ') + msg)


def console_output_no_line(msg):
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f] ') + msg, end='')


def merge_hex(high, low):
    return (high & 0xc) + (low & 0x3)


def merge_bytes(high, low):
    return (high & 0xf0) + (low & 0x0f)
