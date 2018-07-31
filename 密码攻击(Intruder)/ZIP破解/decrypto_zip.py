#!/usr/bin/python3.4
# -*- coding=utf-8 -*-

import zipfile
import optparse
import multiprocessing

def extractFile(zipfilename, password):
	try:
		zFile = zipfile.ZipFile(zipfilename)
		zFile.extractall(pwd=password.encode())#尝试用密码解压文件
		print('密码被找到:' + password)#如果不出现异常，密码就正确
	except RuntimeError:#如果异常就报密码错误
		print('错误的密码:' + password)

if __name__ == "__main__":
	parser = optparse.OptionParser("程序使用方法介绍: -f <压缩文件名> -d <字典>")
	parser.add_option('-f', dest = 'zname', type = 'string', help = '指定压缩文件')
	parser.add_option('-d', dest = 'dname', type = 'string', help = '指定字典文件')
	(options, args) = parser.parse_args()
	#print(options)
	#print(args)
	if (options.zname == None) or (options.dname == None):
		print(parser.usage)
		exit(0)
	else:
		zname = options.zname
		dname = options.dname
	passFile = open(dname)
	for line in passFile.readlines():#使用多进场进行破解！
		password = line.strip('\n')
		crack_process = multiprocessing.Process(target=extractFile, args=(zname, password))
		crack_process.start()