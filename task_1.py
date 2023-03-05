"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:
a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла);
b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
функции реализовать получение данных через вызов функции get_data(), а также
сохранение подготовленных данных в соответствующий CSV-файл;
c. Проверить работу программы через вызов функции write_to_csv().
"""
import csv
import re


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    for i in range(1, 4):
        f = open(f'info_{i}.txt')
        data = f.read()

        reg = re.split(f'\n', data)

        for t in reg:
            if 'Изготовитель системы:' in t:
                os_prod_list.append(' '.join(t.split()[2:]))
            elif "Название ОС:" in t:
                os_name_list.append(' '.join(t.split()[2:]))
            elif "Код продукта:" in t:
                os_code_list.append(' '.join(t.split()[2:]))
            elif "Тип системы:" in t:
                os_type_list.append(' '.join(t.split()[2:]))

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)

    for i in range(0, len(os_prod_list)):
        row_data = list()
        row_data.append(os_prod_list[i])
        row_data.append(os_name_list[i])
        row_data.append(os_code_list[i])
        row_data.append(f'{os_type_list[i]}, str')
        main_data.append(row_data)
    return main_data


def write_to_csv(out_file):
    data = get_data()
    with open(out_file, 'w') as f_n:
        writer = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(data)


write_to_csv('data_report.csv')
