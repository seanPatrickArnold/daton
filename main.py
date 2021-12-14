from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import os
import logging
import traceback

try:

  gauth = GoogleAuth()
  scope = ["https://www.googleapis.com/auth/drive"]
  JSON_FILE = os.path.join(os.getcwd(), 'client_secrets.json')
  gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
  drive = GoogleDrive(gauth)

  file = 'testData.xlsx'
  filename = os.path.join(os.getcwd(), file)



  file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

  # for file1 in file_list:
  #   if file1['title'] == 'testData.csv':
  #     testDataID = file1['id']

  # 'catlove.png'.

  # print(file6)

  import pandas as pd


  # 

  fileFoundBool = False
  for file1 in file_list:
    if file1['title'] == file and fileFoundBool == False:
      file6 = drive.CreateFile({'id': file1['id']})
      file6.GetContentFile(file1['title'])
      df = pd.read_excel(file1['title'], index_col=0)
      file1 = drive.CreateFile({'id': file1['id']})
      file1.SetContentFile(filename)
      file1.Upload({'convert': True})
      fileFoundBool = True
      print('updated title: %s, id: %s' % (file1['title'], file1['id']))
    elif fileFoundBool == True and file1['title'] == file:
      originalTitle = file1['title']
      file1['title'] = originalTitle.split('.')[0] + 'Copy.' + originalTitle.split('.')[1]
      update=drive.auth.service.files().update(fileId=file1['id'],body=file1).execute()
      print('changed filename')
      


  if not fileFoundBool:
    file1 = drive.CreateFile({'title': file})
    file1.SetContentFile(filename)
    file1.Upload()
    
    print('uploaded title: %s, id: %s' % (file1['title'], file1['id']))

  for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))
    file1.FetchMetadata(fields='permissions')
    permissionGranted = False
    for permission in file1['permissions']:
        if permission['emailAddress'] == 'sean.arnold@contractors.roche.com':
          permissionGranted = True
          print(file1['title'] + ' permission already granted')
    if not permissionGranted:
      file1.InsertPermission(
        {
          'type':  'user',
          'value': 'sean.arnold@contractors.roche.com',
          'role':  'writer'
        }
      )
      print(file1['title'] + ' permission granted')
    # file1.Trash()
except Exception as error:
  logging.error(traceback.format_exc())






