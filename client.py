"""Программа-клиент
● сформировать presence-сообщение;
● отправить сообщение серверу;
● получить ответ сервера;
● разобрать сообщение сервера;
● параметры командной строки скрипта client.py <addr> [<port>]:
    ○ addr — ip-адрес сервера;
    ○ port — tcp-порт на сервере, по умолчанию 7777.
"""

import socket
import threading
import time
import json
import sys
import logging
import log.client_log_config
from decorators import log
from metaclasses import ClientVerifier

# Параметры логирования
CLIENT_LOGGER = logging.getLogger('client')


@log
def create_presence():
    m = {
        "action": "authenticate",
        "time": time.time(),
        "user": {
            "account_name": "User1",
            "password": "Password123"
        }
    }
    return m


@log
def send_message(msg_sm, socket_sm):
    js_msg = json.dumps(msg_sm)
    encod_js_ms = js_msg.encode('utf-8')
    socket_sm.send(encod_js_ms)


@log
def get_message(socket_gm):
    server_gm = socket_gm.recv(1000)
    if isinstance(server_gm, bytes):
        js_resp = server_gm.decode('utf-8')
        resp = json.loads(js_resp)
        if isinstance(resp, dict):
            return resp
        raise ValueError
    raise ValueError


@log
def message_from_server(sock, my_username):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    while True:
        try:
            message = get_message(sock)
            if 'action' in message and message['action'] == 'message' and \
                    'from' in message and 'to' in message \
                    and 'mess_text' in message and message['to'] == my_username:
                print(f'\nПолучено сообщение от пользователя {message["from"]}:'
                      f'\n{message["mess_text"]}')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message["from"]}:'
                                   f'\n{message["mess_text"]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
            break


@log
def parse_message(msg_pm):
    if 'response' in msg_pm:
        return f'{msg_pm["response"]} : {msg_pm["alert"]}'
    raise ValueError


@log
def create_message():
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    m = {
        "action": "message",
        "time": time.time(),
        "user": {
            "account_name": "User1",
            "password": "Password123"
        },
        "message_text": message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {m}')
    return m


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def create_exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        'action': 'exit',
        'time': time.time(),
        'account_name': account_name
    }


@log
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


def main():
    """Сообщаем о запуске"""
    print('Консольный месседжер. Клиентский модуль.')

    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        client_name = sys.argv[3]

        if not client_name:
            client_name = input('Введите имя пользователя: ')

        if server_port < 1024 or server_port > 65535:
            raise ValueError
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_address, server_port))
        CLIENT_LOGGER.info(f'Запущен клиент, порт для подключений: {server_port}, '
                           f'адрес сервера: {server_address}. ')
    except IndexError:
        server_address = 'localhost'
        server_port = 7777
        client_mode = 'send'
    except ValueError:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с указанием неподходящего порта {server_port}.')
        sys.exit(1)
    else:
        try:
            msg = create_presence()
            CLIENT_LOGGER.info(f'Cформировано сообщение серверу {msg}')
            send_message(msg, s)
            CLIENT_LOGGER.debug(f'Сообщение отправлено на сервер {s}')
            msg_from_server = get_message(s)
            answer = parse_message(msg_from_server)
            CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        except:
            CLIENT_LOGGER.error(f'При установке соединения сервер произошла ошибка')
            sys.exit(1)
        else:
            # Если соединение с сервером установлено корректно,
            # запускаем клиенский процесс приёма сообщний
            receiver = threading.Thread(target=message_from_server, args=(s, client_name))
            receiver.daemon = True
            receiver.start()

            # затем запускаем отправку сообщений и взаимодействие с пользователем.
            user_interface = threading.Thread(target=user_interactive, args=(s, client_name))
            user_interface.daemon = True
            user_interface.start()
            CLIENT_LOGGER.debug('Запущены процессы')

            while True:
                time.sleep(1)
                if receiver.is_alive() and user_interface.is_alive():
                    continue
                break


if __name__ == '__main__':
    main()
