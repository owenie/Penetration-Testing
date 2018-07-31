#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错
from scapy.all import *
from Tools.GET_IP_netifaces import get_ip_address  # 获取本机IP地址
from Tools.GET_MAC_netifaces import get_mac_address  # 获取本机MAC地址


def arp_request(ip_address, ifname='ens33'):
    # 获取本机IP地址
    localip = get_ip_address(ifname)
    # 获取本机MAC地址
    localmac = get_mac_address(ifname)
    try:  # 发送ARP请求并等待响应
        result_raw = srp(Ether(src=localmac, dst='FF:FF:FF:FF:FF:FF') /
                         ARP(op=1,
                             hwsrc=localmac, hwdst='00:00:00:00:00:00',
                             psrc=localip, pdst=ip_address),
                             #iface=ifname,  # windows 环境需要去掉
                             timeout=1,
                             verbose=False)
        # 把响应的数据包对，产生为清单
        result_list = result_raw[0].res
        # [0]第一组响应数据包
        # [1]接受到的包，[0]为发送的数据包
        # 获取ARP头部字段中的['hwsrc']字段，作为返回值返回
        return ip_address, result_list[0][1].getlayer(ARP).fields['hwsrc']
    except IndexError:
        return ip_address, None


if __name__ == "__main__":
    # Windows Linux均可使用
    arp_result = arp_request('10.1.1.254', "Net1")
    print("IP地址:", arp_result[0], "MAC地址:", arp_result[1])
