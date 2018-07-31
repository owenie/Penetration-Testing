#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import optparse
from socket import *
from datetime import datetime
from threading import *
from multiprocessing.pool import ThreadPool  #多进程


#此脚本无法扫描win10

# 设置开始扫描的时间
t1 = datetime.now()

screenLock = Semaphore(value=1)   #加锁

def conScan(tatHost, tatPort):
	try:
		t1 = datetime.now()
		# pool = ThreadPool(processes=150)    #开150个线程任务同时处理
		connSkt = socket(AF_INET, SOCK_STREAM)
		connSkt.connect((tatHost, tatPort))
		data = 'ViolenPython'
		connSkt.send(data.encode())   #Python3以后send的内容必须市byte形式传输 
		results = connSkt.recv(2048).decode()     #抓取应用的Banner
		'''
		在python3中，利用套接字传输的内容都以byte形式传输，这时候传送时（send/sendto）需要encode，
		接收（recv）时需要decode。
		'''
		t2 = datetime.now()  
		'''
		如果信号量还没被锁上，县城就有权继续允许，
		并输出打印到屏幕上。如果信号量已经被锁定，我们只能等待,直到持有信号的线程释放信号量；
		通过利用信号量，能够确保在任何给定的时间点上只有一个线程可以打印屏幕
		'''
		screenLock.acquire()
		print ('-' * 17 + 'TCP服务详细信息' + '-' * 17)
		print ('端口号：'+ str(tatPort))
		print ('状态：' + 'open')
		print ('版本：' + str(results))
		total = t2 - t1
		print ('Scanning Completed in: ', total)

	except Exception as e:
		screenLock.acquire()
		pass
		# print ('[-]%d/tcp closed' % tatPort)
		# print (e)
	finally:

		screenLock.release()
		connSkt.close()

def portScan(tatHost, ltatPort, htatPort):
	try:
		tatIP = gethostbyname(tatHost)
	except:
		print ("[-] Cannot resolve '%s': Unknow host" % tatHost)
		return
	try:
		tatName = gethostbyaddr(tatIP)
		print ('\n[+] Scan Result for: hostname: ' + tatName[0])
	except:
		print ('\n[+] Scan Result for: ipaddr: ' + tatIP)

	setdefaulttimeout(1)

	pool = ThreadPool(processes=150)    #开150个线程任务同时处理
	
	for tatPort in range(int(ltatPort),int(htatPort)+1):
		result_obj = pool.apply_async(conScan,args=(tatHost, tatPort))
		#第二种方法，second method
		# t = Thread(target=conScan, args=(tatHost, tatPort))
		# t.start()
		# print ('Scaning port ' + str(tatPort))

		# conScan(tatHost, tatPort)

	pool.close()
	pool.join()

def main():
	parser = optparse.OptionParser('usage %prog -H' + \
		'<target host> -l <ltarget port> -h <ltarget port>')
	parser.add_option('-H',dest='tatHost', type='string', \
		help='specify target host')
	parser.add_option('-l',dest='ltatPort', type='string', \
		help='specify ltarget port')
	parser.add_option('-e',dest='htatPort', type='string', \
		help='specify htarget port')

	(options, args) = parser.parse_args()

	tatHost = options.tatHost       #目标主机
	ltatPort = options.ltatPort	    #低端口
	htatPort = options.htatPort		#高端口

	# tatPorts = str(options.tatPort).split(r',')

	if (tatHost == None) & (ltatPort == None) & (htatPort == None):
		print (parser.usage)
		exit(0)
	
	portScan(tatHost, ltatPort, htatPort)


if __name__ == '__main__':
	main()
