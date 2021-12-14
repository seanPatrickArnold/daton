
# https://developers.google.com/drive/api/v3/quickstart/python
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py
from apiclient.discovery import build
from google.oauth2.service_account import Credentials

key_file_location = os.path.join(os.getcwd(), 'client_secrets.json')
print(key_file_location)

credentials = Credentials.from_service_account_file(key_file_location)



credentials = Credentials.from_service_account_file(key_file_location)

# https://developers.google.com/drive/api/v3/quickstart/python
service = build('drive', 'v3', credentials=credentials)

# Call the Drive v3 API
results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

print(results)

file1 = drive.CreateFile()
file1.SetContentFile(path_to_your_file)
file1.Upload()

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

        print('Hello, world!')
import numpy as np
import os
import pandas as pd
from replit import db
import time
import threading

print(os.listdir(os.getcwd()))



#root = tk.Tk()
#labelDictionary = {}
#for i in range(10):
#  labelDictionary[str(i)] = tk.Label(root, text=str(np.sin(i)))
#  labelDictionary[str(i)].pack()
#root.mainloop()

#print(np.sin(10))

print(os.getcwd())

def updateAnalysis():
  df = pd.read_csv(os.path.join(os.getcwd(), 'testData.csv'), index_col=0)
  df.to_excel('testData.xlsx')

  df.insert(2, 'attribute3', [0,1,0,1])
  df.insert(3, 'attribute4', ['a','a','b','b'])
  df.insert(4, 'attribute5', ['a','b','a','b'])

  print(df)

  df.to_excel('analyzedData.xlsx')
  df = df[df['attribute1'] > 1]
  print(df.groupby('attribute3').mean())

#while True:
#  thread = threading.Thread(target=updateAnalysis, args=[])
#  thread.start()
#  time.sleep(30)


for file1 in file_list:
#   if file1['title'] == 'analyzedData.xlsx':
#     url = 'https://docs.google.com/spreadsheets/d/' + spreadsheetId + '/gviz/tq?tqx=out:csv&gid=' + sheetId
#     headers = {'Authorization': 'Bearer ' + gauth.credentials.access_token}
#     res = requests.get(url, headers=headers)

#     file6 = drive.CreateFile({'id': testDataID})
#     file6.GetContentFile('analyzedData.xlsx') # Download file as 

#     df = pd.read_excel('analyzedData.xlsx')
#     print(df.header())

