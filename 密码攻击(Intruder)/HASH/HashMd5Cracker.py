#!/usr/bin/evn python
# -*- coding: utf-8 -*-

import hashlib
r'''
PS C:\Users\360\Desktop> py -3 .\hashMD5.py .\dict\TOP1000.txt 248698d0841cf61fad3d0e4e6d538fda

[+]Found password 123456789*

'''
def gethash(dict_file,md5_txt,md5_file='dictmd5.txt'):
	md5file = open(md5_file,'w')
	passwds = open(dict_file).readlines()

	for passwd in passwds:
		hash = hashlib.md5()
		# 更新密码将空格去掉，并且编码设置为UTF-8
		hash.update(passwd.strip().encode('utf-8'))
		# 测试查看hasd MD5后的密码
		# print (hash.hexdigest())
		if hash.hexdigest() == md5_txt:
			print ()
			print ("[+]Found password {0}".format(passwd))
		else:
			pass
		#将转换后的md5密文写到文件里
		# md5file.write(hash.hexdigest()+'\n')
	md5file.close
if __name__ == '__main__':
	import sys
	gethash(sys.argv[1],sys.argv[2])