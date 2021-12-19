from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import os
import logging
import traceback
import pandas as pd
from scipy.stats import pearsonr
import numpy as np
import xlsxwriter
import openpyxl

try:
  gauth = GoogleAuth()
  scope = ["https://www.googleapis.com/auth/drive"]
  JSON_FILE = os.path.join(os.getcwd(), 'client_secrets.json')
  gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
  drive = GoogleDrive(gauth)

  file = 'testData.xlsx'
  filename = os.path.join(os.getcwd(), file)

  file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

  def readOrCreate(file):
    fileFoundBool = False
    for file1 in file_list:
      if file1['title'] == file and fileFoundBool == False:
        file6 = drive.CreateFile({'id': file1['id']})
        file6.GetContentFile(file1['title'])
        df = pd.read_excel(file1['title'], index_col=None)
        print(df)
        fileFoundBool = True
        # print('updated title: %s, id: %s' % (file1['title'], file1['id']))
      elif fileFoundBool == True and file1['title'] == file:
        originalTitle = file1['title']
        file1['title'] = originalTitle.split('.')[0] + 'Copy.' + originalTitle.split('.')[1]
        update=drive.auth.service.files().update(fileId=file1['id'],body=file1).execute()
        # print('changed filename')

    if not fileFoundBool:
      file1 = drive.CreateFile({'title': file})
      file1.SetContentFile(os.path.join(os.getcwd(), file.split('.')[0]+'Static.'+file.split('.')[1]))
      file1.Upload()
      # print('uploaded title: %s, id: %s' % (file1['title'], file1['id']))
      df = pd.read_excel(os.path.join(os.getcwd(), file.split('.')[0]+'Static.'+file.split('.')[1]))
    return(df)

  def update(file):
    for file1 in file_list:
      if file1['title'] == file:
        file1 = drive.CreateFile({'id': file1['id']})
        file1.SetContentFile(os.path.join(os.getcwd(), file))
        file1.Upload({'convert': True})

  def multiply(a,b):
    return(a*b)

  def modifySeries(df, seriesName, correlationDictionary, columnsList, compColumn, operationOrder):
    for column in columnsList:
      if column != compColumn and seriesName != compColumn:
        operand = df[seriesName]
        correlationName = seriesName
        for operation in operationOrder:
          if operation == 'multiply':
            operand *= df[column]
            correlationName = correlationName + '*' + column
          elif operation == 'add':
            operand += df[column]
            correlationName = correlationName + '+' + column
        correlationName = correlationName + ':' + compColumn
        print(operand)
        data2 = operand.tolist()
        data1 = df[compColumn].tolist()
        # print(data2, data1)
        corr, _ = pearsonr(data1, data2)
        correlationDictionary['correlations'].append(correlationName)
        correlationDictionary['correlationCoefficient'].append(corr)
    # return(modifiedSeries, modifiedSeriesName)

  def analyzeData(df):
    columns = df.columns.values
    # print(columns)
    columnAggDictionary = {}
    correlationDictionary = {'correlations':[], 'correlationCoefficient':[]}
    for column in columns[1:]:
      for compColumn in columns[1:]:
        if column != compColumn:
          # print(column)
          # print(columns[np.where(columns==column)[0][0]-1])
          # print(np.where(columns==column)[0][0])
          # if np.where(columns==column)[0][0] < len(columns):
          data2 = df[column].tolist()
          data1 = df[compColumn].tolist()
          corr, _ = pearsonr(data1, data2)
          print(corr)
          correlationName = column + ':' + compColumn
          correlationDictionary['correlations'].append(correlationName)
          correlationDictionary['correlationCoefficient'].append(corr)
    def seriesMods(operationOrder):
      for column in columns[1:]:
        for compColumn in columns[1:]:
          modifySeries(df, column, correlationDictionary, columns[1:], compColumn, operationOrder)
    seriesMods(['add'])
    seriesMods(['multiply'])
    seriesMods(['multiply', 'add', 'multiply'])
    correlationDF = pd.DataFrame.from_dict(correlationDictionary)
    columnAggDictionary[column] = ['mean', 'median']
    analyzedDF = df.groupby(columns[0]).agg(columnAggDictionary)
    # writer = pd.ExcelWriter('analyzedData.xlsx', engine = 'xlsxwriter')
    analyzedDF.to_excel('analyzedData.xlsx', index=True)
    # analyzedDF.to_excel(writer, sheet_name = 'basicStats', index=True)
    # print(correlationDictionary)
    correlationDF.to_excel('correlationData.xlsx', index=True)


  def checkPermissions():
    for file1 in file_list:
      # print('title: %s, id: %s' % (file1['title'], file1['id']))
      file1.FetchMetadata(fields='permissions')
      permissionGranted = False
      for permission in file1['permissions']:
          if permission['emailAddress'] == 'sean.arnold@contractors.roche.com':
            permissionGranted = True
            # print(file1['title'] + ' permission already granted')
      if not permissionGranted:
        file1.InsertPermission(
          {
            'type':  'user',
            'value': 'sean.arnold@contractors.roche.com',
            'role':  'writer'
          }
        )
        # print(file1['title'] + ' permission granted')

  testDataDF = readOrCreate('testData.xlsx')
  # analyzedDataDF = readOrCreate('analyzedData.xlsx')
  correlationDataDF = readOrCreate('correlationData.xlsx')
  analyzeData(testDataDF)
  update('analyzedData.xlsx')
  update('correlationData.xlsx')
  os.remove(os.path.join(os.getcwd(), 'testData.xlsx'))
  os.remove(os.path.join(os.getcwd(), 'analyzedData.xlsx'))
  # os.remove(os.path.join(os.getcwd(), 'correlationData.xlsx'))
  checkPermissions()

  # print(testDataDF)
  # print(analyzedDataDF)
  # file1.Trash()
except Exception as error:
  logging.error(traceback.format_exc())






