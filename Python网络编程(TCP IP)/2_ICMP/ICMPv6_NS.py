#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# IPv6参考文档
# https://www.idsv6.de/Downloads/IPv6PacketCreationWithScapy.pdf
# https://www.ernw.de/download/Advanced%20Attack%20Techniques%20against%20IPv6%20Networks-final.pdf

import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错
from scapy.all import *
from Tools.GET_MAC_netifaces import get_mac_address
from Tools.IPv6_Tools import Solicited_node_multicast_address,mac_to_ipv6_linklocal


# Windows 查看IPv6邻居 netsh int ipv6 show neigh
# IOS     查看IPv6邻居 show ipv6 neighbors
# Linux   查看IPv6邻居 ip -6 neigh                 | ping6 2001:1::200

def icmpv6_ns(host, ifname):  # 请求特定IPv6地址的MAC地址
    ll_mac = get_mac_address(ifname)  # 获取本机接口MAC地址
    # 构建icmpv6_ns数据包

    # -----------IPv6头部 - -----------
    # Next Header: 0x3A(ICMPv6)
    # 原地址: Link Local address
    # 目的地址: Solicited node multicast address
    #
    # ----------ICMPv6头部 - ---------
    # ICMPv6 Type: 135
    # ICMPv6 Code: 0(NS)
    # 目标地址: 2001:1::253
    #
    # ----Source Link-Layer Address - ---
    # 源地址: 00:50:56:AB:25:08(本地MAC地址)

    packet = IPv6(src=mac_to_ipv6_linklocal(ll_mac), dst=Solicited_node_multicast_address(host)) / ICMPv6ND_NS(tgt=host) / ICMPv6NDOptSrcLLAddr(
        lladdr=ll_mac)
    # packet.show()
    # 发送数据包
    result = sr1(packet, timeout=2, verbose=False)
    # 提取返回的MAC地址
    # result.show()
    return result.getlayer("ICMPv6 Neighbor Discovery Option - Destination Link-Layer Address").fields['lladdr']


if __name__ == '__main__':
    # Windows Linux均可使用
    print(icmpv6_ns("2001:1::253", 'Net1'))
