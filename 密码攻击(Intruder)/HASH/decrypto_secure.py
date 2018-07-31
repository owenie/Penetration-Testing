#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


import os

def cisco_secure(cisco_secure, passwd_dict_file):
	cisco_secure_list = cisco_secure.split('$')
	passwds = open(passwd_dict_file, 'r').readlines()
	for passwd in passwds:
		cmd = 'openssl passwd -1 -salt ' + cisco_secure_list[2] + ' ' + passwd.strip()
		result = os.popen(cmd).readlines()[0].strip()
		if cisco_secure == result:
			print('Password Finded: ' + passwd.strip())
			os._exit(1)
	print('Password no Find!!!')
if __name__ == '__main__':
	secret = input('请输入Cisco Enable Secret: ')
	path = input('请输入密码字典完整路径: ')
	cisco_secure(secret, path)


