from wtforms import Form, FileField


class FileForm(Form):
    file = FileField('Выберите файл формата JSON')