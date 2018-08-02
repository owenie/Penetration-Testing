#!/usr/bin/evn python
# -*- coding: utf-8 -*-

import requests
import re
import bs4
import itertools as its


# dic1 = open("dictionary1.txt",'a')
# for i in range(0,100000):
#     dic1.write(str(i) + "\n")
#     print (str(i).zfill(6))

# dic1.close()



words = "1234567890"
r = its.product(words,repeat=4)
dic2 = open("dictionary2.txt",'a')

for i in r:
    print (''.join(i))
    dic2.write("".join(i)+"\n")
dic2.close()
