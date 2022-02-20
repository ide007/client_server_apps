"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата. Для этого:
a.  Подготовить данные для записи в виде словаря, в котором первому ключу
    соответствует список, второму — целое число, третьему — вложенный словарь,
    где значение каждого ключа — это целое число с юникод-символом,
    отсутствующим в кодировке ASCII (например, €);
b.  Реализовать сохранение данных в файл формата YAML — например, в файл
    file.yaml. При этом обеспечить стилизацию файла с помощью параметра
    default_flow_style, а также установить возможность работы с юникодом:
    allow_unicode = True;
c.  Реализовать считывание данных из созданного файла и проверить, совпадают ли
    они с исходными.
"""
import yaml


def write_dict_to_yaml(data, file):
    with open(file, 'w', encoding='utf-8') as f_w:
        yaml.dump(data, f_w, default_flow_style=False, allow_unicode=True)


def read_from_yaml(file):
    with open(file, 'r', encoding='utf-8') as f_r:
        return yaml.load(f_r, Loader=yaml.SafeLoader)


if __name__ == '__main__':

    my_data = {
        'PC': ['computer', 'monitor', 'keyboard', 'mouse'],
        'some_number': 123456,
        'currency': {
            'dollars': ['1$', '5$', '50$', '100$'],
            'euro': ['1€', '20€', '50€', '100€'],
            'yen': ['1¥', '20¥', '50¥', '100¥'],
            'rubles': ['50₱', '100₱', '500₱', '1000₱']
        }
    }

    write_dict_to_yaml(my_data, 'file.yaml')

    print(read_from_yaml('file.yaml') == my_data)
