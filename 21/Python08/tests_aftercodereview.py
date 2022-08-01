import unittest
from http_get_function import simple_http_get #получение исходной веб-страницы
from proxy_server import MyHttpRequestHandler #реализация прокси-сервера
from html_handling import generate_html_response #парсинг веб-страницы и манипуляции со строками

request="https://raw.githubusercontent.com/Ucharacters/anything/master/21/Python08/test_html_page.html"


class TestMethods(unittest.TestCase):

    def test_can_get_web_page_from_internet(self):
        """Проверка возможности получения веб-страницы"""
        self.assertEqual(simple_http_get("https://dweet.io/get/latest/dweet/for/60cc2805-c135-4d7f-88b7-a8378d7ce7bb"), '{"this":"failed","with":404,"because":"we couldn\'t find this"}')
        
    def test_html_utilities(self):
        """Заменяет слова и возвращает HTML"""
        self.maxDiff=None
        self.assertEqual(generate_html_response(request),'<!DOCTYPE html>\n<html>\n <body>\n  123456\n </body>\n</html>')


    def test_proxy(self):
        self.assertEqual(simple_http_get("http://127.0.0.1:8000/?processor="+request), '<!DOCTYPE html>\n<html>\n <body>\n  123456\n </body>\n</html>')


if __name__ == '__main__':
    unittest.main()
