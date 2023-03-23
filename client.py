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
import time
import json
import sys
import logging
import log.client_log_config
from decorators import log

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

def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        client_mode = sys.argv[3]
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = 'localhost'
        server_port = 7777
        client_mode = 'send'
    except ValueError:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с указанием неподходящего порта {server_port}.')
        sys.exit(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, server_port))
    CLIENT_LOGGER.info(f'Запущен клиент, порт для подключений: {server_port}, '
                       f'адрес сервера: {server_address}. ')

    if client_mode == 'send':
        print('SENDER')
    else:
        print('GETER')
    while True:
        if client_mode == 'send':
            try:
                msg = create_message()
                send_message(msg, s)
            except:
                CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                sys.exit(1)

        if client_mode == 'listen':
            try:
                msg_from_server = get_message(s)
                answer = parse_message(msg_from_server)
                print(answer)
                CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                sys.exit(1)

    # msg = create_presence()
    # CLIENT_LOGGER.info(f'Cформировано сообщение серверу {msg}')
    # send_message(msg, s)
    # CLIENT_LOGGER.debug(f'Сообщение отправлено на сервер {s}')
    #
    # try:
    #     msg_from_server = get_message(s)
    #     answer = parse_message(msg_from_server)
    #     CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
    # except (ValueError, json.JSONDecodeError):
    #     CLIENT_LOGGER.error(f'Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
