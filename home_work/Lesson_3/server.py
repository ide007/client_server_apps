import sys
import json
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.variables import ACTION, ACCOUNT_NAME, MAX_CONNECTIONS,\
    DEFAULT_PORT, DEFAULT_IP_ADDRESS, PRESENCE, RESPONSE, \
    RESPONSE_DEFAULT_IP_ADDRESSES, TIME, USER
from common.utils import read_message, send_message


def check_and_create_answer_to_client(message):
    """
    Функция для проверки коректности сообщения от клиента, и создания ответа
    :param message:
    :return:
    """
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message\
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {RESPONSE_DEFAULT_IP_ADDRESSES: 400}


def main():
    """
    Загрузка параметров из командной строки, в случаи отсутствия присваиваем
    параметры по умолчанию, из файла variables.py
    :return:
    """
    try:
        # при наличии обрабатываем параметры порта
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if 65535 < listen_port < 1024:
            raise ValueError
    except IndexError:
        print('После параметра "-p" нужно указать номер порта сервера.')
        sys.exit(1)
    except ValueError:
        print('Номер порта должен быть в интервале от 1024 до 65535.')
        sys.exit(1)

    try:
        # при наличии обрабатываем параметры ip-адреса
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = DEFAULT_IP_ADDRESS
    except IndexError:
        print('После параметра "-a" нужно указать IP-адрес для сервера.')

    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_sock.bind((listen_address, listen_port))

    server_sock.listen(MAX_CONNECTIONS)

    while True:
        client_socket, address = server_sock.accept()
        try:
            message_from_client = read_message(client_socket)
            print(message_from_client)
            response = check_and_create_answer_to_client(message_from_client)
            send_message(client_socket, response)
            client_socket.close()
        except (ValueError, json.JSONDecoder):
            print('Принятое сообщение от клиента несоответствует протоколу,'
                  ' либо возникла ошибка при декодировании сообщения.')
            client_socket.close()


if __name__ == '__main__':
    main()
