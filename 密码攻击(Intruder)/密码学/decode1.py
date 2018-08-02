#!/usr/bin/python
#encoding=UTF=8
import hashlib
import itertools
from base64 import b64decode
def check(str):
    m1 = hashlib.md5(str)
    if m1.hexdigest() == '16478a151bdd41335dcd69b270f6b985':
        return True
    else:
        return False
list1=itertools.product(['Y','y'],['M','m'],['F','f'],['Z','z'],['Z','z'],['T','t'],['Y','y'],['0'],['D','d'],['3'],['R','r'],['M','m'],['D','d'],['3'],['R','r'],['M','m'],['M','m'],['T','t'],['I','i'],['Z','z'])
for i in list1:
    str1=''.join(i)
    if check(b64decode(str1)):
        print "The Flag is "+b64decode(str1)
        break