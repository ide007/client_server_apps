""" Каждое из слов «разработка», «сокет», «декоратор» представить в строковом
формате и проверить тип и содержание соответствующих переменных. Затем с
помощью онлайн-конвертера преобразовать строковые представление в формат
Unicode и также проверить тип и содержимое переменных."""
print('Слова в строковой форме:')
words_dict = ['разработка', 'сокет', 'декоратор']
help_dict = ['строка "', '" имеет тип - ', 'unicode "']

for word in words_dict:
    print(help_dict[0] + word + help_dict[1], type(word))
print(50 * '#')
print('Слова в форме unicode (кодовых точек):')
unic_dict = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
             '\u0441\u043e\u043a\u0435\u0442',
             '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

for unicode in unic_dict:
    print(help_dict[-1] + unicode + help_dict[1], type(unicode))
print(50 * '#')

print('Сравнение форм:')
for i in range(len(words_dict)):
    print(words_dict[i] == unic_dict[i])
# print(list(i for i in (words_dict, unic_dict)))
