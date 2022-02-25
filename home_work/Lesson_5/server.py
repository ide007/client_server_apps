import sys
import json
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.variables import ACTION, ACCOUNT_NAME, MAX_CONNECTIONS, \
    DEFAULT_PORT, DEFAULT_IP_ADDRESS, PRESENCE, RESPONSE, \
    TIME, USER, ERROR, RESPONSE_DEFAULT_IP_ADDRESS
from common.utils import read_message, send_message
from logs.server_log_config import server_logger


def check_and_create_answer_to_client(message):
    """
    Функция для проверки коректности сообщения от клиента, и создания ответа
    :param message:
    :return:
    """
    server_logger.info(f'Принято сообщение: {message}.')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    server_logger.error(f'Сообщение {message} некорректно.')
    return {
        RESPONSE_DEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad Request'
    }


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

    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_sock.bind((listen_address, listen_port))

    server_sock.listen(MAX_CONNECTIONS)

    while True:
        client_socket, client_address = server_sock.accept()
        server_logger.info(f'Установлено соединение с клиентом {client_address}')
        try:
            message_from_client = read_message(client_socket)
            print(message_from_client)
            server_logger.info(f'Клиент прислал сообщение:'
                               f' {message_from_client}')
            response = check_and_create_answer_to_client(message_from_client)
            server_logger.debug(f'Принято сообщение: {message_from_client} от'
                                f' {client_address}')
            send_message(client_socket, response)
            server_logger.info(f'Попытка отправки сообщения {response} клиенту'
                               f' {client_address}')
            server_logger.debug(f'Соединение с клиентом {client_address} закрыто.')
            client_socket.close()
        except (ValueError, json.JSONDecodeError):
            server_logger.warning('Принятое сообщение от клиента'
                                  ' несоответствует протоколу, либо возникла'
                                  ' ошибка при декодировании сообщения.')
            server_logger.info(f'Соединение с клиентом {client_address} закрыто.')
            client_socket.close()


if __name__ == '__main__':
    main()
