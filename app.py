from flask import Flask, render_template, request, redirect, url_for
from config import Configuration
from forms import FileForm
from sheets import *

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/')
def homepage():
    return render_template('base.html'), 200


@app.route('/post')
def post():
    return render_template('post.html'), 201


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404


@app.route('/json', methods=['POST', 'GET'])
def post_json_to_google_sheets():
    if request.method == 'POST':
        json_file = request.form['file']
        if json_file:
            service = get_service(json_file)
            spreadsheet_id = get_spreadsheet(json_file)
            data_keys = get_data_key(json_file)
            data_values = get_data_value(json_file)

            values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range='Лист1!A1',
                                                            valueInputOption="RAW",
                                                            body={'values': data_keys}).execute()

            values = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range='Лист1!A1',
                                                            valueInputOption="RAW",
                                                            body={"majorDimension": "COLUMNS",
                                                                  'values': data_values}).execute()
            return redirect('/post')
    form = FileForm()
    return render_template('post_json.html', form=form), 200
