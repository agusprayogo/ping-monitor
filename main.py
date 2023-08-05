# python "D:\python\ping monitor\main.py"
import os
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1hLasmmdhGmKKVeVV1a680IZNVJMWeVo_ep8u2evvUpk" # yang asli
# SPREADSHEET_ID = "17wZNfmvI1ihVVHiuRdNMIrAPgwOtRS4K" # schedule it
def main():
	print('managing credentials...')
	credentials = None
	# if os.path.exists("C:/Users/PHBC - 2/Downloads/ping monitor/ping monitor/token.json"):#opis
	if os.path.exists("D:/python/ping monitor/token.json"):#rumah
		# credentials = Credentials.from_authorized_user_file("C:/Users/PHBC - 2/Downloads/ping monitor/ping monitor/token.json", SCOPES)#opis
		credentials = Credentials.from_authorized_user_file("D:/python/ping monitor/ping monitor/token.json", SCOPES)#opis
	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			# flow = InstalledAppFlow.from_client_secrets_file("C:/Users/PHBC - 2/Downloads/ping monitor/ping monitor/credentials.json", SCOPES)#opis
			flow = InstalledAppFlow.from_client_secrets_file("D:/python/ping monitor/credentials.json", SCOPES)#rumah
			credentials = flow.run_local_server(port=0)
		# with open("C:/Users/PHBC - 2/Downloads/ping monitor/ping monitor/token.json", "w") as token:#opis
		with open("D:/python/ping monitor/token.json", "w") as token:#rumah
			token.write(credentials.to_json())
	print('calling data from archive...')
	try:
		service = build("sheets", "v4", credentials=credentials)
		sheets = service.spreadsheets()
		# result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B2:B12").execute() #yang asli
		# values =result.get("values",[])
	except HttpError as error:
		print(error)
	print('pinging devices...')
	status=[]
	# for x in range(len(values)):
	# 	values[x]=values[x][0]
	# while True:
	# 	for x in range(len(values)):
	# 		response = os.popen('ping -n 1 "'+values[x]+'"')
	# 		a = response.readlines()
	# 		print(a[2])
	# 		# if(status[x]!=a[2]):
	# 		# status[x]=a[2]
	# 		sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!C"+str(x+2), valueInputOption='USER_ENTERED', body={'values':[[a[2]]]}).execute()
	tes=21
	timeout=time.time()+1
	while True:
		sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!C"+str(tes), valueInputOption='USER_ENTERED', body={'values':[[str(tes)]]}).execute()
		tes=tes+1
		print(tes)
		print(time.ctime())
		if time.time()>timeout:
			break
if __name__ == "__main__":
	main()
