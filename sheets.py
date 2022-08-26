import json
import apiclient
import httplib2
from flask import Response
from oauth2client.service_account import ServiceAccountCredentials


def get_service(json_file):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    except Exception:
        return Response("Недостаточно/неверные данные для авторизации", 403)
    return service


def get_spreadsheet(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            spreadsheet_id = data['spreadsheetId']
            return spreadsheet_id
    except Exception:
        return Response("ID таблицы тстутсвует / неверный", 404)


def get_data_key(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        try:
            result = data['data']
            data_for_sheets = []
            for key in result:
                for k in key:
                    data_for_sheets.append(k)
            return [data_for_sheets]
        except KeyError:
            return Response("Данные для записи не найдены", 404)


def get_data_value(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        try:
            result = data['data']
            data_for_sheets = []
            for res in result:
                for k, v in res.items():
                    data_for_sheets.append(v)
            return data_for_sheets
        except KeyError:
            return Response("Данные для записи не найдены", 404)



# k = get_service('q.json')
# # t = get_data_value('q.json')
# #
# print(k)







