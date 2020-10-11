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
        elif re.search('/api/student_questions/$', self.path):
            self._get_some_full_data(LocalData.storage['student_questions'])

        # * Получание списка всех часто задаваемые вопросы для инструкторов
        elif re.search('/api/instructor_questions/$', self.path):
            self._get_some_full_data(LocalData.storage['instructor_questions'])

        # * Получание списка всех топиков для студентов
        elif re.search('/api/student_topics/$', self.path):
            self._get_some_full_data(LocalData.storage['student_topics'])

        # * Получание списка всех топиков для инструкторов
        # $ - в регуляром выражении необходимо, для определения конца строки
        elif re.search('/api/instructor_topics/$', self.path):
            self._get_some_full_data(LocalData.storage['instructor_topics'])

        # * Получание списка часто задаваемого вопроса для студентов по id
        elif re.search('/api/student_questions/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._get_some_record(
                LocalData.storage['student_questions'], record_id)

        # * Получание списка часто задаваемого вопроса для инструкторов по id
        elif re.search('/api/instructor_questions/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._get_some_record(
                LocalData.storage['instructor_questions'], record_id)

        # * Получание списка часто задаваемого вопроса для студентов по id
        elif re.search('/api/student_topics/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._get_some_record(
                LocalData.storage['student_topics'], record_id)

        # * Получание списка часто задаваемого вопроса для инструкторов по id
        elif re.search('/api/instructor_topics/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._get_some_record(
                LocalData.storage['instructor_topics'], record_id)

        else:
            self._set_headers(403, False)

    def do_POST(self):

        ctype, pdict = cgi.parse_header(
            self.headers.get('content-type'))

        if ctype != 'application/json':
            self._set_headers(400, False, "Bad Request: must give data")
            return

        length = int(self.headers.get('content-length'))
        rfile_str = self.rfile.read(length).decode('utf8')
        new_data = json.loads(rfile_str)

        logging.info(
            f'POST request\nPath: {str(self.path)}\nHeaders:\n{str(self.headers)}Body:\n{new_data}\n')

        if re.search('/api/student_questions/$', self.path):
            self._post_new_data(
                LocalData.storage['student_questions'], new_data)

        elif re.search('/api/instructor_questions/$', self.path):
            self._post_new_data(
                LocalData.storage['instructor_questions'], new_data)

        elif re.search('/api/student_topics/$', self.path):
            self._post_new_data(
                LocalData.storage['student_topics'], new_data)

        elif re.search('/api/instructor_topics/$', self.path):
            self._post_new_data(
                LocalData.storage['instructor_topics'], new_data)
        else:
            # HTTP 403: forbidden
            self._set_headers(403, False)

    def _get_some_full_data(self, localdata):
        self._set_headers(200, True)
        data = json.dumps(localdata, ensure_ascii=False)
        self.wfile.write(data.encode('utf8'))

    def _get_some_record(self, localdata, record_id):
        print(record_id, len(localdata))
        if record_id >= len(localdata) or record_id < 0:
            self._set_headers(404, False, 'Not Found: record does not exist')
        else:
            self._set_headers(200, True)
            data = json.dumps(localdata[record_id], ensure_ascii=False)
            self.wfile.write(data.encode('utf8'))

    def _post_new_data(self, localdata, new_data):
        self._set_headers(201, True)
        new_data['id'] = len(localdata)
        localdata.append(new_data)
        self.wfile.write(json.dumps(
            new_data, ensure_ascii=False).encode('utf8'))

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

'''
elif re.search('/api/getrecord/*', self.path):
            record_id = self.path.split('/')[-1]
            if record_id in LocalData.records:
                # * Выставляем True, так как нам необходимо установать json формат данных
                self._set_headers(200, True)
                data = json.dumps(LocalData.records[record_id])
                self.wfile.write(data.encode('utf8'))

            else:
                self._set_headers(
                    404, False, 'Not Found: record does not exist')


    def do_POST(self):
        if re.search('/api/addrecord/*', self.path):
            ctype, pdict = cgi.parse_header(
                self.headers.get('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.get('content-length'))
                rfile_str = self.rfile.read(length).decode('utf8')

                data = json.loads(rfile_str)
                record_id = self.path.split('/')[-1]
                LocalData.records[record_id] = data

                logging.info(
                    f'POST request\nPath: {str(self.path)}\nHeaders:\n{str(self.headers)}Body:\n{data}\n')

                # HTTP 200: ok
                self._set_headers(200, False)
            else:
                # HTTP 400: bad request
                self._set_headers(400, False, "Bad Request: must give data")
        else:
            # HTTP 403: forbidden
            self._set_headers(403, False)
'''
