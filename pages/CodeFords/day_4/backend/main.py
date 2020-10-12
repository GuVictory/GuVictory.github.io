#!/usr/bin/env python3

from http.server import HTTPServer
from server import HTTPRequestHandler
import ssl
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def run(ip='127.0.0.1', port=8080, handler_class=HTTPRequestHandler):
    # logging.basicConfig(filename='logs.log', level=logging.DEBUG)

    server = HTTPServer((ip, port), handler_class)
    # logging.info(f'HTTP Server Running \nip: {ip}\nport: {port}\n')
    # print(f'HTTPServer running on: {ip}:{port}')

    server.socket = ssl.wrap_socket(
        server.socket, certfile='./server.pem', server_side=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping server...')
    print('Stopping server...')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
