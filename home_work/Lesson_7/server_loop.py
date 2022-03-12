"""
Программа сервера
"""
import sys
import select
import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.variables import ACTION, ACCOUNT_NAME, MAX_CONNECTIONS, \
    DEFAULT_PORT, DEFAULT_IP_ADDRESS, PRESENCE, RESPONSE, \
    TIME, USER, ERROR, RESPONSE_DEFAULT_IP_ADDRESS, MESSAGE, MESSAGE_TEXT, \
    SENDER
from common.utils import read_message, send_message
from log_decorator import log
from logs.server_log_config import server_logger


@log
def check_and_create_answer_to_client(message, messages_list, client):
    """
    Функция для проверки коректности сообщения от клиента, и создания ответа
    :param message: словарь сообщения, протокол JIM
    :param messages_list: список принятых сообщений
    :param client: список клиентов
    :return:
    """
    server_logger.info(f'Принято сообщение: {message}.')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # server_logger.error(f'Сообщение {message} некорректно.')
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message \
            and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE_DEFAULT_IP_ADDRESS: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def new_socket_listen(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.settimeout(0.5)
    return sock


@log
def main():
    """
    Загрузка параметров из командной строки, в случаи отсутствия присваиваем
    параметры по умолчанию, из файла variables.py
    :return:
    """
    server_logger.info('Запуск сервера... Анализ параметров запуска...')
    try:
        # при наличии обрабатываем параметры порта
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            server_logger.info(f'Применен параметр порта:{listen_port}')
        else:
            listen_port = DEFAULT_PORT
            server_logger.info(f'Применен параментр порта по умолчанию: '
                               f'{listen_port}')
        if 65535 < listen_port < 1024:
            server_logger.warning(f'Ошибка применения параментра порта'
                                  f' {listen_port}, так как параметр не'
                                  f' удовлетворяющий требованиям')
            raise ValueError
    except IndexError:
        print('После параметра "-p" нужно указать номер порта сервера.')
        server_logger.critical(f'Ошибка: После параметра "-p" не указан, или '
                               f'некорректно указан номер порта сервера. '
                               f'Ошибка вызвала остановку выполнения программы'
                               f' с кодом 1.')
        sys.exit(1)
    except ValueError:
        print('Номер порта должен быть в интервале от 1024 до 65535.')
        server_logger.critical(f'Ошибка: некорректно указан номер порта. '
                               f'Значение порта должен быть в интервале от '
                               f'1024 до 65535. Ошибка вызвала остановку'
                               f' выполнения программы с кодом 1.')
        sys.exit(1)

    try:
        # при наличии обрабатываем параметры ip-адреса
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
            server_logger.info(f'Применен параметр ip - адреса:'
                               f' {listen_address}')
        else:
            listen_address = DEFAULT_IP_ADDRESS
            server_logger.info(f'Применен параметр ip - адреса по умолчанию: '
                               f'{listen_address}')
    except IndexError:
        print('После параметра "-a" нужно указать IP-адрес для сервера.')
        server_logger.critical(f'Ошибка: После параметра "-а" не указан, или '
                               f'некорректно указан IP-адрес для запуска'
                               f' сервера. Ошибка вызвала остановку выполнения'
                               f' программы с кодом 1.')
        sys.exit(1)

    #   создаем серверный сокет с заданными параметрами
    address = (listen_address, listen_port)
    all_clients = []  # список всех клиентов
    messages = []   # список сообщений
    sock = new_socket_listen(address)
    sock.listen(MAX_CONNECTIONS)

    while True:
        try:
            client_socket, client_address = sock.accept()
            server_logger.info(f'Установлено соединение с клиентом '
                               f'{client_address}.')
        except OSError as err:
            print(err.errno)  # Номер ошибки None потомучто ошибка по таймауту
            pass
        else:
            server_logger.info(f'Установлено соединение с '
                               f'{client_address}.')
            all_clients.append(client_socket)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        try:
            if all_clients:
                recv_data_lst, send_data_lst, err_lst = select.select(
                    all_clients, all_clients, [], 0
                )
        except OSError:
            pass

        if recv_data_lst:
            for client_message in recv_data_lst:
                try:
                    check_and_create_answer_to_client(
                        read_message(client_message),
                        messages, client_message
                    )
                except:
                    server_logger.info(f'Клиент {client_message.getpeername()}'
                                       f'вышел из чата.')
                    all_clients.remove(client_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1],
            }
            del messages[0]
            for read_client in send_data_lst:
                try:
                    send_message(read_client, message)
                except:
                    server_logger.info(f'Клиент {read_client.getpeername()}'
                                       f'вышел из чата.')
                    read_client.close()
                    all_clients.remove(read_client)


if __name__ == '__main__':
    main()
