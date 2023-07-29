# python "D:\python\ping monitor\main.py"
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# SPREADSHEET_ID = "1hLasmmdhGmKKVeVV1a680IZNVJMWeVo_ep8u2evvUpk" # yang asli
SPREADSHEET_ID = "17wZNfmvI1ihVVHiuRdNMIrAPgwOtRS4K" # schedule it
def main():
	credentials = None
	if os.path.exists("token.json"):
		credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("D:/python/ping monitor/credentials.json", SCOPES)
			credentials = flow.run_local_server(port=0)
		with open("token.json", "w") as token:
			token.write(credentials.to_json())
	try:
		service = build("sheets", "v4", credentials=credentials)
		sheets = service.spreadsheets()
		result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:D2").execute() #yang asli
		result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Juli 2023!A7:AH14").execute()
		values =result.get("values",[])
		for row in values:
			print(row)
	except HttpError as error:
		print(error)
if __name__ == "__main__":
	main()