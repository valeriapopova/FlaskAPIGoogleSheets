import random
import json

import apiclient
import httplib2
from flask import Response
from googleapiclient.errors import HttpError
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


def append_values(service, spreadsheet_id, data_values):
    try:
        values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range='Лист1!A1',
                                                    valueInputOption="RAW",
                                                    body={"majorDimension": "COLUMNS",
                                                          'values': data_values}).execute()
    except HttpError as error:
        return Response(f"An error occurred: {error}")


def append(service, spreadsheet_id, data_keys, data_values):
    try:
        values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range='Лист1!A1',
                                                        valueInputOption="RAW",
                                                        body={'values': data_keys}).execute()

        values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range='Лист1!A1',
                                                        valueInputOption="RAW",
                                                        body={"majorDimension": "COLUMNS",
                                                              'values': data_values}).execute()
    except HttpError as error:
        return Response(f"An error occurred: {error}")


def clear_and_append(service, spreadsheet_id, data_keys, data_values):
    try:
        values = service.spreadsheets().values().batchClear(spreadsheetId=spreadsheet_id,
                                                            body={'ranges': 'A1:Z'}).execute()

        values = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                             body={'valueInputOption': "USER_ENTERED",
                                                                   'data': [{'range': 'Лист1!A1',
                                                                             "majorDimension": "ROWS",
                                                                             "values": data_keys},
                                                                            {'range': 'Лист1!A2',
                                                                             "majorDimension": "COLUMNS",
                                                                             "values": data_values}]}).execute()
    except HttpError as error:
        return Response(f"An error occurred: {error}")


def append_new_list(service, spreadsheet_id, data_keys, data_values):
    try:
        current_sheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        if current_sheet is not None:
            random_integer = random.randint(1, 2147483647)
            new_sheet = {'requests': [
                {'addSheet': {
                    'properties': {
                        "sheetId": random_integer,
                        "title": '' + str(random_integer),
                    },

                }},

            ]}
            new_sheet_title = new_sheet['requests'][0]['addSheet']['properties']['title']
            values = service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id, body=new_sheet).execute()

            values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=f'{new_sheet_title}!A1',
                                                            valueInputOption="RAW",
                                                            body={'values': data_keys}).execute()

            values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=f'{new_sheet_title}!A1',
                                                            valueInputOption="RAW",
                                                            body={"majorDimension": "COLUMNS",
                                                                  'values': data_values}).execute()
    except HttpError as error:
        return Response(f"An error occurred: {error}")