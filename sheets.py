import json
import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


def get_service(json_file):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    return service


def get_spreadsheet(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        spreadsheet_id = data['spreadsheetId']
        return spreadsheet_id


def get_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        result = data['data']
        data_for_sheets = []
        for key in result:
            # for k in key:
            data_for_sheets.append([key])
        return data_for_sheets


def get_data_value(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        result = data['data']
        data_for_sheets = []
        for key in result:
            # for k in key:
            data_for_sheets.append(result[key])
        return data_for_sheets

k = get_data('creds.json')
t = get_data_value('creds.json')

print(k, t)







