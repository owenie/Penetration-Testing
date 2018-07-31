#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


import queue
import threading
import multiprocessing
import os

threads = 10

directory = '/root/Python_Hacker'
filters = [".txt", '.jpeg', '.gif', '.py', '.xml', '.png', '.pyc', '.cap', '.jpg']#这是排除不要的

os.chdir(directory)

local_paths = queue.Queue()

for r,d,f in os.walk("."):
	#路径名，目录列表和文件列表
	for files in f:
		local_path = "%s/%s" % (r,files)
		if local_path.startswith('.'):
			local_path = local_path[1:]
		if os.path.splitext(files)[1] not in filters:
		#>>> os.path.splitext('sdfsdf.txt')[1]
		#'.txt'
		#>>> os.path.splitext('sdfsdf.txt')[0]
		#'sdfsdf'
		#文件类型不在filters中的，添加到local_paths这个队列
			local_paths.put(local_path)

def print_local_paths():
	while not local_paths.empty():
		path = local_paths.get()
		print(path)
		#如果队列不为空，就提取队列数据并且打印

for i in range(threads):
	#使用多线程或者多进程来提取队列内的数据
	#t = threading.Thread(target=print_local_paths)
	#t.start()
	#or
	m = multiprocessing.Process(target=print_local_paths)
	m.start()