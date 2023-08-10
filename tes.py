import threading, os, time
status={}
def function(a,b):
	status[a+b]=None
def ping_device(ip):
	print('start at '+time.ctime()+' for '+ip)
	x = os.popen('ping "'+str(ip)+'"').readlines()
	# for i in x:
	# 	print(i)
	print(' end at '+time.ctime()+' for '+ip)
ip=['172.16.1.212',
'192.168.5.240',
'172.16.0.32',
'10.10.64.6',
'10.10.64.13',
'192.168.5.8',
'172.16.7.41',
'172.16.7.42',
'172.16.7.43',
'172.16.7.44',
'172.16.7.45',
'172.16.7.46',
'172.16.7.47',
'172.16.7.48',
'172.16.7.49',
'172.16.7.50']
ipindex=0
ipcount=0
ipstart=0
def prosesin():
	print(x)
	print(ip[x])
t=[None]*10
print(t)
while True:
	if(ipindex==len(ip)):
		ipindex=0
	ipcount=ipcount+1
	print('proses threading semua')
	print("ipindex\t"+str(ipindex))

	print('ipcount\t'+str(ipcount))
	print('ipstart\t'+str(ipstart))
	print()
	if (ipcount==10):
		if (ipstart>ipindex+1):
			for x in range(ipstart,len(ip)):
				prosesin()
			for x in range(0,ipindex+1):
				prosesin()
		else:
			for x in range(ipstart,ipindex+1):
				prosesin()
		ipstart=ipindex+1
		ipcount=0
	ipindex=ipindex+1
	
	time.sleep(0.5)
	
# for x in ip:
# 	status[x]=''
# print(status)
# for y in ip:
	# ping_device(y)
# ping_device(ip[0])
# ping_device(ip[1])
# t1 = threading.Thread(target=ping_device, args=('172.16.7.212',))
# t2 = threading.Thread(target=ping_device, args=(ip[1]))
# t3 = threading.Thread(target=ping_device, args=(ip[2]))
# t1.start()
# t2.start()
# t3.start()
# t=[]
# count=0
# start=0
# for x in range(len(ip)):
# 	t.append(threading.Thread(target=ping_device, args=(ip[x],)))
# 	t[x].start()
# 	count=count+1
# 	if count==10:
# 		for y in range(start,x+1):
# 			t[x].join()
# 		count=0
# 		start=x+1
# 		
# t1=threading.Thread(target=function, args=(2,3,))
# t1.start()
# t1.join()
# status["color"] = "red"
# status['warna'] = 'merah'
# print(status)
# print(len(status))
