#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Date    : 2017-10-20 16:33:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import urllib.request
import urllib.parse
import json
content = 0
#head = {}
#head['User_Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
while True:
	content =  input('\n请输入需要翻译的内容:')
	if content != 'quit':
		url = 'http://fanyi.baidu.com/v2transapi'
		data = {}
#		data['from'] = 'AUTO'
#		data['to'] = 'AUTO'
		data['query'] = content
		data['transtype'] = 'translang'
		data['simple_means_flag'] = '3'
		data = urllib.parse.urlencode(data).encode('utf-8')
		response = urllib.request.urlopen(url,data)
		html = response.read().decode('utf-8')
		target = json.loads(html)
		tgt = target['trans_result']['data'][0]['dst']
		print ("\n翻译的结果是: %s" % tgt)
	else:
		print ("You've quit！")
		break