"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
 Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""
from chardet import detect

with open('test_file.txt', 'w') as text:
    text.write('сетевое программирование\n')
    text.write('сокет\n')
    text.write('декоратор')
text.close()

# узнаем кодировку файла
with open('test_file.txt', 'rb') as file:
    text = file.read()
    encoding_text = detect(text)['encoding']
print(encoding_text)
print('======================')
# открываем файл в правильной кодировке
with open('test_file.txt', 'r', encoding=encoding_text) as file:
    text = file.read()
print(text)
