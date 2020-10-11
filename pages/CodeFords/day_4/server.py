from http.server import BaseHTTPRequestHandler
import argparse
import re
import cgi
import json
import threading
from urllib import parse
import logging
from localdata import LocalData


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code, json_flag, message=''):
        if message != '':
            self.send_response(status_code, message)
        else:
            self.send_response(status_code)

        if json_flag:
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
            self._get_data('student_questions')

        # * Получание списка всех часто задаваемые вопросы для инструкторов
        elif re.search('/api/instructor_questions/$', self.path):
            self._get_data('instructor_questions')

        # * Получание списка всех топиков для студентов
        elif re.search('/api/student_topics/$', self.path):
            self._get_data('student_topics')

        # * Получание списка всех топиков для инструкторов
        # $ - в регуляром выражении необходимо, для определения конца строки
        elif re.search('/api/instructor_topics/$', self.path):
            self._get_data('instructor_topics')

        # * Получание часто задаваемого вопроса для студентов по id
        elif re.search('/api/student_questions/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._get_data_by_id('student_questions', record_id)

        # * Получание часто задаваемого вопроса для инструкторов по id
        elif re.search('/api/instructor_questions/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._get_data_by_id('instructor_questions', record_id)

        # * Получание топика для студентов по id
        elif re.search('/api/student_topics/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._get_data_by_id('student_topics', record_id)

        # * Получание топика для инструкторов по id
        elif re.search('/api/instructor_topics/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._get_data_by_id('instructor_topics', record_id)

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

        # * Создание нового часто задаваемого вопроса у студентов
        if re.search('/api/student_questions/$', self.path):
            self._post_data('student_questions', new_data)

        # * Создание нового часто задаваемого вопроса у инструкторов
        elif re.search('/api/instructor_questions/$', self.path):
            self._post_data('instructor_questions', new_data)

        # * Создание нового топика у студентов
        elif re.search('/api/student_topics/$', self.path):
            self._post_data('student_topics', new_data)

        # * Создание нового топика у инструкторов
        elif re.search('/api/instructor_topics/$', self.path):
            self._post_data('instructor_topics', new_data)

        # * Изменение часто задаваемого вопроса для студентов по id
        elif re.search('/api/student_questions/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._put_data_by_id('student_questions', new_data, record_id)

        # * Изменение часто задаваемого вопроса для инструкторов по id
        elif re.search('/api/instructor_questions/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._put_data_by_id('instructor_questions', new_data, record_id)

        # * Изменения топика для студентов по id
        elif re.search('/api/student_topics/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._put_data_by_id('student_topics', new_data, record_id)

        # * Изменение топика для инструкторов по id
        elif re.search('/api/instructor_topics/\d+$', self.path):
            record_id = int(self.path.split('/')[-1])
            self._put_data_by_id('instructor_topics', new_data, record_id)
        else:
            self._set_headers(404, True)
            self._send_error_message(
                'Oops, no page with this address was found')

    def _get_data(self, localdata):
        self._set_headers(200, True)
        data = json.dumps(LocalData.get(localdata), ensure_ascii=False)
        self.wfile.write(data.encode('utf8'))

    def _get_data_by_id(self, localdata, record_id):
        was_found, data = LocalData.get_by_id(localdata, record_id)
        print(was_found)
        if was_found:
            self._set_headers(200, True)
            self.wfile.write(json.dumps(
                data, ensure_ascii=False).encode('utf8'))
        else:
            self._set_headers(404, True)
            self._send_error_message(
                'Oops, it looks like you are trying to view a non-existing entry!')

    def _post_data(self, localdata, new_data):
        self._set_headers(201, True)
        created_data = LocalData.create(localdata, new_data)
        self.wfile.write(json.dumps(
            created_data, ensure_ascii=False).encode('utf8'))

    def _put_data_by_id(self, localdata, new_data, record_id):
        was_changed, data = LocalData.change_by_id(
            localdata, new_data, record_id)
        if was_changed:
            self._set_headers(200, True)
            self.wfile.write(json.dumps(
                data, ensure_ascii=False).encode('utf8'))
        else:
            self._set_headers(404, True)
            self._send_error_message(
                'Oops, it looks like you are trying to change a not existing entry!')

    def _shutdown(self):
        # ! Отключение необхдимо производить в отдельном потоке
        def kill_me_please():
            self.server.shutdown()
        threading.Thread(target=kill_me_please).start()
        #  Перед отключением сервера отправим 200
        self._set_headers(200, False)

    def _send_error_message(self, message):
        data = {
            'message': message
        }
        self.wfile.write(json.dumps(
            data, ensure_ascii=False).encode('utf8'))
