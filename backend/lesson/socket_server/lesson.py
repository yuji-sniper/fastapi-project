import http.server
import socketserver


with socketserver.TCPServer(('127.0.0.1', 8080),
                            http.server.SimpleHTTPRequestHandler) as httpd:
    httpd.serve_forever()
