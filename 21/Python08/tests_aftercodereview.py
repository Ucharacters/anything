import unittest
from http_get_function import simple_http_get #получение исходной веб-страницы
from proxy_server import MyHttpRequestHandler #реализация прокси-сервера
from html_handling import generate_html_response #парсинг веб-страницы и манипуляции со строками



class TestMethods(unittest.TestCase):

    def test_can_get_web_page_from_internet(self):
        """Проверка возможности получения веб-страницы"""
        self.assertEqual(simple_http_get("https://dweet.io/get/latest/dweet/for/60cc2805-c135-4d7f-88b7-a8378d7ce7bb"), '{"this":"failed","with":404,"because":"we couldn\'t find this"}')
        
    def test_html_utilities(self):
        """Заменяет слова и возвращает HTML"""
        self.maxDiff=None
        self.assertEqual(generate_html_response("https://www.guidgenerator.com/online-guid-generator.aspx"),"")


    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
