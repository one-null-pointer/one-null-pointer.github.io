import json
import requests

url='http://192.168.0.103:8080/'

head={
	'User-Agent':'Mozilla/5.0(compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
}
for data in open('PH1P.txt'):
    data=data.replace('\n','')
    urls=url+data
    code=requests.get(urls.headers=head).status_code
    print(urls+'|'+str(code))