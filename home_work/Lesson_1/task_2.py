""" Каждое из слов «class», «function», «method» записать в байтовом типе без
преобразования в последовательность кодов (не используя методы encode и decode)
 и определить тип, содержимое и длину соответствующих переменных."""
print('===== Вариант №1 =====')
words_dict = [b'class', b'function', b'method']
bytes_words_dict = []


def fun_1(word):
    print(word, type(word), len(word))


for string in words_dict:
    fun_1(string)

print('===== Вариант №2 =====')
words_dict_2 = ['class', 'function', 'method']

bytes_words_dict_2 = []

for string in words_dict_2:
    byte_string = eval(f'b"{string}"')
    print(50 * '#', '\n')
    print('data: ', byte_string, '\n', 'type: ', type(byte_string))
    print(len(byte_string))
