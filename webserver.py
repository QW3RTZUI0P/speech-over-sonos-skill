import http.server
import socketserver
import os
from threading import Thread

port = 8000
tts_directory_path = "/tmp/mycroft/cache/tts" 
tts_directory = os.path.join(os.path.dirname(__file__), tts_directory_path)
os.chdir(tts_directory)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", port), Handler)
print("serving at port", port)

def start_server():
    httpd.serve_forever()

def stop_server():
    httpd.server_close()

Thread(target=start_server).start()
