#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


import crypt
import os

def decrypto_hash(hashpassword, passwd_dict_file):
	hashpassword_list = hashpassword.split('$')
	salt = '$'+ hashpassword_list[1] + '$' + hashpassword_list[2] + '$'
	#读取盐
	#$1$f6y4$1Lev506HhZ0LE.IR6jRB.0
	#$1$f6y4$
	#print(salt)
	passwds = open(passwd_dict_file, 'r').readlines()
	for passwd in passwds:
		result = crypt.crypt(passwd.strip(), salt)#密码加盐计算得到hash结果
		if hashpassword == result:#如果结果相同密码被找到
			print('Password Finded: ' + passwd.strip())
			os._exit(1)
	print('Password no Find!!!')
if __name__ == '__main__':
	secret = input('请输入Hash后的密码: ')
	path = input('请输入密码字典完整路径: ')
	decrypto_hash(secret, path)


