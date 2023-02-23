"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
в байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""

a1 = 'разработка'
a2 = 'администрирование'
a3 = 'protocol'
a4 = 'standard'

str_list = [a1, a2, a3, a4]
byte_list = []

for el in str_list:
    byte_list.append(el.encode('utf-8'))
print(*byte_list)

print('===============')

new_list = []
for el in byte_list:
    new_list.append(el.decode('utf-8'))
print(*new_list)
