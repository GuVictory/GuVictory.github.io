from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse
import re
import cgi
import json
import threading
from urllib import parse
import logging

from local_data import LocalData


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code, jsonFlag, message=''):
        if message != '':
            self.send_response(status_code, message)
        else:
            self.send_response(status_code)

        if jsonFlag:
            self.send_header('Content-Type', 'application/json; charset=UTF-8')

        self.end_headers()

    def do_GET(self):
        logging.info(
            f'GET request,\nPath: {str(self.path)}\nHeaders:\n{str(self.headers)}\n')

        # * URL для отключения сервера
        if re.search('/api/shutdown', self.path):
            self._shutdown()

        # * Получание списка всех часто задаваемые вопросы для студентов
        elif re.search('/api/student_quesions/', self.path):
            self._get_some_full_data(LocalData.storage['student_questions'])

        # * Получание списка всех часто задаваемые вопросы для инструкторов
        elif re.search('/api/instructor_quesions/', self.path):
            self._get_some_full_data(LocalData.storage['instructor_questions'])

        else:
            self._set_headers(403, False)

    def _get_some_full_data(self, localdata):
        self._set_headers(200, True)
        data = json.dumps(localdata, ensure_ascii=False)
        self.wfile.write(data.encode('utf8'))

    def _shutdown(self):
        # ! Отключение необхдимо производить в отдельном потоке
        def kill_me_please():
            self.server.shutdown()
        threading.Thread(target=kill_me_please).start()
        #  Перед отключением сервера отправим 200
        self._set_headers(200, False)


def run(ip='127.0.0.1', port=8080, handler_class=HTTPRequestHandler):
    logging.basicConfig(filename='logs.log', level=logging.DEBUG)

    server = HTTPServer((ip, port), handler_class)
    logging.info(f'HTTP Server Running \nip: {ip}\nport: {port}\n')
    print(f'HTTPServer running on: {ip}:{port}')
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
