"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""

a1 = b'class'
a2 = b'function'
a3 = b'method'

str_list = [a1, a2, a3]

for el in str_list:
    print(f'type={type(el)}; word={el} len={len(el)}')
