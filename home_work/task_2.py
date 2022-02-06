""" Каждое из слов «class», «function», «method» записать в байтовом типе без
преобразования в последовательность кодов (не используя методы encode и decode)
 и определить тип, содержимое и длину соответствующих переменных."""

words_dict = [b'class', b'function', b'method']
bytes_words_dict = []


def fun_1(word):
    print(word, type(word), len(word))


for string in words_dict:
    fun_1(string)

# возможно я неправильно понял как это делать :( точнее как применить eval
# в 3 задании сделал через .isascii
#не знаю можно ли было применить ord, или chr. но насколько я понял задание нет