#!/usr/bin/python3.6
# -*- coding=utf-8 -*-

def caeser_decode(string):
	for i in range(26):
		
		i += 1   #第一次循环这里i=0 + 1，所以i=1
		print('\n', '偏移位:',i, '\n')
		decode = caeser_encrypt(string,i)
		print ('解密结果:',decode)
		#讲用户输入的字符串全部转给caeser_encrypt，循环26次1-26，每一次传给一个偏移为给caeser_encrypt

def caeser_encrypt(string,i):
	string_new = ''
	for s in string:
		string_new += change(s,i)
		#一次传一个字母一个偏移位给change然后将结果拼一起返回
	print (string_new.upper())
	return string_new

def change(c,i):
	'''
	该算法需要用到ASCII知识，26个小写字母对应的数字是97-122
	'''
	c = c.lower()
	num = ord(c)
	if num >= 97 and num <= 122:
		num = 97 + ((num - 97) + i) % 26
	return (chr(num))

def main():
	print('请输入操作码：')
	print('1:凯撒加密')
	print('2:凯撒解密')
	choice = input()
	if choice == '1':
		string = input('请输入需要加密的字符串：')
		num = int(input('请输入需要偏移的位数：'))
		caeser_encrypt(string,num)
	elif choice == '2':
		string = input('请输入需要解密的字符串：')
		caeser_decode(string)
	else:
		print ('输入错误，请重新输入！')
		main()
if __name__ == '__main__':
	main()