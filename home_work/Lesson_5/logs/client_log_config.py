import logging
import os
import sys

client_logger = logging.getLogger('client')
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(funcName)s '
                              '%(message)s',datefmt='%Y %b %d %H:%M:%S',)
file_hand = logging.FileHandler(PATH, encoding='utf-8')
file_hand.setLevel(logging.DEBUG)


file_hand.setFormatter(formatter)
client_logger.addHandler(file_hand)
client_logger.setLevel(10)


if __name__ == '__main__':
    stream_hand = logging.StreamHandler(sys.stdout)
    stream_hand.setFormatter(formatter)
    client_logger.addHandler(stream_hand)
    client_logger.info('Тестовое сообщение')
