from flask import Flask, render_template, request, redirect
from werkzeug.exceptions import BadRequestKeyError

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
def page_not_found():
    return render_template('404.html'), 404


@app.route('/json', methods=['POST', 'GET'])
def post_json_to_google_sheets():
    if request.method == 'POST':
        try:
            json_file = request.form['file']
            if json_file.endswith('.json'):
                service = get_service(json_file)
                spreadsheet_id = get_spreadsheet(json_file)
                data_keys = get_data_key(json_file)
                data_values = get_data_value(json_file)

                if request.form['submit_button'] == 'Дописать данные(названия колонок и значения)':
                    append(service, spreadsheet_id, data_keys, data_values)
                    return redirect('/post', 301)
                elif request.form['submit_button'] == 'Дописать только значения':
                    append_values(service, spreadsheet_id, data_values)
                    return redirect('/post', 301)
                elif request.form['submit_button'] == 'Перезаписать':
                    clear_and_append(service, spreadsheet_id, data_keys, data_values)
                    return redirect('/post', 301)
                elif request.form['submit_button'] == 'Записать в новый лист':
                    append_new_list(service, spreadsheet_id, data_keys, data_values)
                    return redirect('/post', 301)

            else:
                return Response("Недопустимый формат файла, необходимое расширение - JSON", 404)
        except BadRequestKeyError:
            return Response("Пустое значение", 400)

    form = FileForm()
    return render_template('post_json.html', form=form), 200
