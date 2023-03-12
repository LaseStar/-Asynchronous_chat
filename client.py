"""Программа-клиент
● сформировать presence-сообщение;
● отправить сообщение серверу;
● получить ответ сервера;
● разобрать сообщение сервера;
● параметры командной строки скрипта client.py <addr> [<port>]:
    ○ addr — ip-адрес сервера;
    ○ port — tcp-порт на сервере, по умолчанию 7777.
"""

from socket import *
import time
import json
import sys


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


def send_message(msg_sm, socket_sm):
    js_msg = json.dumps(msg_sm)
    encod_js_ms = js_msg.encode('utf-8')
    socket_sm.send(encod_js_ms)


def get_message(socket_gm):
    server_gm = socket_gm.recv(1000)
    if isinstance(server_gm, bytes):
        js_resp = server_gm.decode('utf-8')
        resp = json.loads(js_resp)
        if isinstance(resp, dict):
            return resp
        raise ValueError
    raise ValueError


def parse_message(msg_pm):
    if 'response' in msg_pm:
        return f'{msg_pm["response"]} : {msg_pm["alert"]}'
    raise ValueError


def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = 'localhost'
        server_port = 7777
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_address, server_port))

    msg = create_presence()
    send_message(msg, s)

    try:
        msg_from_server = get_message(s)
        answer = parse_message(msg_from_server)
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
