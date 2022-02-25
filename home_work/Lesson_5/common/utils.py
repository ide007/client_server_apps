"""
Функции кодирования и отправки, а также приема и декодирования сообщений
"""
import json
from .variables import MAX_MESSAGE_LEN, ENCODING


def send_message(socket, message):
    """
    функция кодирования и отправки сообщения, получает словарь и отправляет
    байты в формате json.
    :param socket:
    :param message:
    :return:
    """

    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    socket.send(encoded_message)


def read_message(socket):
    """
    функция приёма и декодирования сообщения, принимает байты, возвращает
    словарь,
    :param socket:
    :return:
    """
    encoded_response = socket.recv(MAX_MESSAGE_LEN)
    if isinstance(encoded_response, bytes):
        if isinstance(json.loads(encoded_response.decode(ENCODING)), dict):
            return json.loads(encoded_response.decode(ENCODING))
        raise ValueError
    raise ValueError
