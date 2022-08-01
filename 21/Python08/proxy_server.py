#реализация прокси-сервера
import http.server
from urllib.parse import urlparse
from urllib.parse import parse_qs
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        """Функция-обработчик для всех запросов GET"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        name = 'World'
        query_components = parse_qs(urlparse(self.path).query)
        if 'processor' in query_components:
            name = query_components["processor"][0]
        
        html = "<html><head></head><body>"+str(generate_html_response(str(name)))+"</body></html>" 
        self.wfile.write(bytes(html, "utf8"))
        return None
