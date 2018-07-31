#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import nmap
import sys
from datetime import datetime
import optparse
# from multiprocessing.pool import ThreadPool

# screenLock = Semaphore(value=1)   #加锁
# pool = ThreadPool(processes=150)    #开150个线程任务同时处理

def nmapScan(tatHost, tatPorts):

	nmScan = nmap.PortScanner()

	# san_raw_result = nmScan.scan(hosts=tatHost,ports=tatPorts)
	san_raw_result = nmScan.scan(hosts=tatHost,ports=tatPorts, arguments='v -n -A')

	for host,result in san_raw_result['scan'].items():

		if result['status']['state'] == 'up':
			print ('#' * 17 + 'Host:' + host + '#' * 17)
			print('-'*20 + '操作系统猜测' + '-'*20)
			for os in result['osmatch']:
				#系统判断测试暂时无法测试到windows10系统，原因未知
				print('操作系统为: ' + os['name'] + '   准确度为: ' + os['accuracy'])
			idno = 1
			try:
				for port in result['tcp']:
					try:
						print ('-' * 17 + 'TCP服务详细信息' + '[' + str(idno) + ']' + '-' * 17)
						idno += 1
						print ('TCP端口号：' + str(port))
						try:
							print ('状态：' + result['tcp'][port]['state'])
						except:
							pass
						try:
							print ('原因：' + result['tcp'][port]['reason'])
						except:
							pass
						try:
							print ('额外信息：' + result['tcp'][port]['extrainfo'])
						except:
							pass
						try:
							print ('名字：' + result['tcp'][port]['name'])
						except:
							pass
						try:
							print ('版本：' + result['tcp'][port]['version'])
						except:
							pass
						try:
							print ('产品：' + result['tcp'][port]['product'])
						except:
							pass
						try:
							print ('CPE：' + result['tcp'][port]['cpe'])
						except:
							pass
						try:
							print ('脚头：' + result['tcp'][port]['script'])
						except:
							pass
					except:
						pass
			except:
				pass
	#UDP后续补上

def main():
	parser = optparse.OptionParser('usage %prog ' + \
								   '-H <target host> -p <target port[s]>')
	parser.add_option('-H', dest='tatHost', type='string',\
					  help='specify target host')
	parser.add_option('-p', dest='tatPort', type='string',\
					  help='specify target port[s] separated by comma')

	(options, args) = parser.parse_args()

	tatHost = options.tatHost
	tatPorts = str(options.tatPort)
	# tatPorts = str(options.tatPort).split(',')

	if (tatHost == None) | (tatPorts[0] == None):
		print (parser.usage)
		exit(0)

	t1 = datetime.now()
	nmapScan(tatHost,tatPorts)
	t2 = datetime.now()
	total = t2 - t1
	print ('Scanning Completed in: ', total)
	# for tatPort in tatPorts:
	# 	nmapScan(tatHost,tatPort)


if __name__ == '__main__':
	main()
