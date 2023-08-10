# python "D:\python\ping monitor\main.py"
import os, time, threading
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1hLasmmdhGmKKVeVV1a680IZNVJMWeVo_ep8u2evvUpk" # yang asli
# SPREADSHEET_ID = "17wZNfmvI1ihVVHiuRdNMIrAPgwOtRS4K" # schedule it
credentials = None
status={}
def manage_credentials():
	print('managing credentials...')
	if os.path.exists("C:/Users/PHBC - 2/Downloads/ping monitor/ping monitor/token.json"):#opis
	# if os.path.exists("D:/python/ping monitor/token.json"):#rumah
		credentials = Credentials.from_authorized_user_file("C:/Users/PHBC - 2/Downloads/ping monitor/ping monitor/token.json", SCOPES)#opis
		# credentials = Credentials.from_authorized_user_file("D:/python/ping monitor/ping monitor/token.json", SCOPES)#rumah
	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("C:/Users/PHBC - 2/Downloads/ping monitor/ping monitor/credentials.json", SCOPES)#opis
			# flow = InstalledAppFlow.from_client_secrets_file("D:/python/ping monitor/credentials.json", SCOPES)#rumah
			credentials = flow.run_local_server(port=0)
		with open("C:/Users/PHBC - 2/Downloads/ping monitor/ping monitor/token.json", "w") as token:#opis
		# with open("D:/python/ping monitor/token.json", "w") as token:#rumah
			token.write(credentials.to_json())
	return credentials
def read_ip(credentials):
	print('calling data from archive...')
	try:
		service = build("sheets", "v4", credentials=credentials)
		sheets = service.spreadsheets()
		result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B2:B41").execute() #yang asli---------
		values = result.get("values",[])
		for x in range(len(values)):
			status[values[x][0]]=None
	except HttpError as error:
		print(error)
	return status
def ping_device(ip):
	res=os.popen('ping -n 1 "'+ip+'"')
	res=res.readlines()
	status[ip]=res[2]
	
def main():
	credentials = manage_credentials()
	status=read_ip(credentials)
	for key, value in status.items():
	    print(key, ' : ', value)
	print('pinging devices...')
	t=[None]*10
	sttindex, sttcount, sttstart=0
	while True:
		if(sttindex==len(status)):
			sttindex=0
		t[count]=threading.Thread(target=ping_device, args=(ip[index],))
		t[count].start()
		if (sttcount==10):
			if(sttstart<sttindex+1)
		# for x in range(len(values)):
		# 	t.append(threading.Thread(target=ping_device, args=(ip[x],)))
			# response = os.popen('ping -n 1 "'+values[x]+'"')
			# a = response.readlines()
			# print(a[2])



			# if(status[x]!=a[2]):
			# status[x]=a[2]
			# sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!C"+str(x+2), valueInputOption='USER_ENTERED', body={'values':[[a[2]]]}).execute()
	# row=1;
	# body={}
	# while True:
	# 	values=[]
	# 	temp=[]
	# 	for i in range(10):
	# 		temp.append(str(row))
	# 	values.append(temp)
	# 	body={'values':values}
	# 	sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!F"+str(row)+":O"+str(row), valueInputOption='USER_ENTERED', body=body).execute()
	# 	time.sleep(1)
	# 	row=row+1
if __name__ == "__main__":
	main()
