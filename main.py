# python "D:\python\ping monitor\main.py"
import os, time, threading
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
ip=[]
availability=[]
# def read_settings():

def manage_credentials():
	global credentials
	print('managing credentials...')
	if os.path.exists("D:/python/ping monitor/token.json"):
		credentials = Credentials.from_authorized_user_file("D:/python/ping monitor/token.json", SCOPES)
	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("D:/python/ping monitor/credentials.json", SCOPES)
			credentials = flow.run_local_server(port=0)
		with open("D:/python/ping monitor/token.json", "w") as token:
			token.write(credentials.to_json())
def read_data():
	global credentials
	global ip
	print('calling data from archive...')
	try:
		service = build("sheets", "v4", credentials=credentials)
		sheets = service.spreadsheets()
		result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Copy of List WS & Prnt Simphony!B4:K106").execute()
		values = result.get("values",[])
		for x in values:
			if(len(x)==0):
		# for x in values:
		# 	print(x[0]+' and '+x[9])
		# for x in range(len(values)):
		# 	ip.append(values[x][0])
	except HttpError as error:
		print(error)
def ping_device(ip):
	res=os.popen('ping -n 1 "'+ip+'"')
	res=res.readlines()[2]
	res=res[:len(res)-1]
	status[ip]=res
def write_status():
	global credentials
	global sttindex
	# range='Sheet1C'+str(sttindex+2)+':D'+str(sttindex+12)
	service = build("sheets", "v4", credentials=credentials)
	sheets = service.spreadsheets()
	values=[]
	count=0
	for x in status.values():
		if(count>=sttindex-10 and count<=sttindex):
			temp=[x,time.ctime()]
		else:
			temp=[x,None]
		values.append(temp)
		count=count+1
	print('values:')
	print(values)
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
	global sttindex
	# if read_settings():
	manage_credentials()
	read_data()
	print('ini daftar ip')
	for x in ip:
		print(x)
	print('pinging devices...')
	t=[None]*10
	ipindex = ipcount= ipstart=0
	while True:
		if(ipindex==len(status)):
			ipindex=0
		ipcount=ipcount+1
		print('ipindex = '+str(ipindex))
		print('ipcount = '+str(ipcount))
		print('ipstart = '+str(ipstart))
		print()
		print("\t\t\t")
		t[ipcount-1]=threading.Thread(target=ping_device, args=(ip[ipindex],))
		t[ipcount-1].start()
		if (sttcount==10):
			for x in range(10):
				print('x = '+str(x))
				t[x].join()
			write_status()
			sttstart=sttindex+1
			sttcount=0
			print(status)
		sttindex=sttindex+1
if __name__ == "__main__":
	main()
