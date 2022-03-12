import json
import time

from socket import socket, AF_INET, SOCK_STREAM
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ENCODING,\
    ACTION, TIME, USER, ACCOUNT_NAME, MESSAGE, SENDER, PRESENCE, RESPONSE, \
    ERROR, MESSAGE_TEXT
from logs.client_log_config import client_logger


def send(message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    socket.send(encoded_message)


sock = socket(AF_INET, SOCK_STREAM)
sock.connect((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
out = {
        ACTION: MESSAGE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: "Guest"
        }
    }

while True:
    send(out)

sock.close()
