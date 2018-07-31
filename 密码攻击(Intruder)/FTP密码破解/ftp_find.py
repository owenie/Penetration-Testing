#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


from ftplib import FTP
import re
start_path = '/'

def ftp_find(dict, file_type='.py', timeout=1):
	try:
		hostname = dict[0]
		username = dict[1]
		password = dict[2]
		connection = FTP(hostname)
		connection.encoding = 'GB18030'
		connection.login(username, password)
		path = []
		def DirRecursive(dirpath):
			ls = []
			connection.cwd(dirpath)#进入特定目录
			connection.retrlines('LIST', ls.append)#‘LIST’命令的回显，添加到ls这个清单
			#print(ls)
			for line in ls:#提取每一行并且做正则表达式匹配
			#07-28-16  05:37PM       <DIR>          qytang
			#07-28-16  04:44PM         5 			test1.txt
			#07-28-16  04:44PM         5 			test2.txt
				patt = '(\d\d-\d\d-\d\d)\s*(\d\d\:\d\d\w\w)\s*(<DIR>|\d*)\s*(\w.*)'
				scan_result = re.match(patt, line)
				date = scan_result.group(1)
				time = scan_result.group(2)
				dir_or_length = scan_result.group(3)
				dir_or_filename = scan_result.group(4)

				if dir_or_length != '<DIR>':#如果不是目录(那就是文件），添加到path清单
					if dirpath == '/':
						path.append(dirpath + dir_or_filename)
					else:
						path.append(dirpath + '/' + dir_or_filename)
				else:#如果是目录就递归
					if dirpath == '/':
						DirRecursive(dirpath + dir_or_filename)
					else:
						DirRecursive(dirpath + '/' + dir_or_filename)

		DirRecursive(start_path)#从起始目录开始递归查询

		connection.close()
		if file_type == '.':
			return path#如果搜索文件类型没有指定，就返回完整path清单
		else:#如果指定搜索文件类型，就把搜索到的特定文件路径添加到path清单
			filetype_in_ftp = []
			offset = 0 - len(file_type)
			for x in path:
				if x[offset:] == file_type:
					filetype_in_ftp.append(x)

			return filetype_in_ftp
	except Exception as e:
		print(e)

if __name__ == '__main__':
	print(ftp_find(('202.100.1.168', 'administrator', 'Cisc0123'), '.txt'))