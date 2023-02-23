"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
 Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

with open('test_file.txt', 'w', encoding='utf-8') as text:
    text.write('сетевое программирование\n')
    text.write('сокет\n')
    text.write('декоратор')

with open('test_file.txt', encoding='utf-8') as text:
    for each_line in text:
        print(each_line, end="")
