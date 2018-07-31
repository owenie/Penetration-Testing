#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


from ftplib import FTP

def ftp_login(dict, timeout=1):
	try:
		hostname = dict[0]
		username = dict[1]
		password = dict[2]
		connection = FTP(hostname)
		connection.login(username, password)
		connection.quit()
		return [1, hostname, username, password]

	except Exception as e:
		return [0, hostname, username, password]

def ftp_login_result(dict, timeout=1):
	try:
		hostname = dict[0]
		username = dict[1]
		password = dict[2]
		connection = FTP(hostname)
		connection.login(username, password)
		connection.quit()
		print('PASS' * 8)
		print('主机: ' + hostname)
		print('用户名: ' + username)
		print('密码:' + password)
		print('有效！！！！')

	except Exception as e:
		print('FAIL' * 8)
		print('主机: ' + hostname)
		print('用户名: ' + username)
		print('密码:' + password)
		print('无效！！！！')

if __name__ == '__main__':
	print(ftp_login_result(('202.100.1.100', 'cisco', 'cisco123')))