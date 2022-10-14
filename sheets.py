import os
import random
import json
from pprint import pprint
import gspread

from sheetfu import SpreadsheetApp, Table
import apiclient
import httplib2
from flask import Response
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials


def get_service(json_file):
    # аутентификация в сервисном аккаунте Google
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
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
        spreadsheet_id = json_file['spreadsheetId']
        return spreadsheet_id
    except Exception:
        return Response("ID таблицы отсутсвует / неверный", 404)


def get_data_key(json_file):
    try:
        result = json_file['data']
        data_for_sheets = []
        for key in result:
            for k in key:
                if k not in data_for_sheets:
                    data_for_sheets.append(k)
        return [data_for_sheets]
    except KeyError:
        return Response("Данные для записи не найдены", 404)


def get_data_value(json_file):
    try:
        result = json_file['data']
        data_for_sheets = []
        for res in result:
            for k, v in res.items():
                if type(v) != list:
                    data_for_sheets.append([v])
                else:
                    data_for_sheets.append(v)
        return data_for_sheets
    except KeyError:
        return Response("Данные для записи не найдены", 404)


# def get_data_value(json_file):
#     try:
#         result = json_file['data']
#         data_for_sheets = []
#         for res in result:
#             r = res.values()
#             values = list(r)
#             print(values)
#             data_for_sheets.append(values)
#         return data_for_sheets
#     except KeyError:
#         return Response("Данные для записи не найдены", 404)


def append_values(service, spreadsheet_id, data_values):
    try:
        current_sheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        first_list = current_sheet['sheets'][0]['properties']['title']

        values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=f'{first_list}!A1',
                                                    valueInputOption="RAW",
                                                    body={"majorDimension": "COLUMNS",
                                                          'values': data_values}).execute()
    except HttpError as error:
        return Response(f"An error occurred: {error}")


def update_values(table_name, unique_column, json_file, spreadsheet_id, unique_name):
    try:
        random_integer = random.randint(1, 2147483647)
        random_int = random.randint(1, 2147483647)
        filename = f'{random_integer}_{random_int}.json'
        if not os.path.isdir("json_for_updating"):
            os.makedirs("json_for_updating")

        filepath = f'json_for_updating/'
        new_file = filepath + filename
        with open(new_file, 'w') as f:
            json.dump(json_file, f)
        sa = SpreadsheetApp(new_file)
        spreadsheet = sa.open_by_id(spreadsheet_id=spreadsheet_id)
        data_range = spreadsheet.get_sheet_by_name(table_name).get_data_range()

        table = Table(data_range, backgrounds=True)

        for item in table:
            if item.get_field_value(unique_column) == unique_name:
                for k, v in json_file['data'][0].items():
                    item.set_field_value(k, v)
        table.commit()
    except HttpError as error:
        return Response(f"An error occurred: {error}")


def append(service, spreadsheet_id, data_keys, data_values):
    try:
        current_sheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        first_list = current_sheet['sheets'][0]['properties']['title']

        values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=f'{first_list}!A1',
                                                        valueInputOption="RAW",
                                                        body={'values': data_keys}).execute()

        values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=f'{first_list}!A1',
                                                        valueInputOption="RAW",
                                                        body={"majorDimension": "COLUMNS",
                                                              'values': data_values}).execute()
    except HttpError as error:
        return Response(f"An error occurred: {error}")


def clear_and_append(service, spreadsheet_id, data_keys, data_values):
    try:
        current_sheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        first_list = current_sheet['sheets'][0]['properties']['title']

        values = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id,
                                                       range=first_list).execute()


        values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=f'{first_list}!A1',
                                                        valueInputOption="RAW",
                                                        body={'values': data_keys}).execute()


        values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=f'{first_list}!A1',
                                                        valueInputOption="RAW",
                                                        body={"majorDimension": "COLUMNS",
                                                              'values': data_values}).execute()

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

