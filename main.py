# python "D:\python\ping monitor\main.py"
import os, time, threading
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1Aqfni6JAQI6xViilnB1hzYaFig-2BB6EoNZmA6-oAqs"
credentials = None
status=[]
sttindex=0
data=[]
totalnetto=0
# def read_settings():

def manage_credentials():
	global credentials
	print('managing credentials...')
	if os.path.exists("C:/Users/Admin/Documents/Ping Monitor/token.json"):
		credentials = Credentials.from_authorized_user_file("C:/Users/Admin/Documents/Ping Monitor/token.json", SCOPES)
	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("C:/Users/Admin/Documents/Ping Monitor/credentials.json", SCOPES)
			credentials = flow.run_local_server(port=0)
		with open("C:/Users/Admin/Documents/Ping Monitor/token.json", "w") as token:
			token.write(credentials.to_json())
def read_data():
	global credentials
	global data
	global status
	global totalnetto
	print('calling data from archive...')
	try:
		service = build("sheets", "v4", credentials=credentials)
		sheets = service.spreadsheets()
		result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Copy of List WS & Prnt Simphony!B4:K106").execute()
		data = result.get("values",[])
		status=[None]*len(data)
		print('len data')
		print(len(data))
		for x in range(len(data)):
			# print(x)
			if(len(data[x])>1 and len(data[x])<=9):
				del data[x][1:len(data[x])]
				totalnetto=totalnetto+1
			elif(len(data[x])>1 and len(data[x])<=10):
				del data[x][1:9]
				totalnetto=totalnetto+1
	except HttpError as error:
		print(error)
def ping_device(ip, index):
	res=os.popen('ping -n 1 "'+ip+'"')
	res=res.readlines()[2]
	res=res[:len(res)-1]
	status[index]=res
def write_status():
	global credentials
	global ipindex
	global status
	# range='Sheet1C'+str(sttindex+2)+':D'+str(sttindex+12)
	service = build("sheets", "v4", credentials=credentials)
	sheets = service.spreadsheets()
	values=[]
	count=0
	for x in status:
		temp=[x]
		values.append(temp)
	# for x in status.values():
	# 	if(count>=ipindex-10 and count<=ipindex):
	# 		temp=[x,time.ctime()]
	# 	else:
	# 		temp=[x,None]
	# 	values.append(temp)
	# 	count=count+1
	# print('values:')
	# print(values)
	try:
		data = [
		{
			'range': 'Copy of List WS & Prnt Simphony!L4:M106',
			# 'range': 'Sheet1C'+str(sttindex+2)+':D'+str(sttindex+12),
			'values' : values
		}]
		result=sheets.values().batchUpdate(
			spreadsheetId=SPREADSHEET_ID, body={
			'valueInputOption' : 'USER_ENTERED',
			'data' : data
			}).execute()
		print('update succeeded')
		print(f"{(result.get('totalUpdatedCells'))} cells updated.")
		return result
	except HttpError as error:
		print(f"An error occurred: {error}")
def main():
	global ipindex
	global data
	threadcount=int(input('masukkan jumlah thread : '))
	loopcount=0
	# if read_settings():
	manage_credentials()
	read_data()
	# print('ini data')
	# for x in data:
	# 	print(x[0])
	print('pinging devices...')
	t=[None]*threadcount
	ipindex = ipcount = ipstart = dataindex = 0
	print('start at :', end='')
	timestart=time.time()
	print(datetime.fromtimestamp(timestart))
	while True:
		print('\t\t\tloopcount = ', end='')
		print(loopcount)
		if(loopcount==3):
			print('test done')
			print('start at : ', end='')
			print(datetime.fromtimestamp(timestart))
			print('stop at  : ', end='')
			timestop=time.time()
			print(datetime.fromtimestamp(timestop))
			length=timestop-timestart
			print('length   : ', end='')
			print(datetime.fromtimestamp(length))
			break
		if(dataindex==len(data)):
			dataindex=0
			loopcount=loopcount+1
		if(ipindex==totalnetto):
			ipindex=0
		print('ipindex   = '+str(ipindex))
		print('ipcount   = '+str(ipcount))
		print('ipstart   = '+str(ipstart))
		print('dataindex = '+str(dataindex))
		print()
		print("\t\t\t")
		print(data[dataindex])
		print(type(data[dataindex]))
		if(len(data[dataindex])==2):
			print('len = 2')
			if(data[dataindex][0]!=None and data[dataindex][1]=='live'):
				t[ipcount-1]=threading.Thread(target=ping_device, args=(data[dataindex][0], dataindex,))
				t[ipcount-1].start()
				ipcount=ipcount+1
				ipindex=ipindex+1
		dataindex=dataindex+1
		if (ipcount==threadcount):
			for x in range(threadcount):
				print('x = '+str(x))
				t[x].join()
			write_status()
			ipstart=ipindex
			ipcount=0
			for x in status:
				print(x)		
if __name__ == "__main__":
	main()
