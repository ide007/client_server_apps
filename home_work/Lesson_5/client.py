import json
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import ACTION, ACCOUNT_NAME, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT, ERROR, PRESENCE, RESPONSE, TIME, USER
from common.utils import read_message, send_message
from logs.client_log_config import client_logger


def create_presence(account_name='Guest'):
    """
    функция создания словаря согласно требованиям JIM протокола
    :param account_name: по умолчанию 'Guest'
    :return: dict
    """
    client_logger.info('Создание словаря согласно протоколу "JIM"')
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def server_answer(message):
    """
    Обработчик ответа сервера
    :param message:
    :return:
    """
    client_logger.info(f'Принято сообщение {message} от сервера')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            client_logger.info(f'Сообщение от сервера {message}')
            return '200: OK'
        client_logger.warning(f'Что-то пошло не так: {message[ERROR]}')
        return f'400: {message[ERROR]}'
    client_logger.error('Сообщение сервера не содержит поля "RESPONSE"')
    raise ValueError


def main():
    """
    Загрузка параметров из командной строки, в случаи отсутствия присваиваем
    параметры по умолчанию, из файла variables.py
    :return:
    """
    # проводим проверку полученных параметров запуска
    client_logger.info('Запуск клиента... Анализ параметров запуска...')
    try:
        if len(sys.argv) == 1:
            serv_address = DEFAULT_IP_ADDRESS
            serv_port = DEFAULT_PORT
            client_logger.info(f'Применены параметры запуска по умолчанию; '
                               f'адрес сервера-{serv_address}, порт-{serv_port}.')
        elif len(sys.argv) == 2:
            serv_address = sys.argv[1]
            serv_port = DEFAULT_PORT
            client_logger.info(f'Применены параметры запуска; адрес '
                               f'сервера-{serv_address}, порт по умолчанию-{serv_port}.')
        elif len(sys.argv) == 3:
            serv_address = sys.argv[1]
            serv_port = int(sys.argv[2])
            client_logger.info(f'Применены параметры запуска; адрес '
                               f'сервера-{serv_address}, порт-{serv_port}.')
        elif len(sys.argv) > 3:
            client_logger(f'Получены избыточные параметры запуска'
                          f' {sys.argv[3:]}')
    except IndexError:
        serv_address = DEFAULT_IP_ADDRESS
        serv_port = DEFAULT_PORT
        client_logger.info(f'Применены параметры запуска по умолчанию; '
                           f'адрес сервера-{serv_address}, порт-{serv_port}.')
    except ValueError:
        client_logger.critical('Клиент не запущен. Произошла ошибка запуска'
                               'которая вызвала остановку программы с кодом 1')
        print('Можно указать два параметра через пробел:\n'
              'Первый: ip-адрес сервера \n'
              'Второй: tcp-порт на сервере\n'
              'или указать только ip, хотя если лень можно и без параметров')
        sys.exit(1)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_logger.debug(f'Создан клиентский сокет {client_socket}')
    client_socket.connect((serv_address, serv_port))
    client_logger.info(f'Установлено соединение с сервером {serv_address} по'
                       f' порту {serv_port}')
    message_to_server = create_presence()
    send_message(client_socket, message_to_server)
    client_logger.info(f'Попытка отправить сообщение {message_to_server}'
                       f' серверу')
    try:
        answer = server_answer(read_message(client_socket))
        print(answer)
        client_logger.info(f'Получено сообщение от сервера'
                           f' {answer}')
    except (ValueError, json.JSONDecodeError):
        client_logger.error(f'Не удалось прочитать сообщение от сервера.'
                            f' {TypeError}')


if __name__ == '__main__':
    main()
