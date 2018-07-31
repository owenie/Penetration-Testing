#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


from ftplib import FTP
import multiprocessing

def anonymous_ftp(hostname,timeout=1):
	try:
		connection = FTP(hostname, timeout=timeout)
		connection.login('anonymous', '1@2.net')
		connection.quit()
		return [1, hostname]

	except Exception as e:
		return [0, hostname]

def anonymous_scan(network):
	import ipaddress
	net = ipaddress.ip_network(network)
	pool=multiprocessing.Pool(processes=100)
	ip_list = []
	for ip in net:
		ip_list.append(str(ip))
	result = pool.map(anonymous_ftp, ip_list)
	for x in result:
		if x[0] == 1:
			print(x[1] + '为匿名FTP！')

if __name__ == '__main__':
	anonymous_scan('202.100.1.0/24')