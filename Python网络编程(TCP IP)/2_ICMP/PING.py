#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错
from scapy.all import *
import time
import struct
import random
import sys
import re


def ping_one(dst, id_no, seq_no, ttl_no):
    send_time = time.time()
    time_in_bytes = struct.pack('>d', send_time)  # 把发出的时间,写入ICMP数据部分
    # 构建ICMP Echo数据包
    ping_one_reply = sr1(IP(dst=dst, ttl=ttl_no) / ICMP(id=id_no, seq=seq_no) / time_in_bytes, timeout=1, verbose=False)
    try:
        if ping_one_reply.getlayer(ICMP).type == 0 and ping_one_reply.getlayer(
                ICMP).code == 0 and ping_one_reply.getlayer(ICMP).id == id_no:  # 确认type,code和id是否匹配
            # 提取源IP,序列号,TTL,计算数据长度
            reply_source_ip = ping_one_reply.getlayer(IP).src
            reply_seq = ping_one_reply.getlayer(ICMP).seq
            reply_ttl = ping_one_reply.getlayer(IP).ttl
            reply_data_length = len(ping_one_reply.getlayer(Raw).load) + len(ping_one_reply.getlayer(Padding).load) + 8
            # 提取返回数据,转换为时间,并与当前时间计算时间差
            reply_data = ping_one_reply.getlayer(Raw).load
            receive_time = time.time()
            echo_request_sendtime = struct.unpack('>d', reply_data)
            time_to_pass_ms = (receive_time - echo_request_sendtime[0]) * 1000
            # 返回数据长度, 源IP地址,序列号,TTL和用时
            return reply_data_length, reply_source_ip, reply_seq, reply_ttl, time_to_pass_ms
    except Exception as e:
        if re.match('.*NoneType.*', str(e)):
            return None


def qyt_ping(dst):
    # 随机产生ICMP ID
    id_no = random.randint(1, 65535)
    for i in range(1, 6):  # ping五个包
        ping_result = ping_one(dst, id_no, i, 64)
        if ping_result:
            print('%d bytes from %s: icmp_seq=%d ttl=%d time=%4.2f ms' % (
                ping_result[0], ping_result[1], ping_result[2], ping_result[3], ping_result[4]))
            time.sleep(1)
        else:
            print('.', end='', flush=True)  # flush=True立即答应
    print()


if __name__ == '__main__':
    # Windows Linux均可使用
    qyt_ping('10.1.1.254')
