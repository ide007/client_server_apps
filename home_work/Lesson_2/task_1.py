import chardet
import re
import csv


def find_encoding(file):
    code_for_file = chardet.universaldetector.UniversalDetector()
    with open(file, 'rb') as e_f:
        for line in e_f:
            code_for_file.feed(line)
            if code_for_file.done:
                break
        code_for_file.close()
    return code_for_file.result['encoding']


def get_data(lst):
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


# def write_to_csv(new_file, data):



if __name__ == '__main__':
    data_to_write = get_data(['info_1.txt', 'info_2.txt', 'info_3.txt'])

