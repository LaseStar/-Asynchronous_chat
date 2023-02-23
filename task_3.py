"""
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""

a1 = 'attribute'
a2 = 'класс'
a3 = 'функция'
a4 = 'type'

str_list = [a1, a2, a3, a4]

for el in str_list:
    try:
        print('Word in byte type:', eval(f'b"{el}"'))
    except SyntaxError:
        print(f'{el} cannot be written in byte type with b prefix')
