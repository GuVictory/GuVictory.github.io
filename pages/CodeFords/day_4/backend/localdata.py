# * Место для хранения данных
class LocalData(object):
    storage = {
        'student_questions': [
            {
                'title': 'Пожизненный доступ',
                'id': 0
            },
            {
                'title': 'Как работает CodeFords',
                'id': 1
            },
            {
                'title': 'Как найти пропавший курс',
                'id': 2
            },
            {
                'title': 'Сертификат об окончании',
                'id': 3
            },
            {
                'title': 'Загрузка ресурсов курса',
                'id': 4
            },
            {
                'title': 'Решение вопроса оплаты',
                'id': 5
            },
        ],
        'instructor_questions': [
            {
                'title': 'Продвижение своих курсов',
                'id': 0
            },
            {
                'title': 'Как выбрать способ оплаты',
                'id': 1
            },
            {
                'title': 'Контроль качества курсов',
                'id': 2
            },
            {
                'title': 'Доля дохода инструктора',
                'id': 3
            },
            {
                'title': 'Рекламные соглашения',
                'id': 4
            },
            {
                'title': 'Как стать инструктором',
                'id': 5
            },
        ],
        'student_topics': [],
        'instructor_topics': []
    }

    @classmethod
    def get(cls, datatype):
        return cls.storage[datatype]

    @classmethod
    def create(cls, datatype, data):
        data['id'] = len(cls.storage[datatype])
        cls.storage[datatype].append(data)
        return data

    @classmethod
    def get_by_id(cls, datatype, id):
        try:
            data = cls.storage[datatype][id]
            print(data)
            return (True, data)
        except:
            return (False, None)

    @classmethod
    def change_by_id(cls, datatype, new_value, id):
        try:
            new_value['id'] = id
            cls.storage[datatype][id] = new_value
            return (True, new_value)
        except:
            return (False, None)

    @classmethod
    def delete_by_id(cls, datatype, id):
        try:
            cls.storage[datatype] = cls.storage[datatype][:id] + \
                cls.storage[datatype][id + 1:]

            return True
        except:
            return False
