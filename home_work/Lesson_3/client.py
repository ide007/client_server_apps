import json
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import ACTION, ACCOUNT_NAME, DEFAULT_IP_ADDRESS,\
    DEFAULT_PORT, ERROR, PRESENCE, RESPONSE, TIME, USER
from common.utils import read_message, send_message


def create_presence(account_name='Guest'):
    """
    функция создания словаря согласно требованиям JIM протокола
    :param account_name: по умолчанию 'Guest'
    :return: dict
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.asctime(),
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
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200: OK'
        return f'400: {message[ERROR]}'
    raise ValueError


def main():
    """
    Загрузка параметров из командной строки, в случаи отсутствия присваиваем
    параметры по умолчанию, из файла variables.py
    :return:
    """
    # проводим проверку полученных параметров запуска
    try:
        if len(sys.argv) == 1:
            addr = DEFAULT_IP_ADDRESS
            port = DEFAULT_PORT
        elif len(sys.argv) == 2:
            addr = sys.argv[1]
            port = DEFAULT_PORT
        elif len(sys.argv) == 3:
            addr = sys.argv[1]
            port = int(sys.argv[2])
        elif len(sys.argv) > 3:
            print(f'И что ты своим {sys.argv[3:]} хотел сказать?, надо было '
                  f'всего два параметра: адрес и порт.')
    except (ValueError, IndexError):
        print('Можно указать два параметра через пробел:\n'
              'Первый: ip-адрес сервера \n'
              'Второй: tcp-порт на сервере\n'
              'или указать только ip, хотя если лень можно и без параметров')
        sys.exit(1)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((addr, port))
    message_to_server = create_presence()
    send_message(client_socket, message_to_server)
    try:
        print(server_answer(read_message(client_socket)))
    except (ValueError, json.JSONDecoder):
        print('Не удалось прочитать сообщение от сервера.')


if __name__ == '__main__':
    main()
