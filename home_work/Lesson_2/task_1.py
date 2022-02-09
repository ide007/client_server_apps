"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

a.  Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
    данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
    «Изготовитель системы»,  «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить
    в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
    os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и
    поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
    «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
    каждого файла);
b.  Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
    через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
c.  Проверить работу программы через вызов функции write_to_csv().
"""
import chardet
import re
import csv


def find_encoding(file):
    """
    Функция поиска кодировки файла с помощью библиотеки chardet, для последующей передачи в параметр 'encoding='
    :param file:
    :return: 'encoding="encode"'
    """
    code_for_file = chardet.universaldetector.UniversalDetector()
    with open(file, 'rb') as e_f:
        for line in e_f:
            code_for_file.feed(line)
            if code_for_file.done:
                break
        code_for_file.close()
    return code_for_file.result['encoding']


def get_data(lst):
    """
    Функция для считывания данных из принятого списка файлов, и последующего формирования выходных данных в соответствии
    с задаными параметрами
    :param lst:
    :return:
    """
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [['Изготовитель системы',  'Название ОС', 'Код продукта', 'Тип системы']]

    for file in lst:
        decode = find_encoding(file)
        with open(file, 'rb') as r_f:
            for line in r_f:
                row = line.decode(encoding=decode).rstrip()
                if re.match(main_data[0][0], row):
                    os_prod_list.append(re.search(r'(Изготовитель системы).\s*(.*)', row).group(2))
                elif re.match(main_data[0][1], row):
                    os_name_list.append(re.search(r'(Название ОС).\s*(.*)', row).group(2))
                elif re.match(main_data[0][2], row):
                    os_code_list.append(re.search(r'(Код продукта).\s*(.*)', row).group(2))
                elif re.match(main_data[0][3], row):
                    os_type_list.append(re.search(r'(Тип системы).\s*(.*)', row).group(2))

    for idx in range(len(lst)):
        main_data.append([
            os_prod_list[idx],
            os_name_list[idx],
            os_code_list[idx],
            os_type_list[idx]
        ])

    return main_data


def write_to_csv(csv_file_name, data):
    """
    Функция для создания и записи переданных данных в csv - файл.
    :param csv_file_name:
    :param data:
    :return:
    """
    with open(csv_file_name, 'w', encoding='utf-8') as n_f:
        csv.writer(n_f, lineterminator='\r').writerows(data)


if __name__ == '__main__':
    data_to_write = get_data(['info_1.txt', 'info_2.txt', 'info_3.txt'])
    write_to_csv('data_file.csv', data_to_write)

    with open('data_file.csv', encoding='utf-8') as fl:  # чтение итогового файла
        print(fl.read())
