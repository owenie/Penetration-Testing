#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import ipaddress
from multiprocessing.pool import ThreadPool
from ARP_Request import arp_request
from Tools.SORT_IP import sort_ip


def scapy_arp_scan(network,ifname):
    net = ipaddress.ip_network(network)
    ip_list = []
    for ip_add in net:
        ip_list.append(str(ip_add))  # 把IP地址放入ip_list的清单
    pool = ThreadPool(processes=100)  # 创建多进程的进程池（并发为100）
    result = []
    for i in ip_list:
        result.append(pool.apply_async(arp_request,args=(i,ifname))) # 关联函数与参数，并且添加结果到result
    pool.close()  # 关闭pool，不在加入新的进程
    pool.join()  # 等待每一个进程结束
    scan_list = []  # 扫描结果IP地址的清单
    for r in result:
        if r.get()[1] is None:  # 如果没有获得MAC，就continue进入下一次循环
            continue
        scan_list.append(r.get()[0])  # 如果获得了MAC，就把IP地址放入scan_list清单
    return sort_ip(scan_list)  # 排序并且返回清单


if __name__ == '__main__':
    # Windows Linux均可使用
    import time

    t1 = time.time()
    print('活动IP地址如下:')
    for ip in scapy_arp_scan("10.1.1.0/24",'Net1'):
        print(str(ip))
    t2 = time.time()
    print('本次扫描时间: %.2f' % (t2 - t1))  # 计算并且打印扫描时间
