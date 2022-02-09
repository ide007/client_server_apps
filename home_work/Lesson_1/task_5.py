"""Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
 результаты из байтовового в строковый тип на кириллице.
"""
import subprocess
import platform

param = '-n' if platform.system().lower() == 'windows' else '-c'
source = ['yandex.ru', 'youtube.com']
command = 'ping'


def func_5(args):
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        print(line.decode('cp866').encode('utf-8').decode('utf-8'), end='')


for i in source:
    args = [command, param, '2', i]
    func_5(args)
