"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON
с информацией о заказах. Написать скрипт,автоматизирующий его заполнение
данными. Для этого:
a. Создать функцию write_order_to_json(), в которую передается 5 параметров —
   товар (item), количество (quantity), цена (price), покупатель (buyer),
   дата (date). Функция должна предусматривать запись данных в виде словаря в
   файл orders.json. При записи данных указать величину отступа в 4 пробельных
   символа;
b. Проверить работу программы через вызов функции write_order_to_json() с
передачей в нее значений каждого параметра.
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', encoding='utf-8') as file:
        dict_to_json = json.load(file)
        dict_to_json['orders'].append({
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date,
        })

    with open('orders.json', 'w', encoding='utf-8') as f_w:
        json.dump(dict_to_json, f_w, indent=4)


if __name__ == '__main__':
    write_order_to_json('Pen', 2, 15, 'Ivanov', '09.02.2022')
    write_order_to_json('Pencil', 4, 10, 'Petrov', '09.02.2022')
    write_order_to_json('Paper', 500, 250, 'Sidorov', '09.02.2022')
