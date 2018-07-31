#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Date    : 2017-10-20 14:21:52
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import urllib.request
import urllib.parse
import json
while True:
	print ("\033[0;32mYou can enter 'q' quit the program!\033[0m")
	content =  input('\n\033[0;32m请输入需要翻译的内容: \033[0m')
	if content != 'q':
		# 注意这里用unicode编码，否则会显示乱码
#		content = input(u"请输入要翻译的内容：")
		# 网址是Fig6中的 Response URL
		url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=http://www.youdao.com/'
		# 爬下来的数据 data格式是Fig7中的 Form Data
		data = {}
		data['type'] = 'AUTO'
		data['from'] = 'AUTO'
		data['to'] = 'AUTO'
		data['smartresult'] = 'dict'
		#data['sign'] = '798ef2d178a626b34fcffa05d1a10c4b'
		data['action'] = 'FY_BY_CLICKBUTTION'
		data['salt'] = '1508395428816'
		data['i'] = content
		data['doctype'] = 'json'
		#data['version'] = '2.1'
		data['keyfrom'] = 'fanyi.web'
		data['ue'] = 'UTF-8'
		data['typoResult'] = 'true'
		head = {}
		head['User_Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
		# 数据编码
		#data = urllib.urlencode(data)
		data = urllib.parse.urlencode(data).encode('utf-8')
		# 按照data的格式从url爬内容
		response = urllib.request.urlopen(url,data)
		# 将爬到的内容读出到变量字符串html，
		html = response.read().decode('utf-8')
		# 将字符串转换成Fig8所示的字典形式
		target = json.loads(html)
		# 根据Fig8的格式，取出最终的翻译结果
		result = target["translateResult"][0][0]['tgt']

		# 这里用unicode显示中文，避免乱码
		print(u"\n\033[5;31m翻译结果：%s\033[0m" % (target["translateResult"][0][0]['tgt']))
	else:
		print ("You've quit!")
		break
