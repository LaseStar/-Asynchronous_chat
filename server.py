"""Программа-сервер

● принимает сообщение клиента;
● формирует ответ клиенту;
● отправляет ответ клиенту;
● имеет параметры командной строки:
    ○ -p <port> — TCP-порт для работы (по умолчанию использует 7777);
    ○ -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все
    доступные адреса).
"""
from socket import *
import json
import sys


def get_message(client_gm):
    js_resp = client_gm.decode('utf-8')
    resp = json.loads(js_resp)
    if isinstance(resp, dict):
        return resp
    raise ValueError


def client_response_check(msg_crch):
    if 'action' not in msg_crch \
            or 'time' not in msg_crch \
            or 'user' not in msg_crch \
            or 'account_name' not in msg_crch['user'] \
            or 'password' not in msg_crch['user']:
        return {
            'response': 400,
            'alert': 'Bad Request'
        }

    if msg_crch['action'] != 'authenticate':
        return {
            'response': 401,
            'alert': 'Not authorized'
        }

    if msg_crch['user']['account_name'] != 'User1' \
            or msg_crch['user']['password'] != 'Password123':
        return {
            'response': 402,
            'alert': 'wrong username/password'
        }

    return {
        'response': 200,
        'alert': 'OK'
    }


def create_client_presence(msg_ccp, client_ccp):
    js_msg = json.dumps(msg_ccp)
    encod_js_msg = js_msg.encode('utf-8')
    client_ccp.send(encod_js_msg)


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = 7777
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((listen_address, listen_port))
    s.listen(5)

    while True:
        client, addr = s.accept()
        data = client.recv(10000)
        msg_from_client = get_message(data)
        print(msg_from_client)
        response = client_response_check(msg_from_client)
        create_client_presence(response, client)
        client.close()


if __name__ == '__main__':
    main()
