#open in browser http://127.0.0.1:8000/?processor=https://en.wikipedia.org/wiki/Comparison_of_cryptographic_hash_functions

import time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests


USERAGENT_HEADER = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11"""
ACCEPT_HEADER = """text/html,application/xhtml+xml,application/xml;q=0.9,\
*/*;q=0.8"""


def simple_http_get(url, headers=None):
    default_headers = {
        'Accept': ACCEPT_HEADER,
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': USERAGENT_HEADER
    }
    default_headers.update(headers or {})
    try:
        req = requests.get(url, headers=default_headers)
        return req.text
    except:
        return "ERROR"

def generate_html_response(request):
    print("INFO: generate_html_response=>"+request)
    start_time = time.time()

    the_soup=simple_http_get(request)
    doc = BeautifulSoup(the_soup,"html.parser")
    
##    print("raw="+str(the_soup))

    def is_short_string(string):
        return len(string) == 6
    
    only_a_tags = SoupStrainer("a")
    only_short_strings = SoupStrainer(string=is_short_string)
    words_needed=set(BeautifulSoup(the_soup,"html.parser", parse_only=only_short_strings).prettify().split("\n"))
    words_also_needed=set(BeautifulSoup(the_soup,"html.parser").get_text().split(" "))

    for plain_adder in filter(is_short_string, words_also_needed):
        if plain_adder is not None:
            words_needed.add(plain_adder.replace("\n",""))
    for tm_adder in words_needed:
        if tm_adder is not None and len(str(tm_adder.strip())) == 6:
            tm_added = BeautifulSoup("<span>"+str(tm_adder.strip()) +"™</span>", "html.parser")
            try:
                doc.find(text=str(tm_adder)).replace_with(tm_added)
            except:
                pass
            
    print("INFO: All 6-letter words replaced")
    
    for tag in doc.find_all("a"):
        try:
            tag["href"]=tag["href"].replace(tag["href"],'http://127.0.0.1:8000?processor='+tag["href"])
        except:
            pass
        

    print("INFO: All ancors replaced")
    
##    print(doc.prettify())
    process_time = time.time() - start_time
    print("INFO: <=generate_html_response finished in "+str(process_time))
    return str(doc.prettify()) #HTMLResponse(content=str(doc.prettify()), status_code=200)


##print(generate_html_response("https://news.ycombinator.com/item?id=13713480"))
#open in browser http://127.0.0.1:8000/?processor=https://en.wikipedia.org/wiki/Comparison_of_cryptographic_hash_functions

import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        name = 'World'
        query_components = parse_qs(urlparse(self.path).query)
        if 'processor' in query_components:
            name = query_components["processor"][0]
        
        html = "<html><head></head><body>"+str(generate_html_response(str(name)))+"</body></html>" 
        self.wfile.write(bytes(html, "utf8"))
        return

print("====================Starting the server=============")
print("open in browser http://127.0.0.1:8000/?processor=https://en.wikipedia.org/wiki/Comparison_of_cryptographic_hash_functions")
handler_object = MyHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)
my_server.serve_forever()



