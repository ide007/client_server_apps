""" Скрипт запуска/остановки скрипта сервера и клиентов """
import time
from subprocess import Popen, CREATE_NEW_CONSOLE

clients = []
serv = []
while True:
    user = input('Запуск сервера и клиентов (s) / Закрытие клиентов (x) / '
                 'Выход (q)')

    if user == 'q':
        break

    elif user == 's':
        serv.append(Popen('python server_loop.py',
                          creationflags=CREATE_NEW_CONSOLE))
        for i in range(2):
            time.sleep(0.5)
            clients.append(Popen('python client.py -m send',
                                 creationflags=CREATE_NEW_CONSOLE))
            clients.append(Popen('python client.py -m listen',
                                 creationflags=CREATE_NEW_CONSOLE))
            print('Произведен запуск 2 клиентов')
    elif user == 'x':
        for script in clients:
            script.kill()
        serv[0].kill()
        clients.clear()
