
import json
import requests
from requests.exceptions import HTTPError, ConnectionError


URL_API = 'https://api.exchangerate-api.com/v4/latest/'


def get_currency(base_currency):
    response = requests.get(URL_API + base_currency)
    data = response.json()
    if response.status_code == 200:
        status_code = f'{response.status_code} {response.reason}'
    else:
        status_code = f'{response.status_code} {response.reason}'
        data = {"error": "Invalid currency"}
    return status_code, data
        


def app(envirion, start_response):

    path = envirion.get('PATH_INFO', "").strip('/')
    base_currency = path.split("/")[0].upper()

    if path.isalpha() and len(path) == 3:
        try:
            status_code, data = get_currency(base_currency)
            response_headers = [('Content-type', 'application/json')]
            start_response(status_code, response_headers)
            return [json.dumps(data).encode("utf-8")]

        except HTTPError as e:
            # Обрабатываем ошибки внешнего API
            error_data = json.dumps({"error": f"External API error: {e.reason}"})
            status = f"{e.code} {e.reason}"
            headers = [("Content-Type", "application/json")]
            start_response(status, headers)
            return [error_data.encode("utf-8")]

        except ConnectionError as e:
            # Обрабатываем сетевые ошибки
            error_data = json.dumps({"error": f"Network error: {e.reason}"})
            status = "502 Bad Gateway"
            headers = [("Content-Type", "application/json")]
            start_response(status, headers)
            return [error_data.encode("utf-8")]

        except Exception as e:
            # Обрабатываем прочие ошибки
            error_data = json.dumps({"error": f"Unexpected error: {str(e)}"})
            status = "500 Internal Server Error"
            headers = [("Content-Type", "application/json")]
            start_response(status, headers)
            return [error_data.encode("utf-8")]
        
    # Если путь содержит что-то кроме кода валюты
    status = "404 Not Found"
    headers = [("Content-Type", "application/json")]
    start_response(status, headers)
    error_data = json.dumps({"error": "Endpoint not found"})
    return [error_data.encode("utf-8")]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('127.0.0.1', 8080, app)
    print('server start http://127.0.0.1:8080')
    server.serve_forever()
