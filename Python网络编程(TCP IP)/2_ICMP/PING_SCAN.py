#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from multiprocessing.pool import ThreadPool
from PING_ONE import scapy_ping_one
from scapy.all import *
from Tools.SORT_IP import sort_ip


def scapy_ping_scan(network):
    net = ipaddress.ip_network(network)
    ip_list = []
    for ip in net:
        ip_list.append(str(ip))  # 把IP地址放入ip_list的清单
    pool = ThreadPool(processes=10)  # 创建多进程的进程池（并发为10）
    result = pool.map(scapy_ping_one, ip_list)  # 关联函数与参数，并且提取结果到result
    pool.close()  # 关闭pool，不在加入新的进程
    pool.join()  # 等待每一个进程结束
    scan_list = []  # 扫描结果IP地址的清单
    for ip, ok in result:
        if ok == 1:  # 如果范围值为1
            scan_list.append(ip)  # 把IP地址放入scan_list清单里边
    return sort_ip(scan_list)  # 排序并且打印清单


if __name__ == '__main__':
    # Windows Linux均可使用
    import time

    t1 = time.time()
    print('活动IP地址如下:')
    for ip in scapy_ping_scan("10.1.1.0/24"):
        print(str(ip))
    t2 = time.time()
    print('本次扫描时间: %.2f' % (t2 - t1))  # 计算并且打印扫描时间
