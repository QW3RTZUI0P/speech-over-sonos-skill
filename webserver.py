import http.server
import socketserver
import os

port = 8000
tts_directory_path = "/tmp/mycroft/cache/tts" 
tts_directory = os.path.join(os.path.dirname(__file__), tts_directory_path)
os.chdir(tts_directory)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

def start_server:
    httpd.serve_forever()

def stop_server:
    httpd.server_close()
