# APIGoogleSheets

Это методы, которые записывают json в google sheets.

***/google_sheets*** доступ к таблице google sheets

Для того, что бы записать данные в свою таблицу, нужно получить реквизиты (`credentials`) для работы приложения с [Google API](https://console.cloud.google.com/).

***Порядок действий при регистрации таков:***

- Создать новый проект.

- Настроить согласия.

- Выбрать метод аутентификации приложение (`OAuth`).

- Получить реквизиты (`credentials`) для работы приложения с Google API.

- Указать API которые будет использовать приложение.

В процессе регистрации получаем файл `credentials.json` содержащий ключи для подключения приложения и секретики для `OAuth` авторизации пользователя. Этот файл не имеет доступа к данным аккаунта, таким как таблицы или диск. По сути это разрешение от Google для приложения на работу с Google API.

-  Cоздать или получить id необходимой таблицы для записи и добавить в json
```
Авторизационные данные для google sheets (пример)
auth_dict = {
      "type": "service_account",
      "project_id": "ozonsheets",
      "private_key_id": "",
      "private_key": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n",
      "client_email": "account@ozonsheets.iam.gserviceaccount.com",
      "client_id": "",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/account%40ozonsheets.iam.gserviceaccount.com",
      "spreadsheetId": ""
} 
```
___POST___

_/google_sheets/append_ - записывает данные в конец первого листа таблицы

*Parameters*
 json (данные которые нужно записать в таблицу + авторизационные данные + данные для записи("data")
```
{
      "type": "service_account",
      "project_id": "ozonsheets",
      "private_key_id": "",
      "private_key": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n",
      "client_email": "account@ozonsheets.iam.gserviceaccount.com",
      "client_id": "",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/account%40ozonsheets.iam.gserviceaccount.com",
      "spreadsheetId": "",
      "data" : [{"col1": [1, 2, 3]}, {"col2": ["q", "w", "e"]}, {"col3": 1}]
} 
``` 
Responses 200 успешно



___POST___  

_/google_sheets/append_values_   - записывает только значения в google sheets
 
*Parameters*
 json (данные которые нужно записать в таблицу + авторизационные данные + данные для записи("data")
```
{
      "type": "service_account",
      "project_id": "ozonsheets",
      "private_key_id": "",
      "private_key": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n",
      "client_email": "account@ozonsheets.iam.gserviceaccount.com",
      "client_id": "",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/account%40ozonsheets.iam.gserviceaccount.com",
      "spreadsheetId": "",
      "data" : [{"col1": [1, 2, 3]}, {"col2": ["q", "w", "e"]}, {"col3": 1}]
} 
``` 
Responses 200 успешно

___POST___    

_/google_sheets/append_values_   - перезаписывает данные в таблицу google sheets
 
*Parameters*
 json (данные которые нужно записать в таблицу + авторизационные данные + данные для записи("data")
```
{
      "type": "service_account",
      "project_id": "ozonsheets",
      "private_key_id": "",
      "private_key": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n",
      "client_email": "account@ozonsheets.iam.gserviceaccount.com",
      "client_id": "",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/account%40ozonsheets.iam.gserviceaccount.com",
      "spreadsheetId": "",
      "data" : [{"col1": [1, 2, 3]}, {"col2": ["q", "w", "e"]}, {"col3": 1}]
} 
``` 
Responses 200 успешно


___POST___   

_/google_sheets/append_list_   - записывает данные в новый лист google sheets
 
*Parameters*
 json (данные которые нужно записать в таблицу + авторизационные данные + данные для записи("data")
```
{
      "type": "service_account",
      "project_id": "ozonsheets",
      "private_key_id": "",
      "private_key": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n",
      "client_email": "account@ozonsheets.iam.gserviceaccount.com",
      "client_id": "",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/account%40ozonsheets.iam.gserviceaccount.com",
      "spreadsheetId": "",
      "data" : [{"col1": [1, 2, 3]}, {"col2": ["q", "w", "e"]}, {"col3": 1}]
} 
``` 
Responses 200 успешно

___рекомендуемый пример запроса___

```
def post(data, auth_data, host):
    data.update(auth_data)
    url = f'http://{host}:5001/google_sheets/append'
    response = requests.post(url, json=data)
    return response
```
где data(данные для записи в виде json) = {"data" : [{"col1": [1, 2, 3]}, {"col2": ["q", "w", "e"]}, {"col3": 1}}

auth_data(авторизационные данные(credentials) полученные по инструкции выше)