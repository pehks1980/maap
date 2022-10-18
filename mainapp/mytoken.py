import json
import http.client as httplib

# Идентификатор приложения
from bottle import route, request, urlencode, run
from cred_maap import client_id, client_secret


@route('/')
def index():
    # Если скрипт был вызван с указанием параметра "code" в URL,
    # то выполняется запрос на получение токена
    if request.query.get('code'):
        # Формирование параметров (тела) POST-запроса с указанием кода подтверждения
        query = {
            'grant_type': 'authorization_code',
            'code': request.query.get('code'),
            'client_id': client_id,
            'client_secret': client_secret,
        }
        query = urlencode(query)

        # Формирование заголовков POST-запроса
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Выполнение POST-запроса и вывод результата
        connection = httplib.HTTPSConnection('oauth.yandex.ru')
        connection.request('POST', '/token', query, header)
        response = connection.getresponse()
        result = response.read()
        connection.close()

        # Токен необходимо сохранить для использования в запросах к API Директа
        return json.loads(result)

host = "localhost"
port = 8070
print(f"Запускаем веб-сервер http://{host}:{port}/?code=")
run(host='localhost', port=8070, quiet=True)
