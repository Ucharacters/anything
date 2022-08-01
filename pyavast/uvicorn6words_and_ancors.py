import time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI()

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

    the_soup=simple_http_get(request)
    doc = BeautifulSoup(the_soup,"html.parser")
    
##    print("raw="+str(the_soup))

    def is_short_string(string):
        return len(string) == 6
    
    only_a_tags = SoupStrainer("a")
    only_short_strings = SoupStrainer(string=is_short_string)
    words_needed=set(BeautifulSoup(the_soup,"html.parser", parse_only=only_short_strings).prettify().split("\n"))

    for tm_adder in words_needed:
        if tm_adder is not None and len(str(tm_adder)) == 6:
            tm_added = BeautifulSoup("<span>"+str(tm_adder) +"™</span>", "html.parser")
            doc.find(text=str(tm_adder)).replace_with(tm_added)

    print("INFO: All 6 letter word replaced")
    
    for tag in doc.find_all("a"):
        tag["href"]=tag["href"].replace(tag["href"],'http://127.0.0.1:8000/processor/'+tag["href"])

    print("INFO: All ancors replaced")
    
##    print(doc.prettify())
    
    print("INFO: <=generate_html_response")
    return HTMLResponse(content=str(doc.prettify()), status_code=200)


@app.middleware("http")
async def add_process_all_requests(request: Request, generate_html_response):
    start_time = time.time()
    response = await generate_html_response(request)
    process_time = time.time() - start_time
    print(str(process_time))
    return response

@app.get("/processor/{item_id}")
def read_item(item_id: Optional[str] = None):
    if item_id  is not None:
        return HTMLResponse(content=str(generate_html_response(item_id).prettify()), status_code=200)
    else:
        return HTMLResponse(content="404", status_code=404)

print("====================Starting the server=============")
print(generate_html_response("https://news.ycombinator.com/item?id=13713480"))



#open in browser http://127.0.0.1:8000?processor=https://news.ycombinator.com/item?id=13713480

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
        
        html = "<html><head></head><body>"+str(name)+"<br>"+str(generate_html_response(str(name)))+"</body></html>" 
        self.wfile.write(bytes(html, "utf8"))
        return


handler_object = MyHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)
my_server.serve_forever()



