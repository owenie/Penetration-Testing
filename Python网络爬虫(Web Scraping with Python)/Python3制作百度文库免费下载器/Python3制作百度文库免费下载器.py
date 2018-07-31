[mw_shl_code=python,true]#!/usr/bin/env python

#-*-coding:utf-8-*-

__author__ = 'nie zhi yong QQ:1368902371'


import requests


header = {'Accept': 'text/plain, */*; q=0.01', #模拟浏览器头信息

'Accept-Encoding': 'gzip, deflate',

'Accept-Language': 'zh-CN,zh;q=0.9',

'Connection': 'keep-alive',

'Content-Length': '135',

'Content-Type': 'application/x-www-form-urlencoded',

'Host': '39.108.149.27:9999',

'Origin': 'http://39.108.149.27:9999',

'Referer': 'http://39.108.149.27:9999/',

'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',

'X-Requested-With': 'XMLHttpRequest'

}

wenku = input('请输入您要下载文档的地址(前后不要使用引号)：')

mailadd = input('请输入邮箱地址(前后不要使用引号):')

#真实网址

url = 'http://39.108.149.27:9999/default.aspx'

#提交数据

datas = {

'username':'',

'password':'' ,

'txtUrl': '{}'.format(wenku),

'mail': '{}'.format(mailadd)

}

html = requests.request("POST",url,data=datas,headers=header)

print(html.text) 