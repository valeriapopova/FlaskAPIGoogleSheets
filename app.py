from flask import Flask, render_template, request
from werkzeug.exceptions import BadRequestKeyError

from config import Configuration
from sheets import *

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/google_sheets')
def homepage():
    return render_template('base.html'), 200


@app.route('/google_sheets/append', methods=['POST'])
def post_json_to_google_sheets():

    try:
        json_file = request.get_json(force=False)
        service = get_service(json_file)
        spreadsheet_id = get_spreadsheet(json_file)
        data_keys = get_data_key(json_file)
        data_values = get_data_value(json_file)
        append(service, spreadsheet_id, data_keys, data_values)

    except BadRequestKeyError:
        return Response("Пустое значение", 400)
    return render_template('post.html'), 200

@app.route('/google_sheets/append_values', methods=['POST'])
def post_json_to_google_sheets_2():

    try:
        json_file = request.get_json(force=False)
        service = get_service(json_file)
        spreadsheet_id = get_spreadsheet(json_file)
        data_values = get_data_value(json_file)
        append_values(service, spreadsheet_id, data_values)
    except BadRequestKeyError:
        return Response("Пустое значение", 400)
    return render_template('post.html'), 200


@app.route('/google_sheets/delete_row', methods=['POST'])
def google_sheets_delete_row():
    try:
        json_file = request.get_json(force=False)
        spreadsheet_id = get_spreadsheet(json_file)
        table_name = json_file['table_name']
        unique_column = json_file['unique_column']
        unique_name = json_file['data'][0][f'{unique_column}']
        delete_row(json_file, spreadsheet_id, table_name, unique_column, unique_name)
    except BadRequestKeyError:
        return Response("Пустое значение", 400)
    return render_template('post.html'), 200


@app.route('/google_sheets/update_row', methods=['POST'])
def post_json_to_google_sheets_5():
    try:
        json_file = request.get_json(force=False)
        spreadsheet_id = get_spreadsheet(json_file)
        table_name = json_file['table_name']
        unique_column = json_file['unique_column']
        unique_name = json_file['data'][0][f'{unique_column}']
        update_values(table_name, unique_column, json_file, spreadsheet_id, unique_name)
    except BadRequestKeyError:
        return Response("Пустое значение", 400)
    return render_template('post.html'), 200


@app.route('/google_sheets/update_row_list', methods=['POST'])
def post_json_to_google_sheets_6():
    try:
        json_file = request.get_json(force=False)
        spreadsheet_id = get_spreadsheet(json_file)
        table_name = json_file['table_name']
        unique_column = json_file['unique_column']
        update_values_list(table_name, unique_column, json_file, spreadsheet_id)
    except BadRequestKeyError:
        return Response("Пустое значение", 400)
    return render_template('post.html'), 200


@app.route('/google_sheets/clear_append', methods=['POST'])
def post_json_to_google_sheets_3():

    try:
        json_file = request.get_json(force=False)
        service = get_service(json_file)
        spreadsheet_id = get_spreadsheet(json_file)
        data_keys = get_data_key(json_file)
        data_values = get_data_value(json_file)
        clear_and_append(service, spreadsheet_id, data_keys, data_values)
    except BadRequestKeyError:
        return Response("Пустое значение", 400)
    return render_template('post.html'), 200



@app.route('/google_sheets/append_list', methods=['POST'])
def post_json_to_google_sheets_4():

    try:
        json_file = request.get_json(force=False)
        service = get_service(json_file)
        spreadsheet_id = get_spreadsheet(json_file)
        data_keys = get_data_key(json_file)
        data_values = get_data_value(json_file)
        append_new_list(service, spreadsheet_id, data_keys, data_values)
    except BadRequestKeyError:
        return Response("Пустое значение", 400)

    return render_template('post.html'), 200


@app.route('/google_sheets/get_all_rows', methods=['POST'])
def get_all_rows_from_google_sheets():
    """Получить все строки"""
    try:
        json_file = request.get_json(force=False)
        service = get_service(json_file)
        spreadsheet_id = get_spreadsheet(json_file)

        if 'sheet_title' in json_file['data'][0]:
            sheet_title = json_file['data'][0]['sheet_title']
        else:
            sheet_title = None

        result = get_all_rows(service, spreadsheet_id, sheet_title)
        return result
    except BadRequestKeyError:
        return Response("Пустое значение", 400)


@app.route('/google_sheets/search_row', methods=['POST'])
def google_sheets_search_row():
    try:
        json_file = request.get_json(force=False)
        spreadsheet_id = get_spreadsheet(json_file)
        table_name = json_file['table_name']
        unique_column = json_file['unique_column']
        unique_name = json_file['data'][0][f'{unique_column}']
        searched = search_row(json_file, spreadsheet_id, table_name, unique_name)
        return searched
    except BadRequestKeyError:
        return Response("Пустое значение", 400)


@app.route('/google_sheets/search_rows', methods=['POST'])
def google_sheets_search_rows():
    try:
        json_file = request.get_json(force=False)
        spreadsheet_id = get_spreadsheet(json_file)
        table_name = json_file['table_name']
        unique_column = json_file['unique_column']
        searched = search_rows(json_file, spreadsheet_id, table_name, unique_column)
        return searched
    except BadRequestKeyError:
        return Response("Пустое значение", 400)
