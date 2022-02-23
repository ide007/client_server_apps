import logging
import os
import sys

log = logging.getLogger('app.main')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'app.main.log')
file_hand = logging.FileHandler(PATH, encoding='utf-8')
file_hand.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y %b %d %H:%M:%S')

file_hand.setFormatter(formatter)
log.addHandler(file_hand)
log.setLevel(20)


if __name__ == '__main__':
    stream_hand = logging.StreamHandler(sys.stdout)
    stream_hand.setFormatter(formatter)
    log.addHandler(stream_hand)
    log.info('Отладочное сообщение')
