# coding: utf-8
#author： 360college.Run
#Python-ScannerV1.0 本程序可以实现单线程扫描端口，每个端口扫描超时0.5s

#Python Socket编程资料
#https://www.cnblogs.com/fanweibin/p/5053328.html

import socket
from datetime import datetime

# 设置超时时间 单位 S
socket.setdefaulttimeout(0.5)

# 获取目标IP地址
#Linux系统下可以使用该函数获取目标IP地址
remote_server = raw_input("Enter a remote host to scan:\n")
remote_server_ip = socket.gethostbyname(remote_server)
#windows目标地址需要将目标IP内置到程序中
#remote_server_ip = "101.198.186.58"

# 格式化输出 要扫描的ip地址
print '-' * 60
print 'Please wait, scanning remote host ', remote_server_ip
print '-' * 60

# 设置开始扫描的时间
t1 = datetime.now()

# 使用 range（）函数遍历生成要扫描的端口 1-1024
# 加入错误捕捉机制
try:
    for port in range(1,1025):
        sock = socket.socket(2,1) # 2:socket.AF_INET 1:socket.SOCK_STREAM
        res = sock.connect_ex((remote_server_ip,port))
        if res == 0:
            print 'Port {}: OPEN'.format(port)
        sock.close()

except socket.gaierror:
    print 'Hostname could not be resolved.Exiting'

except socket.error:
    print "Could't connect to the server"

# 获取扫描结束时间
t2 = datetime.now()

# 计算扫描使用时长
total = t2 - t1

# 输出扫描结果
print 'Scanning Completed in: ', total
