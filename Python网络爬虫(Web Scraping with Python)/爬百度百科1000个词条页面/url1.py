#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import urllib.request
from http import cookiejar
from bs4 import BeautifulSoup
import re

#第一种方法
def open_url(url):
	req = urllib.request.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
	page = urllib.request.urlopen(req)
	html = page.read().decode('utf-8')
	return len(html),page.getcode()
#第二种方法
def cj(url):
	#声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler=urllib.request.HTTPCookieProcessor(cookie)
    #通过CookieHandler创建opener
    opener = urllib.request.build_opener(handler)

    page = opener.open(url)
    html = page.read().decode('utf-8')

    # print ('\n')
    # print (cookie)
    # print ('\n')
    return len(html),page.getcode()
#网页解析器BeautifulSoup
def Bs():
	html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
	soup = BeautifulSoup(html_doc,'html.parser') #html文档字符串，html解析器，html文档编码
	print ('获取所有的链接')
	links = soup.find_all('a')
	for link in links:
		print (link.name,link['href'],link.get_text())

	print ('获取lacie的链接')
	link_node = soup.find('a',href='http://example.com/lacie')
	print (link_node.name,link_node['href'],link_node.get_text())

	print ('正则匹配tillie')
	link_node = soup.find('a',href=re.compile(r'ill'))
	print (link_node.name,link_node['href'],link_node.get_text())

	print ('获取p段落文字')
	p_node = soup.find('p',class_='title')
	print (p_node.name,p_node.get_text())
if __name__ == '__main__':
	print (open_url('http://www.baidu.com'))
	print (cj('http://www.baidu.com'))
	Bs()