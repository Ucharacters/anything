import time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import re

app = FastAPI()

USERAGENT_HEADER = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11"""
ACCEPT_HEADER = """text/html,application/xhtml+xml,application/xml;q=0.9,\
*/*;q=0.8"""
only_a_tags = SoupStrainer("a")

def simple_http_get(url, headers=None):
    default_headers = {
        'Accept': ACCEPT_HEADER,
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': USERAGENT_HEADER
    }
    default_headers.update(headers or {})
    req = requests.get(url, headers=default_headers)
    return req.text

  



def generate_html_response(request):
    print("generate_html_response=>"+request)
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    the_soup=simple_http_get(request)
##    print("raw="+str(the_soup))

    def is_short_string(string):
        return len(string) == 6
    
    only_short_strings = SoupStrainer(string=is_short_string)
    words_needed=set(BeautifulSoup(the_soup,"html.parser", parse_only=only_short_strings).prettify().split("\n"))
    doc = BeautifulSoup(the_soup,"html.parser")
    
    for tm_adder in words_needed:
        if tm_adder is not None and len(str(tm_adder)) == 6:
            tm_added = BeautifulSoup("<span>"+str(tm_adder) +"™</span>", "html.parser")
            doc.find(text=str(tm_adder)).replace_with(tm_added)
            print(str(tm_added))


    print(doc)
    
    soup=BeautifulSoup(the_soup,"html.parser",parse_only=only_a_tags)
    print(soup.prettify())   
    
    for tag in soup.find_all("a"):
        tag["href"]=tag["href"].replace(tag["href"],'http://127.0.0.1:8000/processor/'+tag["href"])
##        print(tag["href"])
##        print(str(tag.contents))    
##    doc = BeautifulSoup(soup.prettify(), "xml")
##
##    try:
##        doc.find(text="INSERT FOOTER HERE").replace_with(footer+"™")
##    except NoneType:
##        pass
##
##    for link in soup.find_all('a'):
##            print(link.get('href'))
##            print(str(link.a['href']))
##    print("personal_org_menu="+str(soup.find("a").get_text()).strip())
    #print(BeautifulSoup(data1, "html.parser", parse_only=only_a_tags).prettify())
    print("<=generate_html_response")
    return HTMLResponse(content=html_content, status_code=200)


@app.middleware("http")
def add_process_time_header(request: Request, generate_html_response):
#async
    start_time = time.time()
    #response = await generate_html_response(request)
    response = generate_html_response(request)
    process_time = time.time() - start_time
    print(str(process_time))
    return response

   

print("====================Starting the server=============")
generate_html_response("https://news.ycombinator.com/item?id=13713480")
#import uvicorn
#uvicorn.run(app, host='127.0.0.1', port=8000)
#pip install lxml
