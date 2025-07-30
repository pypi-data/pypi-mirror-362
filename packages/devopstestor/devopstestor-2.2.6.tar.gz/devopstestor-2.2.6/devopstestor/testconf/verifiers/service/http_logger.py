#!/usr/bin/env python3
import http.server
import http.client
import socketserver
import logging
logging.basicConfig(level=logging.INFO)
import json
import argparse
import sys
import os
import ssl
from urllib.parse import urlparse
print("-----------------------------")
print('Started')
socketserver.TCPServer.timeout = 15
socketserver.TCPServer.allow_reuse_address = True
file_out = None
protocol="http"
json_endpoint = None

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--listen_port", type=int,
                    help="Port d'ecoute")
parser.add_argument("-o", "--output_filepath", type=str,
                    help="Chemin du fichier en sortie")
parser.add_argument("-s", "--protocol", type=str,
                    help="http (default) ou https")
parser.add_argument("-e", "--endpoints", type=str,
                    help='endpoints au format json : {"<uri>": {"response": {"header": "<header_in_response>", "content": "<content_in_response>"}}}')
args = parser.parse_args()

if not args.listen_port or not args.output_filepath:
    print('argument listen_port ou output_filepath manquant')
    sys.exit(-1)

if args.endpoints:
    try:
        json_endpoint = json.loads(args.endpoints)
    except Exception:
        print("Erreur : argument --endpoints, format non json")


if args.protocol:
    protocol = str(args.protocol).lower()

if os.path.exists(args.output_filepath):
    os.remove(args.output_filepath)

class DumpHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self, trace=""):
        cur_uri_parse =  urlparse(self.path)
        if args.endpoints and cur_uri_parse.path in json_endpoint and 'response' in json_endpoint[cur_uri_parse.path]:
            ressource_trouvee = json_endpoint[cur_uri_parse.path]
            print(ressource_trouvee)
            self.send_response(ressource_trouvee['response']['code'])
            for k,v in ressource_trouvee['response']['headers'].items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(ressource_trouvee['response']['content'].encode("utf-8"))
        else : # Tracage de la requete dans la reponse
            self.send_response(200, trace)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def build_trace(self, data=None):
        req = {
            'command': self.command,
            'path': self.path,
            'version': self.request_version,
            'headers': { c:v for c,v in self.headers.items() },
            'client_addr': "{}:{}".format(self.client_address[0], self.client_address[1]),
            'data': data
        }
        str_req = json.dumps(req)
        print(str_req)
        with open(args.output_filepath, 'a') as file_out:
            file_out.write(str_req + '\n')

        return str_req


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode("utf-8") # <--- Gets the data itself
        ctype=self.headers['Content-Type']
        if ctype == 'application/json':
            post_data = json.loads(post_data)
        self._set_response(trace=self.build_trace(post_data))

    def do_GET(self):
        self._set_response(trace=self.build_trace())

    def do_HEAD(self):
        self._set_response(trace=self.build_trace())

## Nouvelle implementation

httpd = http.server.HTTPServer(('127.0.0.1', args.listen_port), DumpHTTPRequestHandler)
if protocol == 'https':
    cert_dir = os.path.abspath(os.path.join(__file__,'../certs'))
    httpd.socket = ssl.wrap_socket (
        httpd.socket,
        certfile=os.path.join(cert_dir, "cert.pem"),
        keyfile=os.path.join(cert_dir, "key.pem"),
        server_side=True)
httpd.serve_forever()

### Ancienne implementation
# with socketserver.TCPServer(("", args.listen_port), DumpHTTPRequestHandler) as httpd:
#     try:
#         if protocol == 'https':
#             cert_dir = os.path.abspath(os.path.join(__file__,'../certs'))
#             httpd.socket = ssl.wrap_socket (
#                 httpd.socket,
#                 keyfile=os.path.join(cert_dir, "key.pem"),
#                 certfile=os.path.join(cert_dir, "cert.pem"),
#                 server_side=True
#             )
#
#         # logging.info("serving at port", args.listen_port)
#         httpd.serve_forever()
#     except Exception as e:
#         print("Erreur {}".format(e))
#     finally:
#         httpd.server_close()
print('Stop')
