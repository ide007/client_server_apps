"""
Константы для проекта
"""
# порт по умолчанию
DEFAULT_PORT = 7777

# IP-адрес по умолчанию
DEFAULT_IP_ADDRESS = ''

# Максимальная длина очереди на подключение
MAX_CONNECTIONS = 7

# Максимальная длина сообщения в байтах
MAX_MESSAGE_LEN = 1024

# Применяемая кодировка
ENCODING = 'utf-8'

# Протокол JIM, основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Протокол JIM, прочие ключи
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
RESPONSE_DEFAULT_IP_ADDRESSES = 'response_default_ip_addresses'
