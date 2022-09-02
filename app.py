from flask import Flask, render_template, request, redirect
from werkzeug.exceptions import BadRequestKeyError

from config import Configuration
from sheets import *

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/sheets')
def homepage():
    return render_template('base.html'), 200


@app.route('/sheets/post')
def post():
    return render_template('post.html'), 201


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.route('/sheets/append', methods=['POST', 'GET'])
def post_json_to_google_sheets():
    if request.method == 'POST':
        try:
            json_file = request.get_json(force=False)
            service = get_service(json_file)
            spreadsheet_id = get_spreadsheet(json_file)
            data_keys = get_data_key(json_file)
            data_values = get_data_value(json_file)
            append(service, spreadsheet_id, data_keys, data_values)

        except BadRequestKeyError:
            return Response("Пустое значение", 400)

    return render_template('post_json.html'), 200


@app.route('/sheets/append_values', methods=['POST', 'GET'])
def post_json_to_google_sheets_2():
    if request.method == 'POST':
        try:
            json_file = request.get_json(force=False)
            service = get_service(json_file)
            spreadsheet_id = get_spreadsheet(json_file)
            data_values = get_data_value(json_file)
            append_values(service, spreadsheet_id, data_values)
        except BadRequestKeyError:
            return Response("Пустое значение", 400)

    return render_template('post_json.html'), 200


@app.route('/sheets/clear_append', methods=['POST', 'GET'])
def post_json_to_google_sheets_3():
    if request.method == 'POST':
        try:
            json_file = request.get_json(force=False)
            service = get_service(json_file)
            spreadsheet_id = get_spreadsheet(json_file)
            data_keys = get_data_key(json_file)
            data_values = get_data_value(json_file)
            clear_and_append(service, spreadsheet_id, data_keys, data_values)
        except BadRequestKeyError:
            return Response("Пустое значение", 400)

    return render_template('post_json.html'), 200


@app.route('/sheets/append_list', methods=['POST', 'GET'])
def post_json_to_google_sheets_4():
    if request.method == 'POST':
        try:
            json_file = request.get_json(force=False)
            service = get_service(json_file)
            spreadsheet_id = get_spreadsheet(json_file)
            data_keys = get_data_key(json_file)
            data_values = get_data_value(json_file)
            append_new_list(service, spreadsheet_id, data_keys, data_values)
        except BadRequestKeyError:
            return Response("Пустое значение", 400)

    return render_template('post_json.html'), 200
