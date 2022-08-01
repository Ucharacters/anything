import typing
import socketserver

from http_get_function import simple_http_get #получение исходной веб-страницы
from proxy_server import MyHttpRequestHandler #реализация прокси-сервера
from html_handling import generate_html_response #парсинг веб-страницы и манипуляции со строками
from proxy_server_config import * #конфигурация прокси-сервера

if __name__ == '__main__':
    # для примера можно открыть в браузере http://127.0.0.1:8000/?processor=https://en.wikipedia.org/wiki/Comparison_of_cryptographic_hash_functions 
    handler_object = MyHttpRequestHandler
    my_server = socketserver.TCPServer(("", PROXY_PORT), handler_object)
    print("====================Starting the server=============")
    my_server.serve_forever()
    #Сервер можно остановить нажатием Ctrl+C



