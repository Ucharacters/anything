#парсинг веб-страницы и манипуляции со строками
from http_get_function import simple_http_get #получение исходной веб-страницы
from proxy_server_config import * #конфигурация прокси-сервера
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


def generate_html_response(request) -> str:
    """Эта функция готовит веб-страницу для передачи в прокси-сервер"""
    the_source_web_page=simple_http_get(request)
    doc = BeautifulSoup(the_source_web_page,"html.parser")

    def is_short_string(string):
        """Вспомогательная функция для поиска строк длиной 6 символов"""
        return len(string) == 6
    
    only_a_tags = SoupStrainer("a")
    only_short_strings = SoupStrainer(string=is_short_string)
    #все уникальные слова из 6 символов
    words_needed=set(BeautifulSoup(the_source_web_page,"html.parser", parse_only=only_short_strings).prettify().split("\n"))
    #все уникальные слова любой длины
    words_needed_extended=set(BeautifulSoup(the_source_web_page,"html.parser").get_text().split(" "))
    
    #из набора слов любой длины выбираем все слова длиной 6 символов и добавляем в набор words_needed
    for plain_string in filter(is_short_string, words_needed_extended):
        if plain_string is not None:
            words_needed.add(plain_string.replace("\n",""))

    #ко всем словам длиной 6 символов добавляем SPECIAL_CHARACTER        
    for special_character_string in words_needed:
        if special_character_string is not None and len(str(special_character_string.strip())) == 6:
            tm_added = BeautifulSoup("<span>"+str(special_character_string.strip()) +SPECIAL_CHARACTER+"</span>", "html.parser")
            try:
                doc.find(text=str(special_character_string)).replace_with(tm_added)
            except:
                pass
            
    #редактируем все анкоры
    for tag in doc.find_all("a"):
        try:
            tag["href"]=tag["href"].replace(tag["href"],PROXY_CONFIG+tag["href"])
        except:
            pass

    return str(doc.prettify()) 
