"""Преобразовать слова «разработка», «администрирование», «protocol»,
 «standard» из строкового представления в байтовое и выполнить обратное
 преобразование (используя методы encode и decode)."""

words_dict_4 = ['разработка', 'администрирование', 'protocol', 'standard']


def refactor(str_word):
    print(str_word, type(str_word))
    enc_str_bytes = str.encode(str_word, encoding='utf-8')
    print(enc_str_bytes, type(enc_str_bytes))
    dec_str_bytes_3 = bytes.decode(enc_str_bytes, encoding='utf-8')
    print('Сравнение строкового и байтового представления слова ', dec_str_bytes_3 == str_word)


for word in words_dict_4:
    refactor(word)
    print(150 * '=')
