#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import zipfile
from threading import Thread

def extractFile(zfile, password):
	z = zfile 
	try:
		z.extractall(pwd=str(password))
		print("[+] Found password " + password + "\n")
	except Exception,e:
		pass

def main():
	zFile = zipfile.ZipFile('QR_code.zip')  #zip文件
	passfile = open('dictionary.txt')       #字典

	for line in passfile.readlines():
		password = line.strip('\n')

		t = Thread(target=extractFile, args=(zFile, password))
		t.start()

if __name__ == '__main__':
	main()