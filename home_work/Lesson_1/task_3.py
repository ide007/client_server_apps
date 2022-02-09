"""Определить, какие из слов «attribute», «класс», «функция», «type» невозможно
 записать в байтовом типе."""

words_dict = ['attribute', 'класс', 'функция', 'type']

ascii_string = []
not_ascii_string = []


def check(word):
    if word.isascii():
        ascii_string.append(word)
    else:
        not_ascii_string.append(word)


for i in words_dict:
    check(i)

print('Можно записать в байтовом типе : ', ascii_string)

print('Нельзя записать в байтовом типе без преобразования: ', not_ascii_string)
