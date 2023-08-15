# python "D:\python\ping monitor\main.py"
import os, time, threading
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1hLasmmdhGmKKVeVV1a680IZNVJMWeVo_ep8u2evvUpk"
credentials = None
status={}
def read_settings():

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
def read_ip(credentials):
	print('calling data from archive...')
	try:
		service = build("sheets", "v4", credentials=credentials)
		sheets = service.spreadsheets()
		result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B2:B41").execute()
		values = result.get("values",[])
		for x in range(len(values)):
			status[values[x][0]]=None
	except HttpError as error:
		print(error)
	return status
def ping_device(ip):
	res=os.popen('ping -n 1 "'+ip+'"')
	res=res.readlines()[2]
	res=res[:len(res)-1]
	status[ip]=res
def write_status(credentials):
	service = build("sheets", "v4", credentials=credentials)
	sheets = service.spreadsheets()
	values=[]
	for x in status.values():
		temp=[x]
		print(x)
		print(type(x))
		values.append(temp)
	print('values:')
	print(values)
	try:
		data = [
		{
			'range': 'Sheet1!C2:C41',
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
	# if read_settings():
	manage_credentials()
	status=read_ip(credentials)
	for key, value in status.items():
	    print(key, ' : ', value)
	print('pinging devices...')
	t=[None]*10
	sttindex= sttcount= sttstart=0
	while True:
		if(sttindex==len(status)):
			sttindex=0
		sttcount=sttcount+1
		print('sttindex = '+str(sttindex))
		print('sttcount = '+str(sttcount))
		print('sttstart = '+str(sttstart))
		print()
		print("\t\t\t")
		t[sttcount-1]=threading.Thread(target=ping_device, args=(list(status)[sttindex],))
		t[sttcount-1].start()
		if (sttcount==10):
			for x in range(10):
				print('x = '+str(x))
				t[x].join()
			write_status(credentials)
			sttstart=sttindex+1
			sttcount=0
			print(status)
		sttindex=sttindex+1
if __name__ == "__main__":
	main()
